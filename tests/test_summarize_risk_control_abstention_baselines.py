import json

from experiments.summarize_risk_control_abstention_baselines import (
    render_markdown,
    summarize_risk_control_abstention_baselines,
)


def test_summarize_risk_control_abstention_baselines_tracks_best_baselines(tmp_path):
    path = tmp_path / "thresholds.json"
    _write_json(
        path,
        {
            "shared_threshold_protocol_complete": True,
            "risk_targets": [0.2],
            "aggregate": {
                "method_summary": [
                    {
                        "family": "baseline",
                        "method": "calibrated_logistic_orbit",
                        "risk_target": 0.2,
                        "row_count": 3,
                        "test_target_pass_rate": 0.67,
                        "mean_test_coverage": 0.40,
                        "mean_test_risk": 0.18,
                        "no_accept_rows": 0,
                    },
                    {
                        "family": "baseline",
                        "method": "context_sufficiency_clean",
                        "risk_target": 0.2,
                        "row_count": 3,
                        "test_target_pass_rate": 0.33,
                        "mean_test_coverage": 0.70,
                        "mean_test_risk": 0.30,
                        "no_accept_rows": 1,
                    },
                    {
                        "family": "target",
                        "method": "csrm",
                        "risk_target": 0.2,
                        "row_count": 3,
                    },
                ]
            },
        },
    )

    summary = summarize_risk_control_abstention_baselines(path)

    assert summary["risk_control_abstention_baseline_present"] is True
    assert summary["baseline_methods"] == ["calibrated_logistic_orbit", "context_sufficiency_clean"]
    target = summary["by_target"][0]
    assert target["method_count"] == 2
    assert target["best_by_test_target_pass_rate"]["method"] == "calibrated_logistic_orbit"
    assert target["best_mean_coverage_with_mean_risk_at_target"]["method"] == "calibrated_logistic_orbit"
    assert "Risk-Control Abstention Baselines" in render_markdown(summary)


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
