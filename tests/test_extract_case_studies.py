import json

from experiments.extract_case_studies import extract_case_studies


def _record(orbit_id, split, label, support_key, pert_key, support):
    return {
        "orbit_id": orbit_id,
        "clean": {
            "query": "q",
            "answer": "a",
            "label_answerable": True,
            "split": split,
            "metadata": {"support_key": support_key, "perturbation_type": "clean"},
            "docs": [
                {
                    "doc_id": "d1",
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
                "query": "q pert",
                "answer": "a",
                "label_answerable": label,
                "split": split,
                "metadata": {"support_key": pert_key, "perturbation_type": "pert"},
                "docs": [
                    {
                        "doc_id": "d2",
                        "text": "pert evidence",
                        "corm_score": 0.8,
                        "support": support,
                        "conflict": 0.0,
                        "missing": 0.0,
                    }
                ],
            }
        ],
    }


def test_extract_case_studies_writes_json_and_markdown(tmp_path):
    input_path = tmp_path / "orbits.jsonl"
    rows = [
        _record("pos", "stable", True, "gold", "gold", 0.9),
        _record("neg", "fragile", False, "gold", "false", 0.8),
    ]
    input_path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    output_json = tmp_path / "cases.json"
    output_md = tmp_path / "cases.md"

    payload = extract_case_studies(input_path, output_json, output_md, 2, 100)

    assert output_json.exists()
    assert output_md.exists()
    assert "csrm_true_accept" in payload["categories"]
    assert payload["thresholds_at_30_coverage"]["csrm"] > 0.0
