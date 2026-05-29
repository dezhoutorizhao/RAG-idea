import json

from experiments.summarize_neurips_unblock_plan import (
    render_markdown,
    summarize_neurips_unblock_plan,
)


def test_summarize_neurips_unblock_plan_tracks_external_gates(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    _write_json(results / "neurips_readiness_matrix_20260529.json", {
        "ready_for_neurips_main_track": False,
        "status_counts": {"pass": 5, "partial": 5, "fail": 1, "blocked": 3},
    })
    _write_json(results / "human_audit_v4_batch_collection_20260529.json", {
        "human_labels_complete": False,
        "pending_auditor_labels": 2000,
        "pending_adjudicated_labels": 1000,
    })
    _write_json(results / "human_audit_v4_status_20260529.json", {"ready": False, "pending": 1300})
    _write_json(results / "llm_judge_nli_probe_batch_run_status_20260529.json", {
        "status": "blocked",
        "ready_for_batch_submission": False,
        "followup_commands": [{"command": "submit batch"}],
    })
    _write_json(results / "llm_judge_nli_probe_score_status_20260529.json", {"status": "blocked"})
    _write_json(results / "llm_nli_correlation_status_20260529.json", {
        "ready_for_nli_llm_correlation_claim": False,
    })
    _write_json(results / "remote_storage_status_20260529.json", {
        "target": "/mnt/ntfs-disk",
        "target_available_gib": 322.1,
        "target_write_probe_passed": False,
        "ready_for_full_reproduction_storage": False,
    })
    _write_json(results / "remote_home_storage_status_20260529.json", {
        "target": "/home/syk",
        "target_available_gib": 12.2,
        "target_write_probe_passed": True,
        "target_min_free_met": False,
        "ready_for_full_reproduction_storage": False,
    })
    _write_json(results / "remote_ext4_prepare_dryrun_20260529.json", {
        "mode": "dry_run",
        "destructive_operations_executed": False,
    })
    _write_json(results / "remote_cleanup_candidates_20260529.json", {
        "recommended_reclaim_gib_lower_bound": 184.0,
        "destructive_operations_executed": False,
    })
    _write_json(results / "external_review_packet_status_20260529.json", {
        "packet_ready": True,
        "external_review_completed": False,
        "ready_for_independent_external_review_claim": False,
        "review_response_path": "results/external_review_response_20260529.md",
    })

    summary = summarize_neurips_unblock_plan(tmp_path)

    assert summary["ready_for_neurips_main_track"] is False
    assert summary["open_blocker_count"] == 5
    assert summary["external_action_required_count"] == 4
    assert summary["requires_user_approval_count"] == 1
    blockers = {item["id"]: item for item in summary["blockers"]}
    assert blockers["complete_human_audit_v4"]["status"] == "blocked"
    assert blockers["run_api_backed_llm_judge"]["next_commands"] == ["submit batch"]
    assert blockers["repair_storage_for_full_corm_reproduction"]["requires_user_approval"] is True
    assert "home_write_probe_passed=True" in blockers["repair_storage_for_full_corm_reproduction"]["current_evidence"]
    assert "cleanup_candidate_audit_ready=True" in blockers["repair_storage_for_full_corm_reproduction"]["current_evidence"]
    assert blockers["risk_control_claim_boundary"]["status"] == "fail"

    text = render_markdown(summary)
    assert "NeurIPS Evidence Unblock Plan" in text
    assert "complete_human_audit_v4" in text


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
