import json

import pytest

from experiments.evaluate_audited_orbits import evaluate_audited_orbits


def _audit_row(orbit_id, expected, auditor, support_key="gold", split="unit"):
    return {
        "orbit_id": orbit_id,
        "split": split,
        "expected_label_answerable": expected,
        "auditor_label_answerable": auditor,
        "answer": "a",
        "clean": {
            "query": "q",
            "label_answerable": expected,
            "support_key": "gold",
            "perturbation_type": "clean",
            "docs": [
                {
                    "doc_id": "clean",
                    "text": "clean evidence",
                    "corm_score": 0.9,
                    "support": 0.9,
                    "conflict": 0.0,
                    "missing": 0.0,
                }
            ],
        },
        "perturbations": [
            {
                "query": "p",
                "label_answerable": expected,
                "support_key": support_key,
                "perturbation_type": "perturbed",
                "docs": [
                    {
                        "doc_id": "pert",
                        "text": "perturbed evidence",
                        "corm_score": 0.8,
                        "support": 0.8,
                        "conflict": 0.0,
                        "missing": 0.0,
                    }
                ],
            }
        ],
    }


def test_evaluate_audited_orbits_uses_only_labeled_records(tmp_path):
    path = tmp_path / "audit.jsonl"
    rows = [
        _audit_row("pos", True, True),
        _audit_row("neg", False, False, support_key="other"),
        _audit_row("pending", False, None),
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    result = evaluate_audited_orbits(path, bootstrap_samples=0)

    assert result["audit"]["total"] == 3
    assert result["audit"]["labeled"] == 2
    assert result["audit"]["pending"] == 1
    assert result["audit"]["agreement_with_expected"] == 1.0
    assert result["summary"]["csrm"]["n"] == 2
    assert result["splits"]["unit"]["positive"] == 1
    assert result["splits"]["unit"]["negative"] == 1


def test_evaluate_audited_orbits_rejects_invalid_labels(tmp_path):
    path = tmp_path / "audit.jsonl"
    row = _audit_row("bad", True, "maybe")
    path.write_text(json.dumps(row), encoding="utf-8")

    with pytest.raises(ValueError, match="invalid labels in auditor_label_answerable"):
        evaluate_audited_orbits(path, bootstrap_samples=0)


def test_evaluate_audited_orbits_can_use_adjudicated_label(tmp_path):
    path = tmp_path / "audit.jsonl"
    row = _audit_row("adjudicated", True, None)
    row["adjudicated_label_answerable"] = False
    path.write_text(json.dumps(row), encoding="utf-8")

    result = evaluate_audited_orbits(
        path,
        bootstrap_samples=0,
        label_field="adjudicated_label_answerable",
    )

    assert result["audit"]["label_source"] == "adjudicated_label_answerable"
    assert result["audit"]["labeled"] == 1
    assert result["splits"]["unit"]["negative"] == 1
