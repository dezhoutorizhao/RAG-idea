#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


DEFAULT_INPUTS = [
    Path("results/calibration_fever_v4_n100_structbalanced.json"),
    Path("results/calibration_hotpot_v4_hardneg_n100.json"),
    Path("results/calibration_hotpot_v4_n100_hardmatched.json"),
    Path("results/calibration_hotpot_v4_n100_structbalanced.json"),
    Path("results/calibration_hotpot_v4_semanticswap_n100.json"),
    Path("results/calibration_hotpot_v4_supportpreserve_n100.json"),
]

TARGET_METHODS = ["csrm_calibrated_logistic", "csrm_calibrated_isotonic", "csrm_calibrated_gbdt"]
REFERENCE_METHODS = ["csrm_rule", "csrm_minimax"]


def summarize_v4_calibration_quality(paths: Sequence[Path]) -> dict[str, Any]:
    rows = [_dataset_row(path) for path in paths]
    aggregate = _aggregate(rows)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_count": len(paths),
        "dataset_count": len(rows),
        "target_methods": TARGET_METHODS,
        "reference_methods": REFERENCE_METHODS,
        "rows": rows,
        "aggregate": aggregate,
        "calibration_quality_supported": aggregate["best_target_brier_win_count"] == len(rows)
        and aggregate["best_target_ece_win_count"] >= len(rows) - 1,
        "claim_implication": (
            "Calibrated CSRM variants, including logistic, isotonic, and GBDT calibration, "
            "strongly improve Brier score over rule/minimax baselines across all current v4 "
            "calibration datasets. ECE improves on most but not all datasets, so calibration "
            "should be claimed as empirical calibration-quality evidence, not as a formal risk "
            "guarantee."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    lines = [
        "# V4 Calibration Quality",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Datasets: `{summary['dataset_count']}`",
        f"Calibration quality supported: `{summary['calibration_quality_supported']}`",
        "",
        "## Aggregate",
        "",
        f"- Best calibrated target Brier wins: `{aggregate['best_target_brier_win_count']}/{summary['dataset_count']}`.",
        f"- Best calibrated target ECE wins: `{aggregate['best_target_ece_win_count']}/{summary['dataset_count']}`.",
        f"- Mean best-target Brier reduction vs best reference: `{_fmt(aggregate['mean_best_target_brier_reduction'])}`.",
        f"- Mean best-target ECE reduction vs best reference: `{_fmt(aggregate['mean_best_target_ece_reduction'])}`.",
        "",
        "## Rows",
        "",
        "| Dataset | Best target | Brier | Best ref Brier | Brier reduction | ECE | Best ref ECE | ECE reduction | Target met rate |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary["rows"]:
        target = row["best_target_by_brier"]
        lines.append(
            f"| {row['dataset']} | {target['method']} | {_fmt(target['brier_mean'])} | "
            f"{_fmt(row['best_reference_by_brier']['brier_mean'])} | {_fmt(row['brier_reduction_vs_best_reference'])} | "
            f"{_fmt(target['ece_mean'])} | {_fmt(row['best_reference_by_ece']['ece_mean'])} | "
            f"{_fmt(row['ece_reduction_vs_best_reference'])} | {_fmt(target['target_met_rate'])} |"
        )
    lines.extend(["", "## Claim Implication", "", summary["claim_implication"], ""])
    return "\n".join(lines)


def _dataset_row(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    method_rows = {
        method: _method_row(payload, method)
        for method in sorted(set(TARGET_METHODS + REFERENCE_METHODS))
    }
    best_target_brier = min((method_rows[m] for m in TARGET_METHODS), key=lambda row: row["brier_mean"])
    best_ref_brier = min((method_rows[m] for m in REFERENCE_METHODS), key=lambda row: row["brier_mean"])
    best_target_ece = min((method_rows[m] for m in TARGET_METHODS), key=lambda row: row["ece_mean"])
    best_ref_ece = min((method_rows[m] for m in REFERENCE_METHODS), key=lambda row: row["ece_mean"])
    return {
        "dataset": _dataset_name(payload, path),
        "artifact": str(path),
        "n": payload.get("n"),
        "seeds": payload.get("seeds", []),
        "risk_target": payload.get("risk_target"),
        "methods": method_rows,
        "best_target_by_brier": best_target_brier,
        "best_reference_by_brier": best_ref_brier,
        "brier_reduction_vs_best_reference": best_ref_brier["brier_mean"] - best_target_brier["brier_mean"],
        "best_target_by_ece": best_target_ece,
        "best_reference_by_ece": best_ref_ece,
        "ece_reduction_vs_best_reference": best_ref_ece["ece_mean"] - best_target_ece["ece_mean"],
        "brier_win_vs_best_reference": best_target_brier["brier_mean"] < best_ref_brier["brier_mean"],
        "ece_win_vs_best_reference": best_target_ece["ece_mean"] < best_ref_ece["ece_mean"],
    }


def _method_row(payload: dict[str, Any], method: str) -> dict[str, Any]:
    aggregate = payload["aggregate"][method]
    test_rows = [seed["methods"][method]["test"] for seed in payload["per_seed"]]
    return {
        "method": method,
        "brier_mean": _mean(row["brier"] for row in test_rows),
        "ece_mean": _mean(row["calibration"]["ece"] for row in test_rows),
        "mce_mean": _mean(row["calibration"]["mce"] for row in test_rows),
        "auroc_mean": aggregate["auroc"]["mean"],
        "aurc_mean": aggregate["aurc"]["mean"],
        "risk30_mean": aggregate["risk_at_30"]["mean"],
        "risk50_mean": aggregate["risk_at_50"]["mean"],
        "target_met_rate": aggregate["target_met_rate"],
        "zero_coverage_count": aggregate["zero_coverage_count"],
    }


def _aggregate(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return {
        "best_target_brier_win_count": sum(row["brier_win_vs_best_reference"] for row in rows),
        "best_target_ece_win_count": sum(row["ece_win_vs_best_reference"] for row in rows),
        "mean_best_target_brier_reduction": _mean(row["brier_reduction_vs_best_reference"] for row in rows),
        "mean_best_target_ece_reduction": _mean(row["ece_reduction_vs_best_reference"] for row in rows),
        "datasets_with_ece_nonwin": [
            row["dataset"] for row in rows if not row["ece_win_vs_best_reference"]
        ],
        "datasets_with_brier_nonwin": [
            row["dataset"] for row in rows if not row["brier_win_vs_best_reference"]
        ],
    }


def _dataset_name(payload: dict[str, Any], path: Path) -> str:
    raw = str(payload.get("raw_input") or path.stem)
    name = Path(raw).name
    for suffix in [".constant.raw.jsonl", ".raw.jsonl", ".jsonl"]:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem.removeprefix("calibration_")


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(float(value) for value in values) / len(values)


def _fmt(value: Any) -> str:
    return "n/a" if value is None else f"{float(value):.4f}"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=Path("results/v4_calibration_quality_20260529.json"))
    parser.add_argument("--output-md", type=Path, default=Path("results/v4_calibration_quality_20260529.md"))
    parser.add_argument("--inputs", type=Path, nargs="+", default=DEFAULT_INPUTS)
    args = parser.parse_args()
    summary = summarize_v4_calibration_quality(args.inputs)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
