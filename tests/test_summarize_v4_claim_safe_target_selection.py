import json

from experiments.summarize_v4_claim_safe_target_selection import (
    render_markdown,
    summarize_v4_claim_safe_target_selection,
)


def test_summarize_v4_claim_safe_target_selection_prefers_gbdt_with_caveats(tmp_path):
    strong = tmp_path / "strong.json"
    coverage = tmp_path / "coverage.json"
    calibration = tmp_path / "calibration.json"
    human = tmp_path / "human.json"
    text_only = tmp_path / "text.json"
    _write_json(strong, _strong_payload())
    _write_json(
        coverage,
        {
            "rows": [
                {"requirement": "llm_judge", "status": "missing", "boundary": "missing"},
                {
                    "requirement": "faithful_or_official_corm_rag",
                    "status": "partial",
                    "boundary": "partial",
                },
            ]
        },
    )
    _write_json(
        calibration,
        {
            "rows": [
                {
                    "best_target_by_brier": {"method": "csrm_calibrated_gbdt"},
                    "best_target_by_ece": {"method": "csrm_calibrated_isotonic"},
                }
            ]
        },
    )
    _write_json(
        human,
        {
            "human_labels_complete": False,
            "pending_auditor_labels": 2,
            "pending_adjudicated_labels": 1,
        },
    )
    _write_json(text_only, {"ready_for_text_only_main_claim": False})

    summary = summarize_v4_claim_safe_target_selection(
        strong,
        coverage,
        calibration,
        human,
        text_only,
    )

    assert summary["recommended_primary_target"] == "csrm_calibrated_gbdt"
    assert summary["all_win_supported"] is False
    assert any("LLM-as-judge" in item for item in summary["blocked_items"])
    assert any("CSRM-Rule" in item for item in summary["disallowed_wording"])

    text = render_markdown(summary)
    assert "V4 Claim-Safe Target Selection" in text
    assert "primary_with_caveats" in text


def _strong_payload():
    return {
        "aggregate": {
            "csrm_rule_vs_strongest": {
                "by_auroc": {"wins": 0, "ties": 0, "losses": 1},
            },
            "calibrated_targets_vs_all_baselines": {
                "csrm_calibrated_gbdt": _target_metrics(losses=1, wins=2, ties=3, delta=0.05),
                "csrm_calibrated_logistic": _target_metrics(losses=3, wins=1, ties=2, delta=-0.01),
                "csrm_calibrated_isotonic": _target_metrics(losses=4, wins=0, ties=2, delta=-0.02),
            },
        }
    }


def _target_metrics(*, losses, wins, ties, delta):
    return {
        metric: {
            "losses": losses,
            "robust_wins": wins,
            "ties": ties,
            "mean_worst_case_delta": delta,
        }
        for metric in [
            "auroc_improvement",
            "auprc_improvement",
            "risk_at_30_reduction",
            "risk_at_50_reduction",
            "risk_at_70_reduction",
            "aurc_reduction",
        ]
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
