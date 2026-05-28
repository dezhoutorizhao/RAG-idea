import json

from experiments.sample_audit_orbits import sample_audit_orbits


def _record(orbit_id, split, label):
    return {
        "orbit_id": orbit_id,
        "source": "unit",
        "clean": {
            "query": "q",
            "answer": "a",
            "label_answerable": True,
            "split": split,
            "metadata": {"support_key": "gold", "perturbation_type": "clean"},
            "docs": [{"doc_id": "d", "text": "evidence", "corm_score": 0.9}],
        },
        "perturbations": [
            {
                "query": "q2",
                "answer": "a",
                "label_answerable": label,
                "split": split,
                "metadata": {"support_key": "gold", "perturbation_type": "pert"},
                "docs": [{"doc_id": "d2", "text": "perturbed evidence"}],
            }
        ],
    }


def test_sample_audit_orbits_writes_editable_audit_fields(tmp_path):
    source = tmp_path / "orbits.jsonl"
    records = [
        _record("a", "split_a", True),
        _record("b", "split_b", False),
    ]
    source.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
    output = tmp_path / "audit.jsonl"

    sample_audit_orbits([source], output, total=2, seed=1, max_doc_chars=20)

    sampled = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    assert len(sampled) == 2
    assert {item["auditor_label_answerable"] for item in sampled} == {None}
    assert {item["expected_label_answerable"] for item in sampled} == {True, False}
