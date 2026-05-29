import json

from experiments.summarize_v4_baseline_coverage import (
    render_markdown,
    summarize_v4_baseline_coverage,
)


def test_summarize_v4_baseline_coverage_tracks_missing_llm_judge(tmp_path):
    summary_path = tmp_path / "strong.json"
    summary_path.write_text(
        json.dumps(
            {
                "aggregate": {
                    "method_union": [
                        "corm_max_clean",
                        "corm_mean_clean",
                        "faithful_sure_multi",
                        "context_sufficiency_clean",
                        "template_self_consistency",
                        "equal_budget_mean",
                        "equal_budget_min",
                        "equal_budget_q25",
                        "equal_budget_ensemble_logistic",
                        "retrieval_stability",
                        "calibrated_logistic_context",
                        "calibrated_logistic_orbit",
                    ]
                }
            }
        ),
        encoding="utf-8",
    )

    summary = summarize_v4_baseline_coverage(summary_path)
    rows = {row["requirement"]: row for row in summary["rows"]}

    assert rows["llm_judge"]["status"] == "missing"
    assert rows["self_consistency"]["status"] == "present"
    assert rows["faithful_or_official_corm_rag"]["status"] == "partial"
    assert rows["equal_budget_orbit_ensemble"]["status"] == "present"
    assert summary["all_required_baselines_present"] is False

    text = render_markdown(summary)
    assert "V4 Baseline Coverage Matrix" in text
    assert "llm_judge" in text
