import json

from experiments.summarize_audit import summarize_audit


def test_summarize_audit_counts_pending_and_agreement(tmp_path):
    path = tmp_path / "audit.jsonl"
    rows = [
        {
            "orbit_id": "a",
            "split": "stable",
            "expected_label_answerable": True,
            "auditor_label_answerable": "yes",
        },
        {
            "orbit_id": "b",
            "split": "fragile",
            "expected_label_answerable": False,
            "auditor_label_answerable": True,
            "auditor_failure_type": "label_error",
        },
        {
            "orbit_id": "c",
            "split": "fragile",
            "expected_label_answerable": False,
            "auditor_label_answerable": None,
        },
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    summary = summarize_audit(path)

    assert summary["total"] == 3
    assert summary["labeled"] == 2
    assert summary["pending"] == 1
    assert summary["agreement_with_expected"] == 0.5
    assert summary["failure_types"] == {"label_error": 1}
    assert summary["by_split"]["fragile"]["pending"] == 1
