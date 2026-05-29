#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


METHOD_BUDGETS = {
    "corm_max_clean": {
        "status": "lower_budget_control",
        "evidence_scope": "clean_set_only",
        "verifier_call_budget": "clean evidence only",
        "llm_call_budget": 0,
        "boundary": "Uses less orbit evidence than CSRM; keep as a control, not an equal-orbit-budget baseline.",
    },
    "corm_mean_clean": {
        "status": "lower_budget_control",
        "evidence_scope": "clean_set_only",
        "verifier_call_budget": "clean evidence only",
        "llm_call_budget": 0,
        "boundary": "Uses less orbit evidence than CSRM; keep as a control, not an equal-orbit-budget baseline.",
    },
    "context_sufficiency_clean": {
        "status": "lower_budget_control",
        "evidence_scope": "clean_set_only",
        "verifier_call_budget": "clean evidence only",
        "llm_call_budget": 0,
        "boundary": "Single-set context sufficiency control; not equal to orbit-level call budget.",
    },
    "calibrated_logistic_context": {
        "status": "lower_budget_control",
        "evidence_scope": "clean_set_only",
        "verifier_call_budget": "clean evidence features only",
        "llm_call_budget": 0,
        "boundary": "Learned context-only baseline; lower evidence budget than orbit-level methods.",
    },
    "faithful_sure_multi": {
        "status": "equal_orbit_budget",
        "evidence_scope": "all_orbit_sets",
        "verifier_call_budget": "all scored evidence sets in the orbit",
        "llm_call_budget": 0,
        "boundary": "Uses the same scored orbit evidence batch as CSRM.",
    },
    "equal_budget_mean": {
        "status": "equal_orbit_budget",
        "evidence_scope": "all_orbit_sets",
        "verifier_call_budget": "all scored evidence sets in the orbit",
        "llm_call_budget": 0,
        "boundary": "Equal-budget naive orbit aggregation baseline.",
    },
    "equal_budget_min": {
        "status": "equal_orbit_budget",
        "evidence_scope": "all_orbit_sets",
        "verifier_call_budget": "all scored evidence sets in the orbit",
        "llm_call_budget": 0,
        "boundary": "Equal-budget worst-set orbit aggregation baseline.",
    },
    "equal_budget_q25": {
        "status": "equal_orbit_budget",
        "evidence_scope": "all_orbit_sets",
        "verifier_call_budget": "all scored evidence sets in the orbit",
        "llm_call_budget": 0,
        "boundary": "Equal-budget quantile orbit aggregation baseline.",
    },
    "retrieval_stability": {
        "status": "equal_orbit_budget",
        "evidence_scope": "all_orbit_sets",
        "verifier_call_budget": "all scored evidence sets in the orbit",
        "llm_call_budget": 0,
        "boundary": "Uses the same scored orbit evidence batch as CSRM, with retrieval-stability aggregation.",
    },
    "self_consistency_proxy": {
        "status": "proxy_equal_orbit_budget",
        "evidence_scope": "all_orbit_sets",
        "verifier_call_budget": "all scored evidence sets in the orbit",
        "llm_call_budget": 0,
        "boundary": "Proxy over existing answer consistency features; not a fresh multi-sample generation baseline.",
    },
    "template_self_consistency": {
        "status": "equal_orbit_budget",
        "evidence_scope": "all_orbit_sets",
        "verifier_call_budget": "all scored evidence sets in the orbit",
        "llm_call_budget": 0,
        "boundary": "Deterministic multi-template generation self-consistency over the same scored orbit evidence.",
    },
    "equal_budget_ensemble_logistic": {
        "status": "equal_orbit_budget",
        "evidence_scope": "non_csrm_baseline_scores",
        "verifier_call_budget": "same non-CSRM score batch, out-of-fold by source group when possible",
        "llm_call_budget": 0,
        "boundary": "Equal-budget score-fusion baseline; excludes CSRM-specific scores.",
    },
    "calibrated_logistic_orbit": {
        "status": "equal_orbit_budget",
        "evidence_scope": "all_orbit_sets",
        "verifier_call_budget": "all scored evidence sets in the orbit",
        "llm_call_budget": 0,
        "boundary": "Learned orbit-feature baseline using the same scored orbit evidence batch.",
    },
    "csrm_rule": {
        "status": "target_method",
        "evidence_scope": "all_orbit_sets",
        "verifier_call_budget": "all scored evidence sets in the orbit",
        "llm_call_budget": 0,
        "boundary": "Target method used as the budget reference.",
    },
}


