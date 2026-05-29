import json

from experiments.summarize_neurips_readiness import (
    BLOCKED,
    FAIL,
    PARTIAL,
    PASS,
    render_markdown,
    summarize_neurips_readiness,
)


def test_summarize_neurips_readiness_maps_current_gates(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    _write_json(results / "evidence_closure_status_v4.json", _closure())
    _write_json(
        results / "v4_evidence_package_manifest_20260529.json",
        {"artifact_count": 26, "missing_artifact_count": 0},
    )
    _write_json(
        results / "current_evidence_reproduction_20260529.json",
        {
            "gate_summary": {
                "human_audit_v4_ready": False,
                "human_audit_v4_pending": 300,
            }
        },
    )
    _write_json(
        results / "text_only_verifier_status_20260529.json",
        {
            "ready_for_text_only_main_claim": False,
            "nli_probe": {"directional_advantage_ready": True},
        },
    )
    _write_json(results / "external_review_packet_status_20260529.json", _external_review())

    summary = summarize_neurips_readiness(tmp_path)

    by_req = {row["requirement"]: row for row in summary["rows"]}
    assert by_req["Leakage-free v4 pipeline"]["status"] == PASS
    assert by_req["Human-audited orbit labels"]["status"] == BLOCKED
    assert by_req["Text-only semantic verifier"]["status"] == PARTIAL
    assert by_req["Strong baselines and equal-budget controls"]["status"] == PARTIAL
    assert "results/end2end_risk_coverage_curves_20260529.json" in by_req["End-to-end selective RAG"]["evidence"]
    assert "6 target-dir file probes failed" in by_req["Full CoRM-RAG reproduction"]["boundary_or_next_action"]
    assert by_req["Independent external review"]["status"] == BLOCKED
    assert "external_review_packet_20260529.md" in by_req["Independent external review"]["evidence"][1]
    assert "no independent review response" in by_req["Independent external review"]["boundary_or_next_action"]
    assert by_req["Risk-control claim"]["status"] == FAIL
    assert summary["ready_for_neurips_main_track"] is False


def test_render_markdown_lists_status_policy(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    _write_json(results / "evidence_closure_status_v4.json", _closure())
    _write_json(
        results / "v4_evidence_package_manifest_20260529.json",
        {"artifact_count": 26, "missing_artifact_count": 0},
    )
    _write_json(
        results / "current_evidence_reproduction_20260529.json",
        {"gate_summary": {"human_audit_v4_ready": False, "human_audit_v4_pending": 300}},
    )
    _write_json(
        results / "text_only_verifier_status_20260529.json",
        {
            "ready_for_text_only_main_claim": False,
            "nli_probe": {"directional_advantage_ready": True},
        },
    )
    _write_json(results / "external_review_packet_status_20260529.json", _external_review())

    text = render_markdown(summarize_neurips_readiness(tmp_path))

    assert "NeurIPS Readiness Matrix" in text
    assert "Ready for NeurIPS main-track claim: `False`" in text
    assert "A pass means" in text


def _closure():
    return {
        "latest_v4_diagnostics": {
            "anti_shortcut": {"pass_core_anti_shortcut_suite": True},
            "failure_taxonomy": {"dataset_count": 6},
            "case_gallery": {"case_count": 192},
        },
        "v4_strong_baselines": {"baseline_file_count": 6},
        "end2end_selective_rag_proxy": {"row_count": 12},
        "mechanism_ablation": {"strong_alignment_evidence": True},
        "risk_control": {
            "fever_cp": {
                "transfer_sweep": {"negative_evidence_for_main_risk_claim": True}
            }
        },
        "corm_reconstruction": {
            "preflight_ready": False,
            "latest_storage_probe": {
                "target_available_gib": 322.14,
                "target_write_probe_passed": False,
                "write_probe_matrix_summary": {
                    "failed_target_dirs": [{}, {}, {}, {}, {}, {}],
                    "writable_fallback_dirs": ["/home/syk", "/tmp", "/dev/shm"],
                },
            },
        },
        "claim_verification": {"failed_claims": 0},
    }


def _external_review():
    return {
        "packet_ready": True,
        "ready_for_independent_external_review_claim": False,
        "review_response_path": "results/external_review_response_20260529.md",
        "missing_source_artifacts": [],
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
