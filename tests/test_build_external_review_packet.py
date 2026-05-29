import json

from experiments.build_external_review_packet import (
    SOURCE_ARTIFACTS,
    build_external_review_packet,
    render_markdown,
)


def test_build_external_review_packet_marks_packet_ready_and_review_pending(tmp_path):
    _write_minimal_sources(tmp_path)

    summary = build_external_review_packet(tmp_path)

    assert summary["packet_ready"] is True
    assert summary["external_review_completed"] is False
    assert summary["status"] == "packet_ready"
    assert summary["blocker_reason"] == "pending_external_review"
    assert summary["ready_for_independent_external_review_claim"] is False
    assert len(summary["review_questions"]) >= 6
    assert not summary["missing_source_artifacts"]
    text = render_markdown(summary)
    assert "External Review Packet" in text
    assert "pending_external_review" in text
    assert "Reviewer Output Contract" in text


def test_build_external_review_packet_detects_review_response(tmp_path):
    _write_minimal_sources(tmp_path)
    response = tmp_path / "results" / "external_review_response_20260529.md"
    response.write_text("Independent review: still blocked.", encoding="utf-8")

    summary = build_external_review_packet(tmp_path)

    assert summary["external_review_completed"] is True
    assert summary["status"] == "review_completed"
    assert summary["ready_for_independent_external_review_claim"] is True


def test_source_artifacts_include_remote_storage_unblock_evidence():
    defaults = {str(path).replace("\\", "/") for path in SOURCE_ARTIFACTS}

    assert "results/remote_storage_status_20260529.json" in defaults
    assert "results/remote_home_storage_status_20260529.json" in defaults
    assert "results/remote_ext4_prepare_dryrun_20260529.json" in defaults
    assert "results/remote_ext4_prepare_dryrun_20260529.md" in defaults
    assert "results/remote_storage_cleanup_plan_20260529.md" in defaults
    assert "results/remote_cleanup_candidates_20260529.json" in defaults
    assert "results/remote_cleanup_candidates_20260529.md" in defaults
    assert "results/remote_ext4_cleanup_guarded_plan_20260529.json" in defaults
    assert "results/remote_ext4_cleanup_guarded_plan_20260529.md" in defaults


def _write_minimal_sources(root):
    for rel in SOURCE_ARTIFACTS:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if rel.suffix == ".json":
            path.write_text(json.dumps(_payload_for(rel)), encoding="utf-8")
        else:
            path.write_text(f"# {rel.name}\n", encoding="utf-8")


def _payload_for(path):
    name = str(path).replace("\\", "/")
    if name == "CLAIMS_LEDGER.json":
        return {"claims": [{"id": "C1"}]}
    if name.endswith("claims_verification.json"):
        return {"passed_claims": 1, "failed_claims": 0, "total_claims": 1}
    if name.endswith("evidence_closure_status_v4.json"):
        return {"claim_verification": {"passed_claims": 1, "failed_claims": 0, "total_claims": 1}}
    if name.endswith("neurips_readiness_matrix_20260529.json"):
        return {
            "status_counts": {"pass": 4, "partial": 3, "fail": 1, "blocked": 3},
            "hard_blockers": [
                {
                    "requirement": "Independent external review",
                    "status": "blocked",
                    "boundary_or_next_action": "pending",
                }
            ],
            "negative_or_partial_evidence": [],
        }
    if name.endswith("v4_evidence_package_manifest_20260529.json"):
        return {"artifact_count": 12, "missing_artifact_count": 0}
    return {"ok": True}
