#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_PACK_NAME = "v4_paper1000_mixed_blind1000"
DEFAULT_AUDIT_DIR = Path("results/human_audit_v4")
DEFAULT_OUTPUT_DIR = Path("results/human_audit_v4_batches")
DEFAULT_BATCH_SIZE = 200
FORBIDDEN_PUBLIC_KEYS = {
    "adjudicated_label_answerable",
    "construction_type",
    "expected_label_answerable",
    "gold_answer",
    "heuristic_label",
    "human_label",
    "is_support",
    "label_answerable",
    "source_item_group_id",
    "support_key",
}
ALLOWED_LABEL_COLUMNS = {
    "audit_id",
    "dataset",
    "auditor_id",
    "label_semantic",
    "label_answerable",
    "failure_type",
    "confidence",
    "notes",
}
LABEL_COLUMNS = [
    "audit_id",
    "dataset",
    "auditor_id",
    "label_semantic",
    "label_answerable",
    "failure_type",
    "confidence",
    "notes",
]


def materialize_human_audit_v4_assignment_batches(
    audit_dir: Path,
    output_dir: Path,
    *,
    pack_name: str = DEFAULT_PACK_NAME,
    batch_size: int = DEFAULT_BATCH_SIZE,
    preserve_existing_labels: bool = True,
) -> dict[str, Any]:
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    items_path = audit_dir / f"{pack_name}.items.jsonl"
    manifest_path = audit_dir / f"{pack_name}.manifest.json"
    source_manifest = _load_json(manifest_path)
    public_items = _load_jsonl(items_path)
    if not public_items:
        raise ValueError(f"{items_path} contains no public audit items")

    audit_ids = [str(item.get("audit_id") or "") for item in public_items]
    if len(audit_ids) != len(set(audit_ids)):
        raise ValueError(f"{items_path} contains duplicate audit_id values")
    for item in public_items:
        _assert_no_forbidden_public_keys(item)

    label_csvs = {
        auditor_id: Path(path)
        for auditor_id, path in (source_manifest.get("label_csvs") or {}).items()
    }
    if not label_csvs:
        raise ValueError(f"{manifest_path} has no label_csvs")

    output_dir.mkdir(parents=True, exist_ok=True)
    batches: list[dict[str, Any]] = []
    coverage_by_auditor: dict[str, dict[str, Any]] = {}
    for auditor_id, label_path in sorted(label_csvs.items()):
        absolute_label_path = label_path if label_path.is_absolute() else manifest_path.parent / label_path.name
        label_rows = _load_label_rows(absolute_label_path, auditor_id)
        labels_by_id = _label_rows_by_id(label_rows, absolute_label_path)
        missing = [audit_id for audit_id in audit_ids if audit_id not in labels_by_id]
        extra = sorted(set(labels_by_id) - set(audit_ids))
        if missing or extra:
            raise ValueError(
                f"{absolute_label_path} is misaligned with public items: "
                f"missing={missing[:5]}, extra={extra[:5]}"
            )

        auditor_seen: list[str] = []
        for batch_index, start in enumerate(range(0, len(public_items), batch_size), start=1):
            batch_items = public_items[start : start + batch_size]
            batch_audit_ids = [str(item["audit_id"]) for item in batch_items]
            batch_label_rows = [labels_by_id[audit_id] for audit_id in batch_audit_ids]
            prefix = f"{pack_name}.{auditor_id}.batch{batch_index:02d}"
            batch_items_path = output_dir / f"{prefix}.items.jsonl"
            batch_labels_path = output_dir / f"{prefix}.labels.csv"
            batch_review_path = output_dir / f"{prefix}.review.html"

            labels_preserved = False
            if preserve_existing_labels and batch_labels_path.exists():
                existing_rows = _load_label_rows(batch_labels_path, auditor_id)
                existing_ids = [str(row.get("audit_id") or "").strip() for row in existing_rows]
                if existing_ids != batch_audit_ids:
                    raise ValueError(
                        f"{batch_labels_path} exists but does not match expected audit_id order"
                    )
                batch_label_rows = existing_rows
                labels_preserved = True

            _write_jsonl(batch_items_path, batch_items)
            _write_label_csv(batch_labels_path, batch_label_rows)
            _write_review_html(batch_review_path, batch_items, auditor_id=auditor_id, batch_id=prefix)

            batch_row = {
                "batch_id": prefix,
                "auditor_id": auditor_id,
                "batch_index": batch_index,
                "item_count": len(batch_items),
                "audit_id_start": batch_audit_ids[0],
                "audit_id_end": batch_audit_ids[-1],
                "items_jsonl": str(batch_items_path),
                "labels_csv": str(batch_labels_path),
                "labels_preserved": labels_preserved,
                "review_html": str(batch_review_path),
                "artifacts": {
                    "items_jsonl": _artifact_row(batch_items_path),
                    "labels_csv": _artifact_row(batch_labels_path),
                    "review_html": _artifact_row(batch_review_path),
                },
            }
            batches.append(batch_row)
            auditor_seen.extend(batch_audit_ids)

        coverage_by_auditor[auditor_id] = {
            "items_assigned": len(auditor_seen),
            "unique_items_assigned": len(set(auditor_seen)),
            "covers_all_source_items_once": auditor_seen == audit_ids,
            "batch_count": (len(public_items) + batch_size - 1) // batch_size,
        }

    assignment_manifest_path = output_dir / f"{pack_name}.assignment_manifest.json"
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pack_name": pack_name,
        "source_manifest": str(manifest_path),
        "source_items_jsonl": str(items_path),
        "output_dir": str(output_dir),
        "batch_size": batch_size,
        "preserve_existing_labels": preserve_existing_labels,
        "source_item_count": len(public_items),
        "auditors": sorted(label_csvs),
        "batch_count": len(batches),
        "batches_per_auditor": (len(public_items) + batch_size - 1) // batch_size,
        "total_assignment_rows": len(public_items) * len(label_csvs),
        "coverage_by_auditor": coverage_by_auditor,
        "assignment_ready": bool(label_csvs)
        and all(row["covers_all_source_items_once"] for row in coverage_by_auditor.values()),
        "assignment_manifest": str(assignment_manifest_path),
        "batches": batches,
        "claim_policy": (
            "These are execution batches for blind human annotation only. They preserve the "
            "pending-label status and do not support human-audited result claims until "
            "completed labels are merged and adjudicated."
        ),
    }
    _write_json(assignment_manifest_path, summary)
    summary["assignment_manifest_artifact"] = _artifact_row(assignment_manifest_path)
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Human Audit V4 Assignment Batches",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Pack name: `{summary['pack_name']}`",
        f"Source items: `{summary['source_item_count']}`",
        f"Auditors: `{summary['auditors']}`",
        f"Batch size: `{summary['batch_size']}`",
        f"Batch count: `{summary['batch_count']}`",
        f"Total assignment rows: `{summary['total_assignment_rows']}`",
        f"Assignment ready: `{summary['assignment_ready']}`",
        f"Assignment manifest: `{summary['assignment_manifest']}`",
        "",
        "## Coverage",
        "",
        "| Auditor | Batches | Items | Unique items | Covers all once |",
        "|---|---:|---:|---:|---|",
    ]
    for auditor_id, coverage in summary["coverage_by_auditor"].items():
        lines.append(
            f"| {auditor_id} | {coverage['batch_count']} | {coverage['items_assigned']} | "
            f"{coverage['unique_items_assigned']} | `{coverage['covers_all_source_items_once']}` |"
        )
    lines.extend(
        [
            "",
            "## Batches",
            "",
            "| Batch | Auditor | Items | Audit ID range | Labels CSV | Review HTML |",
            "|---|---|---:|---|---|---|",
        ]
    )
    for batch in summary["batches"]:
        lines.append(
            f"| {batch['batch_id']} | {batch['auditor_id']} | {batch['item_count']} | "
            f"`{batch['audit_id_start']}` to `{batch['audit_id_end']}` | "
            f"`{batch['labels_csv']}` | `{batch['review_html']}` |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _assert_no_forbidden_public_keys(obj: Any, path: str = "root") -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in FORBIDDEN_PUBLIC_KEYS:
                raise ValueError(f"forbidden public audit key at {path}.{key}")
            _assert_no_forbidden_public_keys(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            _assert_no_forbidden_public_keys(value, f"{path}[{index}]")


def _load_label_rows(path: Path, auditor_id: str) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"label CSV does not exist: {path}")
    with path.open(newline="", encoding="utf-8-sig") as src:
        reader = csv.DictReader(src)
        columns = set(reader.fieldnames or [])
        unknown = columns - ALLOWED_LABEL_COLUMNS
        if unknown:
            raise ValueError(f"{path} contains unknown label columns: {sorted(unknown)}")
        rows = [dict(row) for row in reader]
    for index, row in enumerate(rows, start=1):
        if str(row.get("auditor_id") or "") != auditor_id:
            raise ValueError(f"{path}:{index} has auditor_id={row.get('auditor_id')!r}")
    return rows


def _label_rows_by_id(rows: list[dict[str, str]], path: Path) -> dict[str, dict[str, str]]:
    by_id: dict[str, dict[str, str]] = {}
    for index, row in enumerate(rows, start=1):
        audit_id = str(row.get("audit_id") or "").strip()
        if not audit_id:
            raise ValueError(f"{path}:{index} is missing audit_id")
        if audit_id in by_id:
            raise ValueError(f"{path}:{index} duplicates audit_id {audit_id}")
        by_id[audit_id] = row
    return by_id


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line in src:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as dst:
        for row in rows:
            dst.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _write_label_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(dst, fieldnames=LABEL_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in LABEL_COLUMNS})


