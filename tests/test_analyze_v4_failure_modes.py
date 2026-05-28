import json

from experiments.analyze_v4_failure_modes import analyze_v4_failure_modes


def test_analyze_v4_failure_modes_writes_json_and_markdown(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    scored = tmp_path / "scored.jsonl"
    output_json = tmp_path / "analysis.json"
    output_md = tmp_path / "analysis.md"
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

    result = analyze_v4_failure_modes(
        raw,
        private,
        scored,
        output_json,
        output_md,
        seed=3,
        top_k=2,
    )

    assert "target" in result["metrics"]
    assert result["feature_gaps"]
    assert output_json.exists()
    assert "Case Gallery" in output_md.read_text(encoding="utf-8")


def _raw(orbit_id, group_id):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "query": "Where is Paris?",
        "candidate_answer": "France",
        "clean_evidence": [
            {"doc_id": orbit_id, "title": "Paris", "text": "Paris is in France.", "retrieval_score": 0.5}
        ],
        "perturbations": [
            {
                "query": "Where is Paris using altered evidence?",
                "candidate_answer": "France",
                "evidence": [
                    {"doc_id": orbit_id + "-p", "title": "Paris", "text": "Paris is a city.", "retrieval_score": 0.5}
                ],
            }
        ],
    }


def _private(orbit_id, group_id, label):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "label_answerable": label,
        "construction_type": "stable" if label else "fragile",
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
        "perturbations": [
            {
                "query": "Where is Paris using altered evidence?",
                "answer": "France",
                "label_answerable": label,
                "docs": [
                    {
                        "doc_id": orbit_id + "-p",
                        "text": "Paris is a city.",
                        "corm_score": support,
                        "support": support,
                        "conflict": 0.0,
                        "missing": 1.0 - support,
                    }
                ],
            }
        ],
    }


def _write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
