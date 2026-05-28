#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TRUE_VALUES = {"true", "yes", "1", "answerable", "supported"}
FALSE_VALUES = {"false", "no", "0", "unanswerable", "unsupported", "insufficient"}


def summarize_audit(input_path: Path) -> dict:
    items = _load_items(input_path)
    if not items:
        raise ValueError("audit file contains no records")

    by_split: dict[str, dict] = {}
    labeled = 0
    agreement = 0
    disagreements = []
    pending = []
    failure_types: dict[str, int] = {}

    for item in items:
        split = str(item.get("split") or "unknown")
        split_summary = by_split.setdefault(
            split,
            {"total": 0, "labeled": 0, "agree": 0, "disagree": 0, "pending": 0},
        )
        split_summary["total"] += 1

        expected = _parse_label(item.get("expected_label_answerable"))
        observed = _parse_label(item.get("auditor_label_answerable"))
        if observed is None:
            split_summary["pending"] += 1
            pending.append(item.get("orbit_id"))
            continue

        labeled += 1
        split_summary["labeled"] += 1
        failure_type = item.get("auditor_failure_type")
        if failure_type:
            failure_types[str(failure_type)] = failure_types.get(str(failure_type), 0) + 1

        if expected is not None and observed == expected:
            agreement += 1
            split_summary["agree"] += 1
        elif expected is not None:
            split_summary["disagree"] += 1
            disagreements.append(
                {
                    "orbit_id": item.get("orbit_id"),
                    "split": split,
                    "expected": expected,
                    "auditor": observed,
                    "notes": item.get("auditor_notes"),
                }
            )

    return {
        "input": str(input_path),
        "total": len(items),
        "labeled": labeled,
        "pending": len(items) - labeled,
        "completion_rate": labeled / len(items),
        "agreement_with_expected": agreement / labeled if labeled else None,
        "by_split": by_split,
        "failure_types": dict(sorted(failure_types.items())),
        "disagreements": disagreements,
        "pending_orbit_ids": pending,
    }


def _load_items(input_path: Path) -> list[dict]:
    items = []
    with input_path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{input_path}:{line_no} is not valid JSON") from exc
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
    args = parser.parse_args()

    summary = summarize_audit(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
