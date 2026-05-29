#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_INPUTS = [
    Path("results/failure_analysis_fever_v4_n100_structbalanced.json"),
    Path("results/failure_analysis_hotpot_v4_hardneg_n100.json"),
    Path("results/failure_analysis_hotpot_v4_n100_hardmatched.json"),
    Path("results/failure_analysis_hotpot_v4_n100_structbalanced.json"),
    Path("results/failure_analysis_hotpot_v4_semanticswap_n100.json"),
    Path("results/failure_analysis_hotpot_v4_supportpreserve_n100.json"),
]


def summarize_v4_failure_taxonomy(inputs: Sequence[Path]) -> dict[str, Any]:
    rows = [_dataset_row(path) for path in inputs]
    if not rows:
        raise ValueError("at least one failure-analysis input is required")
    taxonomy = _taxonomy(rows)
    feature_frequency = _feature_frequency(rows)
    metrics = _metric_aggregate(rows)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [str(path) for path in inputs],
        "dataset_count": len(rows),
        "rows": rows,
        "taxonomy": taxonomy,
        "feature_frequency": feature_frequency,
        "metric_aggregate": metrics,
        "case_gallery_coverage": _case_gallery_coverage(rows),
        "claim_implication": (
            "The v4 failure taxonomy is now machine-readable across FEVER and Hotpot variants. "
            "It supports a paper narrative around counterfactual sufficiency instability and "
            "documents mixed target-vs-baseline behavior. It remains heuristic/private-label "
            "analysis until human audit v4 adjudication is complete."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    metrics = summary["metric_aggregate"]
    lines = [
        "# V4 Failure Taxonomy Summary",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Datasets: `{summary['dataset_count']}`",
        "",
        "## Target vs Baseline",
        "",
        f"- AUROC wins/ties/losses: `{metrics['auroc']['wins']}` / `{metrics['auroc']['ties']}` / `{metrics['auroc']['losses']}`.",
        f"- Risk@30 wins/ties/losses: `{metrics['risk_at_30']['wins']}` / `{metrics['risk_at_30']['ties']}` / `{metrics['risk_at_30']['losses']}`.",
        f"- Risk@50 wins/ties/losses: `{metrics['risk_at_50']['wins']}` / `{metrics['risk_at_50']['ties']}` / `{metrics['risk_at_50']['losses']}`.",
        "",
        "| Dataset | Target AUROC | Baseline AUROC | Target Risk@30 | Baseline Risk@30 | Target Risk@50 | Baseline Risk@50 | Verdict |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary["rows"]:
        target = row["metrics"]["target"]
        baseline = row["metrics"]["baseline_calibrated_logistic_orbit"]
        lines.append(
            f"| {row['dataset']} | {_fmt(target['auroc'])} | {_fmt(baseline['auroc'])} | "
            f"{_fmt(target['risk_at_30'])} | {_fmt(baseline['risk_at_30'])} | "
            f"{_fmt(target['risk_at_50'])} | {_fmt(baseline['risk_at_50'])} | "
            f"{row['target_vs_baseline_verdict']} |"
        )

    lines.extend(
        [
            "",
            "## Construction Taxonomy",
            "",
            "| Construction type | n | positive | negative | Datasets | Target mean | Baseline mean | Target-baseline |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for item in summary["taxonomy"]:
        lines.append(
            f"| {item['construction_type']} | {item['n']} | {item['positive']} | {item['negative']} | "
            f"{item['dataset_count']} | {_fmt(item['target_mean'])} | {_fmt(item['baseline_mean'])} | "
            f"{_fmt(item['target_minus_baseline_mean'])} |"
        )

    lines.extend(
        [
            "",
            "## Recurring Feature Gaps",
            "",
            "| Feature | top-3 appearances | top-5 appearances | mean absolute gap | max absolute gap |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for item in summary["feature_frequency"][:12]:
        lines.append(
            f"| {item['feature']} | {item['top3_count']} | {item['top5_count']} | "
            f"{_fmt(item['mean_absolute_gap'])} | {_fmt(item['max_absolute_gap'])} |"
        )

    lines.extend(["", "## Case Gallery Coverage", ""])
    for bucket, count in summary["case_gallery_coverage"].items():
        lines.append(f"- {bucket}: `{count}` cases.")
    lines.extend(["", "## Claim Implication", "", summary["claim_implication"], ""])
    return "\n".join(lines)


def _dataset_row(path: Path) -> dict[str, Any]:
    payload = _load_json(path)
    metrics = payload["metrics"]
    return {
        "artifact": str(path),
        "dataset": _dataset_name(path),
        "seed": payload.get("seed"),
        "split_sizes": payload.get("split_sizes"),
        "metrics": metrics,
        "target_vs_baseline_verdict": _metric_verdict(
            metrics["target"],
            metrics["baseline_calibrated_logistic_orbit"],
        ),
        "by_construction_type": payload.get("by_construction_type", {}),
        "feature_gaps": payload.get("feature_gaps", []),
        "top_case_counts": {
            name: len(cases)
            for name, cases in payload.get("top_cases", {}).items()
        },
    }


def _taxonomy(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        for construction_type, item in row["by_construction_type"].items():
            buckets[construction_type].append({**item, "dataset": row["dataset"]})
    output = []
    for construction_type, items in buckets.items():
        total = sum(int(item["n"]) for item in items)
        output.append(
            {
                "construction_type": construction_type,
                "n": total,
                "positive": sum(int(item["positive"]) for item in items),
                "negative": sum(int(item["negative"]) for item in items),
                "dataset_count": len({item["dataset"] for item in items}),
                "target_mean": _weighted_mean(items, "target_mean"),
                "baseline_mean": _weighted_mean(items, "baseline_mean"),
                "target_minus_baseline_mean": _weighted_mean(
                    items,
                    "target_minus_baseline_mean",
                ),
            }
        )
    return sorted(output, key=lambda item: (-item["n"], item["construction_type"]))


def _feature_frequency(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    top3 = Counter()
    top5 = Counter()
    gaps: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        for index, item in enumerate(row["feature_gaps"]):
            feature = item["feature"]
            gap = float(item["absolute_gap"])
            gaps[feature].append(gap)
            if index < 3:
                top3[feature] += 1
            if index < 5:
                top5[feature] += 1
    output = []
    for feature, values in gaps.items():
        output.append(
            {
                "feature": feature,
                "top3_count": top3[feature],
                "top5_count": top5[feature],
                "mean_absolute_gap": sum(values) / len(values),
                "max_absolute_gap": max(values),
            }
        )
    return sorted(
        output,
        key=lambda item: (-item["top3_count"], -item["top5_count"], -item["mean_absolute_gap"], item["feature"]),
    )


def _metric_aggregate(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    output = {}
    for metric, lower_is_better in [
        ("auroc", False),
        ("risk_at_30", True),
        ("risk_at_50", True),
    ]:
        verdicts = []
        deltas = []
        for row in rows:
            target = row["metrics"]["target"][metric]
            baseline = row["metrics"]["baseline_calibrated_logistic_orbit"][metric]
            if target is None or baseline is None:
                continue
            delta = baseline - target if lower_is_better else target - baseline
            deltas.append(delta)
            verdicts.append(_sign(delta))
        output[metric] = {
            "wins": verdicts.count("win"),
            "ties": verdicts.count("tie"),
            "losses": verdicts.count("loss"),
            "mean_improvement": sum(deltas) / len(deltas) if deltas else None,
            "min_improvement": min(deltas) if deltas else None,
            "max_improvement": max(deltas) if deltas else None,
        }
    return output


def _case_gallery_coverage(rows: Sequence[dict[str, Any]]) -> dict[str, int]:
    counts = Counter()
    for row in rows:
        counts.update(row["top_case_counts"])
    return dict(sorted(counts.items()))


def _metric_verdict(target: dict[str, Any], baseline: dict[str, Any]) -> str:
    deltas = []
    if target["auroc"] is not None and baseline["auroc"] is not None:
        deltas.append(target["auroc"] - baseline["auroc"])
    deltas.append(baseline["risk_at_30"] - target["risk_at_30"])
    deltas.append(baseline["risk_at_50"] - target["risk_at_50"])
    if all(delta > 1e-12 for delta in deltas):
        return "target_win"
    if all(delta >= -1e-12 for delta in deltas):
        return "tie_or_mixed_positive"
    return "mixed_or_loss"


def _sign(value: float) -> str:
    if value > 1e-12:
        return "win"
    if value < -1e-12:
        return "loss"
    return "tie"


def _weighted_mean(items: Sequence[dict[str, Any]], key: str) -> float:
    total = sum(int(item["n"]) for item in items)
    if total == 0:
        return 0.0
    return sum(float(item[key]) * int(item["n"]) for item in items) / total


def _dataset_name(path: Path) -> str:
    name = path.name
    prefix = "failure_analysis_"
    suffix = ".json"
    if name.startswith(prefix):
        name = name[len(prefix) :]
    if name.endswith(suffix):
        name = name[: -len(suffix)]
    return name


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
    parser.add_argument("--inputs", type=Path, nargs="+", default=DEFAULT_INPUTS)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_v4_failure_taxonomy(args.inputs)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
