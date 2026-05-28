import json

from experiments.evaluate_orbits import evaluate, load_orbits
from experiments.score_orbits_textonly_v4 import score_orbits_textonly_v4


def test_textonly_v4_scores_raw_and_uses_private_only_for_labels(tmp_path):
    raw_path = tmp_path / "raw.jsonl"
    private_path = tmp_path / "private.jsonl"
    output_path = tmp_path / "scored.jsonl"
    report_path = tmp_path / "report.json"
    raw_rows = [
        {
            "orbit_id": "o1:stable",
            "source_item_group_id": "o1",
            "dataset": "demo",
            "query": "What city is the capital of France?",
            "candidate_answer": "Paris",
            "clean_evidence": [
                {"doc_id": "d1", "title": "Paris", "text": "Paris is the capital city of France.", "rank": 0, "retrieval_score": 0.9}
            ],
            "perturbations": [
                {
                    "query": "Verify the capital of France.",
                    "candidate_answer": "Paris",
                    "evidence": [
                        {"doc_id": "d1", "title": "Paris", "text": "France has Paris as its capital.", "rank": 0, "retrieval_score": 0.8}
                    ],
                }
            ],
            "retrieval_scores": [0.9, 0.8],
            "generator_outputs": [],
            "verifier_outputs": {},
        },
        {
            "orbit_id": "o2:fragile",
            "source_item_group_id": "o2",
            "dataset": "demo",
            "query": "What city is the capital of France?",
            "candidate_answer": "Paris",
            "clean_evidence": [
                {"doc_id": "d2", "title": "France", "text": "France is a country in Europe.", "rank": 0, "retrieval_score": 0.7}
            ],
            "perturbations": [],
            "retrieval_scores": [0.7],
            "generator_outputs": [],
            "verifier_outputs": {},
        },
    ]
    private_rows = [
        {"orbit_id": "o1:stable", "label_answerable": True, "construction_type": "stable"},
        {"orbit_id": "o2:fragile", "label_answerable": False, "construction_type": "fragile"},
    ]
    raw_path.write_text("\n".join(json.dumps(row) for row in raw_rows), encoding="utf-8")
    private_path.write_text("\n".join(json.dumps(row) for row in private_rows), encoding="utf-8")

    report = score_orbits_textonly_v4(raw_path, private_path, output_path, report_path)
    assert report["orbits"] == 2
    assert report["scorer"]["uses_private_fields"] is False

    orbits = load_orbits(output_path)
    result = evaluate(orbits, bootstrap_samples=0)
    assert "csrm" in result["summary"]
    assert result["summary"]["csrm"]["n"] == 2
