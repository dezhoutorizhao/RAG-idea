import csv
import json

from experiments.summarize_human_audit_v4_disagreements import (
    render_markdown,
    summarize_human_audit_v4_disagreements,
)


def test_summarize_human_audit_v4_disagreements_counts_conflicts_and_pending(tmp_path):
    audit_dir = tmp_path / "human_audit_v4"
    audit_dir.mkdir()
    _write_json(
        audit_dir / "pack.manifest.json",
        {"pack_name": "pack", "selected_items": 2, "audit_items": [{}, {}]},
    )
    _write_json(
        audit_dir / "pack.agreement.json",
        {
            "conflicts": [{"audit_id": "a1", "ann1": True, "ann2": False}],
            "semantic_conflicts": [
                {"audit_id": "a1", "ann1": "stable_answerable", "ann2": "fragile"}
            ],
        },
    )
    _write_jsonl(
        audit_dir / "pack.adjudicated_labels.jsonl",
        [
            {"audit_id": "a1", "adjudication_status": "pending"},
            {"audit_id": "a2", "adjudication_status": "auto_agree"},
        ],
    )
    _write_jsonl(
        audit_dir / "pack.merged_labels.jsonl",
        [
            {
                "audit_id": "a1",
                "auditor_id": "ann1",
                "label_semantic": "fragile",
                "failure_type": "missing_evidence",
            },
            {
                "audit_id": "a1",
                "auditor_id": "ann2",
                "label_semantic": "fragile",
                "failure_type": "conflicting_evidence",
            },
            {
                "audit_id": "a2",
                "auditor_id": "ann1",
                "label_semantic": "stable_answerable",
                "failure_type": "",
            },
        ],
    )
    _write_csv(audit_dir / "pack.adjudication_template.csv", [{"audit_id": "a1"}])

    summary = summarize_human_audit_v4_disagreements(audit_dir)

    assert summary["taxonomy_artifact_ready"] is True
    assert summary["human_audit_complete"] is False
    assert summary["aggregate"]["binary_conflict_count"] == 1
    assert summary["aggregate"]["semantic_conflict_count"] == 1
    assert summary["aggregate"]["failure_type_disagreement_count"] == 1
    assert summary["aggregate"]["pending_adjudication_count"] == 1
    assert summary["packs"][0]["binary_conflict_taxonomy"][0]["label_pair"] == "True vs False"
    assert (
        summary["packs"][0]["failure_type_disagreement_taxonomy"][0]["failure_type_pair"]
        == "conflicting_evidence vs missing_evidence"
    )

    text = render_markdown(summary)
    assert "Human Audit V4 Disagreement Taxonomy" in text
    assert "Pending adjudications" in text


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")


def _write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
