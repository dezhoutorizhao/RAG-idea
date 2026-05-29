#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag.verifiers.llm_judge import build_llm_judge_request


@dataclass(frozen=True)
class DatasetConfig:
    name: str
    raw: Path


DEFAULT_DATASETS = [
    DatasetConfig("fever_v4_n100_structbalanced", Path("results/fever_orbits_v4_n100.constant.structbalanced.raw.jsonl")),
    DatasetConfig("hotpot_v4_hardneg_n100", Path("results/hotpot_orbits_v4_hardneg_n100.constant.raw.jsonl")),
    DatasetConfig("hotpot_v4_n100_hardmatched", Path("results/hotpot_orbits_v4_n100.constant.hardmatched.raw.jsonl")),
    DatasetConfig("hotpot_v4_n100_structbalanced", Path("results/hotpot_orbits_v4_n100.constant.structbalanced.raw.jsonl")),
    DatasetConfig("hotpot_v4_semanticswap_n100", Path("results/hotpot_orbits_v4_semanticswap_n100.constant.raw.jsonl")),
    DatasetConfig("hotpot_v4_supportpreserve_n100", Path("results/hotpot_orbits_v4_supportpreserve_n100.constant.raw.jsonl")),
]


def materialize_llm_judge_requests_v4(
    datasets: Sequence[DatasetConfig],
    output_jsonl: Path,
    *,
    model: str,
    max_docs_per_set: int = 6,
) -> dict[str, Any]:
    rows = []
    dataset_rows = []
    for dataset in datasets:
        raw_rows = _read_jsonl(dataset.raw)
        dataset_rows.append({"dataset": dataset.name, "raw": str(dataset.raw), "row_count": len(raw_rows)})
        for row in raw_rows:
            request = build_llm_judge_request(row, model=model, max_docs_per_set=max_docs_per_set)
            request["metadata"] = {"dataset": dataset.name, "orbit_id": row["orbit_id"]}
            rows.append(request)

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    output_jsonl.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n", encoding="utf-8")
    api_key_ready = bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("DEEPSEEK_API_KEY"))
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_jsonl": str(output_jsonl),
        "model": model,
        "dataset_count": len(dataset_rows),
        "datasets": dataset_rows,
        "request_count": len(rows),
        "max_docs_per_set": max_docs_per_set,
        "api_key_ready": api_key_ready,
        "request_pack_ready": len(rows) > 0,
        "score_artifact_ready": False,
        "score_artifact": "results/llm_judge_v4_scores_20260529.jsonl",
        "ready_for_baseline_coverage": False,
        "claim_policy": (
            "This materializes an equal-input LLM-judge request pack. It is not an LLM-judge "
            "baseline result until responses are collected and converted into score artifacts."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# LLM Judge V4 Request Pack",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Model: `{summary['model']}`",
        f"Datasets: `{summary['dataset_count']}`",
        f"Requests: `{summary['request_count']}`",
        f"Request pack ready: `{summary['request_pack_ready']}`",
        f"API key ready: `{summary['api_key_ready']}`",
        f"Score artifact ready: `{summary['score_artifact_ready']}`",
        f"Ready for baseline coverage: `{summary['ready_for_baseline_coverage']}`",
        "",
        "## Datasets",
        "",
        "| Dataset | Raw input | Rows |",
        "|---|---|---:|",
    ]
    for row in summary["datasets"]:
        lines.append(f"| {row['dataset']} | `{row['raw']}` | {row['row_count']} |")
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


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
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--model", default="gpt-4.1-mini")
    parser.add_argument("--max-docs-per-set", type=int, default=6)
    args = parser.parse_args()

    summary = materialize_llm_judge_requests_v4(
        DEFAULT_DATASETS,
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
