#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


DEFAULT_REQUESTS = Path("results/llm_judge_nli_probe_requests_20260529.jsonl")
DEFAULT_BATCH_OUTPUT = Path("results/llm_judge_nli_probe_batch_output_20260529.jsonl")
DEFAULT_STATUS_JSON = Path("results/llm_judge_nli_probe_batch_run_status_20260529.json")
DEFAULT_STATUS_MD = Path("results/llm_judge_nli_probe_batch_run_status_20260529.md")
DEFAULT_ENDPOINT = "/v1/chat/completions"
DEFAULT_COMPLETION_WINDOW = "24h"
DEFAULT_BASE_URL = "https://api.openai.com/v1"


class BatchClient(Protocol):
    def upload_batch_file(self, path: Path) -> dict[str, Any]:
        ...

    def create_batch(
        self,
        *,
        input_file_id: str,
        endpoint: str,
        completion_window: str,
        metadata: dict[str, str],
    ) -> dict[str, Any]:
        ...

    def retrieve_batch(self, batch_id: str) -> dict[str, Any]:
        ...

    def download_file_content(self, file_id: str) -> bytes:
        ...


def manage_openai_llm_judge_batch(
    request_jsonl: Path,
    batch_output_jsonl: Path,
    *,
    action: str = "preflight",
    batch_id: str | None = None,
    api_key: str | None = None,
    client: BatchClient | None = None,
    endpoint: str = DEFAULT_ENDPOINT,
    completion_window: str = DEFAULT_COMPLETION_WINDOW,
) -> dict[str, Any]:
    request_status = _validate_batch_requests(request_jsonl, endpoint=endpoint)
    api_key_ready = bool(api_key)
    base = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "request_jsonl": str(request_jsonl),
        "batch_output_jsonl": str(batch_output_jsonl),
        "endpoint": endpoint,
        "completion_window": completion_window,
        "api_key_ready": api_key_ready,
        "request_status": request_status,
        "claim_policy": (
            "This manages API-backed LLM judge batch execution for the paired NLI probe. "
            "Preflight performs no network calls. Submit/retrieve require an API key and "
            "produce execution metadata only; answerable-score normalization and correlation "
            "are evaluated by downstream artifacts."
        ),
    }
    if not request_status["valid"]:
        return _with_status(base, "fail", "invalid_request_jsonl")
    if action == "preflight":
        if not api_key_ready:
            return _with_status(base, "blocked", "missing_openai_api_key")
        return _with_status(base, "ready_to_submit", None)

    if action not in {"submit", "retrieve"}:
        raise ValueError("action must be one of preflight, submit, retrieve")
    if not api_key_ready and client is None:
        return _with_status(base, "blocked", "missing_openai_api_key")

    active_client = client or OpenAIBatchClient(api_key=api_key or "")
    if action == "submit":
        uploaded = active_client.upload_batch_file(request_jsonl)
        file_id = uploaded.get("id")
        if not file_id:
            return _with_status(base | {"file_upload": uploaded}, "fail", "missing_uploaded_file_id")
        batch = active_client.create_batch(
            input_file_id=str(file_id),
            endpoint=endpoint,
            completion_window=completion_window,
            metadata={"artifact": "llm_judge_nli_probe", "source": request_jsonl.name},
        )
        return _with_status(
            base | {"file_upload": uploaded, "batch": batch, "batch_id": batch.get("id")},
            "submitted",
            None,
        )

    if not batch_id:
        return _with_status(base, "blocked", "missing_batch_id")
    batch = active_client.retrieve_batch(batch_id)
    output_file_id = batch.get("output_file_id")
    downloaded = False
    if batch.get("status") == "completed" and output_file_id:
        batch_output_jsonl.parent.mkdir(parents=True, exist_ok=True)
        batch_output_jsonl.write_bytes(active_client.download_file_content(str(output_file_id)))
        downloaded = True
    status = "completed" if downloaded else str(batch.get("status") or "unknown")
    blocker = None if downloaded else _retrieve_blocker(batch)
    return _with_status(
        base
        | {
            "batch": batch,
            "batch_id": batch_id,
            "output_file_id": output_file_id,
            "output_downloaded": downloaded,
        },
        status,
        blocker,
    )


