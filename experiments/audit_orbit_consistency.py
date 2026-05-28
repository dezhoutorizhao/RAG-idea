#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


SPLIT_EXPECTATIONS = {
    "hotpot_stable_support": {
        "source": "hotpot_qa/distractor",
        "label_source": "hotpot_supporting_facts_heuristic",
        "orbit_positive": True,
        "positive_perturbation_types": {"answer_preserving"},
        "positive_count": 2,
        "negative_count": 0,
    },
    "hotpot_missing_hop": {
        "source": "hotpot_qa/distractor",
        "label_source": "hotpot_supporting_facts_heuristic",
        "orbit_positive": False,
        "negative_perturbation_types": {"missing_hop_framing"},
        "positive_count": 0,
        "negative_count": 1,
    },
    "hotpot_false_premise": {
        "source": "hotpot_qa/distractor",
        "label_source": "hotpot_supporting_facts_heuristic",
        "orbit_positive": False,
        "negative_perturbation_types": {"false_premise"},
        "positive_count": 0,
        "negative_count": 1,
    },
    "hotpot_distractor": {
        "source": "hotpot_qa/distractor",
        "label_source": "hotpot_supporting_facts_heuristic",
        "orbit_positive": False,
        "negative_perturbation_types": {"distractor_only"},
        "positive_count": 0,
        "negative_count": 1,
    },
    "fever_stable_evidence": {
        "source": "copenlu/fever_gold_evidence",
        "label_source": "fever_gold_evidence_heuristic",
        "orbit_positive": True,
        "positive_perturbation_types": {"answer_preserving"},
        "positive_count": 2,
        "negative_count": 0,
    },
    "fever_missing_evidence": {
        "source": "copenlu/fever_gold_evidence",
        "label_source": "fever_gold_evidence_heuristic",
        "orbit_positive": False,
        "negative_perturbation_types": {"missing_evidence"},
        "positive_count": 0,
        "negative_count": 1,
    },
    "fever_fragile_mixed": {
        "source": "copenlu/fever_gold_evidence",
        "label_source": "fever_gold_evidence_heuristic",
        "orbit_positive": False,
        "positive_perturbation_types": {"answer_preserving"},
        "negative_perturbation_types": {"single_critical_conflict"},
        "positive_count": 2,
        "negative_count": 1,
    },
    "fever_conflicting_evidence": {
        "source": "copenlu/fever_gold_evidence",
        "label_source": "fever_gold_evidence_heuristic",
        "orbit_positive": False,
        "negative_perturbation_types": {"opposite_label_evidence"},
        "positive_count": 0,
        "negative_count": 1,
    },
    "fever_near_miss_dilution": {
        "source": "copenlu/fever_gold_evidence",
        "label_source": "fever_gold_evidence_heuristic",
        "orbit_positive": False,
        "negative_perturbation_types": {"near_miss_high_sufficiency"},
        "positive_count": 0,
        "negative_count": 4,
    },
    "fever_distractor_only": {
        "source": "copenlu/fever_gold_evidence",
        "label_source": "fever_gold_evidence_heuristic",
        "orbit_positive": False,
        "negative_perturbation_types": {"distractor_only"},
        "positive_count": 0,
        "negative_count": 1,
    },
}


def audit_orbit_consistency(input_path: Path, *, max_examples: int = 20) -> dict[str, Any]:
    records = _load_jsonl(input_path)
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    split_counts: Counter[str] = Counter()
    positive_counts: Counter[str] = Counter()

    for index, record in enumerate(records, start=1):
        orbit_id = str(record.get("orbit_id") or f"line:{index}")
        clean = record.get("clean") or {}
        split = str(clean.get("split") or "unknown")
        split_counts[split] += 1
        if _orbit_label(record):
            positive_counts[split] += 1
        _audit_record(record, orbit_id, split, errors, warnings)

    by_split = {}
    for split, count in sorted(split_counts.items()):
        by_split[split] = {
            "n": count,
            "positive": positive_counts[split],
            "negative": count - positive_counts[split],
        }

    return {
        "input": str(input_path),
        "total": len(records),
        "passed": not errors,
        "errors": errors[:max_examples],
        "warnings": warnings[:max_examples],
        "error_count": len(errors),
        "warning_count": len(warnings),
        "splits": by_split,
        "audit_scope": (
            "Structural and dataset-constraint consistency: validates source provenance, "
            "label-source metadata, generated labels, split names, perturbation counts/types, "
            "support-key lineage, duplicate evidence ids, support-key coverage, support-feature "
            "provenance, and verifier-feature ranges. "
            "It does not replace human semantic audit."
        ),
    }


