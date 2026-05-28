#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Iterable, List


def sample_audit_orbits(
    inputs: List[Path],
    output: Path,
    total: int,
    seed: int,
    max_doc_chars: int,
) -> None:
    records = []
    for path in inputs:
        records.extend(_load_records(path))
    if not records:
        raise ValueError("no orbit records found")

    rng = random.Random(seed)
    by_split: dict[str, list[dict]] = {}
    for record in records:
        split = record.get("clean", {}).get("split", "unknown")
        by_split.setdefault(split, []).append(record)

    split_names = sorted(by_split)
    base = total // len(split_names)
    remainder = total % len(split_names)
    sampled = []
    for index, split in enumerate(split_names):
        want = base + (1 if index < remainder else 0)
        candidates = list(by_split[split])
        rng.shuffle(candidates)
        sampled.extend(candidates[: min(want, len(candidates))])

    if len(sampled) < total:
        selected_ids = {record["orbit_id"] for record in sampled}
        leftovers = [record for record in records if record["orbit_id"] not in selected_ids]
        rng.shuffle(leftovers)
        sampled.extend(leftovers[: total - len(sampled)])

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as dst:
        for record in sampled[:total]:
            dst.write(json.dumps(_audit_item(record, max_doc_chars), ensure_ascii=False) + "\n")


def _load_records(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8") as src:
        for line in src:
            if line.strip():
                record = json.loads(line)
                record.setdefault("metadata", {})["audit_source_file"] = str(path)
                records.append(record)
    return records


def _audit_item(record: dict, max_doc_chars: int) -> dict:
    clean = record["clean"]
    perturbations = record.get("perturbations", [])
    return {
        "orbit_id": record.get("orbit_id"),
        "source": record.get("source"),
        "source_file": record.get("metadata", {}).get("audit_source_file"),
        "split": clean.get("split"),
        "expected_label_answerable": _orbit_label(record),
        "auditor_label_answerable": None,
        "auditor_failure_type": None,
        "auditor_notes": None,
        "answer": clean.get("answer"),
        "clean": _audit_set(clean, max_doc_chars),
        "perturbations": [_audit_set(item, max_doc_chars) for item in perturbations],
    }


def _orbit_label(record: dict) -> bool | None:
    labels = [record["clean"].get("label_answerable")]
    labels.extend(item.get("label_answerable") for item in record.get("perturbations", []))
    if any(label is None for label in labels):
        return None
    return all(bool(label) for label in labels)


def _audit_set(evidence_set: dict, max_doc_chars: int) -> dict:
    return {
        "query": evidence_set.get("query"),
        "label_answerable": evidence_set.get("label_answerable"),
        "support_key": evidence_set.get("metadata", {}).get("support_key"),
        "perturbation_type": evidence_set.get("metadata", {}).get("perturbation_type"),
        "docs": [_audit_doc(doc, max_doc_chars) for doc in evidence_set.get("docs", [])],
    }


def _audit_doc(doc: dict, max_doc_chars: int) -> dict:
    text = doc.get("text", "")
    return {
        "doc_id": doc.get("doc_id"),
        "title": doc.get("title"),
        "rank": doc.get("rank"),
        "corm_score": doc.get("corm_score"),
        "support": doc.get("support"),
        "conflict": doc.get("conflict"),
        "missing": doc.get("missing"),
        "text": text[:max_doc_chars],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--total", type=int, default=100)
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--max-doc-chars", type=int, default=700)
    args = parser.parse_args()
    sample_audit_orbits(
        inputs=args.input,
        output=args.output,
        total=args.total,
        seed=args.seed,
        max_doc_chars=args.max_doc_chars,
    )


if __name__ == "__main__":
    main()