def render_markdown(summary: dict[str, Any]) -> str:
    request = summary["request_status"]
    lines = [
        "# LLM Judge NLI OpenAI Batch Run Status",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Action: `{summary['action']}`",
        f"Status: `{summary['status']}`",
        f"Blocker: `{summary.get('blocker_reason')}`",
        f"API key ready: `{summary['api_key_ready']}`",
        f"Request file: `{summary['request_jsonl']}`",
        f"Request count: `{request['request_count']}`",
        f"Request file valid: `{request['valid']}`",
        f"Endpoint: `{summary['endpoint']}`",
        f"Completion window: `{summary['completion_window']}`",
        f"Batch output: `{summary['batch_output_jsonl']}`",
        "",
    ]
    if request["errors"]:
        lines.extend(["## Request Errors", "", "| Line | Error |", "|---:|---|"])
        for item in request["errors"][:20]:
            lines.append(f"| {item.get('line_no')} | `{item.get('error')}` |")
        lines.append("")
    if "batch" in summary:
        batch = summary["batch"]
        lines.extend(
            [
                "## Batch",
                "",
                f"- Batch id: `{summary.get('batch_id')}`.",
                f"- Batch status: `{batch.get('status')}`.",
                f"- Output file id: `{batch.get('output_file_id')}`.",
                f"- Output downloaded: `{summary.get('output_downloaded')}`.",
                "",
            ]
        )
    lines.extend(["## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


class OpenAIBatchClient:
    def __init__(self, *, api_key: str, base_url: str = DEFAULT_BASE_URL) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def upload_batch_file(self, path: Path) -> dict[str, Any]:
        boundary = "----csrm" + uuid.uuid4().hex
        body = _multipart_form_data(
            boundary,
            fields={"purpose": "batch"},
            files={"file": path},
        )
        return self._request_json(
            "POST",
            "/files",
            body=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )

    def create_batch(
        self,
        *,
        input_file_id: str,
        endpoint: str,
        completion_window: str,
        metadata: dict[str, str],
    ) -> dict[str, Any]:
        return self._request_json(
            "POST",
            "/batches",
            json_body={
                "input_file_id": input_file_id,
                "endpoint": endpoint,
                "completion_window": completion_window,
                "metadata": metadata,
            },
        )

    def retrieve_batch(self, batch_id: str) -> dict[str, Any]:
        return self._request_json("GET", f"/batches/{batch_id}")

    def download_file_content(self, file_id: str) -> bytes:
        return self._request_bytes("GET", f"/files/{file_id}/content")

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        body: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        payload = body
        extra_headers = dict(headers or {})
        if json_body is not None:
            payload = json.dumps(json_body).encode("utf-8")
            extra_headers["Content-Type"] = "application/json"
        data = self._request_bytes(method, path, body=payload, headers=extra_headers)
        return json.loads(data.decode("utf-8"))

    def _request_bytes(
        self,
        method: str,
        path: str,
        *,
        body: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> bytes:
        request = urllib.request.Request(
            self.base_url + path,
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                **(headers or {}),
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI API request failed: HTTP {exc.code}: {detail}") from exc


def _validate_batch_requests(path: Path, *, endpoint: str) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    custom_ids: set[str] = set()
    models: set[str] = set()
    request_count = 0
    if not path.exists() or path.stat().st_size == 0:
        return _request_status(path, 0, [], [], valid=False, errors=[{"line_no": 0, "error": "missing_or_empty_request_jsonl"}])
    with path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            request_count += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append({"line_no": line_no, "error": f"json_decode_failed:{exc}"})
                continue
            custom_id = row.get("custom_id")
            if not custom_id:
                errors.append({"line_no": line_no, "error": "missing_custom_id"})
            elif custom_id in custom_ids:
                errors.append({"line_no": line_no, "error": f"duplicate_custom_id:{custom_id}"})
            else:
                custom_ids.add(str(custom_id))
            if row.get("method") != "POST":
                errors.append({"line_no": line_no, "error": "method_must_be_POST"})
            if row.get("url") != endpoint:
                errors.append({"line_no": line_no, "error": f"unexpected_url:{row.get('url')}"})
            body = row.get("body")
            if not isinstance(body, dict):
                errors.append({"line_no": line_no, "error": "missing_body"})
                continue
            model = body.get("model")
            if not model:
                errors.append({"line_no": line_no, "error": "missing_model"})
            else:
                models.add(str(model))
            if body.get("stream"):
                errors.append({"line_no": line_no, "error": "streaming_not_supported_for_batch"})
    if len(models) > 1:
        errors.append({"line_no": 0, "error": "multiple_models_in_request_file"})
    return _request_status(path, request_count, sorted(custom_ids), sorted(models), valid=not errors, errors=errors)


def _request_status(
    path: Path,
    request_count: int,
    custom_ids: list[str],
    models: list[str],
    *,
    valid: bool,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else 0,
        "request_count": request_count,
        "unique_custom_id_count": len(custom_ids),
        "models": models,
        "valid": valid,
        "errors": errors[:50],
    }


def _with_status(payload: dict[str, Any], status: str, blocker_reason: str | None) -> dict[str, Any]:
    payload["status"] = status
    payload["blocker_reason"] = blocker_reason
    payload["ready_for_batch_submission"] = status == "ready_to_submit"
    payload["ready_for_score_normalization"] = status == "completed" and Path(payload["batch_output_jsonl"]).exists()
    return payload


def _retrieve_blocker(batch: dict[str, Any]) -> str:
    status = str(batch.get("status") or "unknown")
    if status in {"failed", "expired", "cancelled"}:
        return "batch_terminal_without_output"
    return "batch_not_completed_or_output_missing"


def _multipart_form_data(boundary: str, *, fields: dict[str, str], files: dict[str, Path]) -> bytes:
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    for name, path in files.items():
        filename = path.name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    f'Content-Disposition: form-data; name="{name}"; '
                    f'filename="{filename}"\r\n'
                ).encode("utf-8"),
                f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
                path.read_bytes(),
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-jsonl", type=Path, default=DEFAULT_REQUESTS)
    parser.add_argument("--batch-output-jsonl", type=Path, default=DEFAULT_BATCH_OUTPUT)
    parser.add_argument("--status-json", type=Path, default=DEFAULT_STATUS_JSON)
    parser.add_argument("--status-md", type=Path, default=DEFAULT_STATUS_MD)
    parser.add_argument("--action", choices=["preflight", "submit", "retrieve"], default="preflight")
    parser.add_argument("--batch-id")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--completion-window", default=DEFAULT_COMPLETION_WINDOW)
    args = parser.parse_args()

    summary = manage_openai_llm_judge_batch(
        args.request_jsonl,
        args.batch_output_jsonl,
        action=args.action,
        batch_id=args.batch_id,
        api_key=os.environ.get("OPENAI_API_KEY"),
        endpoint=args.endpoint,
        completion_window=args.completion_window,
    )
    _write_json(args.status_json, summary)
    args.status_md.parent.mkdir(parents=True, exist_ok=True)
    args.status_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if summary["status"] in {"fail"}:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
