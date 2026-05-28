import json

from experiments.check_audit_readiness import check_audit_readiness


def _row(orbit_id, split, expected, auditor, failure_type=None, notes=None):
    return {
        "orbit_id": orbit_id,
        "split": split,
        "expected_label_answerable": expected,
        "auditor_label_answerable": auditor,
        "auditor_failure_type": failure_type,
        "auditor_notes": notes,
    }


def test_check_audit_readiness_passes_when_gates_are_met(tmp_path):
    path = tmp_path / "audit.jsonl"
    rows = [
        _row("a", "s1", True, True),
        _row("b", "s1", False, False),
        _row("c", "s2", True, True),
        _row("d", "s2", False, True, "label_error", "expected label seems wrong"),
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    report = check_audit_readiness(path, min_labeled_total=4, min_labeled_per_split=2)

    assert report["ready"] is True
    assert report["failed_gates"] == []
    assert report["agreement_with_expected"] == 0.75


def test_check_audit_readiness_reports_failed_gates(tmp_path):
    path = tmp_path / "audit.jsonl"
    rows = [
        _row("a", "s1", True, "maybe"),
        _row("b", "s1", False, None),
        _row("c", "s2", True, False),
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    report = check_audit_readiness(path, min_labeled_total=3, min_labeled_per_split=2)

    gates = {item["gate"] for item in report["failed_gates"]}
    assert report["ready"] is False
    assert "min_labeled_total" in gates
    assert "min_labeled_per_split" in gates
    assert "valid_auditor_labels" in gates
    assert "disagreement_notes" in gates


def test_check_audit_readiness_can_use_adjudicated_label_field(tmp_path):
    path = tmp_path / "audit.jsonl"
    rows = [
        _row("a", "s1", True, None),
        _row("b", "s1", False, None),
    ]
    rows[0]["adjudicated_label_answerable"] = True
    rows[1]["adjudicated_label_answerable"] = False
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    report = check_audit_readiness(
        path,
        min_labeled_total=2,
        min_labeled_per_split=2,
        label_field="adjudicated_label_answerable",
    )

    assert report["ready"] is True
    assert report["label_field"] == "adjudicated_label_answerable"
