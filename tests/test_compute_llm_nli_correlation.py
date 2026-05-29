import json

from experiments.compute_llm_nli_correlation import (
    compute_llm_nli_correlation,
    render_markdown,
)


def test_compute_llm_nli_correlation_blocks_without_scores(tmp_path):
    nli = tmp_path / "nli.jsonl"
    nli.write_text("\n".join(json.dumps(row) for row in [_row("a", 0.1), _row("b", 0.9)]), encoding="utf-8")

    summary = compute_llm_nli_correlation(nli, tmp_path / "missing.jsonl")

    assert summary["status"] == "blocked"
    assert summary["blocker_reason"] == "missing_or_empty_llm_score_artifact"
    assert summary["nli_score_count"] == 2
    assert summary["ready_for_nli_llm_correlation_claim"] is False


def test_compute_llm_nli_correlation_reads_parsed_scores(tmp_path):
    nli = tmp_path / "nli.jsonl"
    llm = tmp_path / "llm.jsonl"
    nli.write_text(
        "\n".join(json.dumps(row) for row in [_row("a", 0.1), _row("b", 0.4), _row("c", 0.9)]),
        encoding="utf-8",
    )
    llm.write_text(
        "\n".join(
            json.dumps(row)
            for row in [
                {"orbit_id": "a", "answerable_score": 0.1},
                {"orbit_id": "b", "answerable_score": 0.5},
                {"orbit_id": "c", "answerable_score": 0.9},
            ]
        ),
        encoding="utf-8",
    )

    summary = compute_llm_nli_correlation(nli, llm, spearman_minimum=0.30)

    assert summary["status"] == "pass"
    assert summary["paired_count"] == 3
    assert summary["correlations"]["spearman"] == 1.0
    assert summary["ready_for_nli_llm_correlation_claim"] is True


def test_compute_llm_nli_correlation_reads_openai_batch_content(tmp_path):
    nli = tmp_path / "nli.jsonl"
    llm = tmp_path / "llm.jsonl"
    nli.write_text("\n".join(json.dumps(row) for row in [_row("a", 0.1), _row("b", 0.9)]), encoding="utf-8")
    llm.write_text(
        "\n".join(
            json.dumps(row)
            for row in [
                _batch_row("a", 0.2),
                _batch_row("b", 0.8),
            ]
        ),
        encoding="utf-8",
    )

    text = render_markdown(compute_llm_nli_correlation(nli, llm))

    assert "LLM/NLI Correlation Status" in text
    assert "Ready for NLI/LLM correlation claim: `True`" in text


def _row(orbit_id, support):
    return {
        "orbit_id": orbit_id,
        "split": "s",
        "clean": {
            "query": "q",
            "answer": "a",
            "label_answerable": True,
            "docs": [
                {
                    "doc_id": orbit_id,
                    "text": "evidence",
                    "corm_score": support,
                    "support": support,
                    "conflict": 0.0,
                    "missing": 0.0,
                }
            ],
        },
        "perturbations": [],
    }


def _batch_row(orbit_id, score):
    return {
        "custom_id": orbit_id,
        "response": {
            "body": {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "answerable_score": score,
                                    "label": "answerable",
                                    "rationale": "visible evidence",
                                }
                            )
                        }
                    }
                ]
            }
        },
    }
