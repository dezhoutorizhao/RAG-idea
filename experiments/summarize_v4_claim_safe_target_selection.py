#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_STRONG_BASELINES = Path("results/v4_strong_baseline_summary_20260529.json")
DEFAULT_BASELINE_COVERAGE = Path("results/v4_baseline_coverage_matrix_20260529.json")
DEFAULT_CALIBRATION_QUALITY = Path("results/v4_calibration_quality_20260529.json")
DEFAULT_HUMAN_COLLECTION = Path("results/human_audit_v4_batch_collection_20260529.json")
DEFAULT_TEXT_ONLY = Path("results/text_only_verifier_status_20260529.json")

PRIMARY_CANDIDATES = [
    "csrm_calibrated_gbdt",
    "csrm_calibrated_logistic",
    "csrm_calibrated_isotonic",
]
KEY_METRICS = [
    "auroc_improvement",
    "auprc_improvement",
    "risk_at_30_reduction",
    "risk_at_50_reduction",
    "risk_at_70_reduction",
    "aurc_reduction",
]


def summarize_v4_claim_safe_target_selection(
    strong_baselines_path: Path = DEFAULT_STRONG_BASELINES,
    baseline_coverage_path: Path = DEFAULT_BASELINE_COVERAGE,
    calibration_quality_path: Path = DEFAULT_CALIBRATION_QUALITY,
    human_collection_path: Path = DEFAULT_HUMAN_COLLECTION,
    text_only_path: Path = DEFAULT_TEXT_ONLY,
) -> dict[str, Any]:
    strong = _load_json(strong_baselines_path)
    coverage = _load_json(baseline_coverage_path)
    calibration = _load_json(calibration_quality_path)
    human = _load_json(human_collection_path)
    text_only = _load_json(text_only_path)

    candidate_rows = [
        _candidate_row(candidate, strong, calibration)
        for candidate in PRIMARY_CANDIDATES
        if candidate in strong.get("aggregate", {}).get("calibrated_targets_vs_all_baselines", {})
    ]
    recommended = _choose_recommended(candidate_rows)
    rule_negative = strong.get("aggregate", {}).get("csrm_rule_vs_strongest", {})
    missing_requirements = [
        {
            "requirement": row.get("requirement"),
            "status": row.get("status"),
            "boundary": row.get("boundary"),
        }
        for row in coverage.get("rows", [])
        if row.get("status") != "present"
    ]
    blocked_items = _blocked_items(coverage, human, text_only)
    all_win_supported = bool(recommended) and recommended["total_losses"] == 0 and not blocked_items
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "strong_baselines": str(strong_baselines_path),
            "baseline_coverage": str(baseline_coverage_path),
            "calibration_quality": str(calibration_quality_path),
            "human_collection": str(human_collection_path),
            "text_only": str(text_only_path),
        },
        "recommended_primary_target": None if recommended is None else recommended["method"],
        "candidate_rows": candidate_rows,
        "csrm_rule_negative_evidence": rule_negative,
        "baseline_missing_or_partial_requirements": missing_requirements,
        "blocked_items": blocked_items,
        "all_win_supported": all_win_supported,
        "claim_safe_status": "partial",
        "allowed_wording": _allowed_wording(recommended),
        "disallowed_wording": [
            "CSRM-Rule is the primary method against strong learned/context baselines.",
            "CSRM or any calibrated variant is all-win across the current v4 strong-baseline suite.",
            "The strong-baseline evidence is complete without an LLM-as-judge baseline.",
            "The current results are human-audited.",
            "The calibrated model establishes a formal risk-control guarantee.",
        ],
        "claim_policy": (
            "This artifact selects the safest paper-facing target wording from the current "
            "strong-baseline and calibration evidence. It is a claim-boundary audit, not a new "
            "human label source, LLM judge run, or full CoRM-RAG reproduction."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# V4 Claim-Safe Target Selection",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Recommended primary target: `{summary['recommended_primary_target']}`",
        f"All-win supported: `{summary['all_win_supported']}`",
        f"Claim-safe status: `{summary['claim_safe_status']}`",
        "",
        "## Candidate Targets",
        "",
        "| Method | Robust wins | Ties | Losses | Mean worst-case delta | Brier wins | ECE wins | Recommendation |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary["candidate_rows"]:
        lines.append(
            f"| {row['method']} | {row['total_robust_wins']} | {row['total_ties']} | "
            f"{row['total_losses']} | {_fmt(row['mean_worst_case_delta'])} | "
            f"{row['brier_win_count']} | {row['ece_win_count']} | {row['recommendation']} |"
        )
    lines.extend(
        [
            "",
            "## Missing Or Partial Baselines",
            "",
            "| Requirement | Status | Boundary |",
            "|---|---|---|",
        ]
    )
    for row in summary["baseline_missing_or_partial_requirements"]:
        lines.append(f"| {row['requirement']} | `{row['status']}` | {row['boundary']} |")
    lines.extend(["", "## Blocked Items", ""])
    lines.extend(f"- {item}" for item in summary["blocked_items"])
    lines.extend(["", "## Allowed Wording", ""])
    lines.extend(f"- {item}" for item in summary["allowed_wording"])
    lines.extend(["", "## Disallowed Wording", ""])
    lines.extend(f"- {item}" for item in summary["disallowed_wording"])
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _candidate_row(method: str, strong: dict[str, Any], calibration: dict[str, Any]) -> dict[str, Any]:
    metrics = strong["aggregate"]["calibrated_targets_vs_all_baselines"][method]
    wins = sum(metrics[metric]["robust_wins"] for metric in KEY_METRICS)
    ties = sum(metrics[metric]["ties"] for metric in KEY_METRICS)
    losses = sum(metrics[metric]["losses"] for metric in KEY_METRICS)
    deltas = [metrics[metric]["mean_worst_case_delta"] for metric in KEY_METRICS]
    calibration_rows = [
        row for row in calibration.get("rows", [])
        if row.get("best_target_by_brier", {}).get("method") == method
        or row.get("best_target_by_ece", {}).get("method") == method
    ]
    brier_wins = sum(
        1
        for row in calibration.get("rows", [])
        if row.get("best_target_by_brier", {}).get("method") == method
    )
    ece_wins = sum(
        1
        for row in calibration.get("rows", [])
        if row.get("best_target_by_ece", {}).get("method") == method
    )
    return {
        "method": method,
        "metric_rows": metrics,
        "total_robust_wins": wins,
        "total_ties": ties,
        "total_losses": losses,
        "mean_worst_case_delta": sum(deltas) / len(deltas),
        "brier_win_count": brier_wins,
        "ece_win_count": ece_wins,
        "calibration_dataset_mentions": len(calibration_rows),
        "recommendation": _recommendation(method, losses, wins, brier_wins, ece_wins),
    }


def _choose_recommended(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not rows:
        return None
    return sorted(
        rows,
        key=lambda row: (
            row["total_losses"],
            -row["total_robust_wins"],
            -row["brier_win_count"],
            -row["ece_win_count"],
            -row["mean_worst_case_delta"],
        ),
    )[0]


def _recommendation(method: str, losses: int, wins: int, brier_wins: int, ece_wins: int) -> str:
    if losses == 0:
        return "primary_candidate"
    if method == "csrm_calibrated_gbdt" and wins > 0 and brier_wins > 0:
        return "primary_with_caveats"
    if wins > 0 or brier_wins > 0 or ece_wins > 0:
        return "secondary_or_ablation"
    return "do_not_use_as_primary"


def _blocked_items(coverage: dict[str, Any], human: dict[str, Any], text_only: dict[str, Any]) -> list[str]:
    blocked = []
    coverage_rows = {row.get("requirement"): row for row in coverage.get("rows", [])}
    llm = coverage_rows.get("llm_judge")
    if llm and llm.get("status") != "present":
        blocked.append("LLM-as-judge baseline is still missing.")
    corm = coverage_rows.get("faithful_or_official_corm_rag")
    if corm and corm.get("status") != "present":
        blocked.append("Faithful/full CoRM-RAG baseline remains partial until full reproduction is complete.")
    if not human.get("human_labels_complete"):
        blocked.append(
            f"Human audit labels are incomplete: pending auditor labels="
            f"{human.get('pending_auditor_labels')}, pending adjudicated labels="
            f"{human.get('pending_adjudicated_labels')}."
        )
    if not text_only.get("ready_for_text_only_main_claim"):
        blocked.append("Text-only verifier main claim is blocked by missing LLM correlation and human labels.")
    return blocked


def _allowed_wording(recommended: dict[str, Any] | None) -> list[str]:
    target = "the calibrated CSRM target" if recommended is None else recommended["method"]
    return [
        f"Use `{target}` as the current paper-facing target only with caveats.",
        "Claim empirical calibrated-orbit selective-risk evidence, not all-win behavior.",
        "Report CSRM-Rule as a mechanism baseline with negative evidence against strong learned/context baselines.",
        "State that LLM-as-judge, human audit, and full CoRM-RAG reproduction remain open blockers.",
    ]


def _fmt(value: Any) -> str:
    return "n/a" if value is None else f"{float(value):.4f}"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strong-baselines", type=Path, default=DEFAULT_STRONG_BASELINES)
    parser.add_argument("--baseline-coverage", type=Path, default=DEFAULT_BASELINE_COVERAGE)
    parser.add_argument("--calibration-quality", type=Path, default=DEFAULT_CALIBRATION_QUALITY)
    parser.add_argument("--human-collection", type=Path, default=DEFAULT_HUMAN_COLLECTION)
    parser.add_argument("--text-only", type=Path, default=DEFAULT_TEXT_ONLY)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_v4_claim_safe_target_selection(
        args.strong_baselines,
        args.baseline_coverage,
        args.calibration_quality,
        args.human_collection,
        args.text_only,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
