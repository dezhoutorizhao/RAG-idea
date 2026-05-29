#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT_JSON = Path("results/external_review_packet_status_20260529.json")
DEFAULT_OUTPUT_MD = Path("results/external_review_packet_20260529.md")
DEFAULT_REVIEW_RESPONSE = Path("results/external_review_response_20260529.md")

SOURCE_ARTIFACTS = [
    Path("RAG-idea改进.md"),
    Path("CLAIMS_LEDGER.json"),
    Path("results/claims_verification.json"),
    Path("results/evidence_closure_status_v4.json"),
    Path("results/neurips_readiness_matrix_20260529.json"),
    Path("results/v4_evidence_package_manifest_20260529.json"),
    Path("results/text_only_verifier_status_20260529.json"),
    Path("results/v4_strong_baseline_summary_20260529.json"),
    Path("results/v4_calibration_quality_20260529.json"),
    Path("results/v4_claim_safe_target_selection_20260529.json"),
    Path("results/risk_control_abstention_baselines_20260529.json"),
    Path("results/theory_formalization_status_20260529.json"),
    Path("results/novelty_audit_20260529.json"),
    Path("paper/sections/formalization.tex"),
    Path("paper/sections/theory.tex"),
    Path("results/end2end_retriever_generator_matrix_20260529.json"),
    Path("results/end2end_risk_coverage_curves_20260529.json"),
    Path("results/end2end_target_risk_coverage_20260529.json"),
    Path("results/remote_storage_status_20260529.json"),
    Path("results/remote_home_storage_status_20260529.json"),
    Path("results/remote_ext4_prepare_dryrun_20260529.json"),
    Path("results/remote_ext4_prepare_dryrun_20260529.md"),
    Path("results/remote_storage_cleanup_plan_20260529.md"),
    Path("results/remote_cleanup_candidates_20260529.json"),
    Path("results/remote_cleanup_candidates_20260529.md"),
    Path("results/remote_ext4_cleanup_guarded_plan_20260529.json"),
    Path("results/remote_ext4_cleanup_guarded_plan_20260529.md"),
    Path("results/corm_reconstruction_plan_ext4_20260529.json"),
    Path("results/corm_remote_scripts_ext4_manifest.json"),
    Path("results/human_audit_v4_paper_pack_status_20260529.json"),
    Path("results/human_audit_v4_assignment_batches_20260529.json"),
    Path("results/human_audit_v4_batch_collection_20260529.json"),
    Path("results/human_audit_v4_status_20260529.json"),
]


