import csv
import json

from experiments.build_clean_sufficiency_misleading_figure import (
    build_clean_sufficiency_misleading_figure,
)


def test_build_clean_sufficiency_misleading_figure_outputs_artifacts(tmp_path):
    scored = tmp_path / "demo.constant.textonly_scored.jsonl"
    rows = [
        _row("a", True, 0.8, 0.3, 0.6),
        _row("b", False, 0.9, 0.2, 0.5),
        _row("c", False, 0.1, 0.1, 0.1),
    ]
    scored.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    output_csv = tmp_path / "figure.csv"
    output_json = tmp_path / "summary.json"
    output_svg = tmp_path / "figure.svg"
    output_md = tmp_path / "figure.md"

    summary = build_clean_sufficiency_misleading_figure(
        [scored],
        output_csv,
        output_json,
        output_svg,
        output_md,
        bins=5,
    )

    assert summary["row_count"] == 3
    assert summary["failure_count"] == 2
    assert summary["high_sufficiency_failure"]["clean_sufficiency"]["threshold"] == 0.8
    assert summary["high_sufficiency_failure"]["clean_sufficiency"]["n"] == 2
    assert summary["high_sufficiency_failure"]["clean_sufficiency"]["failures"] == 1
    assert "not human-adjudicated" in summary["claim_boundary"]
    assert "<svg" in output_svg.read_text(encoding="utf-8")
    assert "Clean Sufficiency Misleading Diagnostic" in output_md.read_text(encoding="utf-8")
    with output_csv.open(encoding="utf-8") as handle:
        assert len(list(csv.DictReader(handle))) == 15


def test_build_clean_sufficiency_misleading_figure_rejects_missing_labels(tmp_path):
    scored = tmp_path / "demo.constant.textonly_scored.jsonl"
    row = _row("a", True, 0.8, 0.3, 0.6)
    row["clean"].pop("label_answerable")
    scored.write_text(json.dumps(row), encoding="utf-8")

    try:
        build_clean_sufficiency_misleading_figure(
            [scored],
            tmp_path / "figure.csv",
            tmp_path / "summary.json",
            tmp_path / "figure.svg",
            tmp_path / "figure.md",
            bins=5,
        )
    except ValueError as exc:
        assert "missing clean.label_answerable" in str(exc)
    else:
        raise AssertionError("expected missing-label ValueError")


def _row(orbit_id, label, clean, worst, mean):
    return {
        "orbit_id": orbit_id,
        "split": "demo",
        "clean": {"label_answerable": label},
        "metadata": {
            "textonly_v4": {
                "clean_sufficiency": clean,
                "worst_sufficiency": worst,
                "mean_sufficiency": mean,
            }
        },
    }
