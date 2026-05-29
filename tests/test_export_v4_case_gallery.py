import json

from experiments.export_v4_case_gallery import export_v4_case_gallery, render_markdown


def test_export_v4_case_gallery_writes_all_cases_and_summary(tmp_path):
    first = tmp_path / "failure_analysis_first.json"
    second = tmp_path / "failure_analysis_second.json"
    _write_json(first, _payload("missing_hop", "q1"))
    _write_json(second, _payload("semantic_swap", "q2"))
    output_jsonl = tmp_path / "gallery.jsonl"
    output_md = tmp_path / "gallery.md"
    summary_json = tmp_path / "summary.json"

    summary = export_v4_case_gallery(
        [first, second],
        output_jsonl,
        output_md,
        summary_json,
        per_bucket_per_dataset=1,
    )

    assert summary["case_count"] == 4
    assert summary["bucket_counts"]["target_high_false_positive"] == 2
    assert summary["construction_type_counts"]["missing_hop"] == 2
    assert output_jsonl.read_text(encoding="utf-8").count("\n") == 4
    assert "not human-adjudicated evidence" in output_md.read_text(encoding="utf-8")
    assert json.loads(summary_json.read_text(encoding="utf-8"))["case_count"] == 4


def test_render_markdown_limits_representatives_per_bucket_and_dataset(tmp_path):
    first = tmp_path / "failure_analysis_first.json"
    _write_json(first, _payload("missing_hop", "q"))
    summary = export_v4_case_gallery(
        [first],
        tmp_path / "gallery.jsonl",
        tmp_path / "gallery.md",
        tmp_path / "summary.json",
        per_bucket_per_dataset=1,
    )
    cases = [
        {
            "dataset": "first",
            "bucket": "target_high_false_positive",
            "rank_in_bucket": 1,
            "orbit_id": "a",
            "construction_type": "missing_hop",
            "label_answerable": False,
            "target_score": 0.9,
            "baseline_score": 0.8,
            "score_gap_target_minus_baseline": 0.1,
            "query": "q1",
            "candidate_answer": "a",
            "top_features": [{"feature": "min_sufficiency", "value": 0.2}],
        },
        {
            "dataset": "first",
            "bucket": "target_high_false_positive",
            "rank_in_bucket": 2,
            "orbit_id": "b",
            "construction_type": "missing_hop",
            "label_answerable": False,
            "target_score": 0.7,
            "baseline_score": 0.6,
            "score_gap_target_minus_baseline": 0.1,
            "query": "q2",
            "candidate_answer": "b",
            "top_features": [{"feature": "min_sufficiency", "value": 0.3}],
        },
    ]

    text = render_markdown(summary, cases, per_bucket_per_dataset=1)

    assert "Orbit: `a`" in text
    assert "Orbit: `b`" not in text


def _payload(construction_type, query):
    return {
        "top_cases": {
            "target_high_false_positive": [_case("a", construction_type, query)],
            "target_low_false_negative": [_case("b", construction_type, query)],
        }
    }


def _case(suffix, construction_type, query):
    return {
        "orbit_id": f"orbit-{suffix}",
        "query": query,
        "candidate_answer": "answer",
        "label_answerable": False,
        "construction_type": construction_type,
        "target_score": 0.8,
        "baseline_score": 0.7,
        "score_gap_target_minus_baseline": 0.1,
        "top_features": [
            {"feature": "min_sufficiency", "value": 0.2},
            {"feature": "retrieval_overlap", "value": 1.0},
        ],
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
