import csv
import json

from experiments.collect_human_audit_v4_assignment_batches import (
    collect_human_audit_v4_assignment_batches,
)


def test_collect_human_audit_v4_assignment_batches_merges_completed_batches(tmp_path):
    pack_name = "unit_pack"
    audit_dir = tmp_path / "results" / "human_audit_v4"
    batch_dir = tmp_path / "results" / "human_audit_v4_batches"
    output_dir = tmp_path / "results" / "human_audit_v4_collection"
    audit_dir.mkdir(parents=True)
    batch_dir.mkdir(parents=True)
    audit_ids = ["audit-001", "audit-002"]
    source_manifest = audit_dir / f"{pack_name}.manifest.json"
    source_manifest.write_text(
        json.dumps(
            {
                "pack_name": pack_name,
                "audit_items": [
                    {
                        "audit_id": audit_id,
                        "orbit_id": f"orbit-{index}",
                        "dataset": "unit",
                        "expected_label_answerable": index == 1,
                    }
                    for index, audit_id in enumerate(audit_ids, start=1)
                ],
            }
        ),
        encoding="utf-8",
    )
    batches = []
    for auditor in ["auditor1", "auditor2"]:
        path = batch_dir / f"{pack_name}.{auditor}.batch01.labels.csv"
        _write_labels(path, audit_ids, auditor, labels=["stable_answerable", "fragile"])
        batches.append(
            {
                "auditor_id": auditor,
                "batch_index": 1,
                "labels_csv": str(path),
            }
        )
    assignment = batch_dir / f"{pack_name}.assignment_manifest.json"
    assignment.write_text(
        json.dumps(
            {
                "pack_name": pack_name,
                "source_manifest": str(source_manifest),
                "auditors": ["auditor1", "auditor2"],
                "batches": batches,
            }
        ),
        encoding="utf-8",
    )

    summary = collect_human_audit_v4_assignment_batches(assignment, output_dir)

    assert summary["collection_ready"] is True
    assert summary["human_labels_complete"] is True
    assert summary["pending_auditor_labels"] == 0
    assert summary["pending_adjudicated_labels"] == 0
    assert summary["merge_summary"]["rows"] == 4
    assert summary["adjudication_summary"]["auto_agree"] == 2
    assert (output_dir / f"{pack_name}.auditor1.collected.labels.csv").exists()


def test_collect_human_audit_v4_assignment_batches_reports_pending_labels(tmp_path):
    pack_name = "unit_pack"
    audit_dir = tmp_path / "results" / "human_audit_v4"
    batch_dir = tmp_path / "results" / "human_audit_v4_batches"
    output_dir = tmp_path / "results" / "human_audit_v4_collection"
    audit_dir.mkdir(parents=True)
    batch_dir.mkdir(parents=True)
    source_manifest = audit_dir / f"{pack_name}.manifest.json"
    source_manifest.write_text(
        json.dumps(
            {
                "pack_name": pack_name,
                "audit_items": [{"audit_id": "audit-001", "orbit_id": "orbit-1", "dataset": "unit"}],
            }
        ),
        encoding="utf-8",
    )
    path = batch_dir / f"{pack_name}.auditor1.batch01.labels.csv"
    _write_labels(path, ["audit-001"], "auditor1", labels=[""])
    assignment = batch_dir / f"{pack_name}.assignment_manifest.json"
    assignment.write_text(
        json.dumps(
            {
                "pack_name": pack_name,
                "source_manifest": str(source_manifest),
                "auditors": ["auditor1"],
                "batches": [{"auditor_id": "auditor1", "batch_index": 1, "labels_csv": str(path)}],
            }
        ),
        encoding="utf-8",
    )

    summary = collect_human_audit_v4_assignment_batches(assignment, output_dir)

    assert summary["collection_ready"] is True
    assert summary["human_labels_complete"] is False
    assert summary["pending_auditor_labels"] == 1
    assert summary["pending_adjudicated_labels"] == 1


def _write_labels(path, audit_ids, auditor, labels):
    with path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(
            dst,
            fieldnames=[
                "audit_id",
                "dataset",
                "auditor_id",
                "label_semantic",
                "label_answerable",
                "failure_type",
                "confidence",
                "notes",
            ],
        )
        writer.writeheader()
        for audit_id, label in zip(audit_ids, labels):
            writer.writerow(
                {
                    "audit_id": audit_id,
                    "dataset": "unit",
                    "auditor_id": auditor,
                    "label_semantic": label,
                    "label_answerable": "",
                    "failure_type": "",
                    "confidence": "high" if label else "",
                    "notes": "",
                }
            )
