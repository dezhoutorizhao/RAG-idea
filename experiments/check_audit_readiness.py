#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.summarize_audit import FALSE_VALUES, TRUE_VALUES


def check_audit_readiness(
    input_path: Path,
    min_labeled_total: int,
    min_labeled_per_split: int,
    label_field: str = "auditor_label_answerable",
    require_disagreement_notes: bool = True,
) -> dict:
    items = _load_items(input_path)
    by_split: dict[str, dict] = {}
    invalid_labels = []
    disagreements_without_notes = []
    labeled = 0
    agreement = 0
    comparable = 0

    for line_no, item in items:
        split = str(item.get("split") or "unknown")
        split_summary = by_split.setdefault(
            split,
            {
                "total": 0,
                "labeled": 0,
                "pending": 0,
                "invalid": 0,
                "agree": 0,
                "disagree": 0,
            },
        )
        split_summary["total"] += 1

        raw_label = item.get(label_field)
        auditor_label = _parse_label(raw_label)
        if auditor_label is None:
            if raw_label is None or str(raw_label).strip() == "":
                split_summary["pending"] += 1
            else:
                split_summary["invalid"] += 1
                invalid_labels.append(
                    {
                        "line": line_no,
                        "orbit_id": item.get("orbit_id"),
                        "split": split,
                        "label_field": label_field,
                        "value": raw_label,
                    }
                )
            continue

        labeled += 1
        split_summary["labeled"] += 1
        expected = _parse_label(item.get("expected_label_answerable"))
        if expected is None:
            continue
        comparable += 1
        if expected == auditor_label:
            agreement += 1
            split_summary["agree"] += 1
        else:
            split_summary["disagree"] += 1
            note = str(item.get("auditor_notes") or "").strip()
            failure_type = str(item.get("auditor_failure_type") or "").strip()
            if require_disagreement_notes and (not note or not failure_type):
                disagreements_without_notes.append(
                    {
                        "line": line_no,
                        "orbit_id": item.get("orbit_id"),
                        "split": split,
                        "expected": expected,
                        "auditor": auditor_label,
                        "auditor_failure_type": item.get("auditor_failure_type"),
                        "auditor_notes": item.get("auditor_notes"),
                    }
                )

    failed_gates = []
    if labeled < min_labeled_total:
        failed_gates.append(
            {
                "gate": "min_labeled_total",
                "required": min_labeled_total,
                "actual": labeled,
            }
        )
    for split, split_summary in sorted(by_split.items()):
        if split_summary["labeled"] < min_labeled_per_split:
            failed_gates.append(
                {
                    "gate": "min_labeled_per_split",
                    "split": split,
                    "required": min_labeled_per_split,
                    "actual": split_summary["labeled"],
                }
            )
    if invalid_labels:
        failed_gates.append(
            {
                "gate": "valid_auditor_labels",
                "invalid": len(invalid_labels),
                "examples": invalid_labels[:10],
            }
        )
    if disagreements_without_notes:
        failed_gates.append(
            {
                "gate": "disagreement_notes",
                "missing": len(disagreements_without_notes),
                "examples": disagreements_without_notes[:10],
            }
        )

    return {
        "input": str(input_path),
        "ready": not failed_gates,
        "total": len(items),
        "labeled": labeled,
        "pending": len(items) - labeled - len(invalid_labels),
        "invalid": len(invalid_labels),
        "completion_rate": labeled / len(items),
        "agreement_with_expected": agreement / comparable if comparable else None,
        "min_labeled_total": min_labeled_total,
        "min_labeled_per_split": min_labeled_per_split,
        "label_field": label_field,
        "by_split": by_split,
        "failed_gates": failed_gates,
    }


def _load_items(input_path: Path) -> list[tuple[int, dict]]:
    items = []
    with input_path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            try:
                items.append((line_no, json.loads(line)))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{input_path}:{line_no} is not valid JSON") from exc
    if not items:
        raise ValueError(f"{input_path} contains no records")
    return items


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
    parser.add_argument("--min-labeled-total", type=int, required=True)
    parser.add_argument("--min-labeled-per-split", type=int, required=True)
    parser.add_argument(
        "--label-field",
        default="auditor_label_answerable",
        help="Audit item field to check as the final answerability label.",
    )
    parser.add_argument(
        "--allow-unexplained-disagreements",
        action="store_true",
        help="Do not fail when an expected/auditor disagreement lacks notes.",
    )
    args = parser.parse_args()

    report = check_audit_readiness(
        input_path=args.input,
        min_labeled_total=args.min_labeled_total,
        min_labeled_per_split=args.min_labeled_per_split,
        label_field=args.label_field,
        require_disagreement_notes=not args.allow_unexplained_disagreements,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
