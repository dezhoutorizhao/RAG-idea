#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_INPUTS = [
    Path("results/hotpot_corm_multiseed_summary_fullabl.json"),
    Path("results/fever_nearmiss_corm_v3_multiseed_summary.json"),
]

ABLATION_METHODS = [
    "csrm_no_answer_consistency",
    "csrm_no_worst_sufficiency",
    "csrm_shuffled_perturbations",
    "naive_orbit_average",
    "single_set_sure_style",
    "corm_max_clean",
]


def summarize_mechanism_ablation(inputs: Sequence[Path]) -> dict[str, Any]:
    rows = []
    for path in inputs:
        rows.extend(_dataset_rows(path))
    if not rows:
        raise ValueError("no mechanism ablation rows found")
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [str(path) for path in inputs],
        "dataset_count": len(inputs),
        "rows": rows,
        "aggregate": _aggregate(rows),
        "claim_implication": (
            "Mechanism ablations strongly support orbit alignment as necessary: shuffled "
            "perturbations collapse on both Hotpot and FEVER. Answer consistency is important "
            "on Hotpot and mildly positive on FEVER. Worst-sufficiency removal is not consistently "
            "harmful in the current bridge artifacts, so it should be framed as a weak or redundant "
            "component rather than a required standalone mechanism."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    lines = [
        "# Mechanism Ablation Summary",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Datasets: `{summary['dataset_count']}`",
        "",
        "## Aggregate by Method",
        "",
        "| Method | Datasets | AUROC drop mean | Risk@30 increase mean | AURC increase mean | Strong mechanism evidence |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for method, item in aggregate["by_method"].items():
        lines.append(
            f"| {method} | {item['dataset_count']} | {_fmt(item['auroc_drop_mean'])} | "
            f"{_fmt(item['risk30_increase_mean'])} | {_fmt(item['aurc_increase_mean'])} | "
            f"`{item['strong_mechanism_evidence']}` |"
        )

    lines.extend(
        [
            "",
            "## Per Dataset",
            "",
            "| Dataset | Method | CSRM AUROC | Method AUROC | AUROC drop | Risk@30 increase | AURC increase |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in summary["rows"]:
        lines.append(
            f"| {row['dataset']} | {row['method']} | {_fmt(row['csrm']['auroc'])} | "
            f"{_fmt(row['method_metrics']['auroc'])} | {_fmt(row['deltas']['auroc_drop'])} | "
            f"{_fmt(row['deltas']['risk30_increase'])} | {_fmt(row['deltas']['aurc_increase'])} |"
        )

    lines.extend(
        [
            "",
            "## Claim Implication",
            "",
            summary["claim_implication"],
            "",
        ]
    )
    return "\n".join(lines)


def _dataset_rows(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    aggregate = payload["aggregate"]
    csrm = _metrics(aggregate["csrm"])
    rows = []
    for method in ABLATION_METHODS:
        if method not in aggregate:
            continue
        method_metrics = _metrics(aggregate[method])
        rows.append(
            {
                "artifact": str(path),
                "dataset": _dataset_name(path),
                "method": method,
                "csrm": csrm,
                "method_metrics": method_metrics,
                "deltas": {
                    "auroc_drop": None
                    if csrm["auroc"] is None or method_metrics["auroc"] is None
                    else csrm["auroc"] - method_metrics["auroc"],
                    "risk30_increase": method_metrics["risk_at_30"] - csrm["risk_at_30"],
                    "risk50_increase": method_metrics["risk_at_50"] - csrm["risk_at_50"],
                    "aurc_increase": method_metrics["aurc"] - csrm["aurc"],
                },
            }
        )
    return rows


def _aggregate(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    by_method = {}
    for method in sorted({row["method"] for row in rows}):
        selected = [row for row in rows if row["method"] == method]
        auroc_drops = [row["deltas"]["auroc_drop"] for row in selected if row["deltas"]["auroc_drop"] is not None]
        risk30 = [row["deltas"]["risk30_increase"] for row in selected]
        aurc = [row["deltas"]["aurc_increase"] for row in selected]
        by_method[method] = {
            "dataset_count": len(selected),
            "auroc_drop_mean": _mean(auroc_drops),
            "risk30_increase_mean": _mean(risk30),
            "aurc_increase_mean": _mean(aurc),
            "strong_mechanism_evidence": _strong_mechanism_evidence(auroc_drops, risk30, aurc),
        }
    return {
        "by_method": by_method,
        "strong_alignment_evidence": by_method.get("csrm_shuffled_perturbations", {}).get(
            "strong_mechanism_evidence"
        ),
        "methods_with_negative_or_weak_evidence": [
            method
            for method, item in by_method.items()
            if not item["strong_mechanism_evidence"]
        ],
    }


def _strong_mechanism_evidence(
    auroc_drops: Sequence[float],
    risk30_increases: Sequence[float],
    aurc_increases: Sequence[float],
) -> bool:
    if not auroc_drops or not risk30_increases or not aurc_increases:
        return False
    return (
        min(auroc_drops) > 0.05
        and min(risk30_increases) > 0.02
        and min(aurc_increases) > 0.02
    )


def _metrics(item: dict[str, Any]) -> dict[str, float | None]:
    return {
        "auroc": _metric(item.get("auroc")),
        "risk_at_30": _metric(item.get("risk_at_30")),
        "risk_at_50": _metric(item.get("risk_at_50")),
        "aurc": _metric(item.get("aurc")),
    }


def _metric(item: Any) -> float | None:
    if item is None:
        return None
    if isinstance(item, dict):
        item = item.get("mean")
    if item is None:
        return None
    return float(item)


def _mean(values: Sequence[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _dataset_name(path: Path) -> str:
    name = path.name
    replacements = {
        "hotpot_corm_multiseed_summary_fullabl.json": "hotpot_corm_multiseed",
        "fever_nearmiss_corm_v3_multiseed_summary.json": "fever_nearmiss_corm_v3_multiseed",
    }
    return replacements.get(name, name.removesuffix(".json"))


def _fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.4f}"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, nargs="+", default=DEFAULT_INPUTS)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_mechanism_ablation(args.inputs)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
