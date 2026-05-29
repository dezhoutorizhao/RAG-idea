import json

from experiments.manage_openai_llm_judge_batch import (
    manage_openai_llm_judge_batch,
    render_markdown,
)


class FakeClient:
    def __init__(self):
        self.uploaded = False
        self.created = False
        self.retrieved = False

    def upload_batch_file(self, path):
        self.uploaded = True
        assert path.exists()
        return {"id": "file-batch"}

    def create_batch(self, *, input_file_id, endpoint, completion_window, metadata):
        self.created = True
        assert input_file_id == "file-batch"
        assert endpoint == "/v1/chat/completions"
        assert completion_window == "24h"
        assert metadata["artifact"] == "llm_judge_nli_probe"
        return {"id": "batch-1", "status": "validating"}

    def retrieve_batch(self, batch_id):
        self.retrieved = True
        assert batch_id == "batch-1"
        return {"id": "batch-1", "status": "completed", "output_file_id": "file-output"}

    def download_file_content(self, file_id):
        assert file_id == "file-output"
        return b'{"custom_id":"orbit-1","response":{"body":{"choices":[]}}}\n'


def test_manage_openai_llm_judge_batch_preflight_blocks_without_api_key(tmp_path):
    requests = tmp_path / "requests.jsonl"
    requests.write_text(json.dumps(_request_row("orbit-1")) + "\n", encoding="utf-8")

    summary = manage_openai_llm_judge_batch(
        requests,
        tmp_path / "batch_output.jsonl",
        action="preflight",
        api_key=None,
    )

    assert summary["status"] == "blocked"
    assert summary["blocker_reason"] == "missing_openai_api_key"
    assert summary["request_status"]["valid"] is True
    assert summary["request_status"]["request_count"] == 1
    assert "missing_openai_api_key" in render_markdown(summary)


def test_manage_openai_llm_judge_batch_preflight_fails_invalid_requests(tmp_path):
    requests = tmp_path / "requests.jsonl"
    requests.write_text(json.dumps({"custom_id": "orbit-1", "method": "GET"}) + "\n", encoding="utf-8")

    summary = manage_openai_llm_judge_batch(
        requests,
        tmp_path / "batch_output.jsonl",
        action="preflight",
        api_key="sk-test",
    )

    assert summary["status"] == "fail"
    assert summary["blocker_reason"] == "invalid_request_jsonl"
    assert summary["request_status"]["valid"] is False


def test_manage_openai_llm_judge_batch_submit_uses_client(tmp_path):
    requests = tmp_path / "requests.jsonl"
    requests.write_text(json.dumps(_request_row("orbit-1")) + "\n", encoding="utf-8")
    client = FakeClient()

    summary = manage_openai_llm_judge_batch(
        requests,
        tmp_path / "batch_output.jsonl",
        action="submit",
        api_key="sk-test",
        client=client,
    )

    assert client.uploaded is True
    assert client.created is True
    assert summary["status"] == "submitted"
    assert summary["batch_id"] == "batch-1"


def test_manage_openai_llm_judge_batch_retrieve_downloads_output(tmp_path):
    requests = tmp_path / "requests.jsonl"
    output = tmp_path / "batch_output.jsonl"
    requests.write_text(json.dumps(_request_row("orbit-1")) + "\n", encoding="utf-8")
    client = FakeClient()

    summary = manage_openai_llm_judge_batch(
        requests,
        output,
        action="retrieve",
        batch_id="batch-1",
        api_key="sk-test",
        client=client,
    )

    assert client.retrieved is True
    assert summary["status"] == "completed"
    assert summary["output_downloaded"] is True
    assert output.read_text(encoding="utf-8").startswith('{"custom_id"')


def _request_row(custom_id):
    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4.1-mini",
            "messages": [{"role": "user", "content": "judge"}],
        },
    }
