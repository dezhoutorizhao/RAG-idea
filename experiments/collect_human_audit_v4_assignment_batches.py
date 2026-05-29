#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from annotation.adjudicate_labels_v4 import adjudicate_labels_v4
from annotation.compute_agreement_v4 import compute_agreement_v4
from annotation.merge_audit_labels_v4 import merge_audit_labels_v4
from experiments.check_audit_readiness import check_audit_readiness
from experiments.materialize_human_audit_v4_assignment_batches import (
    DEFAULT_PACK_NAME,
    LABEL_COLUMNS,
)


DEFAULT_ASSIGNMENT_MANIFEST = Path(
    "results/human_audit_v4_batches/v4_paper1000_mixed_blind1000.assignment_manifest.json"
)
DEFAULT_OUTPUT_DIR = Path("results/human_audit_v4_collection")


def collect_human_audit_v4_assignment_batches(
    assignment_manifest_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    assignment = _load_json(assignment_manifest_path)
    source_manifest = Path(assignment["source_manifest"])
    if not source_manifest.is_absolute():
        source_manifest = ROOT / source_manifest
    source_items = _source_audit_ids(source_manifest)
    pack_name = str(assignment.get("pack_name") or DEFAULT_PACK_NAME)
    output_dir.mkdir(parents=True, exist_ok=True)

    collected_label_csvs = []
    auditor_summaries = []
    for auditor_id in assignment.get("auditors", []):
        batches = [
            batch
            for batch in assignment.get("batches", [])
            if str(batch.get("auditor_id") or "") == auditor_id
        ]
        batches = sorted(batches, key=lambda batch: int(batch.get("batch_index") or 0))
        rows = []
        for batch in batches:
            labels_csv = Path(batch["labels_csv"])
            if not labels_csv.is_absolute():
                labels_csv = ROOT / labels_csv
            rows.extend(_load_label_rows(labels_csv, auditor_id))
        audit_ids = [row["audit_id"] for row in rows]
        if audit_ids != source_items:
            raise ValueError(f"collected audit_id order for {auditor_id} does not match source pack")
        collected = output_dir / f"{pack_name}.{auditor_id}.collected.labels.csv"
        _write_label_csv(collected, rows)
        collected_label_csvs.append(collected)
        labeled = sum(_row_has_label(row) for row in rows)
        auditor_summaries.append(
            {
                "auditor_id": auditor_id,
                "batch_count": len(batches),
                "rows": len(rows),
                "labeled": labeled,
                "pending": len(rows) - labeled,
                "completion_rate": labeled / len(rows) if rows else None,
                "collected_labels_csv": str(collected),
            }
        )

    merged_path = output_dir / f"{pack_name}.merged_labels.jsonl"
    agreement_path = output_dir / f"{pack_name}.agreement.json"
    adjudicated_path = output_dir / f"{pack_name}.adjudicated_labels.jsonl"
    template_path = output_dir / f"{pack_name}.adjudication_template.csv"
    readiness_path = output_dir / f"{pack_name}.readiness.json"

    merge_summary = merge_audit_labels_v4(source_manifest, collected_label_csvs, merged_path)
    agreement = compute_agreement_v4(merged_path)
    _write_json(agreement_path, agreement)
    adjudication = adjudicate_labels_v4(merged_path, adjudicated_path, template_csv=template_path)
    readiness = check_audit_readiness(
        adjudicated_path,
        min_labeled_total=len(source_items),
        min_labeled_per_split=max(1, len(source_items) // 2),
        label_field="adjudicated_label_answerable",
        require_disagreement_notes=False,
    )
    _write_json(readiness_path, readiness)

    collection_ready = bool(auditor_summaries) and all(
        summary["rows"] == len(source_items) for summary in auditor_summaries
    )
    human_labels_complete = bool(auditor_summaries) and all(
        summary["pending"] == 0 for summary in auditor_summaries
    )
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pack_name": pack_name,
        "assignment_manifest": str(assignment_manifest_path),
        "source_manifest": str(source_manifest),
        "output_dir": str(output_dir),
        "source_item_count": len(source_items),
        "auditor_summaries": auditor_summaries,
        "collection_ready": collection_ready,
        "human_labels_complete": human_labels_complete,
        "pending_auditor_labels": sum(item["pending"] for item in auditor_summaries),
        "pending_adjudicated_labels": readiness["pending"],
        "artifacts": {
            "collected_label_csvs": [str(path) for path in collected_label_csvs],
            "merged_labels": str(merged_path),
            "agreement": str(agreement_path),
            "adjudicated_labels": str(adjudicated_path),
            "adjudication_template": str(template_path),
            "readiness": str(readiness_path),
        },
        "merge_summary": merge_summary,
        "agreement_summary": {
            "audit_items": agreement["audit_items"],
            "auditors": agreement["auditors"],
            "pairwise": agreement["pairwise"],
            "semantic_pairwise": agreement["semantic_pairwise"],
        },
        "adjudication_summary": adjudication,
        "readiness_summary": readiness,
        "claim_policy": (
            "This collects completed assignment batches into merge/adjudication artifacts. "
            "It supports human-audit claims only when human_labels_complete and readiness.ready "
            "are both true."
        ),
    }
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Human Audit V4 Batch Collection",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Pack name: `{summary['pack_name']}`",
        f"Source items: `{summary['source_item_count']}`",
        f"Collection ready: `{summary['collection_ready']}`",
        f"Human labels complete: `{summary['human_labels_complete']}`",
        f"Pending auditor labels: `{summary['pending_auditor_labels']}`",
        f"Pending adjudicated labels: `{summary['pending_adjudicated_labels']}`",
        "",
        "## Auditors",
        "",
        "| Auditor | Batches | Rows | Labeled | Pending | Completion |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for auditor in summary["auditor_summaries"]:
        completion = auditor["completion_rate"]
        completion_text = "" if completion is None else f"{completion:.3f}"
        lines.append(
            f"| {auditor['auditor_id']} | {auditor['batch_count']} | {auditor['rows']} | "
            f"{auditor['labeled']} | {auditor['pending']} | `{completion_text}` |"
        )
    lines.extend(["", "## Artifacts", ""])
    for name, value in summary["artifacts"].items():
        if isinstance(value, list):
            for index, path in enumerate(value, start=1):
                lines.append(f"- {name}[{index}]: `{path}`")
        else:
            lines.append(f"- {name}: `{value}`")
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _source_audit_ids(manifest_path: Path) -> list[str]:
    manifest = _load_json(manifest_path)
    audit_ids = [str(item.get("audit_id") or "").strip() for item in manifest.get("audit_items", [])]
    if not audit_ids:
        raise ValueError(f"{manifest_path} has no audit_items")
    if len(audit_ids) != len(set(audit_ids)):
        raise ValueError(f"{manifest_path} contains duplicate audit_id values")
    return audit_ids


def _load_label_rows(path: Path, auditor_id: str) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as src:
        reader = csv.DictReader(src)
        fieldnames = set(reader.fieldnames or [])
        missing = [column for column in ["audit_id", "auditor_id"] if column not in fieldnames]
        if missing:
            raise ValueError(f"{path} is missing required columns: {missing}")
        rows = [dict(row) for row in reader]
    for index, row in enumerate(rows, start=2):
        if str(row.get("auditor_id") or "").strip() != auditor_id:
            raise ValueError(f"{path}:{index} has unexpected auditor_id={row.get('auditor_id')!r}")
    return rows


def _row_has_label(row: dict[str, str]) -> bool:
    return bool(str(row.get("label_semantic") or "").strip() or str(row.get("label_answerable") or "").strip())


def _write_label_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(dst, fieldnames=LABEL_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in LABEL_COLUMNS})


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignment-manifest", type=Path, default=DEFAULT_ASSIGNMENT_MANIFEST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = collect_human_audit_v4_assignment_batches(
        args.assignment_manifest,
        args.output_dir,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
