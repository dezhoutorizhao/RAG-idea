import json

from experiments.plot_end2end_risk_coverage_curves import (
    build_end2end_risk_coverage_curves,
    render_markdown,
    render_svg,
)
from experiments.run_end2end_retriever_generator_matrix_v4 import DatasetConfig


def test_build_end2end_risk_coverage_curves_reports_aggregate_and_svg(tmp_path):
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

    summary = build_end2end_risk_coverage_curves(
        [DatasetConfig("unit", raw, private, scored)],
        retrievers=["bm25_orbit_pool", "dense_hash_orbit_pool"],
        generators=["copy_candidate", "lexical_guarded"],
        coverages=[0.25, 0.50, 1.00],
    )

    assert summary["protocol_complete"] is True
    assert summary["row_count"] == 4
    assert summary["aggregate"]["coverage_count"] == 3
    assert "csrm" in summary["aggregate"]["method_curves"]
    assert "strongest_non_csrm" in summary["aggregate"]["method_curves"]
    assert len(summary["aggregate"]["csrm_vs_strongest_non_csrm"]) == 3
    assert "End-to-End Risk-Coverage Curves" in render_markdown(summary)
    svg = render_svg(summary)
    assert "<svg" in svg
    assert "csrm" in svg
    assert "strongest_non_csrm" in svg


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
