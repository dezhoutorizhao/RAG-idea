import json

from experiments.compare_methods import compare_methods


def _record(orbit_id, label, clean_support, pert_support, support_key="gold"):
    return {
        "orbit_id": orbit_id,
        "clean": {
            "query": "q",
            "answer": "a",
            "label_answerable": True,
            "split": "unit",
            "metadata": {"support_key": "gold"},
            "docs": [
                {
                    "doc_id": "clean",
                    "text": "clean",
                    "corm_score": 0.9,
                    "support": clean_support,
                    "conflict": 0.0,
                    "missing": 0.0,
                }
            ],
        },
        "perturbations": [
            {
                "query": "p",
                "answer": "a",
                "label_answerable": label,
                "split": "unit",
                "metadata": {"support_key": support_key},
                "docs": [
                    {
                        "doc_id": "pert",
                        "text": "pert",
                        "corm_score": 0.8,
                        "support": pert_support,
                        "conflict": 0.0,
                        "missing": 0.0,
                    }
                ],
            }
        ],
    }


def test_compare_methods_reports_paired_deltas(tmp_path):
    path = tmp_path / "orbits.jsonl"
    rows = [
        _record("pos1", True, 0.9, 0.9, "gold"),
        _record("pos2", True, 0.8, 0.8, "gold"),
        _record("neg1", False, 0.9, 0.8, "false"),
        _record("neg2", False, 0.8, 0.7, "false"),
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    result = compare_methods(path, "csrm", ["naive_orbit_average"], 10, 1)

    comp = result["comparisons"]["naive_orbit_average"]
    assert "risk_at_30_reduction" in comp["point"]
    assert comp["bootstrap_ci"]["risk_at_30_reduction"] is not None
