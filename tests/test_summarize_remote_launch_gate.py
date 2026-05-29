import json

from experiments.summarize_remote_launch_gate import (
    render_markdown,
    summarize_remote_launch_gate,
)


def test_summarize_remote_launch_gate_blocks_without_cleanup(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    _write_json(results / "remote_home_storage_status_latest.json", {
        "target": "/home/syk",
        "target_available_gib": 12.2,
        "target_min_free_met": False,
        "target_write_probe_passed": True,
        "ready_for_full_reproduction_storage": False,
        "gpu_query": {
            "exit_status": 0,
            "stdout": "0, NVIDIA GeForce RTX 4090, 24564, 24076\n",
        },
    })
    _write_json(results / "remote_ntfs_storage_status_latest.json", {
        "target": "/mnt/ntfs-disk",
        "target_available_gib": 322.1,
        "target_min_free_met": True,
        "target_write_probe_passed": False,
        "ready_for_full_reproduction_storage": False,
    })
    _write_json(results / "corm_remote_scripts_ext4_manifest.json", {
        "status": "materialized",
        "remote_root": "/home/syk/csrm_corm_reconstruction",
        "script_count": 9,
        "contains_secret_markers": False,
        "claim_policy": "launch plan only",
    })
    _write_json(results / "remote_ext4_cleanup_guarded_plan_20260529.json", {
        "destructive_operations_executed": False,
        "confirm_token_required": "APPROVE_EXT4_LOG_CACHE_CLEANUP_FOR_FULL_CORM_RAG_REPRO",
        "preflight": {"passed": True},
    })
    _write_json(results / "remote_cleanup_candidates_20260529.json", {
        "recommended_reclaim_gib_lower_bound": 182.8,
    })

    summary = summarize_remote_launch_gate(tmp_path)

    assert summary["ready_to_launch_full_corm_reproduction"] is False
    assert summary["home_ext4_gate"]["write_probe_passed"] is True
    assert summary["home_ext4_gate"]["min_free_met"] is False
    assert summary["ntfs_gate"]["write_probe_passed"] is False
    assert summary["corm_script_gate"]["manifest_ready"] is True
    assert summary["cleanup_gate"]["destructive_operations_executed"] is False
    assert "guarded_ext4_cleanup_not_executed" in summary["must_not_launch_reasons"]
    assert summary["gpu_summary"]["gpus"][0]["memory_free_mib"] == 24076

    text = render_markdown(summary)
    assert "Remote Full CoRM-RAG Launch Gate" in text
    assert "Ready to launch Full CoRM-RAG: `False`" in text
    assert "/home/syk/csrm_corm_reconstruction" in text


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