def summarize_v4_baseline_budget_parity(strong_baseline_summary: Path) -> dict[str, Any]:
    strong = _load_json(strong_baseline_summary)
    method_union = sorted(strong.get("aggregate", {}).get("method_union", []))
    rows = [_budget_row(method) for method in method_union]
    missing_llm = {
        "method": "llm_judge",
        "status": "missing",
        "evidence_scope": "not_run",
        "verifier_call_budget": "not run",
        "llm_call_budget": "not run",
        "boundary": "No explicit LLM-as-judge baseline artifact exists in this batch.",
    }
    rows.append(missing_llm)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(strong_baseline_summary),
        "method_count": len(method_union),
        "rows": rows,
        "status_counts": _status_counts(rows),
        "same_input_rows_all_files": _all_fairness(strong.get("baseline_rows", []), strong_baseline_summary, "same_input_rows"),
        "same_scored_evidence_all_files": _all_fairness(
            strong.get("baseline_rows", []), strong_baseline_summary, "same_scored_evidence"
        ),
        "budget_parity_claim_supported": False,
        "claim_policy": (
            "This audit documents baseline budget parity. It supports equal-orbit-budget claims "
            "only for methods marked equal_orbit_budget, and explicitly excludes clean-only controls, "
            "proxy self-consistency, and the missing LLM judge baseline from full parity claims."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# V4 Baseline Budget Parity",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Source: `{summary['source']}`",
        "",
        f"Method count: `{summary['method_count']}`",
        f"Status counts: `{summary['status_counts']}`",
        f"Same input rows across files: `{summary['same_input_rows_all_files']}`",
        f"Same scored evidence across files: `{summary['same_scored_evidence_all_files']}`",
        f"Full budget-parity claim supported: `{summary['budget_parity_claim_supported']}`",
        "",
        "## Method Budgets",
        "",
        "| Method | Status | Evidence scope | Verifier-call budget | LLM calls | Boundary |",
        "|---|---|---|---|---:|---|",
    ]
    for row in summary["rows"]:
        lines.append(
            f"| {row['method']} | `{row['status']}` | {row['evidence_scope']} | "
            f"{row['verifier_call_budget']} | `{row['llm_call_budget']}` | {row['boundary']} |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _budget_row(method: str) -> dict[str, Any]:
    spec = METHOD_BUDGETS.get(
        method,
        {
            "status": "unknown",
            "evidence_scope": "unknown",
            "verifier_call_budget": "unknown",
            "llm_call_budget": "unknown",
            "boundary": "Method is not in the budget specification table.",
        },
    )
    return {"method": method, **spec}


def _all_fairness(baseline_rows: list[dict[str, Any]], strong_path: Path, key: str) -> bool | None:
    values = []
    for row in baseline_rows:
        artifact = row.get("artifact")
        if not artifact:
            continue
        path = Path(artifact)
        if not path.is_absolute():
            path = strong_path.parent.parent / path
        if not path.exists():
            continue
        payload = _load_json(path)
        values.append(bool(payload.get("fairness", {}).get(key)))
    return all(values) if values else None


def _status_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    statuses = sorted({str(row["status"]) for row in rows})
    return {status: sum(1 for row in rows if row["status"] == status) for status in statuses}


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

    summary = summarize_v4_baseline_budget_parity(args.strong_baseline_summary)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
