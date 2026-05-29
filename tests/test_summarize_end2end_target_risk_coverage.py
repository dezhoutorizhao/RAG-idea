import json

from experiments.summarize_end2end_target_risk_coverage import (
    render_markdown,
    summarize_end2end_target_risk_coverage,
)


def test_summarize_end2end_target_risk_coverage_reports_coverage_delta(tmp_path):
    source = tmp_path / "curves.json"
    _write_json(
        source,
        {
            "row_count": 2,
            "datasets": ["unit"],
            "retrievers": ["r1"],
            "generators": ["g1", "g2"],
            "rows": [
                _row("g1", csrm=[(0.3, 0.10), (0.5, 0.20)], strongest=[(0.3, 0.20), (0.5, 0.40)]),
                _row("g2", csrm=[(0.3, 0.25), (0.5, 0.40)], strongest=[(0.3, 0.35), (0.5, 0.45)]),
            ],
        },
    )

    summary = summarize_end2end_target_risk_coverage(source, risk_targets=[0.20, 0.30])

    assert summary["row_count"] == 4
    assert summary["aggregate"]["target_count"] == 2
    assert summary["aggregate"]["by_target"][0]["wins"] == 1
    assert summary["aggregate"]["by_target"][0]["losses"] == 0
    assert summary["coverage_at_target_risk_supported"] is True
    assert "Coverage at Target Risk" in render_markdown(summary)


def _row(generator, *, csrm, strongest):
    return {
        "dataset": "unit",
        "retriever": "r1",
        "generator": generator,
        "curves": {
            "csrm": [{"coverage": cov, "risk": risk} for cov, risk in csrm],
            "strongest_non_csrm": [{"coverage": cov, "risk": risk} for cov, risk in strongest],
        },
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
