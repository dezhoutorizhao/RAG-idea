import json

from experiments.build_reproducibility_bundle import (
    build_reproducibility_bundle,
    _hidden_path_audit,
    _seeds,
)


def test_build_reproducibility_bundle_writes_core_outputs(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    artifact = results / "artifact.json"
    artifact.write_text('{"ok": true}', encoding="utf-8")
    seed_file = results / "hotpot_corm_calibration_multiseed.json"
    _write_json(seed_file, {"seeds": [17, 31]})
    _write_json(
        results / "v4_evidence_package_manifest_20260529.json",
        {
            "artifact_count": 1,
            "missing_artifact_count": 0,
            "artifacts": [
                {
                    "path": "results/artifact.json",
                    "exists": True,
                    "size_bytes": artifact.stat().st_size,
                    "sha256": "abc",
                }
            ],
        },
    )
    _write_json(
        results / "evidence_closure_status_v4.json",
        {
            "current_evidence_reproduction": {"ready_for_neurips_main_claim": False},
            "corm_reconstruction": {"latest_storage_probe": {"ready_for_full_reproduction_storage": False}},
        },
    )
    _write_json(
        results / "corm_remote_checkpoint_status.json",
        {
            "local": {"path": "checkpoint.pt", "size_bytes": 7, "sha256": "ckpt"},
            "remote_sha256": "ckpt",
            "sha256_match": True,
        },
    )
    _write_json(
        results / "claims_ledger_markdown_summary_20260529.json",
        {"total_claims": 1, "failed_claims": 0},
    )

    summary = build_reproducibility_bundle(tmp_path)

    assert summary["artifact_checksum_count"] == 1
    assert summary["checkpoint_hash_available"] is True
    assert summary["claims_ledger_markdown_ready"] is True
    assert summary["claims_ledger_total_claims"] == 1
    assert summary["hidden_local_path_passed"] is True
    assert (tmp_path / "reproducibility/checksums.json").exists()
    assert (tmp_path / "reproducibility/seeds.json").exists()
    assert (tmp_path / "reproducibility/hardware.md").exists()
    assert (tmp_path / "reproducibility/artifact_manifest.md").exists()


def test_hidden_path_audit_flags_windows_absolute_paths(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    artifact = results / "artifact.md"
    artifact.write_text("hidden path C:\\Users\\example\\secret", encoding="utf-8")
    manifest = {
        "artifacts": [
            {
                "path": "results/artifact.md",
                "exists": True,
                "size_bytes": artifact.stat().st_size,
            }
        ]
    }

    audit = _hidden_path_audit(tmp_path, manifest)

    assert audit["passed"] is False
    assert audit["finding_count"] == 1


def test_hidden_path_audit_ignores_json_escaped_quotes_after_colon(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    artifact = results / "artifact.jsonl"
    artifact.write_text('{"text": "Stephen Elien:\\""}', encoding="utf-8")
    manifest = {
        "artifacts": [
            {
                "path": "results/artifact.jsonl",
                "exists": True,
                "size_bytes": artifact.stat().st_size,
            }
        ]
    }

    audit = _hidden_path_audit(tmp_path, manifest)

    assert audit["passed"] is True
    assert audit["finding_count"] == 0


def test_hidden_path_audit_ignores_json_key_suffix_before_colon(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    artifact = results / "remote_probe.json"
    artifact.write_text('{"command": "r={\\"directory\\": str(d)}"}', encoding="utf-8")
    manifest = {
        "artifacts": [
            {
                "path": "results/remote_probe.json",
                "exists": True,
                "size_bytes": artifact.stat().st_size,
            }
        ]
    }

    audit = _hidden_path_audit(tmp_path, manifest)

    assert audit["passed"] is True
    assert audit["finding_count"] == 0


def test_seeds_extracts_explicit_seed_lists(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    _write_json(results / "hotpot_corm_calibration_multiseed.json", {"seeds": [17, 31, 47]})

    seeds = _seeds(tmp_path)

    assert seeds["unique_seeds"] == [17, 31, 47]
    assert len(seeds["sources"]) == 1


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
