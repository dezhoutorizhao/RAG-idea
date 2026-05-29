import json

from experiments.summarize_v4_split_threshold_protocol import (
    render_markdown,
    summarize_v4_split_threshold_protocol,
)


def test_summarize_v4_split_threshold_protocol_marks_missing_shared_threshold(tmp_path):
    root = tmp_path
    baseline = root / "results" / "baselines_unit.json"
    comparison = root / "results" / "compare_unit.json"
    baseline.parent.mkdir()
    baseline.write_text(
        json.dumps(
            {
                "fairness": {
                    "same_input_rows": True,
                    "same_scored_evidence": True,
                    "logistic_scores": "out-of-fold by source_item_group_id when possible",
                }
            }
        ),
        encoding="utf-8",
    )
    comparison.write_text(
        json.dumps(
            {
                "source_item_groups": 10,
                "seeds": [17],
                "cal_frac": 0.2,
                "per_seed": [
                    {
                        "split_sizes": {
                            "train_groups": 6,
                            "calibration_groups": 2,
                            "test_groups": 2,
                            "calibration": 4,
                        },
                        "target_metrics": {
                            "csrm_calibrated_logistic": {},
                            "csrm_calibrated_isotonic": {},
                            "csrm_calibrated_gbdt": {},
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    strong = root / "results" / "v4_strong_baseline_summary_20260529.json"
    strong.write_text(
        json.dumps(
            {
                "aggregate": {
                    "csrm_rule_vs_strongest": {
                        "by_auroc": {"losses": [{"dataset": "unit"}]},
                    }
                },
                "baseline_rows": [{"artifact": "results/baselines_unit.json"}],
                "comparison_rows": [{"artifact": "results/compare_unit.json"}],
            }
        ),
        encoding="utf-8",
    )

    summary = summarize_v4_split_threshold_protocol(strong, tmp_path / "missing_threshold.json")
    rows = {row["requirement"]: row for row in summary["rows"]}

    assert rows["same_input_rows"]["status"] == "pass"
    assert rows["same_scored_evidence"]["status"] == "pass"
    assert rows["source_item_group_split"]["status"] == "pass"
    assert rows["target_calibration_split"]["status"] == "pass"
    assert rows["shared_calibration_threshold_selection"]["status"] == "missing"
    assert summary["source_item_group_split_supported"] is True
    assert summary["threshold_selection_claim_supported"] is False
    assert summary["protocol_complete"] is False

    text = render_markdown(summary)
    assert "V4 Split and Threshold Protocol" in text
    assert "fixed-coverage" in text


def test_summarize_v4_split_threshold_protocol_accepts_shared_threshold_artifact(tmp_path):
    baseline = tmp_path / "results" / "baselines_unit.json"
    comparison = tmp_path / "results" / "compare_unit.json"
    threshold = tmp_path / "results" / "threshold_unit.json"
    baseline.parent.mkdir()
    baseline.write_text(
        json.dumps(
            {
                "fairness": {
                    "same_input_rows": True,
                    "same_scored_evidence": True,
                    "logistic_scores": "out-of-fold by source_item_group_id when possible",
                }
            }
        ),
        encoding="utf-8",
    )
    comparison.write_text(
        json.dumps(
            {
                "source_item_groups": 10,
                "seeds": [17],
                "cal_frac": 0.2,
                "per_seed": [
                    {
                        "split_sizes": {
                            "train_groups": 6,
                            "calibration_groups": 2,
                            "test_groups": 2,
                            "calibration": 4,
                        },
                        "target_metrics": {
                            "csrm_calibrated_logistic": {},
                            "csrm_calibrated_isotonic": {},
                            "csrm_calibrated_gbdt": {},
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    threshold.write_text(
        json.dumps(
            {
                "dataset_count": 6,
                "seeds": [17, 31, 47],
                "risk_targets": [0.2, 0.3],
                "shared_threshold_protocol_complete": True,
                "protocol": {
                    "threshold_selected_on": "calibration split",
                    "threshold_applied_to": "held-out test split",
                },
            }
        ),
        encoding="utf-8",
    )
    strong = tmp_path / "results" / "v4_strong_baseline_summary_20260529.json"
    strong.write_text(
        json.dumps(
            {
                "aggregate": {
                    "csrm_rule_vs_strongest": {
                        "by_auroc": {"losses": [{"dataset": "unit"}]},
                    }
                },
                "baseline_rows": [{"artifact": str(baseline)}],
                "comparison_rows": [{"artifact": str(comparison)}],
            }
        ),
        encoding="utf-8",
    )

    summary = summarize_v4_split_threshold_protocol(strong, threshold)
    rows = {row["requirement"]: row for row in summary["rows"]}

    assert rows["shared_calibration_threshold_selection"]["status"] == "pass"
    assert summary["threshold_selection_claim_supported"] is True
    assert summary["protocol_complete"] is True
