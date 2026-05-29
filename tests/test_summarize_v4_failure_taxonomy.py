import json

from experiments.summarize_v4_failure_taxonomy import (
    render_markdown,
    summarize_v4_failure_taxonomy,
)


def test_summarize_v4_failure_taxonomy_aggregates_taxonomy_and_metrics(tmp_path):
    first = tmp_path / "failure_analysis_first.json"
    second = tmp_path / "failure_analysis_second.json"
    _write_json(first, _payload("missing_hop", target_risk=0.1, baseline_risk=0.3))
    _write_json(second, _payload("semantic_swap", target_risk=0.4, baseline_risk=0.2))

    summary = summarize_v4_failure_taxonomy([first, second])

    assert summary["dataset_count"] == 2
    assert summary["metric_aggregate"]["risk_at_30"]["wins"] == 1
    assert summary["metric_aggregate"]["risk_at_30"]["losses"] == 1
    assert {item["construction_type"] for item in summary["taxonomy"]} == {
        "missing_hop",
        "semantic_swap",
    }
    assert summary["case_gallery_coverage"]["target_high_false_positive"] == 2


def test_render_markdown_includes_claim_boundary(tmp_path):
    path = tmp_path / "failure_analysis_demo.json"
    _write_json(path, _payload("missing_hop", target_risk=0.1, baseline_risk=0.3))

    text = render_markdown(summarize_v4_failure_taxonomy([path]))

    assert "V4 Failure Taxonomy Summary" in text
    assert "Construction Taxonomy" in text
    assert "human audit v4" in text


def _payload(construction_type, *, target_risk, baseline_risk):
    return {
        "seed": 31,
        "split_sizes": {"test": 10},
        "metrics": {
            "target": {
                "auroc": 0.8,
                "risk_at_30": target_risk,
                "risk_at_50": target_risk,
                "mean_score_positive": 0.7,
                "mean_score_negative": 0.2,
            },
            "baseline_calibrated_logistic_orbit": {
                "auroc": 0.7,
                "risk_at_30": baseline_risk,
                "risk_at_50": baseline_risk,
                "mean_score_positive": 0.6,
                "mean_score_negative": 0.3,
            },
        },
        "by_construction_type": {
            construction_type: {
                "n": 10,
                "positive": 5,
                "negative": 5,
                "target_mean": 0.4,
                "baseline_mean": 0.5,
                "target_minus_baseline_mean": -0.1,
            }
        },
        "feature_gaps": [
            {
                "feature": "answer_consistency",
                "absolute_gap": 0.5,
                "positive_mean": 0.7,
                "negative_mean": 0.2,
                "positive_minus_negative": 0.5,
            },
            {
                "feature": "worst_sufficiency",
                "absolute_gap": 0.2,
                "positive_mean": 0.6,
                "negative_mean": 0.4,
                "positive_minus_negative": 0.2,
            },
        ],
        "top_cases": {
            "target_high_false_positive": [{"orbit_id": "a"}],
            "target_low_false_negative": [{"orbit_id": "b"}],
        },
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
