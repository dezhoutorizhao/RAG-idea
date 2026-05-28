import json

from experiments.build_v4_matched_subset import build_v4_matched_subset
from experiments.score_orbits_textonly_v4 import score_orbits_textonly_v4


def test_build_v4_matched_subset_outputs_aligned_balanced_files(tmp_path):
    raw_path = tmp_path / "raw.jsonl"
    private_path = tmp_path / "private.jsonl"
    scored_path = tmp_path / "scored.jsonl"
    prefix = tmp_path / "matched"
    raw_rows = [
        _raw("g1:stable", "g1", 0.90, "Paris is in France."),
        _raw("g1:fragile", "g1", 0.88, "Paris is a city."),
        _raw("g2:stable", "g2", 0.10, "Berlin is in Germany."),
        _raw("g2:fragile", "g2", 0.12, "Berlin is a city."),
    ]
    private_rows = [
        _private("g1:stable", "g1", True),
        _private("g1:fragile", "g1", False),
        _private("g2:stable", "g2", True),
        _private("g2:fragile", "g2", False),
    ]
    raw_path.write_text("\n".join(json.dumps(row) for row in raw_rows), encoding="utf-8")
    private_path.write_text("\n".join(json.dumps(row) for row in private_rows), encoding="utf-8")
    score_orbits_textonly_v4(raw_path, private_path, scored_path)

    report = build_v4_matched_subset(raw_path, private_path, scored_path, prefix)

    assert report["matched_positive"] == 2
    assert report["matched_negative"] == 2
    assert all(pair["same_group"] for pair in report["pairs"])
    raw_out = [json.loads(line) for line in (tmp_path / "matched.raw.jsonl").read_text(encoding="utf-8").splitlines()]
    private_out = [json.loads(line) for line in (tmp_path / "matched.private_eval.jsonl").read_text(encoding="utf-8").splitlines()]
    scored_out = [json.loads(line) for line in (tmp_path / "matched.textonly_scored.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [row["orbit_id"] for row in raw_out] == [row["orbit_id"] for row in private_out]
    assert [row["orbit_id"] for row in raw_out] == [row["orbit_id"] for row in scored_out]


def test_build_v4_matched_subset_appends_to_dotted_prefix(tmp_path):
    raw_path = tmp_path / "raw.jsonl"
    private_path = tmp_path / "private.jsonl"
    scored_path = tmp_path / "scored.jsonl"
    prefix = tmp_path / "demo.matched"
    raw_rows = [
        _raw("g1:stable", "g1", 0.90, "Paris is in France."),
        _raw("g1:fragile", "g1", 0.88, "Paris is a city."),
    ]
    private_rows = [
        _private("g1:stable", "g1", True),
        _private("g1:fragile", "g1", False),
    ]
    raw_path.write_text("\n".join(json.dumps(row) for row in raw_rows), encoding="utf-8")
    private_path.write_text("\n".join(json.dumps(row) for row in private_rows), encoding="utf-8")
    score_orbits_textonly_v4(raw_path, private_path, scored_path)

    report = build_v4_matched_subset(raw_path, private_path, scored_path, prefix)

    assert report["outputs"]["raw"].endswith("demo.matched.raw.jsonl")
    assert (tmp_path / "demo.matched.raw.jsonl").exists()
    assert not (tmp_path / "demo.raw.jsonl").exists()


def _raw(orbit_id: str, group_id: str, score: float, text: str) -> dict:
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "query": "Where is the city?",
        "candidate_answer": "France",
        "clean_evidence": [{"doc_id": orbit_id, "text": text, "retrieval_score": score}],
        "perturbations": [],
        "retrieval_scores": [score],
        "generator_outputs": [],
        "verifier_outputs": {},
    }


def _private(orbit_id: str, group_id: str, label: bool) -> dict:
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "label_answerable": label,
        "construction_type": "stable" if label else "fragile",
    }
