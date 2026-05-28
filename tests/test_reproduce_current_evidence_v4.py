from experiments.reproduce_current_evidence_v4 import render_markdown


def test_render_markdown_reports_blockers():
    report = {
        "generated_at_utc": "2026-05-29T00:00:00+00:00",
        "ready_for_neurips_main_claim": False,
        "commands": [{"name": "step", "ready": False, "outputs": ["a.json"]}],
        "gate_summary": {
            "human_audit_v4_ready": False,
            "human_audit_v4_eval_ready": False,
            "human_audit_v4_pending": 300,
            "human_audit_v4_evaluated_pack_count": 0,
            "full_corm_reconstruction_ready": False,
            "remote_storage_ready": False,
            "claim_verifier_passed": True,
        },
        "blockers": {"human_audit": ["labels pending"], "non_human": ["storage pending"]},
        "claim_policy": "No main claim.",
    }

    text = render_markdown(report)

    assert "labels pending" in text
    assert "storage pending" in text
    assert "No main claim." in text
