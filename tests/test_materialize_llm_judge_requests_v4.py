import json

from experiments.materialize_llm_judge_requests_v4 import (
    DatasetConfig,
    materialize_llm_judge_requests_v4,
    render_markdown,
)


def test_materialize_llm_judge_requests_v4_writes_equal_input_pack(tmp_path):
    raw = tmp_path / "raw.jsonl"
    raw.write_text(json.dumps(_raw("o1")) + "\n" + json.dumps(_raw("o2")) + "\n", encoding="utf-8")
    output = tmp_path / "requests.jsonl"

    summary = materialize_llm_judge_requests_v4(
        [DatasetConfig("unit", raw)],
        output,
        model="unit-model",
    )

    lines = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    assert summary["request_count"] == 2
    assert summary["request_pack_ready"] is True
    assert summary["score_artifact_ready"] is False
    assert lines[0]["body"]["model"] == "unit-model"
    assert "label_answerable" not in lines[0]["body"]["messages"][1]["content"]
    assert "LLM Judge V4 Request Pack" in render_markdown(summary)


def _raw(orbit_id):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": orbit_id,
        "dataset": "unit",
        "query": "Where is Paris?",
        "candidate_answer": "France",
        "clean_evidence": [{"doc_id": "d1", "title": "Paris", "text": "Paris is in France.", "rank": 0}],
        "perturbations": [
            {
                "query": "Where is Paris located?",
                "candidate_answer": "France",
                "evidence": [{"doc_id": "d2", "title": "France", "text": "France contains Paris.", "rank": 0}],
            }
        ],
    }
