import json

from experiments.summarize_v4_strong_baselines import (
    render_markdown,
    summarize_v4_strong_baselines,
)


def test_summarize_v4_strong_baselines_tracks_rule_losses_and_calibrated_rows(tmp_path):
    baseline = tmp_path / "baselines_toy.json"
    comparison = tmp_path / "compare_calibrated_toy.json"
    _write_json(baseline, _baseline_payload())
    _write_json(comparison, _comparison_payload())

    summary = summarize_v4_strong_baselines([baseline], [comparison])

    rule = summary["aggregate"]["csrm_rule_vs_strongest"]["by_auroc"]
    assert rule["losses"] == 1
    assert "calibrated_logistic_orbit" in summary["aggregate"]["method_union"]
    logistic = summary["aggregate"]["calibrated_targets_vs_all_baselines"]["csrm_calibrated_logistic"]
    assert logistic["risk_at_30_reduction"]["losses"] == 1
    assert "not an all-win" in summary["claim_implication"]


def test_render_markdown_mentions_strong_baseline_package(tmp_path):
    baseline = tmp_path / "baselines_toy.json"
    comparison = tmp_path / "compare_calibrated_toy.json"
    _write_json(baseline, _baseline_payload())
    _write_json(comparison, _comparison_payload())

    text = render_markdown(summarize_v4_strong_baselines([baseline], [comparison]))

    assert "V4 Strong Baseline Coverage" in text
    assert "CSRM-Rule vs Strongest Non-CSRM" in text
    assert "calibrated_logistic_orbit" in text


def _baseline_payload():
    return {
        "n": 4,
        "source_item_groups": 2,
        "methods": {
            "csrm_rule": {},
            "calibrated_logistic_orbit": {},
            "context_sufficiency_clean": {},
        },
        "strongest_non_csrm": {
            "by_auroc": {"method": "calibrated_logistic_orbit"},
            "by_risk_at_30": {"method": "calibrated_logistic_orbit"},
            "by_aurc": {"method": "calibrated_logistic_orbit"},
        },
        "csrm_vs_strongest_non_csrm": {
            "by_auroc": {
                "auroc_improvement": -0.1,
                "risk_at_30_reduction": -0.2,
                "risk_at_50_reduction": 0.0,
                "aurc_reduction": -0.05,
            },
            "by_risk_at_30": {
                "auroc_improvement": -0.1,
                "risk_at_30_reduction": -0.2,
                "risk_at_50_reduction": 0.0,
                "aurc_reduction": -0.05,
            },
            "by_aurc": {
                "auroc_improvement": -0.1,
                "risk_at_30_reduction": -0.2,
                "risk_at_50_reduction": 0.0,
                "aurc_reduction": -0.05,
            },
        },
    }


def _comparison_payload():
    return {
        "n": 4,
        "seeds": [1],
        "aggregate": {
            "csrm_calibrated_logistic": {
                "calibrated_logistic_orbit": _metric_block(-0.1),
                "context_sufficiency_clean": _metric_block(0.2),
            },
            "csrm_rule": {
                "calibrated_logistic_orbit": _metric_block(-0.2),
                "context_sufficiency_clean": _metric_block(0.1),
            },
        },
    }


def _metric_block(value):
    return {
        "auroc_improvement": {"mean": value},
        "risk_at_30_reduction": {"mean": value},
        "risk_at_50_reduction": {"mean": value},
        "aurc_reduction": {"mean": value},
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
