import json

from experiments.materialize_llm_judge_requests_nli_probe import (
    materialize_llm_judge_requests_nli_probe,
    render_markdown,
)


def test_nli_probe_request_pack_strips_private_fields(tmp_path):
    input_jsonl = tmp_path / "nli.jsonl"
    output_jsonl = tmp_path / "requests.jsonl"
    input_jsonl.write_text(json.dumps(_record()) + "\n", encoding="utf-8")

    summary = materialize_llm_judge_requests_nli_probe(
        input_jsonl,
        output_jsonl,
        model="judge-model",
    )

    assert summary["request_count"] == 1
    assert summary["request_pack_ready"] is True
    assert summary["paired_to_nli_probe"] is True
    assert summary["score_artifact_ready"] is False

    request = json.loads(output_jsonl.read_text(encoding="utf-8").splitlines()[0])
    prompt = request["body"]["messages"][1]["content"]
    assert "Visible query" not in prompt
    assert "claim?" in prompt
    assert "visible evidence" in prompt
    for forbidden in [
        "expected_label_answerable",
        "auditor_label_answerable",
        "label_answerable",
        "support_key",
        "corm_score",
        "nli_model",
    ]:
        assert forbidden not in prompt


def test_nli_probe_request_pack_markdown_reports_correlation_status(tmp_path):
    input_jsonl = tmp_path / "nli.jsonl"
    output_jsonl = tmp_path / "requests.jsonl"
    input_jsonl.write_text(json.dumps(_record()) + "\n", encoding="utf-8")

    text = render_markdown(
        materialize_llm_judge_requests_nli_probe(input_jsonl, output_jsonl, model="judge-model")
    )

    assert "LLM Judge Requests Paired To NLI Probe" in text
    assert "Ready for NLI/LLM correlation: `False`" in text


def _record():
    return {
        "orbit_id": "orbit-1",
        "split": "split-a",
        "expected_label_answerable": False,
        "auditor_label_answerable": None,
        "answer": "answer",
        "clean": {
            "query": "claim?",
            "label_answerable": True,
            "support_key": "hidden",
            "docs": [
                {
                    "doc_id": "d1",
                    "title": "Doc",
                    "rank": 0,
                    "text": "visible evidence",
                    "corm_score": 0.9,
                    "nli_model": "nli",
                }
            ],
        },
        "perturbations": [
            {
                "query": "perturbed?",
                "label_answerable": False,
                "support_key": "hidden2",
                "docs": [
                    {
                        "doc_id": "d2",
                        "title": "Doc 2",
                        "rank": 0,
                        "text": "counterfactual evidence",
                    }
                ],
            }
        ],
    }
