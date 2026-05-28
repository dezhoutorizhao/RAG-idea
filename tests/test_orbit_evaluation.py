import json

from experiments.convert_corm_scored import convert_scored_file
from experiments.evaluate_orbits import evaluate, load_orbits


def test_convert_corm_scored_fixture(tmp_path):
    source = tmp_path / "scored.json"
    source.write_text(
        json.dumps(
            {
                "CoRM-RAG": [
                    [
                        {
                            "idx": 1,
                            "text": "Paris is the capital of France.",
                            "score": 12.0,
                            "rerank_score": 0.93,
                        }
                    ]
                ]
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "orbits.jsonl"
    convert_scored_file(
        input_path=source,
        output_path=output,
        dataset="demo",
    )
    converted = json.loads(output.read_text(encoding="utf-8"))
    assert converted["orbit_id"] == "demo:0"
    assert converted["clean"]["docs"][0]["corm_score"] == 0.93


def test_evaluate_labeled_orbits_with_verifier_fields(tmp_path):
    records = [
        {
            "orbit_id": "stable",
            "clean": {
                "query": "q",
                "answer": "a",
                "label_answerable": True,
                "split": "stable_support",
                "metadata": {"support_key": "a"},
                "docs": [
                    {"doc_id": "d1", "corm_score": 0.9, "support": 0.9, "conflict": 0.0, "missing": 0.0}
                ],
            },
            "perturbations": [
                {
                    "query": "q pert",
                    "answer": "a",
                    "label_answerable": True,
                    "split": "stable_support",
                    "metadata": {"support_key": "a"},
                    "docs": [
                        {"doc_id": "d1", "corm_score": 0.8, "support": 0.8, "conflict": 0.0, "missing": 0.0}
                    ],
                }
            ],
        },
        {
            "orbit_id": "fragile",
            "clean": {
                "query": "q",
                "answer": "a",
                "label_answerable": False,
                "split": "fragile_support",
                "metadata": {"support_key": "a"},
                "docs": [
                    {"doc_id": "d2", "corm_score": 0.9, "support": 0.8, "conflict": 0.0, "missing": 0.0}
                ],
            },
            "perturbations": [
                {
                    "query": "q pert",
                    "answer": "a",
                    "label_answerable": False,
                    "split": "fragile_support",
                    "metadata": {"support_key": "false"},
                    "docs": [
                        {"doc_id": "d3", "corm_score": 0.8, "support": 0.8, "conflict": 0.2, "missing": 0.0}
                    ],
                }
            ],
        },
    ]
    path = tmp_path / "orbits.jsonl"
    path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")

    result = evaluate(load_orbits(path), bootstrap_samples=0)
    assert "summary" in result
    assert "csrm" in result["summary"]
    assert "csrm_no_worst_sufficiency" in result["summary"]
    assert "csrm_shuffled_perturbations" in result["summary"]
    assert result["splits"]["stable_support"]["positive"] == 1
    assert result["splits"]["fragile_support"]["negative"] == 1


def test_load_orbits_uses_top_level_split_as_fallback(tmp_path):
    record = {
        "orbit_id": "audit-row",
        "split": "audit_split",
        "clean": {
            "query": "q",
            "answer": "a",
            "label_answerable": True,
            "metadata": {"support_key": "a"},
            "docs": [
                {"doc_id": "d1", "corm_score": 0.9, "support": 0.9, "conflict": 0.0, "missing": 0.0}
            ],
        },
        "perturbations": [
            {
                "query": "q pert",
                "answer": "a",
                "label_answerable": True,
                "metadata": {"support_key": "a"},
                "docs": [
                    {"doc_id": "d1", "corm_score": 0.8, "support": 0.8, "conflict": 0.0, "missing": 0.0}
                ],
            }
        ],
    }
    path = tmp_path / "audit_orbits.jsonl"
    path.write_text(json.dumps(record), encoding="utf-8")

    [orbit] = load_orbits(path)

    assert orbit.clean.split == "audit_split"
    assert orbit.perturbations[0].split == "audit_split"
