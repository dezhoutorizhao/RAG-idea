#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = "pass"
PARTIAL = "partial"
MISSING = "missing"


def summarize_v4_split_threshold_protocol(
    strong_baseline_summary: Path,
    threshold_summary: Path = Path("results/v4_shared_threshold_selection_20260529.json"),
) -> dict[str, Any]:
    strong = _load_json(strong_baseline_summary)
    baseline_payloads = _load_artifacts(strong_baseline_summary, strong.get("baseline_rows", []))
    comparison_payloads = _load_artifacts(strong_baseline_summary, strong.get("comparison_rows", []))
    threshold_payload = _load_json(threshold_summary) if threshold_summary.exists() else None
    rows = _protocol_rows(baseline_payloads, comparison_payloads, strong, threshold_payload)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(strong_baseline_summary),
        "threshold_source": str(threshold_summary),
        "baseline_file_count": len(baseline_payloads),
        "comparison_file_count": len(comparison_payloads),
        "rows": rows,
        "status_counts": _status_counts(rows),
        "source_item_group_split_supported": _row_status(rows, "source_item_group_split") == PASS,
        "threshold_selection_claim_supported": _row_status(rows, "shared_calibration_threshold_selection") == PASS,
        "protocol_complete": all(row["status"] == PASS for row in rows),
        "claim_policy": (
            "This audit covers the route-plan requirements that comparisons use the same inputs, "
            "same group split, and same threshold-selection protocol. It supports the current ranking "
            "and fixed-coverage comparison scope, but it does not claim a shared calibration-threshold "
            "selective-RAG protocol because that experiment has not been run for every baseline."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# V4 Split and Threshold Protocol",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Source: `{summary['source']}`",
        f"Threshold source: `{summary['threshold_source']}`",
        "",
        f"Baseline files: `{summary['baseline_file_count']}`",
        f"Comparison files: `{summary['comparison_file_count']}`",
        f"Source-item group split supported: `{summary['source_item_group_split_supported']}`",
        f"Shared calibration-threshold claim supported: `{summary['threshold_selection_claim_supported']}`",
        f"Protocol complete: `{summary['protocol_complete']}`",
        f"Status counts: `{summary['status_counts']}`",
        "",
        "## Protocol Matrix",
        "",
        "| Requirement | Status | Evidence | Boundary |",
        "|---|---|---|---|",
    ]
    for row in summary["rows"]:
        evidence = "<br>".join(row["evidence"])
        lines.append(
            f"| {row['requirement']} | `{row['status']}` | {evidence} | {row['boundary']} |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _protocol_rows(
    baseline_payloads: list[dict[str, Any]],
    comparison_payloads: list[dict[str, Any]],
    strong: dict[str, Any],
    threshold_payload: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    return [
        _row(
            "same_input_rows",
            PASS if _all_baseline_fairness(baseline_payloads, "same_input_rows") else MISSING,
            [
                f"baseline files with fairness flag: {len(baseline_payloads)}",
                "fairness.same_input_rows is true in every loaded baseline artifact",
            ],
            "The audit is limited to loaded v4 baseline artifacts referenced by the strong-baseline summary.",
        ),
        _row(
            "same_scored_evidence",
            PASS if _all_baseline_fairness(baseline_payloads, "same_scored_evidence") else MISSING,
            [
                f"baseline files with fairness flag: {len(baseline_payloads)}",
                "fairness.same_scored_evidence is true in every loaded baseline artifact",
            ],
            "This verifies shared scored evidence files, not external LLM judge calls.",
        ),
        _row(
            "source_item_group_split",
            PASS if _all_comparisons_have_group_split(comparison_payloads) else MISSING,
            [
                f"comparison files: {len(comparison_payloads)}",
                "each per-seed result records train/calibration/test source-item group counts",
            ],
            "The comparison script uses source_item_group_id groups; this does not by itself add human labels.",
        ),
        _row(
            "out_of_fold_logistic_baseline_split",
            PASS if _all_out_of_fold_by_group(baseline_payloads) else PARTIAL,
            [
                "standalone baseline artifacts record logistic_scores='out-of-fold by source_item_group_id when possible'",
                f"baseline files checked: {len(baseline_payloads)}",
            ],
            "This covers standalone baseline scoring; train/test comparison artifacts train learned baselines inside each split.",
        ),
        _row(
            "target_calibration_split",
            PASS if _all_calibrated_targets_have_calibration(comparison_payloads) else PARTIAL,
            [
                "comparison artifacts include train_frac, cal_frac, seeds, and calibration split sizes",
                "calibrated CSRM targets are fit with train and calibration orbits before test scoring",
            ],
            "This supports calibrated CSRM targets, not a universal baseline threshold-selection protocol.",
        ),
        _row(
            "shared_calibration_threshold_selection",
            PASS if _threshold_protocol_complete(threshold_payload) else MISSING,
            _threshold_evidence(threshold_payload),
            _threshold_boundary(threshold_payload),
        ),
        _row(
            "failed_baselines_reported",
            PASS if _failed_baselines_are_reported(strong) else MISSING,
            [
                "v4 strong-baseline summary records losses/ties/wins against strongest baselines",
                "coverage and budget-parity matrices preserve partial/missing baseline boundaries",
            ],
            "Negative and partial baseline evidence must remain in the paper-facing limitations.",
        ),
    ]


def _row(requirement: str, status: str, evidence: list[str], boundary: str) -> dict[str, Any]:
    return {
        "requirement": requirement,
        "status": status,
        "evidence": evidence,
        "boundary": boundary,
    }


def _load_artifacts(strong_path: Path, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    payloads = []
    root = strong_path.parent.parent
    for row in rows:
        artifact = row.get("artifact")
        if not artifact:
            continue
        path = Path(artifact)
        if not path.is_absolute():
            path = root / path
        if path.exists():
            payload = _load_json(path)
            payload["_artifact"] = str(path)
            payloads.append(payload)
    return payloads


def _all_baseline_fairness(payloads: list[dict[str, Any]], key: str) -> bool:
    return bool(payloads) and all(bool(payload.get("fairness", {}).get(key)) for payload in payloads)


def _all_out_of_fold_by_group(payloads: list[dict[str, Any]]) -> bool:
    if not payloads:
        return False
    for payload in payloads:
        note = str(payload.get("fairness", {}).get("logistic_scores", "")).lower()
        if "out-of-fold" not in note or "source_item_group_id" not in note:
            return False
    return True


def _all_comparisons_have_group_split(payloads: list[dict[str, Any]]) -> bool:
    if not payloads:
        return False
    return all(_comparison_has_group_split(payload) for payload in payloads)


def _comparison_has_group_split(payload: dict[str, Any]) -> bool:
    if not payload.get("source_item_groups"):
        return False
    if not payload.get("seeds"):
        return False
    for seed_row in payload.get("per_seed", []):
        sizes = seed_row.get("split_sizes", {})
        if not all(sizes.get(key, 0) > 0 for key in ["train_groups", "calibration_groups", "test_groups"]):
            return False
    return True


def _all_calibrated_targets_have_calibration(payloads: list[dict[str, Any]]) -> bool:
    if not payloads:
        return False
    for payload in payloads:
        if float(payload.get("cal_frac", 0.0)) <= 0.0:
            return False
        for seed_row in payload.get("per_seed", []):
            sizes = seed_row.get("split_sizes", {})
            if sizes.get("calibration", 0) <= 0 or sizes.get("calibration_groups", 0) <= 0:
                return False
            targets = set(seed_row.get("target_metrics", {}))
            if not {
                "csrm_calibrated_logistic",
                "csrm_calibrated_isotonic",
                "csrm_calibrated_gbdt",
            }.issubset(targets):
                return False
    return True


def _failed_baselines_are_reported(strong: dict[str, Any]) -> bool:
    aggregate = strong.get("aggregate", {})
    by_auroc = aggregate.get("csrm_rule_vs_strongest", {}).get("by_auroc", {})
    if by_auroc.get("losses"):
        return True
    for row in strong.get("comparison_rows", []):
        for target in row.get("targets", {}).values():
            for metric in target.values():
                if metric.get("losses_against_baselines", 0) > 0 or metric.get("ties_against_baselines", 0) > 0:
                    return True
    return False


def _threshold_protocol_complete(payload: dict[str, Any] | None) -> bool:
    if not payload:
        return False
    protocol = payload.get("protocol", {})
    return bool(
        payload.get("shared_threshold_protocol_complete")
        and payload.get("dataset_count", 0) >= 6
        and protocol.get("threshold_selected_on") == "calibration split"
        and protocol.get("threshold_applied_to") == "held-out test split"
    )


def _threshold_evidence(payload: dict[str, Any] | None) -> list[str]:
    if not payload:
        return [
            "compare_calibrated artifacts report fixed-coverage AUROC/risk/AURC metrics",
            "no shared-threshold artifact is available",
        ]
    return [
        f"threshold artifact datasets: {payload.get('dataset_count')}",
        f"seeds: {payload.get('seeds')}",
        f"risk targets: {payload.get('risk_targets')}",
        f"protocol complete: {payload.get('shared_threshold_protocol_complete')}",
    ]


def _threshold_boundary(payload: dict[str, Any] | None) -> str:
    if not payload:
        return (
            "The current evidence is valid for ranking/fixed-coverage comparisons, but not for a "
            "shared risk-target threshold-selection claim across every baseline."
        )
    return (
        "The shared-threshold protocol is now auditable. Test risk may still miss the calibration target, "
        "so this closes protocol fairness rather than proving formal risk control."
    )


def _row_status(rows: list[dict[str, Any]], requirement: str) -> str | None:
    for row in rows:
        if row["requirement"] == requirement:
            return row["status"]
    return None


def _status_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        status: sum(1 for row in rows if row["status"] == status)
        for status in [PASS, PARTIAL, MISSING]
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
    parser.add_argument(
        "--threshold-summary",
        type=Path,
        default=Path("results/v4_shared_threshold_selection_20260529.json"),
    )
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_v4_split_threshold_protocol(args.strong_baseline_summary, args.threshold_summary)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
