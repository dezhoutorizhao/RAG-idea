#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Sequence


def audit_hotpot_semantic_swap(raw_path: Path, private_path: Path, output_path: Path) -> dict[str, Any]:
    raw_rows = _read_jsonl(raw_path)
    private_rows = _read_jsonl(private_path)
    if len(raw_rows) != len(private_rows):
        raise ValueError("raw and private files must contain the same number of rows")
    private_by_id = {row["orbit_id"]: row for row in private_rows}
    groups: dict[str, list[dict[str, Any]]] = {}
    for raw in raw_rows:
        private = private_by_id.get(raw["orbit_id"])
        if private is None:
            raise ValueError(f"missing private row for orbit_id={raw['orbit_id']}")
        groups.setdefault(str(raw["source_item_group_id"]), []).append({"raw": raw, "private": private})

    failures = []
    group_reports = []
    for group_id, rows in sorted(groups.items()):
        report = _audit_group(group_id, rows)
        group_reports.append(report)
        if not report["passed"]:
            failures.append(report)

    summary = {
        "raw_input": str(raw_path),
        "private_input": str(private_path),
        "groups": len(groups),
        "rows": len(raw_rows),
        "passed": not failures,
        "failed_groups": len(failures),
        "failure_examples": failures[:20],
        "aggregate": _aggregate(group_reports),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def _audit_group(group_id: str, rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    issues = []
    by_type = {str(item["private"].get("construction_type")): item for item in rows}
    stable = by_type.get("stable")
    fragile = by_type.get("semantic_swap")
    if stable is None or fragile is None:
        issues.append("missing stable/semantic_swap pair")
        return _group_report(group_id, rows, issues)

    stable_raw = stable["raw"]
    fragile_raw = fragile["raw"]
    stable_private = stable["private"]
    fragile_private = fragile["private"]
    if stable_private.get("label_answerable") is not True:
        issues.append("stable label is not answerable")
    if fragile_private.get("label_answerable") is not False:
        issues.append("semantic_swap label is not fragile")
    if stable_raw.get("candidate_answer") != fragile_raw.get("candidate_answer"):
        issues.append("raw candidate_answer differs between stable and semantic_swap")
    if not _same_docs(stable_raw.get("clean_evidence") or [], fragile_raw.get("clean_evidence") or []):
        issues.append("clean evidence doc ids differ")
    stable_pert = _first_perturbation(stable_raw)
    fragile_pert = _first_perturbation(fragile_raw)
    if stable_pert is None or fragile_pert is None:
        issues.append("missing first perturbation")
        return _group_report(group_id, rows, issues)
    if stable_pert.get("candidate_answer") != fragile_pert.get("candidate_answer"):
        issues.append("perturbation candidate_answer differs")
    if not _same_docs(stable_pert.get("evidence") or [], fragile_pert.get("evidence") or []):
        issues.append("perturbation doc ids differ")
    clean_doc_overlap = _doc_overlap(stable_raw.get("clean_evidence") or [], fragile_raw.get("clean_evidence") or [])
    perturbation_doc_overlap = _doc_overlap(stable_pert.get("evidence") or [], fragile_pert.get("evidence") or [])
    stable_text = _joined_text(stable_pert.get("evidence") or [])
    fragile_text = _joined_text(fragile_pert.get("evidence") or [])
    answer = str(stable_raw.get("candidate_answer") or "")
    stable_answer_count = _count_answer(stable_text, answer)
    fragile_answer_count = _count_answer(fragile_text, answer)
    if stable_text == fragile_text:
        issues.append("semantic_swap perturbation text did not change")
    if stable_answer_count <= fragile_answer_count:
        issues.append("semantic_swap did not reduce answer mentions")
    return {
        "group_id": group_id,
        "passed": not issues,
        "issues": issues,
        "stable_orbit_id": stable_raw.get("orbit_id"),
        "semantic_swap_orbit_id": fragile_raw.get("orbit_id"),
        "candidate_answer": answer,
        "clean_doc_overlap": clean_doc_overlap,
        "perturbation_doc_overlap": perturbation_doc_overlap,
        "stable_answer_mentions": stable_answer_count,
        "semantic_swap_answer_mentions": fragile_answer_count,
        "perturbation_text_changed": stable_text != fragile_text,
    }


def _group_report(group_id: str, rows: Sequence[dict[str, Any]], issues: list[str]) -> dict[str, Any]:
    return {
        "group_id": group_id,
        "passed": False,
        "issues": issues,
        "orbit_ids": [item["raw"].get("orbit_id") for item in rows],
    }


def _aggregate(group_reports: Sequence[dict[str, Any]]) -> dict[str, Any]:
    valid = [row for row in group_reports if "clean_doc_overlap" in row]
    if not valid:
        return {}
    return {
        "mean_clean_doc_overlap": _mean([row["clean_doc_overlap"] for row in valid]),
        "mean_perturbation_doc_overlap": _mean([row["perturbation_doc_overlap"] for row in valid]),
        "text_changed_rate": _mean([1.0 if row["perturbation_text_changed"] else 0.0 for row in valid]),
        "answer_mentions_reduced_rate": _mean(
            [
                1.0 if row["stable_answer_mentions"] > row["semantic_swap_answer_mentions"] else 0.0
                for row in valid
            ]
        ),
    }


def _first_perturbation(row: dict[str, Any]) -> dict[str, Any] | None:
    perturbations = row.get("perturbations") or []
    return perturbations[0] if perturbations else None


def _same_docs(left: Sequence[dict[str, Any]], right: Sequence[dict[str, Any]]) -> bool:
    return [str(doc.get("doc_id") or "") for doc in left] == [str(doc.get("doc_id") or "") for doc in right]


def _doc_overlap(left: Sequence[dict[str, Any]], right: Sequence[dict[str, Any]]) -> float:
    left_ids = {str(doc.get("doc_id") or "") for doc in left}
    right_ids = {str(doc.get("doc_id") or "") for doc in right}
    union = left_ids | right_ids
    if not union:
        return 1.0
    return len(left_ids & right_ids) / len(union)


def _joined_text(docs: Sequence[dict[str, Any]]) -> str:
    return "\n".join(str(doc.get("text") or "") for doc in docs)


def _count_answer(text: str, answer: str) -> int:
    if not answer:
        return 0
    return len(re.findall(re.escape(answer), text, flags=re.IGNORECASE))


def _mean(values: Sequence[float]) -> float:
    return float(sum(values) / len(values)) if values else 0.0


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary = audit_hotpot_semantic_swap(args.raw, args.private, args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
