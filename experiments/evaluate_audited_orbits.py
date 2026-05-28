#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from csrm_rag import EvidenceDoc, EvidenceSet, QueryOrbit

from experiments.evaluate_orbits import evaluate


TRUE_VALUES = {"true", "yes", "1", "answerable", "supported"}
FALSE_VALUES = {"false", "no", "0", "unanswerable", "unsupported", "insufficient"}


def evaluate_audited_orbits(
    audit_path: Path,
    bootstrap_samples: int = 200,
    bootstrap_seed: int = 13,
    label_field: str = "auditor_label_answerable",
) -> dict:
    items = _load_audit_items(audit_path)
    labeled_items = []
    pending = 0
    invalid = []
    agreement = 0
    comparable = 0

    for line_no, item in items:
        auditor_label = _parse_label(item.get(label_field))
        if auditor_label is None:
            raw_value = item.get(label_field)
            if raw_value is None or str(raw_value).strip() == "":
                pending += 1
            else:
                invalid.append(
                    {
                        "line": line_no,
                        "orbit_id": item.get("orbit_id"),
                        label_field: raw_value,
                    }
                )
            continue

        expected = _parse_label(item.get("expected_label_answerable"))
        if expected is not None:
            comparable += 1
            if expected == auditor_label:
                agreement += 1
        labeled_items.append((item, auditor_label))

    if invalid:
        raise ValueError(
            f"{audit_path} contains invalid labels in {label_field}: "
            + ", ".join(str(item["orbit_id"]) for item in invalid[:5])
        )
    if not labeled_items:
        raise ValueError(f"{audit_path} contains no labeled audit records")

    orbits = [_audit_item_to_orbit(item, auditor_label) for item, auditor_label in labeled_items]
    result = evaluate(orbits, bootstrap_samples=bootstrap_samples, bootstrap_seed=bootstrap_seed)
    result["audit"] = {
        "input": str(audit_path),
        "total": len(items),
        "labeled": len(labeled_items),
        "pending": pending,
        "invalid": len(invalid),
        "completion_rate": len(labeled_items) / len(items),
        "agreement_with_expected": agreement / comparable if comparable else None,
        "label_source": label_field,
    }
    result["audit"]["by_split"] = _audit_split_summary(labeled_items)
    return result


def _load_audit_items(audit_path: Path) -> list[tuple[int, dict]]:
    items = []
    with audit_path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            try:
                items.append((line_no, json.loads(line)))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{audit_path}:{line_no} is not valid JSON") from exc
    if not items:
        raise ValueError(f"{audit_path} contains no records")
    return items


def _audit_item_to_orbit(item: dict, auditor_label: bool) -> QueryOrbit:
    answer = str(item.get("answer") or "")
    clean = _audit_set_to_evidence_set(
        item["clean"],
        answer=answer,
        split=str(item.get("split") or item["clean"].get("split") or "unknown"),
        label_answerable=auditor_label,
    )
    perturbations = [
        _audit_set_to_evidence_set(
            raw,
            answer=answer,
            split=str(item.get("split") or raw.get("split") or clean.split),
            label_answerable=True,
        )
        for raw in item.get("perturbations", [])
    ]
    return QueryOrbit(str(item.get("orbit_id") or ""), clean, perturbations)


def _audit_set_to_evidence_set(
    raw: dict,
    answer: str,
    split: str,
    label_answerable: bool,
) -> EvidenceSet:
    metadata = {
        "support_key": str(raw.get("support_key") or ""),
        "perturbation_type": str(raw.get("perturbation_type") or ""),
        "original_label_answerable": str(raw.get("label_answerable")),
    }
    return EvidenceSet(
        query=str(raw.get("query") or ""),
        answer=answer,
        docs=[_audit_doc_to_evidence_doc(doc) for doc in raw.get("docs", [])],
        label_answerable=label_answerable,
        split=split,
        metadata=metadata,
    ).normalized()


def _audit_doc_to_evidence_doc(raw: dict) -> EvidenceDoc:
    return EvidenceDoc(
        doc_id=str(raw.get("doc_id") or ""),
        text=str(raw.get("text") or ""),
        corm_score=float(raw.get("corm_score") or 0.0),
        support=float(raw.get("support") or 0.0),
        conflict=float(raw.get("conflict") or 0.0),
        missing=float(raw.get("missing") or 0.0),
    ).clipped()


def _audit_split_summary(labeled_items: list[tuple[dict, bool]]) -> dict:
    summary: dict[str, dict] = {}
    for item, auditor_label in labeled_items:
        split = str(item.get("split") or "unknown")
        split_summary = summary.setdefault(
            split,
            {"labeled": 0, "positive": 0, "negative": 0, "agree": 0, "disagree": 0},
        )
        split_summary["labeled"] += 1
        if auditor_label:
            split_summary["positive"] += 1
        else:
            split_summary["negative"] += 1
        expected = _parse_label(item.get("expected_label_answerable"))
        if expected is None:
            continue
        if expected == auditor_label:
            split_summary["agree"] += 1
        else:
            split_summary["disagree"] += 1
    return summary


def _parse_label(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        if value == 1:
            return True
        if value == 0:
            return False
    normalized = str(value).strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-samples", type=int, default=200)
    parser.add_argument("--bootstrap-seed", type=int, default=13)
    parser.add_argument(
        "--label-field",
        default="auditor_label_answerable",
        help="Audit item field to use as the final answerability label.",
    )
    args = parser.parse_args()

    result = evaluate_audited_orbits(
        args.input,
        bootstrap_samples=args.bootstrap_samples,
        bootstrap_seed=args.bootstrap_seed,
        label_field=args.label_field,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
