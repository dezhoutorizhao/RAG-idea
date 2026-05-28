#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

try:
    from annotation.merge_audit_labels_v4 import FALSE_VALUES, TRUE_VALUES, UNSURE_VALUES
except ModuleNotFoundError:
    from merge_audit_labels_v4 import FALSE_VALUES, TRUE_VALUES, UNSURE_VALUES


def adjudicate_labels_v4(
    merged_labels_path: Path,
    output_path: Path,
    *,
    template_csv: Path | None = None,
    adjudication_csv: Path | None = None,
) -> dict[str, Any]:
    rows = _load_jsonl(merged_labels_path)
    if not rows:
        raise ValueError(f"{merged_labels_path} contains no labels")
    by_audit: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_audit.setdefault(str(row["audit_id"]), []).append(row)

    manual = _load_adjudication_csv(adjudication_csv) if adjudication_csv else {}
    output_rows = []
    template_rows = []
    for audit_id, labels in sorted(by_audit.items()):
        bool_labels = [row.get("label_answerable_bool") for row in labels]
        known = [label for label in bool_labels if label is not None]
        base = labels[0]
        if audit_id in manual:
            adjudicated = manual[audit_id]["adjudicated_label_answerable"]
            status = "manual"
            notes = manual[audit_id].get("adjudication_notes") or ""
        elif known and all(label == known[0] for label in known) and len(known) == len(labels):
            adjudicated = known[0]
            status = "auto_agree"
            notes = ""
        else:
            adjudicated = None
            status = "pending"
            notes = ""
            template_rows.append(_template_row(audit_id, labels))
        output_rows.append(
            {
                "audit_id": audit_id,
                "orbit_id": base.get("orbit_id"),
                "dataset": base.get("dataset"),
                "adjudicated_label_answerable": adjudicated,
                "adjudication_status": status,
                "adjudication_notes": notes,
                "expected_label_answerable": base.get("expected_label_answerable"),
                "construction_type": base.get("construction_type"),
                "auditor_labels": [
                    {
                        "auditor_id": row.get("auditor_id"),
                        "label_answerable_bool": row.get("label_answerable_bool"),
                        "failure_type": row.get("failure_type"),
                        "confidence": row.get("confidence"),
                        "notes": row.get("notes"),
                    }
                    for row in labels
                ],
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as dst:
        for row in output_rows:
            dst.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    if template_csv:
        template_csv.parent.mkdir(parents=True, exist_ok=True)
        _write_template_csv(template_csv, template_rows)

    return {
        "merged_labels": str(merged_labels_path),
        "output": str(output_path),
        "template_csv": str(template_csv) if template_csv else None,
        "items": len(output_rows),
        "auto_agree": sum(row["adjudication_status"] == "auto_agree" for row in output_rows),
        "manual": sum(row["adjudication_status"] == "manual" for row in output_rows),
        "pending": sum(row["adjudication_status"] == "pending" for row in output_rows),
    }


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line in src:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _template_row(audit_id: str, labels: list[dict[str, Any]]) -> dict[str, str]:
    label_text = "; ".join(
        f"{row.get('auditor_id')}={row.get('label_answerable')}:{row.get('notes') or ''}"
        for row in labels
    )
    return {
        "audit_id": audit_id,
        "auditor_labels": label_text,
        "adjudicated_label_answerable": "",
        "adjudication_notes": "",
    }


def _write_template_csv(path: Path, rows: list[dict[str, str]]) -> None:
    columns = ["audit_id", "auditor_labels", "adjudicated_label_answerable", "adjudication_notes"]
    with path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(dst, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _load_adjudication_csv(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    rows = {}
    with path.open("r", newline="", encoding="utf-8-sig") as src:
        reader = csv.DictReader(src)
        for row_no, row in enumerate(reader, start=2):
            audit_id = str(row.get("audit_id") or "").strip()
            if not audit_id:
                continue
            if audit_id in rows:
                raise ValueError(f"{path}:{row_no} duplicates audit_id {audit_id}")
            rows[audit_id] = {
                "adjudicated_label_answerable": _parse_label(row.get("adjudicated_label_answerable")),
                "adjudication_notes": str(row.get("adjudication_notes") or "").strip(),
            }
    return rows


def _parse_label(value: Any) -> bool | None:
    normalized = str(value or "").strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    if normalized in UNSURE_VALUES:
        return None
    raise ValueError(f"unknown adjudicated label {value!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--merged-labels", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--template-csv", type=Path)
    parser.add_argument("--adjudication-csv", type=Path)
    args = parser.parse_args()

    result = adjudicate_labels_v4(
        args.merged_labels,
        args.output,
        template_csv=args.template_csv,
        adjudication_csv=args.adjudication_csv,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