def build_external_review_packet(
    root: Path,
    *,
    output_md: Path = DEFAULT_OUTPUT_MD,
    review_response: Path = DEFAULT_REVIEW_RESPONSE,
) -> dict[str, Any]:
    claims = _load_optional_json(root / "CLAIMS_LEDGER.json")
    closure = _load_optional_json(root / "results/evidence_closure_status_v4.json")
    readiness = _load_optional_json(root / "results/neurips_readiness_matrix_20260529.json")
    manifest = _load_optional_json(root / "results/v4_evidence_package_manifest_20260529.json")
    sources = [_artifact_status(root, path) for path in SOURCE_ARTIFACTS]
    missing_sources = [item["path"] for item in sources if not item["exists"]]
    response_abs = root / review_response
    response_ready = response_abs.exists() and response_abs.stat().st_size > 0
    packet_ready = not missing_sources and bool(readiness) and bool(closure)
    status = "review_completed" if response_ready else "packet_ready" if packet_ready else "packet_incomplete"
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "packet_path": str(output_md),
        "review_response_path": str(review_response),
        "packet_ready": packet_ready,
        "external_review_completed": response_ready,
        "ready_for_independent_external_review_claim": response_ready,
        "status": status,
        "blocker_reason": None if response_ready else "pending_external_review",
        "source_artifacts": sources,
        "missing_source_artifacts": missing_sources,
        "allowed_claim_count": len(claims.get("claims", [])),
        "verified_claims": _claim_verification(closure),
        "readiness_status_counts": readiness.get("status_counts", {}),
        "hard_blockers": readiness.get("hard_blockers", []),
        "negative_or_partial_evidence": readiness.get("negative_or_partial_evidence", []),
        "manifest_artifact_count": manifest.get("artifact_count"),
        "manifest_missing_artifact_count": manifest.get("missing_artifact_count"),
        "review_questions": _review_questions(),
        "claim_policy": (
            "This packet prepares the current evidence package for independent external review. "
            "It is not itself an external review and does not upgrade any claim until an "
            "independent review response is present."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# External Review Packet",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Packet ready: `{summary['packet_ready']}`",
        f"External review completed: `{summary['external_review_completed']}`",
        f"Status: `{summary['status']}`",
        f"Blocker: `{summary['blocker_reason']}`",
        "",
        "## Required Review Questions",
        "",
    ]
    for idx, question in enumerate(summary["review_questions"], start=1):
        lines.append(f"{idx}. {question}")

    lines.extend(
        [
            "",
            "## Current Claim Boundary",
            "",
            f"- Verified claims: `{summary['verified_claims']}`.",
            f"- Readiness status counts: `{summary['readiness_status_counts']}`.",
            f"- Evidence manifest artifacts: `{summary['manifest_artifact_count']}`.",
            f"- Evidence manifest missing artifacts: `{summary['manifest_missing_artifact_count']}`.",
            "",
            "## Hard Blockers",
            "",
            "| Requirement | Status | Boundary / next action |",
            "|---|---|---|",
        ]
    )
    for row in summary["hard_blockers"]:
        lines.append(
            f"| {row.get('requirement')} | `{row.get('status')}` | {row.get('boundary_or_next_action')} |"
        )

    lines.extend(
        [
            "",
            "## Negative Or Partial Evidence",
            "",
            "| Requirement | Status | Boundary / next action |",
            "|---|---|---|",
        ]
    )
    for row in summary["negative_or_partial_evidence"]:
        lines.append(
            f"| {row.get('requirement')} | `{row.get('status')}` | {row.get('boundary_or_next_action')} |"
        )

    lines.extend(
        [
            "",
            "## Source Artifacts",
            "",
            "| Artifact | Exists | Size | SHA256 |",
            "|---|---|---:|---|",
        ]
    )
    for item in summary["source_artifacts"]:
        sha = item.get("sha256") or ""
        lines.append(f"| `{item['path']}` | `{item['exists']}` | {item.get('size_bytes')} | `{sha}` |")

    lines.extend(
        [
            "",
            "## Reviewer Output Contract",
            "",
            (
                "Place the independent review response at "
                f"`{summary['review_response_path']}`. The response should state whether the "
                "current claim ledger is acceptable, list any unsupported claims, identify missing "
                "experiments, and give a final accept/reject recommendation for NeurIPS main-track "
                "readiness under the current evidence boundaries."
            ),
            "",
            "## Claim Policy",
            "",
            summary["claim_policy"],
            "",
        ]
    )
    return "\n".join(lines)


def _artifact_status(root: Path, path: Path) -> dict[str, Any]:
    abs_path = root / path
    exists = abs_path.exists()
    return {
        "path": str(path),
        "exists": exists,
        "size_bytes": abs_path.stat().st_size if exists else None,
        "sha256": _sha256(abs_path) if exists and abs_path.is_file() else None,
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _claim_verification(closure: dict[str, Any]) -> dict[str, Any]:
    verification = closure.get("claim_verification", {})
    return {
        "passed_claims": verification.get("passed_claims"),
        "failed_claims": verification.get("failed_claims"),
        "total_claims": verification.get("total_claims"),
    }


def _review_questions() -> list[str]:
    return [
        "Are every allowed claim and every disallowed claim in CLAIMS_LEDGER.json consistent with the current evidence package?",
        "Does the negative evidence on FEVER risk transfer and strong baselines require weakening the main method claim further?",
        "Are the text-only verifier and LLM judge artifacts sufficient as prepared execution paths, or is API-backed scoring required before paper writing?",
        "Does the pending 300-item human audit block all human-audited validity language?",
        "Does the remote storage evidence justify keeping full CoRM-RAG reproduction as unsupported until the NTFS/fuseblk write failure is repaired?",
        "What exact additional experiments or labels are mandatory before a NeurIPS main-track submission claim can be made?",
    ]


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--review-response", type=Path, default=DEFAULT_REVIEW_RESPONSE)
    args = parser.parse_args()

    summary = build_external_review_packet(
        args.root,
        output_md=args.output_md,
        review_response=args.review_response,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["packet_ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
