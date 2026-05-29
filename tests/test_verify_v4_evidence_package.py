import json

from experiments.verify_v4_evidence_package import (
    DEFAULT_ARTIFACTS,
    render_markdown,
    verify_v4_evidence_package,
)


def test_verify_v4_evidence_package_hashes_artifacts_and_keeps_blockers(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    artifact = results / "artifact.txt"
    artifact.write_text("payload", encoding="utf-8")
    _write_json(
        results / "current_evidence_reproduction_20260529.json",
        {
            "ready_for_neurips_main_claim": False,
            "gate_summary": {"human_audit_v4_ready": False},
        },
    )
    _write_json(
        results / "evidence_closure_status_v4.json",
        {
            "claim_verification": {"passed_claims": 1, "total_claims": 1, "failed_claims": 0},
            "remaining_human_audit_blockers": ["labels pending"],
            "remaining_non_human_blockers": ["full reproduction pending"],
            "allowed_claims": ["diagnostic"],
            "disallowed_claims": ["human audited"],
        },
    )

    manifest = verify_v4_evidence_package(
        tmp_path,
        [artifact.relative_to(tmp_path), tmp_path.joinpath("missing.txt").relative_to(tmp_path)],
    )

    assert manifest["artifact_count"] == 2
    assert manifest["missing_artifact_count"] == 1
    assert manifest["artifacts"][0]["sha256"]
    assert manifest["ready_for_neurips_main_claim"] is False
    assert manifest["package_status"] == "incomplete_missing_artifacts"


def test_render_markdown_lists_artifacts_and_claim_boundary():
    manifest = {
        "generated_at_utc": "now",
        "package_status": "complete_with_known_blockers",
        "ready_for_neurips_main_claim": False,
        "missing_artifact_count": 0,
        "gate_summary": {"remote_storage_ready": False},
        "claim_verification": {"passed_claims": 2, "total_claims": 2, "failed_claims": 0},
        "allowed_claim_count": 1,
        "disallowed_claim_count": 1,
        "artifacts": [
            {"path": "a.json", "exists": True, "size_bytes": 7, "sha256": "abc"}
        ],
        "remaining_human_audit_blockers": ["labels pending"],
        "remaining_non_human_blockers": ["storage pending"],
        "claim_boundary": "does not convert pending human audit",
    }

    text = render_markdown(manifest)

    assert "V4 Evidence Package Manifest" in text
    assert "`a.json`" in text
    assert "does not convert pending human audit" in text


def test_default_manifest_tracks_human_audit_protocol_docs():
    defaults = {str(path).replace("\\", "/") for path in DEFAULT_ARTIFACTS}

    assert "annotation/README.md" in defaults
    assert "annotation/audit_card_template.md" in defaults
    assert "annotation/guidelines_v4.md" in defaults
    assert "annotation/label_schema_v4.json" in defaults


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
