import json

from experiments.build_v4_score_controlled_variant import build_v4_score_controlled_variant


def test_build_v4_score_controlled_variant_constant_mode_rewrites_all_visible_scores(tmp_path):
    raw_path = tmp_path / "raw.jsonl"
    output_path = tmp_path / "constant.raw.jsonl"
    report_path = tmp_path / "constant.report.json"
    raw_path.write_text(json.dumps(_raw_row()) + "\n", encoding="utf-8")

    report = build_v4_score_controlled_variant(
        raw_path,
        output_path,
        report_path,
        mode="constant",
        constant_score=0.42,
    )

    row = json.loads(output_path.read_text(encoding="utf-8"))
    assert report["score_summary_after"]["unique_values"] == 1
    assert row["retrieval_scores"] == [0.42, 0.42, 0.42, 0.42]
    assert [doc["retrieval_score"] for doc in row["clean_evidence"]] == [0.42, 0.42]
    assert [doc["retrieval_score"] for doc in row["perturbations"][0]["evidence"]] == [0.42, 0.42]
    assert json.loads(report_path.read_text(encoding="utf-8"))["mode"] == "constant"


def test_build_v4_score_controlled_variant_rank_mode_is_set_local(tmp_path):
    raw_path = tmp_path / "raw.jsonl"
    output_path = tmp_path / "rank.raw.jsonl"
    raw_path.write_text(json.dumps(_raw_row()) + "\n", encoding="utf-8")

    build_v4_score_controlled_variant(raw_path, output_path, mode="rank")

    row = json.loads(output_path.read_text(encoding="utf-8"))
    assert [doc["retrieval_score"] for doc in row["clean_evidence"]] == [1.0, 0.0]
    assert [doc["retrieval_score"] for doc in row["perturbations"][0]["evidence"]] == [1.0, 0.0]
    assert row["retrieval_scores"] == [1.0, 0.0, 1.0, 0.0]


def _raw_row() -> dict:
    return {
        "orbit_id": "demo:stable",
        "source_item_group_id": "demo",
        "dataset": "demo",
        "query": "Where is Paris?",
        "candidate_answer": "France",
        "clean_evidence": [
            {"doc_id": "d1", "text": "Paris is in France.", "rank": 0, "retrieval_score": 0.9},
            {"doc_id": "d2", "text": "France is in Europe.", "rank": 1, "retrieval_score": 0.3},
        ],
        "perturbations": [
            {
                "query": "Where is Paris?",
                "candidate_answer": "France",
                "evidence": [
                    {"doc_id": "d3", "text": "Paris is a city.", "rank": 0, "retrieval_score": 0.7},
                    {"doc_id": "d4", "text": "France has cities.", "rank": 1, "retrieval_score": 0.2},
                ],
            }
        ],
        "retrieval_scores": [0.9, 0.3, 0.7, 0.2],
        "generator_outputs": [],
        "verifier_outputs": {},
    }
