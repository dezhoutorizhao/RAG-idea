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
    rows = _rows(closure, manifest, reproduction)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "plan": "RAG-idea改进.md Sections 13.1/13.2 plus current closure blockers",
            "closure": "results/evidence_closure_status_v4.json",
            "manifest": "results/v4_evidence_package_manifest_20260529.json",
            "reproduction": "results/current_evidence_reproduction_20260529.json",
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


def _rows(closure: dict[str, Any], manifest: dict[str, Any], reproduction: dict[str, Any]) -> list[dict[str, Any]]:
    latest = closure.get("latest_v4_diagnostics", {})
    strong = closure.get("v4_strong_baselines") or {}
    end2end = closure.get("end2end_selective_rag_proxy") or {}
    mechanism = closure.get("mechanism_ablation") or {}
    risk = closure.get("risk_control") or {}
    reconstruction = closure.get("corm_reconstruction") or {}
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
                "results/human_audit_v4_status_20260529.json",
                "results/human_audit_v4_disagreement_taxonomy_20260529.json",
                "results/human_audit_v4_mismatch_20260529.json",
                "results/human_audit_v4_eval_status_20260529.json",
            ],
            f"Pending labels: {gate.get('human_audit_v4_pending')}; cannot claim human-audited results.",
        ),
        _row(
            "Strong baselines and equal-budget controls",
            PARTIAL if strong else FAIL,
            [
                "results/v4_strong_baseline_summary_20260529.json",
                "results/v4_baseline_coverage_matrix_20260529.json",
                "results/v4_baseline_budget_parity_20260529.json",
                "results/v4_split_threshold_protocol_20260529.json",
            ],
            (
                "Baseline package exists, but CSRM-Rule has losses/ties against strongest learned/context baselines; "
                "coverage/budget matrices also mark faithful CoRM and self-consistency as partial, "
                "clean-only controls as lower-budget, LLM judge as missing, and shared calibration-threshold "
                "selection across every baseline as not yet run."
            ),
        ),
        _row(
            "End-to-end selective RAG",
            PARTIAL if end2end and end2end.get("row_count") else FAIL,
            ["results/end2end_selective_rag_proxy_summary_20260529.json"],
            "Proxy evidence is directional but mixed and not a full CoRM-RAG retrieval-generation reproduction.",
        ),
        _row(
            "Full CoRM-RAG reproduction",
            BLOCKED if not reconstruction.get("preflight_ready") else PASS,
            [
                "results/corm_reproduction_preflight.json",
                "results/corm_full_wikipedia_job_status.json",
                "results/remote_storage_status_20260529.json",
            ],
            "Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts.",
        ),
        _row(
            "Mechanism ablations",
            PASS if mechanism.get("strong_alignment_evidence") else PARTIAL,
            ["results/mechanism_ablation_summary_20260529.json"],
            "Alignment evidence is strong; no-worst-sufficiency is weak/redundant in current bridge artifacts.",
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
            BLOCKED,
            [],
            "Not rerun after latest evidence package; requires explicit external/subagent review or another approved review path.",
        ),
    ]


def _row(requirement: str, status: str, evidence: list[str], boundary: str) -> dict[str, Any]:
    return {
        "requirement": requirement,
        "status": status,
        "evidence": evidence,
        "boundary_or_next_action": boundary,
    }


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