def _write_review_html(path: Path, items: list[dict[str, Any]], *, auditor_id: str, batch_id: str) -> None:
    body = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'>",
        f"<title>{html.escape(batch_id)}</title>",
        "<style>",
        "body{font-family:Arial,sans-serif;line-height:1.45;margin:24px;max-width:1200px}",
        "table{border-collapse:collapse;width:100%;margin:10px 0}",
        "th,td{border:1px solid #ccc;padding:6px;vertical-align:top}",
        "th{background:#f2f2f2;width:160px}",
        ".item{border-top:3px solid #333;margin-top:24px;padding-top:16px}",
        ".doc{margin:8px 0;padding:8px;background:#fafafa;border-left:3px solid #bbb}",
        ".meta{color:#555;font-size:0.92em}",
        "</style></head><body>",
        f"<h1>{html.escape(batch_id)}</h1>",
        f"<p class='meta'>Auditor: {html.escape(auditor_id)}. Items: {len(items)}.</p>",
    ]
    for item in items:
        body.extend(_render_item_html(item))
    body.extend(["</body></html>"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")


def _render_item_html(item: dict[str, Any]) -> list[str]:
    lines = [
        "<section class='item'>",
        f"<h2>{html.escape(str(item.get('audit_id') or ''))}</h2>",
        "<table>",
        f"<tr><th>Dataset</th><td>{html.escape(str(item.get('dataset') or ''))}</td></tr>",
        f"<tr><th>Query</th><td>{html.escape(str(item.get('query') or ''))}</td></tr>",
        f"<tr><th>Candidate answer</th><td>{html.escape(str(item.get('candidate_answer') or ''))}</td></tr>",
        "</table>",
        "<h3>Clean evidence</h3>",
    ]
    lines.extend(_render_docs(item.get("clean_evidence") or []))
    for index, perturbation in enumerate(item.get("perturbations") or [], start=1):
        lines.append(f"<h3>Perturbation {index}</h3>")
        lines.append(f"<p><b>Query:</b> {html.escape(str(perturbation.get('query') or ''))}</p>")
        lines.append(
            f"<p><b>Candidate answer:</b> "
            f"{html.escape(str(perturbation.get('candidate_answer') or ''))}</p>"
        )
        lines.extend(_render_docs(perturbation.get("evidence") or []))
    lines.append("</section>")
    return lines


def _render_docs(docs: list[dict[str, Any]]) -> list[str]:
    if not docs:
        return ["<p class='meta'>No evidence passages.</p>"]
    lines = []
    for doc in docs:
        title = html.escape(str(doc.get("title") or ""))
        rank = html.escape(str(doc.get("rank") if doc.get("rank") is not None else ""))
        text = html.escape(str(doc.get("text") or ""))
        lines.append(f"<div class='doc'><p class='meta'>Rank {rank}: {title}</p><p>{text}</p></div>")
    return lines


def _artifact_row(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else None,
        "sha256": _sha256(path) if path.exists() else None,
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-dir", type=Path, default=DEFAULT_AUDIT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--pack-name", default=DEFAULT_PACK_NAME)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--overwrite-existing-labels", action="store_true")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = materialize_human_audit_v4_assignment_batches(
        args.audit_dir,
        args.output_dir,
        pack_name=args.pack_name,
        batch_size=args.batch_size,
        preserve_existing_labels=not args.overwrite_existing_labels,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
