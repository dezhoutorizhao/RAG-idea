#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TRUE_VALUES = {"true", "yes", "1", "answerable", "supported"}
FALSE_VALUES = {"false", "no", "0", "unanswerable", "unsupported", "insufficient"}


def summarize_adjudication(input_path: Path) -> dict:
    items = _load_items(input_path)
    if not items:
        raise ValueError(f"{input_path} contains no records")

    totals = _empty_counts()
    by_split: dict[str, dict] = {}
    invalid_labels = []
    unresolved_disagreements = []

    for line_no, item in items:
        split = str(item.get("split") or "unknown")
        split_counts = by_split.setdefault(split, _empty_counts())
        for counts in (totals, split_counts):
            counts["total"] += 1

        label1, invalid1 = _parse_label_with_invalid(item.get("auditor_label_answerable"))
        label2, invalid2 = _parse_label_with_invalid(item.get("auditor2_label_answerable"))
        adjudicated, invalid_adj = _parse_label_with_invalid(
            item.get("adjudicated_label_answerable")
        )

        for field, invalid in [
            ("auditor_label_answerable", invalid1),
            ("auditor2_label_answerable", invalid2),
            ("adjudicated_label_answerable", invalid_adj),
        ]:
            if invalid:
                invalid_labels.append(
                    {
                        "line": line_no,
                        "orbit_id": item.get("orbit_id"),
                        "split": split,
                        "field": field,
                        "value": item.get(field),
                    }
                )

        if label1 is not None:
            for counts in (totals, split_counts):
                counts["auditor1_labeled"] += 1
        if label2 is not None:
            for counts in (totals, split_counts):
                counts["auditor2_labeled"] += 1
        if adjudicated is not None:
            for counts in (totals, split_counts):
                counts["adjudicated_labeled"] += 1

        if label1 is None or label2 is None:
            continue

        for counts in (totals, split_counts):
            counts["double_labeled"] += 1
            if label1:
                counts["auditor1_positive"] += 1
            else:
                counts["auditor1_negative"] += 1
            if label2:
                counts["auditor2_positive"] += 1
            else:
                counts["auditor2_negative"] += 1

        if label1 == label2:
            for counts in (totals, split_counts):
                counts["agree"] += 1
        else:
            for counts in (totals, split_counts):
                counts["disagree"] += 1
            if adjudicated is None:
                unresolved_disagreements.append(
                    {
                        "line": line_no,
                        "orbit_id": item.get("orbit_id"),
                        "split": split,
                        "auditor_label_answerable": label1,
                        "auditor2_label_answerable": label2,
                    }
                )

    _finalize_counts(totals)
    for counts in by_split.values():
        _finalize_counts(counts)

    return {
        "input": str(input_path),
        "total": totals,
        "by_split": by_split,
        "invalid_labels": invalid_labels,
        "unresolved_disagreements": unresolved_disagreements,
        "ready_for_adjudicated_claims": (
            totals["total"] > 0
            and totals["adjudicated_labeled"] == totals["total"]
            and not invalid_labels
            and not unresolved_disagreements
        ),
    }


def _empty_counts() -> dict:
    return {
        "total": 0,
        "auditor1_labeled": 0,
        "auditor2_labeled": 0,
        "double_labeled": 0,
        "adjudicated_labeled": 0,
        "agree": 0,
        "disagree": 0,
        "auditor1_positive": 0,
        "auditor1_negative": 0,
        "auditor2_positive": 0,
        "auditor2_negative": 0,
    }


def _finalize_counts(counts: dict) -> None:
    total = counts["total"]
    double_labeled = counts["double_labeled"]
    counts["auditor1_completion_rate"] = counts["auditor1_labeled"] / total if total else None
    counts["auditor2_completion_rate"] = counts["auditor2_labeled"] / total if total else None
    counts["double_labeled_rate"] = double_labeled / total if total else None
    counts["adjudicated_completion_rate"] = (
        counts["adjudicated_labeled"] / total if total else None
    )
    counts["raw_agreement"] = counts["agree"] / double_labeled if double_labeled else None
    counts["cohen_kappa"] = _cohen_kappa(counts)


def _cohen_kappa(counts: dict) -> float | None:
    n = counts["double_labeled"]
    if n == 0:
        return None
    observed = counts["agree"] / n
    p1_pos = counts["auditor1_positive"] / n
    p1_neg = counts["auditor1_negative"] / n
    p2_pos = counts["auditor2_positive"] / n
    p2_neg = counts["auditor2_negative"] / n
    expected = p1_pos * p2_pos + p1_neg * p2_neg
    if expected == 1.0:
        return 1.0 if observed == 1.0 else 0.0
    return (observed - expected) / (1.0 - expected)


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
    return items


def _parse_label_with_invalid(value: Any) -> tuple[bool | None, bool]:
    if value is None:
        return None, False
    if isinstance(value, bool):
        return value, False
    if isinstance(value, (int, float)):
        if value == 1:
            return True, False
        if value == 0:
            return False, False
    normalized = str(value).strip().lower()
    if not normalized:
        return None, False
    if normalized in TRUE_VALUES:
        return True, False
    if normalized in FALSE_VALUES:
        return False, False
    return None, True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_adjudication(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
