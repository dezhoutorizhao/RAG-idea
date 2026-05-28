import json

from experiments.build_v4_hard_negative_matched_subset import build_v4_hard_negative_matched_subset


def test_build_v4_hard_negative_matched_subset_prefers_same_group_and_balances_answer_overlap(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    scored = tmp_path / "scored.jsonl"
    prefix = tmp_path / "hard"
    raw_rows = [
        _raw("g1:stable", "g1", "Paris is in France.", "France"),
        _raw("g1:missing", "g1", "Paris is a city in France.", "France"),
        _raw("g2:stable", "g2", "Berlin is in Germany.", "Germany"),
        _raw("g2:missing", "g2", "Berlin is a city in Germany.", "Germany"),
    ]
    private_rows = [
        _private("g1:stable", "g1", True, "stable"),
        _private("g1:missing", "g1", False, "missing"),
        _private("g2:stable", "g2", True, "stable"),
        _private("g2:missing", "g2", False, "missing"),
    ]
    scored_rows = [
        _scored("g1:stable", True),
        _scored("g1:missing", False),
        _scored("g2:stable", True),
        _scored("g2:missing", False),
    ]
    _write_jsonl(raw, raw_rows)
    _write_jsonl(private, private_rows)
    _write_jsonl(scored, scored_rows)

    report = build_v4_hard_negative_matched_subset(raw, private, scored, prefix)

    assert report["matched_positive"] == 2
    assert report["matched_negative"] == 2
    assert report["negative_construction_counts"] == {"missing": 2}
    assert all(pair["same_group"] for pair in report["pairs"])
    assert report["feature_balance"]["answer_all_coverage"]["absolute_mean_gap"] == 0.0
    assert (tmp_path / "hard.raw.jsonl").exists()


def _raw(orbit_id, group_id, text, answer):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "query": "Where is the city?",
        "candidate_answer": answer,
        "clean_evidence": [{"doc_id": orbit_id, "text": text, "retrieval_score": 0.5}],
        "perturbations": [{"query": "Where is the city?", "candidate_answer": answer, "evidence": [{"doc_id": orbit_id + ":p", "text": text, "retrieval_score": 0.5}]}],
        "retrieval_scores": [0.5, 0.5],
        "generator_outputs": [],
        "verifier_outputs": {},
    }


def _private(orbit_id, group_id, label, construction):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "label_answerable": label,
        "construction_type": construction,
    }


def _scored(orbit_id, label):
    return {
        "orbit_id": orbit_id,
        "split": "unit",
        "clean": {
            "query": "Where is the city?",
            "answer": "x",
            "label_answerable": label,
            "docs": [{"doc_id": orbit_id, "text": "text", "corm_score": 0.5, "support": 0.5, "conflict": 0.0, "missing": 0.5}],
        },
        "perturbations": [],
    }


def _write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
