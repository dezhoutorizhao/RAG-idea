import json

from experiments.compare_equal_budget_thresholds_v4 import (
    DatasetConfig,
    compare_equal_budget_thresholds_v4,
    render_markdown,
)


def test_compare_equal_budget_thresholds_v4_uses_calibration_thresholds(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    scored = tmp_path / "scored.jsonl"
    raw_rows = []
    private_rows = []
    scored_rows = []
    for index in range(18):
        label = index % 2 == 0
        orbit_id = f"g{index}:{'stable' if label else 'fragile'}"
        group_id = f"g{index}"
        raw_rows.append(_raw(orbit_id, group_id))
        private_rows.append(_private(orbit_id, group_id, label))
        scored_rows.append(_scored(orbit_id, label, 0.90 if label else 0.10))
    _write_jsonl(raw, raw_rows)
    _write_jsonl(private, private_rows)
    _write_jsonl(scored, scored_rows)

    summary = compare_equal_budget_thresholds_v4(
        [DatasetConfig("unit", raw, private, scored)],
        seeds=[3],
        risk_targets=[0.20],
    )

    assert summary["shared_threshold_protocol_complete"] is True
    assert summary["dataset_count"] == 1
    seed_row = summary["datasets"][0]["per_seed"][0]
    assert seed_row["protocol_complete"] is True
    assert seed_row["method_count"] > 4
    assert all(row["calibration"]["selected_on_calibration"] for row in seed_row["threshold_rows"])
    assert "target_vs_strongest_baseline" in summary["aggregate"]

    text = render_markdown(summary)
    assert "Shared Calibration-Threshold" in text
    assert "csrm_calibrated_logistic" in text


def _raw(orbit_id, group_id):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "query": "Where is Paris?",
        "candidate_answer": "France",
        "clean_evidence": [{"doc_id": orbit_id, "text": "Paris is in France.", "retrieval_score": 0.5}],
        "perturbations": [],
    }


def _private(orbit_id, group_id, label):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "label_answerable": label,
    }


def _scored(orbit_id, label, support):
    return {
        "orbit_id": orbit_id,
        "split": "unit",
        "clean": {
            "query": "Where is Paris?",
            "answer": "France",
            "label_answerable": label,
            "docs": [
                {
                    "doc_id": orbit_id,
                    "text": "Paris is in France.",
                    "corm_score": support,
                    "support": support,
                    "conflict": 0.0,
                    "missing": 1.0 - support,
                }
            ],
        },
        "perturbations": [],
    }


def _write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
