import json

from experiments.run_end2end_retriever_generator_matrix_v4 import (
    DatasetConfig,
    render_markdown,
    run_end2end_retriever_generator_matrix_v4,
)


def test_run_end2end_retriever_generator_matrix_v4_reports_two_by_two(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    scored = tmp_path / "scored.jsonl"
    raw_rows = []
    private_rows = []
    scored_rows = []
    for index in range(8):
        label = index % 2 == 0
        orbit_id = f"g{index}:{'stable' if label else 'fragile'}"
        raw_rows.append(_raw(orbit_id, f"g{index}", "Paris"))
        private_rows.append(_private(orbit_id, f"g{index}", label, "Paris"))
        scored_rows.append(_scored(orbit_id, label, "Paris", 0.85 if label else 0.15))
    _write_jsonl(raw, raw_rows)
    _write_jsonl(private, private_rows)
    _write_jsonl(scored, scored_rows)

    summary = run_end2end_retriever_generator_matrix_v4(
        [DatasetConfig("unit", raw, private, scored)],
        retrievers=["bm25_orbit_pool", "dense_hash_orbit_pool"],
        generators=["copy_candidate", "lexical_guarded"],
    )

    assert summary["protocol_complete"] is True
    assert summary["row_count"] == 4
    assert {row["retriever"] for row in summary["rows"]} == {"bm25_orbit_pool", "dense_hash_orbit_pool"}
    assert {row["generator"] for row in summary["rows"]} == {"copy_candidate", "lexical_guarded"}
    assert "risk30_wins" in summary["aggregate"]
    assert "V4 End-to-End Retriever-Generator Matrix" in render_markdown(summary)


def _raw(orbit_id, group_id, answer):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "query": "Where is Paris?",
        "candidate_answer": answer,
        "clean_evidence": [
            {"doc_id": f"{orbit_id}:a", "title": "Paris", "text": "Paris is in France.", "retrieval_score": 0.5}
        ],
        "perturbations": [
            {
                "query": "Where is Paris located?",
                "candidate_answer": answer,
                "evidence": [
                    {
                        "doc_id": f"{orbit_id}:b",
                        "title": "France",
                        "text": "France contains Paris.",
                        "retrieval_score": 0.4,
                    }
                ],
            }
        ],
    }


def _private(orbit_id, group_id, label, answer):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "label_answerable": label,
        "gold_answer": answer,
    }


def _scored(orbit_id, label, answer, support):
    return {
        "orbit_id": orbit_id,
        "split": "unit",
        "clean": {
            "query": "Where is Paris?",
            "answer": answer,
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
