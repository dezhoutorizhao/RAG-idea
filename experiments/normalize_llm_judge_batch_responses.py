#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag.verifiers.llm_judge import parse_llm_judge_response


DEFAULT_BATCH_OUTPUT = Path("results/llm_judge_nli_probe_batch_output_20260529.jsonl")
DEFAULT_SCORE_OUTPUT = Path("results/llm_judge_nli_probe_scores_20260529.jsonl")
DEFAULT_STATUS_JSON = Path("results/llm_judge_nli_probe_score_status_20260529.json")
DEFAULT_STATUS_MD = Path("results/llm_judge_nli_probe_score_status_20260529.md")


def normalize_llm_judge_batch_responses(
    batch_output_jsonl: Path,
    score_output_jsonl: Path,
    *,
    require_all_success: bool = True,
) -> dict[str, Any]:
    if not batch_output_jsonl.exists() or batch_output_jsonl.stat().st_size == 0:
        return _summary(
            batch_output_jsonl,
            score_output_jsonl,
            status="blocked",
            blocker_reason="missing_or_empty_batch_output_artifact",
            request_count=0,
            parsed_score_count=0,
            error_count=0,
            require_all_success=require_all_success,
        )

    parsed_rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line_no, row in _read_jsonl_with_line_numbers(batch_output_jsonl):
        orbit_id = _orbit_id(row)
        if not orbit_id:
            errors.append({"line_no": line_no, "error": "missing_orbit_id_or_custom_id"})
            continue
        if orbit_id in seen:
            errors.append({"line_no": line_no, "orbit_id": orbit_id, "error": "duplicate_orbit_id"})
            continue
        seen.add(orbit_id)

        content = _openai_batch_content(row)
        if content is None:
            errors.append({"line_no": line_no, "orbit_id": orbit_id, "error": _response_error(row)})
            continue

        try:
            parsed = parse_llm_judge_response(content)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            errors.append({"line_no": line_no, "orbit_id": orbit_id, "error": f"parse_failed:{exc}"})
            continue

        parsed_rows.append(
            {
                "orbit_id": orbit_id,
                "custom_id": row.get("custom_id") or orbit_id,
                "answerable_score": parsed["answerable_score"],
                "label": parsed["label"],
                "rationale": parsed["rationale"],
                "source_response_id": _response_id(row),
                "finish_reason": _finish_reason(row),
            }
        )

    score_output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    score_output_jsonl.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in parsed_rows)
        + ("\n" if parsed_rows else ""),
        encoding="utf-8",
    )
    status = "pass" if parsed_rows and (not require_all_success or not errors) else "fail"
    return _summary(
        batch_output_jsonl,
        score_output_jsonl,
        status=status,
        blocker_reason=None,
        request_count=len(parsed_rows) + len(errors),
        parsed_score_count=len(parsed_rows),
        error_count=len(errors),
        require_all_success=require_all_success,
        errors=errors[:20],
    )


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# LLM Judge NLI Score Normalization",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Status: `{summary['status']}`",
        f"Batch output: `{summary['batch_output_jsonl']}`",
        f"Score output: `{summary['score_output_jsonl']}`",
        f"Rows seen: `{summary['request_count']}`",
        f"Parsed scores: `{summary['parsed_score_count']}`",
        f"Errors: `{summary['error_count']}`",
        f"Require all success: `{summary['require_all_success']}`",
        f"Ready for correlation: `{summary['ready_for_nli_llm_correlation']}`",
        "",
    ]
    if summary["status"] == "blocked":
        lines.extend(["## Blocker", "", f"- Reason: `{summary['blocker_reason']}`.", ""])
    elif summary["error_count"]:
        lines.extend(["## First Errors", "", "| Line | Orbit | Error |", "|---:|---|---|"])
        for item in summary["sample_errors"]:
            lines.append(
                f"| {item.get('line_no')} | {item.get('orbit_id', '')} | `{item.get('error')}` |"
            )
        lines.append("")
    lines.extend(["## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _summary(
    batch_output_jsonl: Path,
    score_output_jsonl: Path,
    *,
    status: str,
    blocker_reason: str | None,
    request_count: int,
    parsed_score_count: int,
    error_count: int,
    require_all_success: bool,
    errors: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    ready = status == "pass" and parsed_score_count > 0 and error_count == 0
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "batch_output_jsonl": str(batch_output_jsonl),
        "score_output_jsonl": str(score_output_jsonl),
        "request_count": request_count,
        "parsed_score_count": parsed_score_count,
        "error_count": error_count,
        "require_all_success": require_all_success,
        "ready_for_nli_llm_correlation": ready,
        "status": status,
        "blocker_reason": blocker_reason,
        "sample_errors": errors or [],
        "claim_policy": (
            "This normalizes API-backed LLM judge batch responses into answerable-score "
            "rows for the paired NLI probe. It is an ingestion artifact only; the "
            "correlation claim is evaluated separately."
        ),
    }


def _read_jsonl_with_line_numbers(path: Path) -> list[tuple[int, dict[str, Any]]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            try:
                rows.append((line_no, json.loads(line)))
            except json.JSONDecodeError as exc:
                rows.append((line_no, {"error": f"json_decode_failed:{exc}"}))
    return rows


def _orbit_id(row: dict[str, Any]) -> str | None:
    metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    return row.get("orbit_id") or row.get("custom_id") or metadata.get("orbit_id")


def _openai_batch_content(row: dict[str, Any]) -> str | None:
    response = row.get("response")
    if not isinstance(response, dict):
        return None
    body = response.get("body")
    if not isinstance(body, dict):
        return None
    choices = body.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    choice0 = choices[0]
    message = choice0.get("message") if isinstance(choice0, dict) else None
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    return content if isinstance(content, str) else None


def _response_error(row: dict[str, Any]) -> str:
    if "error" in row:
        return f"api_error:{row['error']}"
    response = row.get("response")
    if isinstance(response, dict) and "error" in response:
        return f"api_error:{response['error']}"
    return "missing_response_content"


def _response_id(row: dict[str, Any]) -> str | None:
    response = row.get("response")
    if not isinstance(response, dict):
        return None
    body = response.get("body")
    if not isinstance(body, dict):
        return None
    value = body.get("id")
    return str(value) if value is not None else None


def _finish_reason(row: dict[str, Any]) -> str | None:
    response = row.get("response")
    if not isinstance(response, dict):
        return None
    body = response.get("body")
    if not isinstance(body, dict):
        return None
    choices = body.get("choices")
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        return None
    value = choices[0].get("finish_reason")
    return str(value) if value is not None else None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-output-jsonl", type=Path, default=DEFAULT_BATCH_OUTPUT)
    parser.add_argument("--score-output-jsonl", type=Path, default=DEFAULT_SCORE_OUTPUT)
    parser.add_argument("--status-json", type=Path, default=DEFAULT_STATUS_JSON)
    parser.add_argument("--status-md", type=Path, default=DEFAULT_STATUS_MD)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    summary = normalize_llm_judge_batch_responses(
        args.batch_output_jsonl,
        args.score_output_jsonl,
        require_all_success=not args.allow_partial,
    )
    _write_json(args.status_json, summary)
    args.status_md.parent.mkdir(parents=True, exist_ok=True)
    args.status_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
