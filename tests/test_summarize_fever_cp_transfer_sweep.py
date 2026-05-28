import json

from experiments.summarize_fever_cp_transfer_sweep import (
    render_markdown,
    summarize_fever_cp_transfer_sweep,
)


def test_summarize_fever_cp_transfer_sweep_finds_relaxed_boundary(tmp_path):
    target020 = tmp_path / "target020.json"
    target035 = tmp_path / "target035.json"
    _write_json(target020, _run(0.20, [0.10, 0.25, 0.23]))
    _write_json(target035, _run(0.35, [0.10, 0.32, 0.34]))

    summary = summarize_fever_cp_transfer_sweep([target035, target020])

    assert summary["risk_targets"] == [0.20, 0.35]
    assert summary["primary_method_target_020"]["target_met_count"] == 1
    assert summary["primary_method_first_supported_target"]["risk_target"] == 0.35
    assert summary["negative_evidence_for_main_risk_claim"] is True
    assert len(summary["primary_method_failures_at_020"]) == 2
    assert "negative evidence" in summary["claim_implication"]


def test_render_markdown_reports_boundary(tmp_path):
    target020 = tmp_path / "target020.json"
    target035 = tmp_path / "target035.json"
    _write_json(target020, _run(0.20, [0.10, 0.25, 0.23]))
    _write_json(target035, _run(0.35, [0.10, 0.32, 0.34]))

    summary = summarize_fever_cp_transfer_sweep([target020, target035])
    text = render_markdown(summary)

    assert "FEVER CP Transfer Sweep" in text
    assert "0.3500" in text
    assert "0.20" in text


def _run(risk_target, risks):
    per_seed = []
    for seed, risk in zip([17, 31, 47], risks):
        per_seed.append(
            {
                "seed": seed,
                "methods": {
                    "csrm_logreg_calibrated": {
                        "test": {
                            "accepted": 10,
                            "coverage": 0.1,
                            "errors": round(risk * 10),
                            "empirical_risk": risk,
                            "target_met": risk <= risk_target,
                        }
                    },
                    "csrm_fixed_weights": {
                        "test": {
                            "accepted": 10,
                            "coverage": 0.1,
                            "errors": round(risk * 10),
                            "empirical_risk": risk,
                            "target_met": risk <= risk_target,
                        }
                    },
                },
            }
        )
    return {
        "input": "results/fever.jsonl",
        "risk_target": risk_target,
        "seeds": [17, 31, 47],
        "n_seeds": 3,
        "aggregate": {
            "csrm_logreg_calibrated": _aggregate(risk_target, risks),
            "csrm_fixed_weights": _aggregate(risk_target, risks),
        },
        "per_seed": per_seed,
    }


def _aggregate(risk_target, risks):
    met = [risk <= risk_target for risk in risks]
    return {
        "target_met_count": sum(met),
        "target_miss_count": len(met) - sum(met),
        "cp_feasible_count": len(risks),
        "nonzero_coverage_count": len(risks),
        "test_empirical_risk": {
            "mean": sum(risks) / len(risks),
            "max": max(risks),
            "min": min(risks),
        },
        "test_coverage": {"mean": 0.1, "max": 0.1, "min": 0.1},
        "empirical_transfer_supported": all(met),
        "formal_risk_guarantee_supported": False,
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
