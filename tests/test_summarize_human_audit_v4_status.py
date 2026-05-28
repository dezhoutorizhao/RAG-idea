import csv
import json

from experiments.summarize_human_audit_v4_status import summarize_human_audit_v4_status


def test_human_audit_v4_status_reports_pending_pack(tmp_path):
    audit_dir = tmp_path / "human_audit_v4"
    audit_dir.mkdir()
    manifest = audit_dir / "pack.manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "pack_name": "pack",
                "selected_items": 2,
                "audit_items": [
                    {"audit_id": "a1", "expected_label_answerable": True},
                    {"audit_id": "a2", "expected_label_answerable": False},
                ],
                "label_csvs": {
                    "auditor1": str(audit_dir / "pack.auditor1.labels.csv"),
                    "auditor2": str(audit_dir / "pack.auditor2.labels.csv"),
                },
            }
        ),
        encoding="utf-8",
    )
    _write_csv(
        audit_dir / "pack.auditor1.labels.csv",
        [
            {"audit_id": "a1", "dataset": "unit", "auditor_id": "auditor1", "label_answerable": "answerable"},
            {"audit_id": "a2", "dataset": "unit", "auditor_id": "auditor1", "label_answerable": ""},
        ],
    )
    _write_csv(
        audit_dir / "pack.auditor2.labels.csv",
        [
            {"audit_id": "a1", "dataset": "unit", "auditor_id": "auditor2", "label_answerable": ""},
            {"audit_id": "a2", "dataset": "unit", "auditor_id": "auditor2", "label_answerable": ""},
        ],
    )
    (audit_dir / "pack.adjudicated_labels.jsonl").write_text(
        "\n".join(
            [
                json.dumps({"audit_id": "a1", "adjudicated_label_answerable": True, "adjudication_status": "auto_agree"}),
                json.dumps({"audit_id": "a2", "adjudicated_label_answerable": None, "adjudication_status": "pending"}),
            ]
        ),
        encoding="utf-8",
    )

    status = summarize_human_audit_v4_status(audit_dir)

    assert status["ready"] is False
    assert status["total_items"] == 2
    assert status["adjudicated_labeled"] == 1
    assert status["pending"] == 1
    assert status["packs"][0]["auditors"]["pack.auditor1.labels"]["labeled"] == 1
    assert status["packs"][0]["failed_gates"][0]["gate"] == "all_items_adjudicated"


def _write_csv(path, rows):
    fieldnames = ["audit_id", "dataset", "auditor_id", "label_answerable", "failure_type", "confidence", "notes"]
    with path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})
