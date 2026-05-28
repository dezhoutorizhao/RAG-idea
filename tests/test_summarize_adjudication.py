import json

from experiments.summarize_adjudication import summarize_adjudication


def _row(orbit_id, split, label1, label2, adjudicated=None):
    return {
        "orbit_id": orbit_id,
        "split": split,
        "auditor_label_answerable": label1,
        "auditor2_label_answerable": label2,
        "adjudicated_label_answerable": adjudicated,
    }


def test_summarize_adjudication_reports_agreement_and_kappa(tmp_path):
    path = tmp_path / "audit.jsonl"
    rows = [
        _row("a", "s1", True, True, True),
        _row("b", "s1", False, False, False),
        _row("c", "s2", True, False, False),
        _row("d", "s2", False, True, True),
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    summary = summarize_adjudication(path)

    assert summary["total"]["double_labeled"] == 4
    assert summary["total"]["agree"] == 2
    assert summary["total"]["disagree"] == 2
    assert summary["total"]["raw_agreement"] == 0.5
    assert summary["total"]["cohen_kappa"] == 0.0
    assert summary["ready_for_adjudicated_claims"] is True


def test_summarize_adjudication_tracks_unresolved_and_invalid(tmp_path):
    path = tmp_path / "audit.jsonl"
    rows = [
        _row("a", "s1", True, False, None),
        _row("b", "s1", "maybe", True, True),
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    summary = summarize_adjudication(path)

    assert summary["ready_for_adjudicated_claims"] is False
    assert len(summary["unresolved_disagreements"]) == 1
    assert len(summary["invalid_labels"]) == 1
