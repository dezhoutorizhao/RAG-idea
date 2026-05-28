import json

from experiments.run_v4_anti_shortcut_probes import run_v4_anti_shortcut_probes
from experiments.score_orbits_textonly_v4 import score_orbits_textonly_v4


def test_v4_anti_shortcut_report_contains_required_probes(tmp_path):
    raw_path = tmp_path / "raw.jsonl"
    private_path = tmp_path / "private.jsonl"
    scored_path = tmp_path / "scored.jsonl"
    output_path = tmp_path / "anti_shortcut.json"
    raw_rows = [
        {
            "orbit_id": "g1:stable",
            "source_item_group_id": "g1",
            "dataset": "demo",
            "query": "Where is Paris?",
            "candidate_answer": "France",
            "clean_evidence": [{"doc_id": "d1", "text": "Paris is in France.", "retrieval_score": 0.9}],
            "perturbations": [],
            "retrieval_scores": [0.9],
            "generator_outputs": [],
            "verifier_outputs": {},
        },
        {
            "orbit_id": "g2:fragile",
            "source_item_group_id": "g2",
            "dataset": "demo",
            "query": "Where is Paris?",
            "candidate_answer": "France",
            "clean_evidence": [{"doc_id": "d2", "text": "Paris is a city.", "retrieval_score": 0.2}],
            "perturbations": [],
            "retrieval_scores": [0.2],
            "generator_outputs": [],
            "verifier_outputs": {},
        },
    ]
    private_rows = [
        {"orbit_id": "g1:stable", "source_item_group_id": "g1", "label_answerable": True, "construction_type": "stable"},
        {"orbit_id": "g2:fragile", "source_item_group_id": "g2", "label_answerable": False, "construction_type": "fragile"},
    ]
    raw_path.write_text("\n".join(json.dumps(row) for row in raw_rows), encoding="utf-8")
    private_path.write_text("\n".join(json.dumps(row) for row in private_rows), encoding="utf-8")
    score_orbits_textonly_v4(raw_path, private_path, scored_path)

    report = run_v4_anti_shortcut_probes(
        raw_path,
        private_path,
        scored_path,
        output_path=output_path,
        random_trials=10,
        seed=5,
    )

    assert report["raw_firewall_passed"] is True
    assert "structural_only_probe" in report
    assert "random_label_sanity" in report
    assert "group_split_probe" in report
    assert "private_metadata_leakage_upper_bound" in report
