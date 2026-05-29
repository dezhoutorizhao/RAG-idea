#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any


def compute_agreement_v4(merged_labels_path: Path) -> dict[str, Any]:
    rows = _load_jsonl(merged_labels_path)
    if not rows:
        raise ValueError(f"{merged_labels_path} contains no labels")

    auditors = sorted({str(row.get("auditor_id") or "") for row in rows if row.get("auditor_id")})
    by_audit: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rows:
        by_audit.setdefault(str(row["audit_id"]), {})[str(row["auditor_id"])] = row

    completion = {}
    for auditor in auditors:
        auditor_rows = [row for row in rows if row.get("auditor_id") == auditor]
        labeled = sum(row.get("label_answerable_bool") is not None for row in auditor_rows)
        completion[auditor] = {
            "rows": len(auditor_rows),
            "labeled": labeled,
            "completion_rate": labeled / len(auditor_rows) if auditor_rows else None,
        }

    pairwise = []
    conflicts = []
    semantic_pairwise = []
    semantic_conflicts = []
    for left, right in combinations(auditors, 2):
        compared = []
        semantic_compared = []
        for audit_id, labels in sorted(by_audit.items()):
            if left not in labels or right not in labels:
                continue
            left_label = labels[left].get("label_answerable_bool")
            right_label = labels[right].get("label_answerable_bool")
            if left_label is None or right_label is None:
                pass
            else:
                compared.append((audit_id, bool(left_label), bool(right_label)))
            left_semantic = str(labels[left].get("label_semantic") or "").strip()
            right_semantic = str(labels[right].get("label_semantic") or "").strip()
            if left_semantic and right_semantic:
                semantic_compared.append((audit_id, left_semantic, right_semantic))
        agree = sum(l == r for _, l, r in compared)
        semantic_agree = sum(l == r for _, l, r in semantic_compared)
        for audit_id, left_label, right_label in compared:
            if left_label != right_label:
                conflicts.append(
                    {
                        "audit_id": audit_id,
                        left: left_label,
                        right: right_label,
                    }
                )
        for audit_id, left_label, right_label in semantic_compared:
            if left_label != right_label:
                semantic_conflicts.append(
                    {
                        "audit_id": audit_id,
                        left: left_label,
                        right: right_label,
                    }
                )
        pairwise.append(
            {
                "auditors": [left, right],
                "compared": len(compared),
                "agreements": agree,
                "agreement_rate": agree / len(compared) if compared else None,
                "cohen_kappa": _cohen_kappa([(l, r) for _, l, r in compared]),
                "gwet_ac1": _gwet_ac1([(l, r) for _, l, r in compared]),
            }
        )
        semantic_pairwise.append(
            {
                "auditors": [left, right],
                "compared": len(semantic_compared),
                "agreements": semantic_agree,
                "agreement_rate": semantic_agree / len(semantic_compared)
                if semantic_compared
                else None,
                "gwet_ac1": _gwet_ac1([(l, r) for _, l, r in semantic_compared]),
            }
        )

    return {
        "input": str(merged_labels_path),
        "rows": len(rows),
        "audit_items": len(by_audit),
        "auditors": auditors,
        "completion": completion,
        "pairwise": pairwise,
        "conflicts": conflicts,
        "semantic_pairwise": semantic_pairwise,
        "semantic_conflicts": semantic_conflicts,
    }


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line in src:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _cohen_kappa(pairs: list[tuple[bool, bool]]) -> float | None:
    if not pairs:
        return None
    observed = sum(left == right for left, right in pairs) / len(pairs)
    left_true = sum(left for left, _ in pairs) / len(pairs)
    right_true = sum(right for _, right in pairs) / len(pairs)
    expected = left_true * right_true + (1 - left_true) * (1 - right_true)
    if expected == 1:
        return 1.0 if observed == 1 else None
    return (observed - expected) / (1 - expected)


def _gwet_ac1(pairs: list[tuple[Any, Any]]) -> float | None:
    if not pairs:
        return None
    observed = sum(left == right for left, right in pairs) / len(pairs)
    ratings = [label for pair in pairs for label in pair]
    categories = sorted({str(label) for label in ratings})
    if len(categories) <= 1:
        return observed
    total = len(ratings)
    proportions = [
        sum(str(label) == category for label in ratings) / total
        for category in categories
    ]
    chance = sum(p * (1 - p) for p in proportions) / (len(categories) - 1)
    if chance == 1:
        return 1.0 if observed == 1 else None
    return (observed - chance) / (1 - chance)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--merged-labels", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = compute_agreement_v4(args.merged_labels)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
