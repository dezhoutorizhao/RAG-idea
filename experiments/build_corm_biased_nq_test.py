#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_PERTURBATION_TYPES = {1, 2, 3}


def build_biased_nq_test(
    perturbations: Path,
    output: Path,
    *,
    require_all_types: bool = True,
    manifest: Path | None = None,
) -> dict[str, Any]:
    rows = [_normalize_row(row, line_no=i + 1) for i, row in enumerate(_read_jsonl(perturbations))]
    if not rows:
        raise ValueError("no perturbation rows found")
    rows.sort(key=lambda item: int(item["query_idx"]))

    missing_type_rows = [
        int(row["query_idx"])
        for row in rows
        if not REQUIRED_PERTURBATION_TYPES.issubset(
            {int(item["perturbation_type"]) for item in row["perturbations"]}
        )
    ]
    if require_all_types and missing_type_rows:
        preview = ", ".join(str(idx) for idx in missing_type_rows[:10])
        raise ValueError(f"rows missing required perturbation types: {preview}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    report = {
        "input": str(perturbations),
        "output": str(output),
        "rows": len(rows),
        "require_all_types": require_all_types,
        "missing_required_type_rows": missing_type_rows,
        "status": "built",
        "note": (
            "Supplemental materialization helper for CoRM-RAG Biased_NQ. The output "
            "matches the fields consumed by run_evaluation.py, but exact equivalence "
            "to the authors' original biased_nq_test.jsonl depends on the perturbation "
            "JSONL input."
        ),
    }
    if manifest:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_no}: {exc}") from exc
            if not isinstance(item, dict):
                raise ValueError(f"line {line_no} is not a JSON object")
            rows.append(item)
    return rows


def _normalize_row(row: dict[str, Any], *, line_no: int) -> dict[str, Any]:
    required = ["query_idx", "question", "all_answers", "perturbations"]
    missing = [field for field in required if field not in row]
    if missing:
        raise ValueError(f"line {line_no} missing required fields: {missing}")
    if not isinstance(row["all_answers"], list) or not row["all_answers"]:
        raise ValueError(f"line {line_no} all_answers must be a non-empty list")
    perturbations = row["perturbations"]
    if not isinstance(perturbations, list) or not perturbations:
        raise ValueError(f"line {line_no} perturbations must be a non-empty list")

    normalized_perturbations = []
    for idx, item in enumerate(perturbations):
        if not isinstance(item, dict):
            raise ValueError(f"line {line_no} perturbation {idx} is not an object")
        if "perturbation_type" not in item or "perturbed_query" not in item:
            raise ValueError(
                f"line {line_no} perturbation {idx} must include perturbation_type and perturbed_query"
            )
        ptype = int(item["perturbation_type"])
        if ptype not in REQUIRED_PERTURBATION_TYPES:
            raise ValueError(f"line {line_no} perturbation {idx} has unsupported type {ptype}")
        perturbed_query = str(item["perturbed_query"]).strip()
        if not perturbed_query:
            raise ValueError(f"line {line_no} perturbation {idx} has empty perturbed_query")
        normalized = dict(item)
        normalized["perturbation_type"] = ptype
        normalized["perturbed_query"] = perturbed_query
        normalized_perturbations.append(normalized)

    return {
        "query_idx": int(row["query_idx"]),
        "question": str(row["question"]),
        "correct_answer": row.get("correct_answer", row["all_answers"][0]),
        "all_answers": [str(answer) for answer in row["all_answers"]],
        "perturbations": normalized_perturbations,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--perturbations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--allow-missing-types", action="store_true")
    args = parser.parse_args()

    result = build_biased_nq_test(
        args.perturbations,
        args.output,
        require_all_types=not args.allow_missing_types,
        manifest=args.manifest,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
