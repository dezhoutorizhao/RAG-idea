import json

from experiments.summarize_eval_seeds import summarize_eval_seeds


def _eval_file(path, auroc, risk30):
    payload = {
        "summary": {
            "csrm": {
                "auroc": auroc,
                "aurc": 0.4,
                "risk_at_30_coverage": {"risk": risk30},
                "risk_at_50_coverage": {"risk": 0.5},
                "accuracy_at_0_5": 0.75,
            }
        }
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_summarize_eval_seeds_aggregates_metrics(tmp_path):
    first = tmp_path / "a.json"
    second = tmp_path / "b.json"
    _eval_file(first, 0.9, 0.2)
    _eval_file(second, 1.0, 0.1)

    result = summarize_eval_seeds([first, second], ["csrm"])

    assert result["n_seeds"] == 2
    assert result["aggregate"]["csrm"]["auroc"]["mean"] == 0.95
    assert result["aggregate"]["csrm"]["risk_at_30"]["min"] == 0.1
