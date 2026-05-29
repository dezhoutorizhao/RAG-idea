import json

from experiments.normalize_llm_judge_batch_responses import (
    normalize_llm_judge_batch_responses,
    render_markdown,
)


def _batch_row(custom_id: str, content: str) -> dict:
    return {
        "custom_id": custom_id,
        "response": {
            "body": {
                "id": f"chatcmpl-{custom_id}",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"content": content},
                    }
                ],
            }
        },
    }


def test_normalize_llm_judge_batch_responses_blocks_without_batch_output(tmp_path):
    summary = normalize_llm_judge_batch_responses(
        tmp_path / "missing.jsonl",
        tmp_path / "scores.jsonl",
    )

    assert summary["status"] == "blocked"
    assert summary["blocker_reason"] == "missing_or_empty_batch_output_artifact"
    assert summary["ready_for_nli_llm_correlation"] is False
    assert "missing_or_empty_batch_output_artifact" in render_markdown(summary)


def test_normalize_llm_judge_batch_responses_writes_scores(tmp_path):
    batch = tmp_path / "batch.jsonl"
    scores = tmp_path / "scores.jsonl"
    content = json.dumps(
        {
            "answerable_score": 0.82,
            "label": "answerable",
            "rationale": "visible evidence supports the answer",
        }
    )
    batch.write_text(json.dumps(_batch_row("orbit-1", content)) + "\n", encoding="utf-8")

    summary = normalize_llm_judge_batch_responses(batch, scores)
    rows = [json.loads(line) for line in scores.read_text(encoding="utf-8").splitlines()]

    assert summary["status"] == "pass"
    assert summary["parsed_score_count"] == 1
    assert summary["error_count"] == 0
    assert summary["ready_for_nli_llm_correlation"] is True
    assert rows == [
        {
            "answerable_score": 0.82,
            "custom_id": "orbit-1",
            "finish_reason": "stop",
            "label": "answerable",
            "orbit_id": "orbit-1",
            "rationale": "visible evidence supports the answer",
            "source_response_id": "chatcmpl-orbit-1",
        }
    ]


def test_normalize_llm_judge_batch_responses_reports_parse_errors(tmp_path):
    batch = tmp_path / "batch.jsonl"
    scores = tmp_path / "scores.jsonl"
    bad_content = json.dumps({"answerable_score": 1.5, "label": "answerable"})
    batch.write_text(json.dumps(_batch_row("orbit-1", bad_content)) + "\n", encoding="utf-8")

    summary = normalize_llm_judge_batch_responses(batch, scores)

    assert summary["status"] == "fail"
    assert summary["parsed_score_count"] == 0
    assert summary["error_count"] == 1
    assert summary["sample_errors"][0]["orbit_id"] == "orbit-1"
    assert "parse_failed" in summary["sample_errors"][0]["error"]
