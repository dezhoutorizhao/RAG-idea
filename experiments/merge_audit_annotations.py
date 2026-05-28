#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


EDITABLE_COLUMNS = {
    "auditor_label_answerable",
    "auditor_failure_type",
    "auditor_notes",
    "auditor2_label_answerable",
    "auditor2_failure_type",
    "auditor2_notes",
    "adjudicated_label_answerable",
    "adjudication_notes",
}
TRUE_VALUES = {"true", "yes", "1", "answerable", "supported"}
FALSE_VALUES = {"false", "no", "0", "unanswerable", "unsupported", "insufficient"}


def merge_audit_annotations(input_path: Path, labels_csv: Path, output_path: Path) -> dict:
    if input_path.resolve() == output_path.resolve():
        raise ValueError("input and output paths must differ to avoid overwriting the audit file")
    annotations = _load_annotations(labels_csv)
    updated = 0
    total = 0
    seen = set()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open("r", encoding="utf-8") as src, output_path.open(
        "w", encoding="utf-8"
    ) as dst:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            total += 1
            item = json.loads(line)
            orbit_id = str(item.get("orbit_id") or "")
            if orbit_id in annotations:
                seen.add(orbit_id)
                annotation = annotations[orbit_id]
                for column in EDITABLE_COLUMNS:
                    if column not in annotation:
                        continue
                    if column in {
                        "auditor_label_answerable",
                        "auditor2_label_answerable",
                        "adjudicated_label_answerable",
                    }:
                        item[column] = _normalize_label(annotation[column])
                    else:
                        item[column] = annotation[column].strip() or None
                updated += 1
            dst.write(json.dumps(item, ensure_ascii=False) + "\n")

    unused = sorted(set(annotations) - seen)
    if unused:
        raise ValueError(
            f"{labels_csv} contains orbit_id values not found in {input_path}: "
            + ", ".join(unused[:5])
        )
    return {
        "input": str(input_path),
        "labels_csv": str(labels_csv),
        "output": str(output_path),
        "total": total,
        "updated": updated,
    }


def _load_annotations(labels_csv: Path) -> dict[str, dict[str, str]]:
    annotations: dict[str, dict[str, str]] = {}
    with labels_csv.open("r", newline="", encoding="utf-8-sig") as src:
        reader = csv.DictReader(src)
        if "orbit_id" not in (reader.fieldnames or []):
            raise ValueError(f"{labels_csv} is missing required orbit_id column")
        editable_columns = EDITABLE_COLUMNS & set(reader.fieldnames or [])
        if not editable_columns:
            raise ValueError(
                f"{labels_csv} must include at least one editable column: "
                f"{sorted(EDITABLE_COLUMNS)}"
            )
        for row_no, row in enumerate(reader, start=2):
            orbit_id = str(row.get("orbit_id") or "").strip()
            if not orbit_id:
                continue
            if orbit_id in annotations:
                raise ValueError(f"{labels_csv}:{row_no} duplicates orbit_id {orbit_id}")
            annotations[orbit_id] = {
                column: str(row.get(column) or "") for column in editable_columns
            }
    return annotations


def _normalize_label(value: Any) -> bool | None:
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if not normalized:
        return None
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return str(value).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--labels-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = merge_audit_annotations(args.input, args.labels_csv, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
