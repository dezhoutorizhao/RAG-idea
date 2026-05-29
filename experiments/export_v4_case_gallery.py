#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from experiments.summarize_v4_failure_taxonomy import DEFAULT_INPUTS


def export_v4_case_gallery(
    inputs: Sequence[Path],
    output_jsonl: Path,
    output_md: Path,
    summary_json: Path,
    *,
    per_bucket_per_dataset: int,
) -> dict[str, Any]:
    cases = _load_cases(inputs)
    summary = _summary(cases, inputs, output_jsonl, output_md)

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with output_jsonl.open("w", encoding="utf-8") as handle:
        for case in cases:
            handle.write(json.dumps(case, sort_keys=True, ensure_ascii=False) + "\n")

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(
        render_markdown(summary, cases, per_bucket_per_dataset=per_bucket_per_dataset),
        encoding="utf-8",
    )

    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def render_markdown(
    summary: dict[str, Any],
    cases: Sequence[dict[str, Any]],
    *,
    per_bucket_per_dataset: int,
) -> str:
    lines = [
        "# V4 Case Study Gallery",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Inputs: `{summary['input_count']}` failure-analysis files.",
        f"Exported cases: `{summary['case_count']}`.",
        "",
        "## Coverage",
        "",
        "| Bucket | Cases |",
        "|---|---:|",
    ]
    for bucket, count in summary["bucket_counts"].items():
        lines.append(f"| {bucket} | {count} |")

    lines.extend(
        [
            "",
            "## Construction Types",
            "",
            "| Construction type | Cases |",
            "|---|---:|",
        ]
    )
    for construction_type, count in summary["construction_type_counts"].items():
        lines.append(f"| {construction_type} | {count} |")

    lines.extend(
        [
            "",
            "## Representative Cases",
            "",
        ]
    )
    shown = _representative_cases(cases, per_bucket_per_dataset)
    for case in shown:
        feature_text = ", ".join(
            f"{item['feature']}={_fmt(item['value'])}"
            for item in case.get("top_features", [])[:4]
        )
        lines.extend(
            [
                f"### {case['dataset']} / {case['bucket']} / rank {case['rank_in_bucket']}",
                "",
                f"- Orbit: `{case['orbit_id']}`",
                f"- Construction: `{case.get('construction_type')}`; label answerable: `{case.get('label_answerable')}`.",
                f"- Target score: `{_fmt(case.get('target_score'))}`; baseline score: `{_fmt(case.get('baseline_score'))}`; "
                f"target-baseline gap: `{_fmt(case.get('score_gap_target_minus_baseline'))}`.",
                f"- Query: {case.get('query')}",
                f"- Candidate answer: {case.get('candidate_answer')}",
                f"- Top features: {feature_text}",
                "",
            ]
        )

    lines.extend(
        [
            "## Claim Boundary",
            "",
            "This gallery is a paper-facing diagnostic artifact exported from private-label v4 failure analyses. "
            "It is useful for selecting qualitative examples, but it is not human-adjudicated evidence and "
            "must not be used as a substitute for human audit v4.",
            "",
        ]
    )
    return "\n".join(lines)


def _load_cases(inputs: Sequence[Path]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in inputs:
        payload = json.loads(path.read_text(encoding="utf-8"))
        dataset = _dataset_name(path)
        top_cases = payload.get("top_cases", {})
        for bucket, bucket_cases in top_cases.items():
            for index, case in enumerate(bucket_cases, start=1):
                cases.append(
                    {
                        **case,
                        "dataset": dataset,
                        "source_artifact": str(path),
                        "bucket": bucket,
                        "rank_in_bucket": index,
                    }
                )
    return cases


def _summary(
    cases: Sequence[dict[str, Any]],
    inputs: Sequence[Path],
    output_jsonl: Path,
    output_md: Path,
) -> dict[str, Any]:
    feature_counts = Counter()
    for case in cases:
        feature_counts.update(item["feature"] for item in case.get("top_features", [])[:4])
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [str(path) for path in inputs],
        "input_count": len(inputs),
        "case_count": len(cases),
        "bucket_counts": dict(sorted(Counter(case["bucket"] for case in cases).items())),
        "dataset_counts": dict(sorted(Counter(case["dataset"] for case in cases).items())),
        "construction_type_counts": dict(
            sorted(Counter(str(case.get("construction_type")) for case in cases).items())
        ),
        "label_answerable_counts": dict(
            sorted(Counter(str(case.get("label_answerable")) for case in cases).items())
        ),
        "top_feature_counts": dict(sorted(feature_counts.items(), key=lambda item: (-item[1], item[0]))),
        "outputs": {
            "jsonl": str(output_jsonl),
            "markdown": str(output_md),
        },
        "claim_boundary": (
            "Diagnostic case gallery exported from private-label v4 failure analyses; "
            "not human-adjudicated evidence."
        ),
    }


def _representative_cases(
    cases: Sequence[dict[str, Any]],
    per_bucket_per_dataset: int,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    counts: Counter[tuple[str, str]] = Counter()
    for case in sorted(cases, key=lambda item: (item["dataset"], item["bucket"], item["rank_in_bucket"])):
        key = (case["dataset"], case["bucket"])
        if counts[key] >= per_bucket_per_dataset:
            continue
        selected.append(case)
        counts[key] += 1
    return selected


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, nargs="+", default=DEFAULT_INPUTS)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--per-bucket-per-dataset", type=int, default=2)
    args = parser.parse_args()

    summary = export_v4_case_gallery(
        args.inputs,
        args.output_jsonl,
        args.output_md,
        args.summary_json,
        per_bucket_per_dataset=args.per_bucket_per_dataset,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