def _audit_record(
    record: dict[str, Any],
    orbit_id: str,
    split: str,
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
) -> None:
    expected = SPLIT_EXPECTATIONS.get(split)
    if expected is None:
        _add(errors, orbit_id, "unknown_split", f"unknown split {split!r}")
        return

    clean = record.get("clean") or {}
    perturbations = record.get("perturbations") or []
    if not perturbations:
        _add(errors, orbit_id, "missing_perturbations", "orbit has no perturbations")
    source = record.get("source")
    if source != expected["source"]:
        _add(errors, orbit_id, "source_mismatch", f"expected source {expected['source']!r} got {source!r}")
    if clean.get("label_answerable") is not True:
        _add(errors, orbit_id, "clean_not_positive", "clean set must be labeled answerable")
    if _perturbation_type(clean) != "clean":
        _add(errors, orbit_id, "clean_type", "clean perturbation_type must be clean")
    if _label_source(clean) != expected["label_source"]:
        _add(
            errors,
            orbit_id,
            "label_source_mismatch",
            f"clean label_source expected {expected['label_source']!r} got {_label_source(clean)!r}",
        )

    actual_orbit_positive = _orbit_label(record)
    if actual_orbit_positive is not expected["orbit_positive"]:
        _add(
            errors,
            orbit_id,
            "orbit_label_mismatch",
            f"expected orbit_positive={expected['orbit_positive']} got {actual_orbit_positive}",
        )

    clean_key = str((clean.get("metadata") or {}).get("support_key") or "")
    positive_count = sum(1 for item in perturbations if item.get("label_answerable") is True)
    negative_count = sum(1 for item in perturbations if item.get("label_answerable") is False)
    if positive_count != expected.get("positive_count", 0) or negative_count != expected.get("negative_count", 0):
        _add(
            errors,
            orbit_id,
            "perturbation_count_mismatch",
            (
                f"expected positive={expected.get('positive_count', 0)} negative={expected.get('negative_count', 0)} "
                f"got positive={positive_count} negative={negative_count}"
            ),
        )
    for set_index, evidence_set in enumerate(perturbations, start=1):
        label = evidence_set.get("label_answerable")
        perturbation_type = _perturbation_type(evidence_set)
        evidence_split = evidence_set.get("split")
        if evidence_split != split:
            _add(
                errors,
                orbit_id,
                "split_mismatch",
                f"perturbation {set_index} split expected {split!r} got {evidence_split!r}",
            )
        if _label_source(evidence_set) != expected["label_source"]:
            _add(
                errors,
                orbit_id,
                "label_source_mismatch",
                (
                    f"perturbation {set_index} label_source expected {expected['label_source']!r} "
                    f"got {_label_source(evidence_set)!r}"
                ),
            )
        allowed_key = (
            "positive_perturbation_types" if label is True else "negative_perturbation_types"
        )
        allowed_types = expected.get(allowed_key, set())
        if perturbation_type not in allowed_types:
            _add(
                errors,
                orbit_id,
                "perturbation_type_mismatch",
                f"perturbation {set_index} has type {perturbation_type!r} for label {label}",
            )
        if label not in {True, False}:
            _add(errors, orbit_id, "invalid_label", f"perturbation {set_index} label is {label!r}")
        _audit_support_key_lineage(evidence_set, orbit_id, set_index, split, clean_key, errors)

    _audit_support_key_coverage(record, orbit_id, split, clean_key, errors, warnings)
    _audit_duplicate_docs(record, orbit_id, errors)
    _audit_feature_ranges(record, orbit_id, errors)


