import json

from csrm_rag.end2end import coverage_at_risk, evaluate_selective_policy, generate_answer
from experiments.run_end2end_selective_rag import run_end2end_selective_rag


def test_generate_answer_requires_answerability_for_correctness():
    raw = {
        "candidate_answer": "SUPPORTS",
        "query": "Determine whether this claim is supported or refuted: A is B.",
        "clean_evidence": [{"title": "A", "text": "A is B.", "retrieval_score": 1.0}],
        "perturbations": [],
    }
    private = {"label_answerable": False, "gold_answer": "SUPPORTS", "dataset": "fever"}

    generated = generate_answer(raw, private, "copy_candidate")

    assert generated.answer == "SUPPORTS"
    assert generated.correct is False


def test_selective_policy_reports_coverage_at_target_risk():
    metrics = evaluate_selective_policy([0.9, 0.8, 0.1], [True, False, True])

    assert metrics["accepted_error_at_30"]["accepted"] == 1
    assert metrics["coverage_at_risk_10"]["coverage"] == 1 / 3
    assert coverage_at_risk([0.2, 0.1], [False, False], 0.0)["coverage"] == 0.0


def test_run_end2end_selective_rag_smoke(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    scored = tmp_path / "scored.jsonl"
    output = tmp_path / "out.json"
    raw_rows = [
        _raw("o1", "SUPPORTS", 1.0),
        _raw("o2", "SUPPORTS", 0.1),
    ]
    private_rows = [
        _private("o1", True),
        _private("o2", False),
    ]
    scored_rows = [
        _scored("o1", True, 0.9),
        _scored("o2", False, 0.2),
    ]
    _write_jsonl(raw, raw_rows)
    _write_jsonl(private, private_rows)
    _write_jsonl(scored, scored_rows)

    result = run_end2end_selective_rag(
        raw,
        private,
        scored,
        output,
        generators=["copy_candidate", "lexical_guarded"],
    )

    assert result["n"] == 2
    assert result["results"]["copy_candidate"]["answer_accuracy"] == 0.5
    assert result["results"]["copy_candidate"]["methods"]["csrm"]["accepted_error_at_50"]["risk"] == 0.0
    assert output.exists()


def _raw(orbit_id, answer, retrieval_score):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": orbit_id,
        "dataset": "fever",
        "query": "Determine whether this claim is supported or refuted: A is B.",
        "candidate_answer": answer,
        "clean_evidence": [
            {
                "doc_id": "d1",
                "title": "A",
                "text": "A is B.",
                "rank": 0,
                "retrieval_score": retrieval_score,
            }
        ],
        "perturbations": [],
    }


def _private(orbit_id, label):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": orbit_id,
        "dataset": "fever",
        "label_answerable": label,
        "construction_type": "stable" if label else "missing",
        "label_source": "unit",
        "gold_answer": "SUPPORTS",
    }


def _scored(orbit_id, label, support):
    return {
        "orbit_id": orbit_id,
        "split": "unit",
        "clean": {
            "query": "q",
            "answer": "SUPPORTS",
            "label_answerable": label,
            "docs": [
                {
                    "doc_id": "d1",
                    "text": "A is B.",
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
