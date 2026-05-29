#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


DEFAULT_BASELINES = [
    Path("results/baselines_fever_v4_n100_structbalanced.json"),
    Path("results/baselines_hotpot_v4_hardneg_n100.json"),
    Path("results/baselines_hotpot_v4_n100_hardmatched.json"),
    Path("results/baselines_hotpot_v4_n100_structbalanced.json"),
    Path("results/baselines_hotpot_v4_semanticswap_n100.json"),
    Path("results/baselines_hotpot_v4_supportpreserve_n100.json"),
]

DEFAULT_COMPARISONS = [
    Path("results/compare_calibrated_fever_v4_n100_structbalanced.json"),
    Path("results/compare_calibrated_hotpot_v4_hardneg_n100.json"),
    Path("results/compare_calibrated_hotpot_v4_n100_hardmatched.json"),
    Path("results/compare_calibrated_hotpot_v4_n100_structbalanced.json"),
    Path("results/compare_calibrated_hotpot_v4_semanticswap_n100.json"),
    Path("results/compare_calibrated_hotpot_v4_supportpreserve_n100.json"),
]

METRICS = [
    "auroc_improvement",
    "auprc_improvement",
    "risk_at_30_reduction",
    "risk_at_50_reduction",
    "risk_at_70_reduction",
    "aurc_reduction",
]
TARGETS = [
    "csrm_rule",
    "csrm_minimax",
    "csrm_calibrated_logistic",
    "csrm_calibrated_isotonic",
    "csrm_calibrated_gbdt",
]