def _audit_support_key_lineage(
    evidence_set: dict[str, Any],
    orbit_id: str,
    set_index: int,
    split: str,
    clean_key: str,
    errors: list[dict[str, Any]],
) -> None:
    support_key = str((evidence_set.get("metadata") or {}).get("support_key") or "")
    perturbation_type = _perturbation_type(evidence_set)
    if perturbation_type == "answer_preserving":
        expected_key = clean_key
        valid = support_key == expected_key
    elif perturbation_type == "missing_hop_framing":
        expected_key = clean_key
        valid = support_key == expected_key
    elif perturbation_type == "missing_evidence":
        expected_key = f"{clean_key}:partial"
        valid = support_key == expected_key
    elif perturbation_type == "false_premise":
        expected_key = f"{clean_key}:false_premise"
        valid = support_key == expected_key
    elif perturbation_type == "distractor_only":
        expected_key = "distractor_only"
        valid = support_key == expected_key
    elif perturbation_type in {"single_critical_conflict", "opposite_label_evidence"}:
        expected_key = "opposite:<label>"
        valid = support_key.startswith("opposite:") and len(support_key.split(":", 1)[1]) > 0
    elif perturbation_type == "near_miss_high_sufficiency":
        expected_key = "near_miss:<label>:<index>"
        valid = support_key.startswith("near_miss:") and len(support_key.split(":")) >= 3
    else:
        return

    if not valid:
        _add(
            errors,
            orbit_id,
            "support_key_lineage_mismatch",
            (
                f"{split} perturbation {set_index} type {perturbation_type!r} "
                f"expected support_key {expected_key!r} got {support_key!r}"
            ),
        )


def _audit_duplicate_docs(
    record: dict[str, Any],
    orbit_id: str,
    errors: list[dict[str, Any]],
) -> None:
    for set_name, evidence_set in _iter_sets(record):
        seen: set[str] = set()
        for doc_index, doc in enumerate(evidence_set.get("docs") or []):
            doc_id = str(doc.get("doc_id") or doc.get("title") or "")
            if not doc_id:
                _add(errors, orbit_id, "missing_doc_id", f"{set_name} doc {doc_index} lacks doc_id/title")
                continue
            if doc_id in seen:
                _add(errors, orbit_id, "duplicate_doc_id", f"{set_name} repeats doc id {doc_id!r}")
            seen.add(doc_id)


def _audit_support_key_coverage(
    record: dict[str, Any],
    orbit_id: str,
    split: str,
    clean_key: str,
    errors: list[dict[str, Any]],
    warnings: list[dict[str, Any]],
) -> None:
    if not clean_key or clean_key in {"distractor_only"} or clean_key.startswith(("opposite:", "near_miss:")):
        _add(warnings, orbit_id, "support_key_unchecked", "clean support key is not auditable")
        return

    support_ids = set(_split_support_key(clean_key))
    if not support_ids:
        _add(warnings, orbit_id, "support_key_empty", "support key has no auditable ids")
        return

    clean_coverage = _support_coverage(record.get("clean") or {}, support_ids)
    if clean_coverage < 1.0:
        _add(
            errors,
            orbit_id,
            "clean_support_incomplete",
            f"clean coverage {clean_coverage:.3f} for support key {clean_key!r}",
        )
    _audit_support_feature_profile(record.get("clean") or {}, orbit_id, "clean", support_ids, errors)

    for index, evidence_set in enumerate(record.get("perturbations") or [], start=1):
        label = evidence_set.get("label_answerable")
        perturbation_type = _perturbation_type(evidence_set)
        coverage = _support_coverage(evidence_set, support_ids)
        if label is True and coverage < 1.0:
            _add(
                errors,
                orbit_id,
                "positive_support_incomplete",
                f"positive perturbation {index} coverage {coverage:.3f}",
            )
        if perturbation_type in {"missing_hop_framing", "missing_evidence"} and coverage >= 1.0:
            _add(
                errors,
                orbit_id,
                "missing_split_has_full_support",
                f"missing perturbation {index} unexpectedly covers all support ids",
            )
        if perturbation_type == "distractor_only" and coverage > 0.0:
            _add(
                errors,
                orbit_id,
                "distractor_has_support",
                f"distractor perturbation {index} covers support ids",
            )
        if split.startswith("fever_") and perturbation_type in {
            "opposite_label_evidence",
            "single_critical_conflict",
            "near_miss_high_sufficiency",
        }:
            if coverage > 0.0:
                _add(
                    errors,
                    orbit_id,
                    "fever_negative_reuses_gold",
                    f"negative FEVER perturbation {index} reuses clean gold evidence",
                )
        _audit_support_feature_profile(
            evidence_set,
            orbit_id,
            f"perturbation {index}",
            support_ids,
            errors,
        )


