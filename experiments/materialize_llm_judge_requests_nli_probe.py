#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
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

from csrm_rag.verifiers.llm_judge import build_llm_judge_request


DEFAULT_INPUT = Path("results/audit_sample_paper_1000_v3_nli_set.jsonl")
DEFAULT_OUTPUT_JSONL = Path("results/llm_judge_nli_probe_requests_20260529.jsonl")
DEFAULT_OUTPUT_JSON = Path("results/llm_judge_nli_probe_request_status_20260529.json")
DEFAULT_OUTPUT_MD = Path("results/llm_judge_nli_probe_request_status_20260529.md")
DEFAULT_SCORE_ARTIFACT = Path("results/llm_judge_nli_probe_scores_20260529.jsonl")


def materialize_llm_judge_requests_nli_probe(
    input_jsonl: Path,
    output_jsonl: Path,
    *,
    model: str,
    max_docs_per_set: int = 6,
    score_artifact: Path = DEFAULT_SCORE_ARTIFACT,
) -> dict[str, Any]:
    rows = []
    split_counts: dict[str, int] = {}
    for record in _read_jsonl(input_jsonl):
        request_input = _to_llm_request_input(record)
        request = build_llm_judge_request(
            request_input,
            model=model,
            max_docs_per_set=max_docs_per_set,
        )
        split = str(record.get("split") or "unknown")
        split_counts[split] = split_counts.get(split, 0) + 1
        request["metadata"] = {
            "dataset": "audit_sample_paper_1000_v3_nli_set",
            "orbit_id": record["orbit_id"],
            "split": split,
            "paired_nli_source": str(input_jsonl),
        }
        rows.append(request)

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    output_jsonl.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )
    api_key_ready = bool(
        os.environ.get("OPENAI_API_KEY")
        or os.environ.get("DASHSCOPE_API_KEY")
        or os.environ.get("DEEPSEEK_API_KEY")
    )
    score_ready = score_artifact.exists() and score_artifact.stat().st_size > 0
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_jsonl": str(input_jsonl),
        "output_jsonl": str(output_jsonl),
        "model": model,
        "request_count": len(rows),
        "split_counts": split_counts,
        "max_docs_per_set": max_docs_per_set,
        "api_key_ready": api_key_ready,
        "request_pack_ready": len(rows) > 0,
        "paired_to_nli_probe": True,
        "paired_nli_artifact": str(input_jsonl),
        "score_artifact": str(score_artifact),
        "score_artifact_ready": score_ready,
        "ready_for_nli_llm_correlation": score_ready,
        "claim_policy": (
            "This materializes LLM-judge requests over the exact NLI scored probe rows, "
            "after stripping labels, support keys, and construction metadata from prompts. "
            "It is not an LLM/NLI correlation result until API-backed scores are collected."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# LLM Judge Requests Paired To NLI Probe",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Model: `{summary['model']}`",
        f"Input NLI artifact: `{summary['input_jsonl']}`",
        f"Requests: `{summary['request_count']}`",
        f"Request pack ready: `{summary['request_pack_ready']}`",
        f"Paired to NLI probe: `{summary['paired_to_nli_probe']}`",
        f"API key ready: `{summary['api_key_ready']}`",
        f"Score artifact ready: `{summary['score_artifact_ready']}`",
        f"Ready for NLI/LLM correlation: `{summary['ready_for_nli_llm_correlation']}`",
        "",
        "## Splits",
        "",
        "| Split | Requests |",
        "|---|---:|",
    ]
    for split, count in sorted(summary["split_counts"].items()):
        lines.append(f"| {split} | {count} |")
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _to_llm_request_input(record: dict[str, Any]) -> dict[str, Any]:
    clean = record.get("clean") or {}
    return {
        "orbit_id": record["orbit_id"],
        "query": clean.get("query"),
        "candidate_answer": record.get("answer") or clean.get("answer"),
        "clean_evidence": _docs(clean.get("docs") or []),
        "perturbations": [
            {
                "query": item.get("query"),
                "candidate_answer": record.get("answer") or item.get("answer"),
                "evidence": _docs(item.get("docs") or []),
            }
            for item in record.get("perturbations") or []
        ],
    }


def _docs(docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "doc_id": doc.get("doc_id"),
            "title": doc.get("title"),
            "rank": doc.get("rank"),
            "text": doc.get("text"),
        }
        for doc in docs
    ]


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no} is not valid JSON") from exc
    return rows


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-jsonl", type=Path, default=DEFAULT_OUTPUT_JSONL)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--model", default="gpt-4.1-mini")
    parser.add_argument("--max-docs-per-set", type=int, default=6)
    args = parser.parse_args()
    summary = materialize_llm_judge_requests_nli_probe(
        args.input_jsonl,
        args.output_jsonl,
        model=args.model,
        max_docs_per_set=args.max_docs_per_set,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
