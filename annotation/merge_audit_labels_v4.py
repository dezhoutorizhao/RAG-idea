#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


REQUIRED_COLUMNS = {"audit_id", "auditor_id", "label_answerable"}
TRUE_VALUES = {"true", "yes", "1", "answerable", "supported"}
FALSE_VALUES = {"false", "no", "0", "fragile", "unanswerable", "unsupported", "insufficient"}
UNSURE_VALUES = {"", "unsure", "unknown", "unclear"}


def merge_audit_labels_v4(
    manifest_path: Path,
    label_csvs: list[Path],
    output_path: Path,
) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    hidden_by_audit_id = {
        str(item["audit_id"]): item for item in manifest.get("audit_items", [])
    }
    if not hidden_by_audit_id:
        raise ValueError(f"{manifest_path} has no audit_items mapping")
    if not label_csvs:
        raise ValueError("at least one labels CSV is required")

    rows = []
    seen: set[tuple[str, str]] = set()
    for labels_csv in label_csvs:
        for row in _load_csv(labels_csv):
            audit_id = str(row.get("audit_id") or "").strip()
            auditor_id = str(row.get("auditor_id") or "").strip()
            if audit_id not in hidden_by_audit_id:
                raise ValueError(f"{labels_csv} contains unknown audit_id {audit_id!r}")
            key = (audit_id, auditor_id)
            if key in seen:
                raise ValueError(f"duplicate label for audit_id={audit_id} auditor_id={auditor_id}")
            seen.add(key)
            hidden = hidden_by_audit_id[audit_id]
            label_text = str(row.get("label_answerable") or "").strip()
            rows.append(
                {
                    "audit_id": audit_id,
                    "auditor_id": auditor_id,
                    "dataset": row.get("dataset") or hidden.get("dataset") or "",
                    "label_answerable": label_text,
                    "label_answerable_bool": _parse_label(label_text),
                    "failure_type": str(row.get("failure_type") or "").strip(),
                    "confidence": str(row.get("confidence") or "").strip(),
                    "notes": str(row.get("notes") or "").strip(),
                    "orbit_id": hidden.get("orbit_id"),
                    "source_item_group_id": hidden.get("source_item_group_id"),
                    "expected_label_answerable": hidden.get("expected_label_answerable"),
                    "construction_type": hidden.get("construction_type"),
                    "label_source": hidden.get("label_source"),
                    "heuristic_label": hidden.get("heuristic_label"),
                    "support_key": hidden.get("support_key"),
                    "gold_answer": hidden.get("gold_answer"),
                }
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as dst:
        for row in rows:
            dst.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    labeled = sum(row["label_answerable_bool"] is not None for row in rows)
    return {
        "manifest": str(manifest_path),
        "label_csvs": [str(path) for path in label_csvs],
        "output": str(output_path),
        "rows": len(rows),
        "labeled": labeled,
        "pending_or_unsure": len(rows) - labeled,
    }


def _load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as src:
        reader = csv.DictReader(src)
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - fieldnames)
        if missing:
            raise ValueError(f"{path} is missing required columns: {missing}")
        if "orbit_id" in fieldnames or "construction_type" in fieldnames:
            raise ValueError(f"{path} appears unblinded; remove orbit/construction columns")
        return [dict(row) for row in reader]


def _parse_label(value: Any) -> bool | None:
    normalized = str(value or "").strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    if normalized in UNSURE_VALUES:
        return None
    raise ValueError(f"unknown label_answerable value {value!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--labels-csv", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = merge_audit_labels_v4(args.manifest, args.labels_csv, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
