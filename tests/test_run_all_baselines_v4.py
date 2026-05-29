import json

from experiments.run_all_baselines_v4 import run_all_baselines_v4


def test_run_all_baselines_v4_reports_strongest_non_csrm(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    scored = tmp_path / "scored.jsonl"
    output = tmp_path / "baselines.json"
    raw_rows = [_raw("g1:stable", "g1"), _raw("g1:fragile", "g1"), _raw("g2:stable", "g2"), _raw("g2:fragile", "g2")]
    private_rows = [
        _private("g1:stable", "g1", True),
        _private("g1:fragile", "g1", False),
        _private("g2:stable", "g2", True),
        _private("g2:fragile", "g2", False),
    ]
    scored_rows = [
        _scored("g1:stable", True, 0.9),
        _scored("g1:fragile", False, 0.2),
        _scored("g2:stable", True, 0.8),
        _scored("g2:fragile", False, 0.1),
    ]
    _write_jsonl(raw, raw_rows)
    _write_jsonl(private, private_rows)
    _write_jsonl(scored, scored_rows)

    result = run_all_baselines_v4(raw, private, scored, output)

    assert result["n"] == 4
    assert result["source_item_groups"] == 2
    assert "faithful_sure_multi" in result["methods"]
    assert "equal_budget_ensemble_logistic" in result["methods"]
    assert "calibrated_logistic_orbit" in result["methods"]
    assert "template_self_consistency" in result["methods"]
    assert result["strongest_non_csrm"]["by_aurc"]["method"] != "csrm_rule"
    assert result["strongest_non_csrm"]["by_risk_at_30"]["method"] != "csrm_rule"
    assert result["strongest_non_csrm"]["by_auroc"]["method"] != "csrm_rule"
    assert output.exists()


def _raw(orbit_id, group_id):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "query": "q",
        "candidate_answer": "a",
        "clean_evidence": [],
        "perturbations": [],
    }


def _private(orbit_id, group_id, label):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "label_answerable": label,
    }


def _scored(orbit_id, label, support):
    return {
        "orbit_id": orbit_id,
        "split": "unit",
        "clean": {
            "query": "q",
            "answer": "a",
            "label_answerable": label,
            "docs": [
                {
                    "doc_id": orbit_id,
                    "text": "text",
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
