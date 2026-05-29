import json

from experiments.build_results_provenance_readme import (
    build_results_provenance_readme,
    render_markdown,
)


def test_build_results_provenance_maps_steps_to_hashes(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    output = results / "table.json"
    output.write_text("payload", encoding="utf-8")
    _write_json(
        results / "current_evidence_reproduction_20260529.json",
        {
            "ready_for_neurips_main_claim": False,
            "commands": [
                {
                    "name": "summarize_neurips_readiness",
                    "ready": False,
                    "outputs": [str(output)],
                }
            ],
            "blockers": {
                "human_audit": ["labels pending"],
                "non_human": ["full reproduction pending"],
            },
        },
    )
    _write_json(
        results / "v4_evidence_package_manifest_20260529.json",
        {
            "artifact_count": 1,
            "missing_artifact_count": 0,
            "artifacts": [
                {
                    "path": "results/table.json",
                    "exists": True,
                    "size_bytes": 7,
                    "sha256": "abc123def456",
                }
            ],
        },
    )
    _write_json(
        results / "neurips_readiness_matrix_20260529.json",
        {
            "status_counts": {"blocked": 1},
            "hard_blockers": [
                {
                    "requirement": "Human-audited labels",
                    "status": "blocked",
                    "boundary_or_next_action": "Collect labels",
                }
            ],
        },
    )

    summary = build_results_provenance_readme(
        tmp_path,
        results / "current_evidence_reproduction_20260529.json",
        results / "v4_evidence_package_manifest_20260529.json",
        results / "neurips_readiness_matrix_20260529.json",
    )

    output_row = summary["steps"][0]["outputs"][0]
    assert summary["step_count"] == 1
    assert summary["reproduction_ready_for_neurips_main_claim"] is False
    assert summary["steps"][0]["source_script"] == "experiments/summarize_neurips_readiness.py"
    assert output_row["path"] == "results/table.json"
    assert output_row["sha256"] == "abc123def456"
    assert output_row["manifest_tracked"] is True
    assert summary["known_blockers"]["human_audit"] == ["labels pending"]


def test_render_markdown_keeps_boundary_and_reproduce_commands():
    summary = {
        "generated_at_utc": "now",
        "reproduction_ready_for_neurips_main_claim": False,
        "source_reports": {
            "current_evidence_reproduction": "results/current.json",
            "v4_evidence_package_manifest": "results/manifest.json",
            "neurips_readiness_matrix": "results/readiness.json",
        },
        "steps": [
            {
                "step": "summarize_neurips_readiness",
                "ready": False,
                "source_script": "experiments/summarize_neurips_readiness.py",
                "outputs": [
                    {
                        "path": "results/readiness.json",
                        "exists": True,
                        "manifest_tracked": True,
                        "sha256": "abc123def456",
                    }
                ],
            }
        ],
        "artifact_count": 1,
        "manifest_missing_artifact_count": 0,
        "missing_output_count": 0,
        "untracked_output_count": 0,
        "untracked_or_missing_output_count": 0,
        "readiness_status_counts": {"blocked": 1},
        "known_blockers": {
            "human_audit": ["labels pending"],
            "non_human": ["storage pending"],
            "hard_readiness_blockers": [
                {
                    "requirement": "Human labels",
                    "status": "blocked",
                    "boundary_or_next_action": "Collect labels",
                }
            ],
        },
        "claim_boundary": "does not complete pending human audit labels",
    }

    text = render_markdown(summary)

    assert "Results Provenance" in text
    assert "python -m experiments.reproduce_current_evidence_v4" in text
    assert "`experiments/summarize_neurips_readiness.py`" in text
    assert "does not complete pending human audit labels" in text


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