def _audit_support_feature_profile(
    evidence_set: dict[str, Any],
    orbit_id: str,
    set_name: str,
    support_ids: set[str],
    errors: list[dict[str, Any]],
) -> None:
    perturbation_type = _perturbation_type(evidence_set)
    if perturbation_type == "near_miss_high_sufficiency":
        return
    for doc_index, doc in enumerate(evidence_set.get("docs") or []):
        doc_ids = _doc_identifiers(doc)
        try:
            support = float(doc.get("support"))
        except (TypeError, ValueError):
            continue
        if doc_ids & support_ids:
            if support < 0.5:
                _add(
                    errors,
                    orbit_id,
                    "gold_doc_low_support_feature",
                    f"{set_name} doc {doc_index} has support={support:.3f} despite matching support_key",
                )
        elif support > 0.5:
            _add(
                errors,
                orbit_id,
                "non_gold_doc_high_support_feature",
                f"{set_name} doc {doc_index} has support={support:.3f} without matching support_key",
            )


def _audit_feature_ranges(
    record: dict[str, Any],
    orbit_id: str,
    errors: list[dict[str, Any]],
) -> None:
    for set_name, evidence_set in _iter_sets(record):
        docs = evidence_set.get("docs") or []
        if not docs:
            _add(errors, orbit_id, "empty_docs", f"{set_name} has no docs")
        for doc_index, doc in enumerate(docs):
            for key in ["corm_score", "support", "conflict", "missing"]:
                value = doc.get(key)
                try:
                    numeric = float(value)
                except (TypeError, ValueError):
                    _add(errors, orbit_id, "invalid_feature", f"{set_name} doc {doc_index} {key}={value!r}")
                    continue
                if numeric < 0.0 or numeric > 1.0:
                    _add(errors, orbit_id, "feature_out_of_range", f"{set_name} doc {doc_index} {key}={numeric}")


def _support_coverage(evidence_set: dict[str, Any], support_ids: set[str]) -> float:
    present = _doc_id_set(evidence_set)
    if not support_ids:
        return 0.0
    return len(support_ids & present) / len(support_ids)


def _doc_id_set(evidence_set: dict[str, Any]) -> set[str]:
    ids = set()
    for doc in evidence_set.get("docs") or []:
        ids.update(_doc_identifiers(doc))
    return ids


def _doc_identifiers(doc: dict[str, Any]) -> set[str]:
    return {str(doc[key]) for key in ["doc_id", "title"] if doc.get(key)}


def _split_support_key(support_key: str) -> list[str]:
    if support_key.endswith(":partial"):
        support_key = support_key[: -len(":partial")]
    return [part for part in support_key.split("|") if part]


def _iter_sets(record: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    yield "clean", record.get("clean") or {}
    for index, perturbation in enumerate(record.get("perturbations") or [], start=1):
        yield f"perturbation_{index}", perturbation


def _perturbation_type(evidence_set: dict[str, Any]) -> str:
    return str((evidence_set.get("metadata") or {}).get("perturbation_type") or "")


def _label_source(evidence_set: dict[str, Any]) -> str:
    return str((evidence_set.get("metadata") or {}).get("label_source") or "")


def _orbit_label(record: dict[str, Any]) -> bool:
    clean = record.get("clean") or {}
    if clean.get("label_answerable") is not True:
        return False
    return all(item.get("label_answerable") is True for item in record.get("perturbations") or [])


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
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


def _add(
    collection: list[dict[str, Any]],
    orbit_id: str,
    code: str,
    message: str,
) -> None:
    collection.append({"orbit_id": orbit_id, "code": code, "message": message})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-examples", type=int, default=20)
    args = parser.parse_args()

    report = audit_orbit_consistency(args.input, max_examples=args.max_examples)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
