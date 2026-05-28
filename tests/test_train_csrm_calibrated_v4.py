import json

from experiments.train_csrm_calibrated_v4 import train_csrm_calibrated_v4


def test_train_csrm_calibrated_v4_outputs_group_split_metrics(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    scored = tmp_path / "scored.jsonl"
    output = tmp_path / "calibrated.json"
    raw_rows = []
    private_rows = []
    scored_rows = []
    for index in range(12):
        label = index % 2 == 0
        orbit_id = f"g{index}:{'stable' if label else 'fragile'}"
        group_id = f"g{index}"
        raw_rows.append(_raw(orbit_id, group_id))
        private_rows.append(_private(orbit_id, group_id, label))
        scored_rows.append(_scored(orbit_id, label, 0.85 if label else 0.15))
    _write_jsonl(raw, raw_rows)
    _write_jsonl(private, private_rows)
    _write_jsonl(scored, scored_rows)

    result = train_csrm_calibrated_v4(raw, private, scored, output, seeds=[3], risk_target=0.25)

    assert result["n"] == 12
    assert "csrm_calibrated_logistic" in result["aggregate"]
    assert result["per_seed"][0]["split_sizes"]["test"] > 0
    test_metrics = result["per_seed"][0]["methods"]["csrm_calibrated_logistic"]["test"]
    assert "brier" in test_metrics
    assert "selected_risk" in test_metrics
    assert output.exists()


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