def summarize_v4_strong_baselines(
    baseline_paths: Sequence[Path],
    comparison_paths: Sequence[Path],
) -> dict[str, Any]:
    baseline_rows = [_baseline_row(path) for path in baseline_paths]
    comparison_rows = [_comparison_row(path) for path in comparison_paths]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "baseline_inputs": [str(path) for path in baseline_paths],
        "comparison_inputs": [str(path) for path in comparison_paths],
        "baseline_rows": baseline_rows,
        "comparison_rows": comparison_rows,
        "aggregate": {
            "baseline_file_count": len(baseline_rows),
            "comparison_file_count": len(comparison_rows),
            "method_union": sorted({method for row in baseline_rows for method in row["methods"]}),
            "csrm_rule_vs_strongest": _aggregate_rule_rows(baseline_rows),
            "calibrated_targets_vs_all_baselines": _aggregate_comparison_rows(comparison_rows),
        },
        "claim_implication": (
            "The v4 strong-baseline package is present and includes context sufficiency, faithful "
            "SURE-style multi-set scoring, equal-budget orbit reducers, retrieval stability, "
            "self-consistency, and out-of-fold calibrated logistic context/orbit baselines. "
            "It strengthens reviewer-facing baseline coverage, but it is also negative boundary "
            "evidence: CSRM-Rule is not an all-win method against the strongest learned/context "
            "baselines, and calibrated CSRM should be reported with per-setting caveats."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    rule = summary["aggregate"]["csrm_rule_vs_strongest"]
    target_agg = summary["aggregate"]["calibrated_targets_vs_all_baselines"]
    lines = [
        "# V4 Strong Baseline Coverage",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        "## Baseline Package",
        "",
        f"- Baseline files: `{summary['aggregate']['baseline_file_count']}`.",
        f"- Comparison files: `{summary['aggregate']['comparison_file_count']}`.",
        f"- Method union: `{', '.join(summary['aggregate']['method_union'])}`.",
        "",
        "## CSRM-Rule vs Strongest Non-CSRM",
        "",
        f"- By AUROC strongest: wins/ties/losses = `{rule['by_auroc']['wins']}` / "
        f"`{rule['by_auroc']['ties']}` / `{rule['by_auroc']['losses']}`.",
        f"- By AUPRC strongest: wins/ties/losses = `{rule['by_auprc']['wins']}` / "
        f"`{rule['by_auprc']['ties']}` / `{rule['by_auprc']['losses']}`.",
        f"- By Risk@30 strongest: wins/ties/losses = `{rule['by_risk_at_30']['wins']}` / "
        f"`{rule['by_risk_at_30']['ties']}` / `{rule['by_risk_at_30']['losses']}`.",
        f"- By AURC strongest: wins/ties/losses = `{rule['by_aurc']['wins']}` / "
        f"`{rule['by_aurc']['ties']}` / `{rule['by_aurc']['losses']}`.",
        "",
        "| Dataset | Strongest by AUROC | AUROC delta | AUPRC delta | Risk@30 delta | Risk@50 delta | Risk@70 delta | AURC delta | Verdict |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary["baseline_rows"]:
        strongest = row["strongest"]["by_auroc"]
        delta = row["csrm_vs_strongest"]["by_auroc"]
        lines.append(
            f"| {row['dataset']} | {strongest} | {_fmt(delta['auroc_improvement'])} | "
            f"{_fmt(delta.get('auprc_improvement'))} | "
            f"{_fmt(delta['risk_at_30_reduction'])} | {_fmt(delta['risk_at_50_reduction'])} | "
            f"{_fmt(delta.get('risk_at_70_reduction'))} | "
            f"{_fmt(delta['aurc_reduction'])} | {row['rule_verdict_by_auroc']} |"
        )

    lines.extend(["", "## Calibrated Targets vs All Non-CSRM Baselines", ""])
    lines.extend(
        [
            "| Target | Metric | Robust wins | Ties | Losses | Mean worst-case delta |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for target in TARGETS:
        if target not in target_agg:
            continue
        for metric in METRICS:
            item = target_agg[target][metric]
            lines.append(
                f"| {target} | {metric} | {item['robust_wins']} | {item['ties']} | "
                f"{item['losses']} | {_fmt(item['mean_worst_case_delta'])} |"
            )

    lines.extend(["", "## Claim Implication", "", summary["claim_implication"], ""])
    return "\n".join(lines)


def _baseline_row(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    strongest = {
        key: value["method"]
        for key, value in payload.get("strongest_non_csrm", {}).items()
    }
    deltas = payload.get("csrm_vs_strongest_non_csrm", {})
    return {
        "artifact": str(path),
        "dataset": _dataset_name(path, prefix="baselines_", suffix=".json"),
        "n": payload.get("n"),
        "source_item_groups": payload.get("source_item_groups"),
        "methods": sorted(payload.get("methods", {})),
        "strongest": strongest,
        "csrm_vs_strongest": deltas,
        "rule_verdict_by_auroc": _delta_verdict(deltas.get("by_auroc", {})),
    }


def _comparison_row(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    aggregate = payload["aggregate"]
    targets = {}
    for target in TARGETS:
        if target not in aggregate:
            continue
        targets[target] = {}
        for metric in METRICS:
            values = [
                item[metric]["mean"]
                for item in aggregate[target].values()
                if item[metric]["mean"] is not None
            ]
            targets[target][metric] = {
                "worst_case_delta": min(values) if values else None,
                "mean_delta": _mean(values) if values else None,
                "wins_against_baselines": sum(1 for value in values if value > 1e-12),
                "ties_against_baselines": sum(1 for value in values if abs(value) <= 1e-12),
                "losses_against_baselines": sum(1 for value in values if value < -1e-12),
            }
    return {
        "artifact": str(path),
        "dataset": _dataset_name(path, prefix="compare_calibrated_", suffix=".json"),
        "n": payload.get("n"),
        "seeds": payload.get("seeds"),
        "targets": targets,
    }


def _aggregate_rule_rows(rows: Sequence[dict[str, Any]]) -> dict[str, dict[str, int]]:
    output = {}
    for key in ["by_auroc", "by_auprc", "by_risk_at_30", "by_aurc"]:
        verdicts = [_delta_verdict(row["csrm_vs_strongest"].get(key, {})) for row in rows]
        output[key] = {
            "wins": sum(1 for verdict in verdicts if verdict == "win"),
            "ties": sum(1 for verdict in verdicts if verdict == "tie_or_mixed"),
            "losses": sum(1 for verdict in verdicts if verdict == "loss"),
        }
    return output


def _aggregate_comparison_rows(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    output = {}
    for target in TARGETS:
        output[target] = {}
        for metric in METRICS:
            values = [
                row["targets"][target][metric]["worst_case_delta"]
                for row in rows
                if target in row["targets"] and row["targets"][target][metric]["worst_case_delta"] is not None
            ]
            output[target][metric] = {
                "robust_wins": sum(1 for value in values if value > 1e-12),
                "ties": sum(1 for value in values if abs(value) <= 1e-12),
                "losses": sum(1 for value in values if value < -1e-12),
                "mean_worst_case_delta": _mean(values) if values else None,
            }
    return output


def _delta_verdict(delta: dict[str, Any]) -> str:
    auroc = delta.get("auroc_improvement")
    auprc = delta.get("auprc_improvement")
    risk30 = delta.get("risk_at_30_reduction")
    risk70 = delta.get("risk_at_70_reduction")
    aurc = delta.get("aurc_reduction")
    values = [value for value in [auroc, auprc, risk30, risk70, aurc] if value is not None]
    if values and all(value > 1e-12 for value in values):
        return "win"
    if values and all(value >= -1e-12 for value in values):
        return "tie_or_mixed"
    return "loss"


def _dataset_name(path: Path, *, prefix: str, suffix: str) -> str:
    name = path.name
    if name.startswith(prefix):
        name = name[len(prefix) :]
    if name.endswith(suffix):
        name = name[: -len(suffix)]
    return name


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values)


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.4f}"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baselines", type=Path, nargs="+", default=DEFAULT_BASELINES)
    parser.add_argument("--comparisons", type=Path, nargs="+", default=DEFAULT_COMPARISONS)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_v4_strong_baselines(args.baselines, args.comparisons)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
