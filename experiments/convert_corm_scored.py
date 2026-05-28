#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def convert_scored_file(input_path: Path, output_path: Path, dataset: str) -> None:
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    if "CoRM-RAG" not in raw:
        raise ValueError(f"{input_path} does not contain a CoRM-RAG method key")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for query_idx, docs in enumerate(raw["CoRM-RAG"]):
            record = {
                "orbit_id": f"{dataset}:{query_idx}",
                "dataset": dataset,
                "clean": {
                    "query_id": query_idx,
                    "query": None,
                    "answer": None,
                    "label_answerable": None,
                    "split": "corm_scored",
                    "metadata": {
                        "source_file": str(input_path),
                        "support_key": None,
                    },
                    "docs": [_convert_doc(doc, rank) for rank, doc in enumerate(docs)],
                },
                "perturbations": [],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _convert_doc(doc: Dict[str, Any], rank: int) -> Dict[str, Any]:
    return {
        "doc_id": str(doc.get("idx", rank)),
        "text": doc.get("text", ""),
        "corm_score": float(doc.get("rerank_score", doc.get("score", 0.0))),
        "retrieval_score": _optional_float(doc.get("score")),
        "support": _optional_float(doc.get("support")),
        "conflict": _optional_float(doc.get("conflict")),
        "missing": _optional_float(doc.get("missing")),
        "rank": rank,
    }


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    return float(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()
    convert_scored_file(args.input, args.output, args.dataset)


if __name__ == "__main__":
    main()
