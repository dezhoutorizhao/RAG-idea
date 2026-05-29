#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = "pass"
PARTIAL = "partial"
FAIL = "fail"
BLOCKED = "blocked"


def summarize_neurips_readiness(root: Path) -> dict[str, Any]:
    results = root / "results"
    closure = _load_json(results / "evidence_closure_status_v4.json")
    manifest = _load_json(results / "v4_evidence_package_manifest_20260529.json")
    reproduction = _load_json(results / "current_evidence_reproduction_20260529.json")
    text_only = _load_optional_json(results / "text_only_verifier_status_20260529.json")
    theory = _load_optional_json(results / "theory_formalization_status_20260529.json")
    novelty = _load_optional_json(results / "novelty_audit_20260529.json")
    external_review = _load_optional_json(results / "external_review_packet_status_20260529.json")
    rows = _rows(closure, manifest, reproduction, text_only, theory, novelty, external_review)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "plan": "RAG-idea改进.md Sections 13.1/13.2 plus current closure blockers",
            "closure": "results/evidence_closure_status_v4.json",
            "manifest": "results/v4_evidence_package_manifest_20260529.json",
            "reproduction": "results/current_evidence_reproduction_20260529.json",
            "text_only_verifier": "results/text_only_verifier_status_20260529.json",
            "theory_formalization": "results/theory_formalization_status_20260529.json",
            "novelty_audit": "results/novelty_audit_20260529.json",
            "external_review": "results/external_review_packet_status_20260529.json",
        },
        "rows": rows,
        "status_counts": _status_counts(rows),
        "ready_for_neurips_main_track": all(row["status"] == PASS for row in rows),
        "hard_blockers": [row for row in rows if row["status"] == BLOCKED],
        "negative_or_partial_evidence": [row for row in rows if row["status"] in {FAIL, PARTIAL}],
        "claim_policy": (
            "This matrix tracks readiness against the NeurIPS main-track evidence plan. "
            "A pass means the current artifact supports that checklist item at the stated scope; "
            "partial means useful evidence exists but is too narrow or mixed; fail means current "
            "evidence contradicts the strong version of the requirement; blocked means the item "
            "cannot be completed without human labels, storage repair/approval, or an external review."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# NeurIPS Readiness Matrix",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Ready for NeurIPS main-track claim: `{summary['ready_for_neurips_main_track']}`",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in summary["status_counts"].items():
        lines.append(f"- {status}: `{count}`")

    lines.extend(
        [
            "",
            "## Checklist",
            "",
            "| Requirement | Status | Evidence | Boundary / next action |",
            "|---|---|---|---|",
        ]
    )
    for row in summary["rows"]:
        evidence = "<br>".join(f"`{item}`" for item in row["evidence"])
        lines.append(
            f"| {row['requirement']} | `{row['status']}` | {evidence} | {row['boundary_or_next_action']} |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _rows(
    closure: dict[str, Any],
    manifest: dict[str, Any],
    reproduction: dict[str, Any],
    text_only: dict[str, Any],
    theory: dict[str, Any],
    novelty: dict[str, Any],
    external_review: dict[str, Any],
) -> list[dict[str, Any]]:
    latest = closure.get("latest_v4_diagnostics", {})
    strong = closure.get("v4_strong_baselines") or {}
    end2end = closure.get("end2end_selective_rag_proxy") or {}
    mechanism = closure.get("mechanism_ablation") or {}
    calibration = closure.get("v4_calibration_quality") or {}
    risk = closure.get("risk_control") or {}
    reconstruction = closure.get("corm_reconstruction") or {}
    storage_probe = reconstruction.get("latest_storage_probe") or {}
    gate = reproduction.get("gate_summary", {})
    return [
        _row(
            "Leakage-free v4 pipeline",
            PASS if _g(latest, "anti_shortcut", "pass_core_anti_shortcut_suite") else FAIL,
            [
                "results/v4_anti_shortcut_summary_20260529.json",
                "results/evidence_closure_status_v4.json",
            ],
            "Core anti-shortcut suite passes; private construction metadata remains evaluator-only.",
        ),
        _row(
            "Human-audited orbit labels",
            BLOCKED if not gate.get("human_audit_v4_ready") else PASS,
            [
                "results/human_audit_v4_paper_pack_status_20260529.json",
                "results/human_audit_v4_assignment_batches_20260529.json",
                "results/human_audit_v4_batch_collection_20260529.json",
                "results/human_audit_v4_status_20260529.json",
                "results/human_audit_v4_disagreement_taxonomy_20260529.json",
                "results/human_audit_v4_mismatch_20260529.json",
                "results/human_audit_v4_eval_status_20260529.json",
            ],
            (
                f"Assignment batches ready: {gate.get('human_audit_v4_assignment_ready')}; "
                f"batch collection complete: {gate.get('human_audit_v4_batch_collection_complete')}; "
                f"pending labels: {gate.get('human_audit_v4_pending')}; "
                "cannot claim human-audited results."
            ),
        ),
        _row(
            "Text-only semantic verifier",
            PASS
            if text_only.get("ready_for_text_only_main_claim")
            else PARTIAL
            if _g(text_only, "nli_probe", "directional_advantage_ready")
            else FAIL,
            [
                "results/text_only_verifier_status_20260529.json",
                "results/audit_sample_paper_1000_v3_nli_set_eval.json",
                "results/llm_judge_v4_request_status_20260529.json",
            ],
            (
                "NLI cross-scorer evidence is directionally positive against required weak baselines, "
                "but LLM-NLI correlation and human-label text-only evaluation are not ready."
            ),
        ),
        _row(
            "Strong baselines and equal-budget controls",
            PARTIAL if strong else FAIL,
            [
                "results/v4_strong_baseline_summary_20260529.json",
                "results/v4_baseline_coverage_matrix_20260529.json",
                "results/v4_baseline_budget_parity_20260529.json",
                "results/v4_shared_threshold_selection_20260529.json",
                "results/v4_split_threshold_protocol_20260529.json",
                "results/risk_control_abstention_baselines_20260529.json",
                "results/llm_judge_v4_request_status_20260529.json",
            ],
            (
                "Baseline package exists, but CSRM-Rule has losses/ties against strongest learned/context baselines; "
                "coverage/budget matrices still mark faithful CoRM as partial, clean-only controls as lower-budget, "
                "and LLM judge scores as missing. The LLM judge request pack is ready, but no API-backed "
                "score artifact exists. Template multi-sample self-consistency, risk-control abstention baselines, "
                "and shared calibration-threshold selection are auditable, but test risk/coverage remains mixed "
                "rather than all-win."
            ),
        ),
        _row(
            "End-to-end selective RAG",
            PARTIAL if end2end and end2end.get("row_count") else FAIL,
            [
                "results/end2end_selective_rag_proxy_summary_20260529.json",
                "results/end2end_retriever_generator_matrix_20260529.json",
                "results/end2end_risk_coverage_curves_20260529.json",
                "results/end2end_target_risk_coverage_20260529.json",
                "paper/figures/end2end_risk_coverage_curves_20260529.svg",
            ],
            (
                "Proxy evidence now covers two local retrievers and two generators, but remains mixed "
                "and is not a full CoRM-RAG Wikipedia retrieval-generation reproduction. The "
                "risk-coverage and target-risk coverage artifacts summarize lower accepted-error "
                "risk at fixed coverage and higher coverage at fixed target risk, but do not remove "
                "the full-reproduction boundary."
            ),
        ),
        _row(
            "Full CoRM-RAG reproduction",
            BLOCKED if not reconstruction.get("preflight_ready") else PASS,
            [
                "results/corm_reproduction_preflight.json",
                "results/corm_full_wikipedia_job_status.json",
                "results/remote_storage_status_20260529.json",
            ],
            _full_corm_boundary(storage_probe),
        ),
        _row(
            "Mechanism ablations",
            PASS if mechanism.get("strong_alignment_evidence") else PARTIAL,
            ["results/mechanism_ablation_summary_20260529.json"],
            "Alignment evidence is strong; no-worst-sufficiency is weak/redundant in current bridge artifacts.",
        ),
        _row(
            "Theory and formalization",
            PASS if theory.get("theory_module_ready") else PARTIAL,
            [
                "paper/sections/formalization.tex",
                "paper/sections/theory.tex",
                "results/theory_formalization_status_20260529.json",
            ],
            (
                "Formalization now states the orbit-risk object and three information-structure "
                "propositions. This supports the mechanism rationale but does not imply empirical "
                "all-win behavior, human validity, or a formal risk-control guarantee."
            ),
        ),
        _row(
            "Novelty and positioning",
            PARTIAL if novelty else FAIL,
            ["results/novelty_audit_20260529.json", "results/novelty_audit_20260529.md"],
            (
                "Latest novelty audit recommends proceed-with-caution: closest risks are CoRM-RAG, "
                "SURE-RAG, Sufficient Context, CF-RAG, and conformal factuality work. Positioning "
                "must stay narrow around aligned evidence-orbit selective risk and cannot claim "
                "strong novelty until human-audited results and remaining baselines are complete."
            ),
        ),
        _row(
            "Calibrated orbit risk model",
            PASS
            if calibration.get("calibration_quality_supported")
            else PARTIAL
            if calibration
            else FAIL,
            [
                "results/v4_calibration_quality_20260529.json",
                "results/v4_calibration_quality_20260529.md",
            ],
            (
                "Calibration-quality artifact shows Brier wins "
                f"{calibration.get('best_target_brier_win_count')}/{calibration.get('dataset_count')} "
                "against rule/minimax references, but ECE wins "
                f"{calibration.get('best_target_ece_win_count')}/{calibration.get('dataset_count')}. "
                "This supports empirical calibration-quality wording, not a formal risk guarantee."
            ),
        ),
        _row(
            "Failure taxonomy and case studies",
            PASS
            if _g(latest, "failure_taxonomy", "dataset_count") and _g(latest, "case_gallery", "case_count")
            else PARTIAL,
            [
                "results/v4_failure_taxonomy_summary_20260529.json",
                "paper/case_studies/v4_case_gallery_20260529.md",
                "paper/figures/clean_sufficiency_misleading_v4_20260529.svg",
            ],
            "Paper-facing diagnostics are complete but private-label, not human-adjudicated.",
        ),
        _row(
            "Risk-control claim",
            FAIL if _g(risk, "fever_cp", "transfer_sweep", "negative_evidence_for_main_risk_claim") else PARTIAL,
            ["results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json"],
            "Hotpot-only empirical transfer is positive; FEVER 0.20 target is negative, so no general/formal claim.",
        ),
        _row(
            "Claim ledger and evidence package",
            PASS
            if manifest.get("missing_artifact_count") == 0
            and closure.get("claim_verification", {}).get("failed_claims") == 0
            else FAIL,
            [
                "CLAIMS_LEDGER.json",
                "results/claims_verification.json",
                "results/v4_evidence_package_manifest_20260529.json",
            ],
            f"Manifest artifacts: {manifest.get('artifact_count')}; missing: {manifest.get('missing_artifact_count')}.",
        ),
        _row(
            "Independent external review",
            PASS if external_review.get("ready_for_independent_external_review_claim") else BLOCKED,
            [
                "results/external_review_packet_status_20260529.json",
                "results/external_review_packet_20260529.md",
            ],
            _external_review_boundary(external_review),
        ),
    ]


def _row(requirement: str, status: str, evidence: list[str], boundary: str) -> dict[str, Any]:
    return {
        "requirement": requirement,
        "status": status,
        "evidence": evidence,
        "boundary_or_next_action": boundary,
    }


def _full_corm_boundary(storage_probe: dict[str, Any]) -> str:
    matrix = storage_probe.get("write_probe_matrix_summary") or {}
    failed_target_dirs = matrix.get("failed_target_dirs") or []
    writable_fallback_dirs = matrix.get("writable_fallback_dirs") or []
    available = storage_probe.get("target_available_gib")
    available_text = "unknown" if available is None else f"{available:.1f} GiB"
    return (
        "Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original "
        f"artifacts. Latest storage probe shows {available_text} available and "
        f"target_write_probe_passed={storage_probe.get('target_write_probe_passed')}; "
        f"{len(failed_target_dirs)} target-dir file probes failed while writable fallback dirs are "
        f"{writable_fallback_dirs}."
    )


def _external_review_boundary(external_review: dict[str, Any]) -> str:
    if external_review.get("ready_for_independent_external_review_claim"):
        return "Independent external review response is present; inspect the response before upgrading paper claims."
    if external_review.get("packet_ready"):
        return (
            "External review packet is ready, but no independent review response is present; "
            f"place the response at `{external_review.get('review_response_path')}`."
        )
    missing = external_review.get("missing_source_artifacts") or []
    return (
        "External review packet is incomplete; regenerate the evidence package first. "
        f"Missing packet sources: {missing}."
    )


def _status_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        status: sum(1 for row in rows if row["status"] == status)
        for status in [PASS, PARTIAL, FAIL, BLOCKED]
    }


def _g(payload: dict[str, Any], *path: str) -> Any:
    cursor: Any = payload
    for part in path:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(part)
    return cursor


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _load_json(path)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_neurips_readiness(args.root)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
