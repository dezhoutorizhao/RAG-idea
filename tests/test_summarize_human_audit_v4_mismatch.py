import json

from experiments.summarize_human_audit_v4_mismatch import (
    render_markdown,
    summarize_human_audit_v4_mismatch,
)


def test_summarize_human_audit_v4_mismatch_counts_binary_and_semantic(tmp_path):
    audit_dir = tmp_path / "human_audit_v4"
    audit_dir.mkdir()
    _write_json(
        audit_dir / "pack.manifest.json",
        {
            "pack_name": "pack",
            "selected_items": 3,
            "audit_items": [
                {
                    "audit_id": "a1",
                    "dataset": "unit",
                    "orbit_id": "o1",
                    "construction_type": "stable",
                    "expected_label_answerable": True,
                    "heuristic_label": "stable_answerable",
                },
                {
                    "audit_id": "a2",
                    "dataset": "unit",
                    "orbit_id": "o2",
                    "construction_type": "semantic_swap",
                    "expected_label_answerable": False,
                    "heuristic_label": "fragile",
                },
                {
                    "audit_id": "a3",
                    "dataset": "unit",
                    "orbit_id": "o3",
                    "construction_type": "stable",
                    "expected_label_answerable": True,
                    "heuristic_label": "stable_answerable",
                },
            ],
        },
    )
    _write_jsonl(
        audit_dir / "pack.adjudicated_labels.jsonl",
        [
            {
                "audit_id": "a1",
                "adjudicated_label_answerable": True,
                "adjudicated_label_semantic": "stable_answerable",
                "adjudication_status": "auto_agree",
            },
            {
                "audit_id": "a2",
                "adjudicated_label_answerable": True,
                "adjudicated_label_semantic": "stable_answerable",
                "adjudication_status": "manual",
            },
            {
                "audit_id": "a3",
                "adjudicated_label_answerable": None,
                "adjudicated_label_semantic": "",
                "adjudication_status": "pending",
            },
        ],
    )

    summary = summarize_human_audit_v4_mismatch(audit_dir)

    assert summary["mismatch_artifact_ready"] is True
    assert summary["human_audit_complete"] is False
    assert summary["binary_comparable"] == 2
    assert summary["binary_mismatches"] == 1
    assert summary["binary_mismatch_rate"] == 0.5
    assert summary["semantic_comparable"] == 2
    assert summary["semantic_mismatches"] == 1
    assert summary["semantic_mismatch_rate"] == 0.5
    assert summary["packs"][0]["pending_adjudications"] == 1
    assert summary["packs"][0]["mismatch_examples"][0]["audit_id"] == "a2"

    text = render_markdown(summary)
    assert "Human Audit V4 Heuristic-Human Mismatch" in text
    assert "Binary mismatch rate" in text


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
