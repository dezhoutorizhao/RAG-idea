import json

from experiments.summarize_v4_baseline_budget_parity import (
    render_markdown,
    summarize_v4_baseline_budget_parity,
)


def test_summarize_v4_baseline_budget_parity_marks_controls_and_missing_llm(tmp_path):
    baseline = tmp_path / "baselines_unit.json"
    baseline.write_text(
        json.dumps({"fairness": {"same_input_rows": True, "same_scored_evidence": True}}),
        encoding="utf-8",
    )
    summary_path = tmp_path / "results" / "v4_strong_baseline_summary_20260529.json"
    summary_path.parent.mkdir()
    summary_path.write_text(
        json.dumps(
            {
                "aggregate": {
                    "method_union": [
                        "corm_mean_clean",
                        "faithful_sure_multi",
                        "equal_budget_mean",
                        "self_consistency_proxy",
                        "template_self_consistency",
                        "csrm_rule",
                    ]
                },
                "baseline_rows": [{"artifact": str(baseline)}],
            }
        ),
        encoding="utf-8",
    )

    summary = summarize_v4_baseline_budget_parity(summary_path)
    rows = {row["method"]: row for row in summary["rows"]}

    assert rows["corm_mean_clean"]["status"] == "lower_budget_control"
    assert rows["faithful_sure_multi"]["status"] == "equal_orbit_budget"
    assert rows["self_consistency_proxy"]["status"] == "proxy_equal_orbit_budget"
    assert rows["template_self_consistency"]["status"] == "equal_orbit_budget"
    assert rows["llm_judge"]["status"] == "missing"
    assert summary["same_input_rows_all_files"] is True
    assert summary["same_scored_evidence_all_files"] is True
    assert summary["budget_parity_claim_supported"] is False

    text = render_markdown(summary)
    assert "V4 Baseline Budget Parity" in text
    assert "clean-only controls" in text
