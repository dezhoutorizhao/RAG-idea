import json

from experiments.summarize_v4_calibration_quality import (
    render_markdown,
    summarize_v4_calibration_quality,
)


def test_summarize_v4_calibration_quality_tracks_brier_and_ece_wins(tmp_path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    _write_calibration_result(first, "first.raw.jsonl", rule=(0.30, 0.09), minimax=(0.28, 0.08), logistic=(0.12, 0.03), isotonic=(0.14, 0.04))
    _write_calibration_result(second, "second.raw.jsonl", rule=(0.22, 0.02), minimax=(0.21, 0.03), logistic=(0.11, 0.04), isotonic=(0.13, 0.05))

    summary = summarize_v4_calibration_quality([first, second])

    assert summary["dataset_count"] == 2
    assert summary["aggregate"]["best_target_brier_win_count"] == 2
    assert summary["aggregate"]["best_target_ece_win_count"] == 1
    assert summary["aggregate"]["datasets_with_ece_nonwin"] == ["second"]
    assert summary["calibration_quality_supported"] is True

    text = render_markdown(summary)
    assert "V4 Calibration Quality" in text
    assert "Best calibrated target Brier wins: `2/2`" in text


def _write_calibration_result(path, raw_input, *, rule, minimax, logistic, isotonic):
    methods = {
        "csrm_rule": rule,
        "csrm_minimax": minimax,
        "csrm_calibrated_logistic": logistic,
        "csrm_calibrated_isotonic": isotonic,
    }
    payload = {
        "raw_input": raw_input,
        "n": 20,
        "seeds": [17, 31],
        "risk_target": 0.30,
        "aggregate": {
            method: {
                "auroc": {"mean": 0.80},
                "aurc": {"mean": 0.10},
                "risk_at_30": {"mean": 0.20},
                "risk_at_50": {"mean": 0.18},
                "target_met_rate": 1.0,
                "zero_coverage_count": 0,
            }
            for method in methods
        },
        "per_seed": [
            {
                "methods": {
                    method: {
                        "test": {
                            "brier": brier,
                            "calibration": {"ece": ece, "mce": ece + 0.01},
                        }
                    }
                    for method, (brier, ece) in methods.items()
                }
            },
            {
                "methods": {
                    method: {
                        "test": {
                            "brier": brier + 0.02,
                            "calibration": {"ece": ece + 0.01, "mce": ece + 0.02},
                        }
                    }
                    for method, (brier, ece) in methods.items()
                }
            },
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
