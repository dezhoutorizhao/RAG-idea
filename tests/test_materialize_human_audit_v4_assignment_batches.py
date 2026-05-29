import csv
import json

from experiments.materialize_human_audit_v4_assignment_batches import (
    materialize_human_audit_v4_assignment_batches,
)


def test_materialize_human_audit_v4_assignment_batches_splits_public_pack(tmp_path):
    audit_dir = tmp_path / "results" / "human_audit_v4"
    output_dir = tmp_path / "results" / "human_audit_v4_batches"
    audit_dir.mkdir(parents=True)
    pack_name = "unit_pack"
    items = [_public_item(index) for index in range(5)]
    _write_jsonl(audit_dir / f"{pack_name}.items.jsonl", items)
    label_csvs = {}
    for auditor in ["auditor1", "auditor2"]:
        path = audit_dir / f"{pack_name}.{auditor}.labels.csv"
        _write_labels(path, items, auditor)
        label_csvs[auditor] = str(path)
    (audit_dir / f"{pack_name}.manifest.json").write_text(
        json.dumps({"pack_name": pack_name, "label_csvs": label_csvs}, indent=2),
        encoding="utf-8",
    )

    summary = materialize_human_audit_v4_assignment_batches(
        audit_dir,
        output_dir,
        pack_name=pack_name,
        batch_size=2,
    )

    assert summary["assignment_ready"] is True
    assert summary["source_item_count"] == 5
    assert summary["batch_count"] == 6
    assert summary["batches_per_auditor"] == 3
    assert summary["total_assignment_rows"] == 10
    for coverage in summary["coverage_by_auditor"].values():
        assert coverage["covers_all_source_items_once"] is True

    first_batch = output_dir / "unit_pack.auditor1.batch01.items.jsonl"
    assert first_batch.exists()
    assert len(first_batch.read_text(encoding="utf-8").strip().splitlines()) == 2
    labels = list(
        csv.DictReader(
            (output_dir / "unit_pack.auditor1.batch01.labels.csv").open(
                newline="",
                encoding="utf-8-sig",
            )
        )
    )
    assert [row["audit_id"] for row in labels] == ["audit-000", "audit-001"]
    assert labels[0]["label_answerable"] == ""
    assert (output_dir / "unit_pack.assignment_manifest.json").exists()


def test_materialize_human_audit_v4_assignment_batches_rejects_public_labels(tmp_path):
    audit_dir = tmp_path / "results" / "human_audit_v4"
    audit_dir.mkdir(parents=True)
    pack_name = "unit_pack"
    item = _public_item(0)
    item["label_answerable"] = True
    _write_jsonl(audit_dir / f"{pack_name}.items.jsonl", [item])
    label_path = audit_dir / f"{pack_name}.auditor1.labels.csv"
    _write_labels(label_path, [item], "auditor1")
    (audit_dir / f"{pack_name}.manifest.json").write_text(
        json.dumps({"pack_name": pack_name, "label_csvs": {"auditor1": str(label_path)}}),
        encoding="utf-8",
    )

    try:
        materialize_human_audit_v4_assignment_batches(
            audit_dir,
            tmp_path / "batches",
            pack_name=pack_name,
        )
    except ValueError as exc:
        assert "forbidden public audit key" in str(exc)
    else:
        raise AssertionError("expected forbidden public key failure")


def _public_item(index):
    return {
        "audit_id": f"audit-{index:03d}",
        "dataset": "unit",
        "query": f"query {index}",
        "candidate_answer": "answer",
        "clean_evidence": [{"rank": 0, "title": "title", "doc_id": "doc", "text": "text"}],
        "perturbations": [
            {
                "query": f"query {index}",
                "candidate_answer": "answer",
                "evidence": [{"rank": 0, "title": "pert", "doc_id": "doc2", "text": "pert"}],
            }
        ],
    }


def _write_labels(path, items, auditor):
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
        for item in items:
            writer.writerow(
                {
                    "audit_id": item["audit_id"],
                    "dataset": item["dataset"],
                    "auditor_id": auditor,
                    "label_semantic": "",
                    "label_answerable": "",
                    "failure_type": "",
                    "confidence": "",
                    "notes": "",
                }
            )


def _write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
