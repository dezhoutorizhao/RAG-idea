#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_BASELINES = [
    {
        "requirement": "faithful_or_official_corm_rag",
        "plan_reference": "RAG-idea改进.md 5.5.2",
        "methods": ["corm_max_clean", "corm_mean_clean"],
        "status_if_present": "partial",
        "boundary": (
            "CoRM-derived clean/context reducers are present, but full faithful CoRM-RAG "
            "risk-aware end-to-end reproduction remains blocked."
        ),
    },
    {
        "requirement": "faithful_sure_style_multi_evidence",
        "plan_reference": "RAG-idea改进.md 5.5.2 / 6.4",
        "methods": ["faithful_sure_multi"],
        "status_if_present": "present",
        "boundary": "Multi-evidence SURE-style sufficiency aggregation is present.",
    },
    {
        "requirement": "context_sufficiency_classifier",
        "plan_reference": "RAG-idea改进.md 5.5.2",
        "methods": ["context_sufficiency_clean", "calibrated_logistic_context"],
        "status_if_present": "present",
        "boundary": "Context-sufficiency and learned context-only baselines are present.",
    },
    {
        "requirement": "llm_judge",
        "plan_reference": "RAG-idea改进.md 5.5.2 / 14.3 Phase 2",
        "methods": ["llm_judge", "llm_as_judge"],
        "status_if_present": "present",
        "boundary": (
            "No explicit LLM-as-judge baseline artifact is present in the current v4 baseline "
            "method union. Self-consistency proxy should not be reported as an LLM judge."
        ),
    },
    {
        "requirement": "self_consistency",
        "plan_reference": "RAG-idea改进.md 5.5.2",
        "methods": ["template_self_consistency"],
        "status_if_present": "present",
        "boundary": (
            "A deterministic template multi-sample generation self-consistency baseline is present; "
            "the older self_consistency_proxy remains lower-evidence diagnostic support."
        ),
    },
    {
        "requirement": "equal_budget_orbit_ensemble",
        "plan_reference": "RAG-idea改进.md 5.5.2",
        "methods": [
            "equal_budget_mean",
            "equal_budget_min",
            "equal_budget_q25",
            "equal_budget_ensemble_logistic",
        ],
        "status_if_present": "present",
        "boundary": "Equal-budget reducers and out-of-fold logistic ensemble are present.",
    },
    {
        "requirement": "retrieval_stability",
        "plan_reference": "RAG-idea改进.md 5.5.2",
        "methods": ["retrieval_stability"],
        "status_if_present": "present",
        "boundary": "Retrieval-stability shortcut baseline is present.",
    },
    {
        "requirement": "calibrated_logistic_baseline",
        "plan_reference": "RAG-idea改进.md 5.5.2 / 5.6",
        "methods": ["calibrated_logistic_context", "calibrated_logistic_orbit"],
        "status_if_present": "present",
        "boundary": "Learned calibrated context/orbit baselines are present.",
    },
]


def summarize_v4_baseline_coverage(strong_baseline_summary: Path) -> dict[str, Any]:
    strong = _load_json(strong_baseline_summary)
    method_union = set(strong.get("aggregate", {}).get("method_union", []))
    rows = [_coverage_row(requirement, method_union) for requirement in REQUIRED_BASELINES]
    counts = _status_counts(rows)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(strong_baseline_summary),
        "method_union": sorted(method_union),
        "rows": rows,
        "status_counts": counts,
        "all_required_baselines_present": counts.get("missing", 0) == 0
        and counts.get("partial", 0) == 0,
        "claim_policy": (
            "This matrix audits coverage of required strong-baseline families. It does not "
            "upgrade proxy or partial baselines into faithful end-to-end baselines."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# V4 Baseline Coverage Matrix",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Source: `{summary['source']}`",
        "",
        f"All required baselines present: `{summary['all_required_baselines_present']}`",
        f"Status counts: `{summary['status_counts']}`",
        "",
        "## Method Union",
        "",
        "`" + ", ".join(summary["method_union"]) + "`",
        "",
        "## Required Baselines",
        "",
        "| Requirement | Status | Matched methods | Missing methods | Boundary |",
        "|---|---|---|---|---|",
    ]
    for row in summary["rows"]:
        lines.append(
            f"| {row['requirement']} | `{row['status']}` | "
            f"`{', '.join(row['matched_methods'])}` | "
            f"`{', '.join(row['missing_methods'])}` | {row['boundary']} |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _coverage_row(requirement: dict[str, Any], method_union: set[str]) -> dict[str, Any]:
    required_methods = list(requirement["methods"])
    matched = [method for method in required_methods if method in method_union]
    missing = [method for method in required_methods if method not in method_union]
    if matched:
        status = requirement["status_if_present"]
    else:
        status = "missing"
    return {
        "requirement": requirement["requirement"],
        "plan_reference": requirement["plan_reference"],
        "status": status,
        "required_methods": required_methods,
        "matched_methods": matched,
        "missing_methods": missing,
        "boundary": requirement["boundary"],
    }


def _status_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        status: sum(1 for row in rows if row["status"] == status)
        for status in ["present", "partial", "missing"]
    }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strong-baseline-summary",
        type=Path,
        default=Path("results/v4_strong_baseline_summary_20260529.json"),
    )
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_v4_baseline_coverage(args.strong_baseline_summary)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
