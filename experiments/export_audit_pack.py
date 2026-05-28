#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import json
import random
from pathlib import Path


LABEL_COLUMNS = [
    "orbit_id",
    "split",
    "expected_label_answerable",
    "auditor_label_answerable",
    "auditor_failure_type",
    "auditor_notes",
    "auditor2_label_answerable",
    "auditor2_failure_type",
    "auditor2_notes",
    "adjudicated_label_answerable",
    "adjudication_notes",
]
ANNOTATOR_COLUMNS = {
    "auditor1": [
        "orbit_id",
        "split",
        "auditor_label_answerable",
        "auditor_failure_type",
        "auditor_notes",
    ],
    "auditor2": [
        "orbit_id",
        "split",
        "auditor2_label_answerable",
        "auditor2_failure_type",
        "auditor2_notes",
    ],
}


def export_audit_pack(
    input_path: Path,
    output_prefix: Path,
    *,
    blind: bool = False,
    shuffle_seed: int | None = None,
    annotator: str = "auditor1",
) -> dict:
    items = _load_items(input_path)
    if not items:
        raise ValueError(f"{input_path} contains no audit records")
    if annotator not in ANNOTATOR_COLUMNS:
        raise ValueError(f"unknown annotator {annotator!r}; expected auditor1 or auditor2")
    ordered_items = list(items)
    if shuffle_seed is not None:
        random.Random(shuffle_seed).shuffle(ordered_items)

    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    suffix = ".blind" if blind else ""
    csv_path = output_prefix.with_suffix(f"{suffix}.labels.csv")
    html_path = output_prefix.with_suffix(f"{suffix}.review.html")
    manifest_path = output_prefix.with_suffix(f"{suffix}.manifest.json")

    if blind:
        _write_blind_label_csv(csv_path, ordered_items, annotator)
    else:
        _write_label_csv(csv_path, ordered_items)
    _write_review_html(html_path, input_path, csv_path, ordered_items, blind=blind)
    manifest = {
        "input": str(input_path),
        "items": len(ordered_items),
        "label_csv": str(csv_path),
        "review_html": str(html_path),
        "blind": blind,
        "shuffle_seed": shuffle_seed,
        "annotator": annotator if blind else None,
        "review_order": [item.get("orbit_id") for item in ordered_items],
        "columns_to_edit": _editable_columns(blind, annotator),
    }
    if blind:
        manifest["hidden_fields"] = [
            "expected_label_answerable",
            "clean.label_answerable",
            "perturbations[].label_answerable",
            "docs[].corm_score",
            "docs[].support",
            "docs[].conflict",
            "docs[].missing",
        ]
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest | {"manifest": str(manifest_path)}


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


def _write_label_csv(csv_path: Path, items: list[dict]) -> None:
    with csv_path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(dst, fieldnames=LABEL_COLUMNS)
        writer.writeheader()
        for item in items:
            writer.writerow(
                {
                    "orbit_id": item.get("orbit_id"),
                    "split": item.get("split"),
                    "expected_label_answerable": _label_to_text(
                        item.get("expected_label_answerable")
                    ),
                    "auditor_label_answerable": _label_to_text(
                        item.get("auditor_label_answerable")
                    ),
                    "auditor_failure_type": item.get("auditor_failure_type") or "",
                    "auditor_notes": item.get("auditor_notes") or "",
                    "auditor2_label_answerable": _label_to_text(
                        item.get("auditor2_label_answerable")
                    ),
                    "auditor2_failure_type": item.get("auditor2_failure_type") or "",
                    "auditor2_notes": item.get("auditor2_notes") or "",
                    "adjudicated_label_answerable": _label_to_text(
                        item.get("adjudicated_label_answerable")
                    ),
                    "adjudication_notes": item.get("adjudication_notes") or "",
                }
            )


def _write_blind_label_csv(csv_path: Path, items: list[dict], annotator: str) -> None:
    columns = ANNOTATOR_COLUMNS[annotator]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(dst, fieldnames=columns)
        writer.writeheader()
        for item in items:
            writer.writerow({column: _blind_csv_value(item, column) for column in columns})


def _blind_csv_value(item: dict, column: str) -> str:
    if column == "orbit_id":
        return str(item.get("orbit_id") or "")
    if column == "split":
        return str(item.get("split") or "")
    if column in {"auditor_label_answerable", "auditor2_label_answerable"}:
        return _label_to_text(item.get(column))
    return str(item.get(column) or "")


def _write_review_html(
    html_path: Path,
    input_path: Path,
    csv_path: Path,
    items: list[dict],
    *,
    blind: bool,
) -> None:
    split_counts: dict[str, int] = {}
    for item in items:
        split = str(item.get("split") or "unknown")
        split_counts[split] = split_counts.get(split, 0) + 1

    body = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'>",
        "<title>CSRM-RAG Audit Pack</title>",
        "<style>",
        "body{font-family:Arial,sans-serif;line-height:1.45;margin:24px;max-width:1200px}",
        "table{border-collapse:collapse;width:100%;margin:12px 0}",
        "th,td{border:1px solid #ccc;padding:6px;vertical-align:top}",
        "th{background:#f2f2f2}",
        ".orbit{border-top:3px solid #333;margin-top:24px;padding-top:16px}",
        ".set{border:1px solid #bbb;margin:12px 0;padding:10px}",
        ".doc{margin:8px 0;padding:8px;background:#fafafa;border-left:3px solid #bbb}",
        ".meta{color:#555;font-size:0.92em}",
        "code{background:#f4f4f4;padding:1px 3px}",
        "</style></head><body>",
        "<h1>CSRM-RAG Audit Pack</h1>",
        f"<p><b>Source JSONL:</b> <code>{html.escape(str(input_path))}</code></p>",
        f"<p><b>Label CSV:</b> <code>{html.escape(str(csv_path))}</code></p>",
        _instruction_text(blind),
        "<h2>Split Counts</h2>",
        "<table><tr><th>Split</th><th>Count</th></tr>",
    ]
    for split, count in sorted(split_counts.items()):
        body.append(f"<tr><td>{html.escape(split)}</td><td>{count}</td></tr>")
    body.extend(["</table>", "<h2>Audit Items</h2>"])

    for index, item in enumerate(items, start=1):
        body.append(_render_item(index, item, blind=blind))
    body.append("</body></html>")
    html_path.write_text("\n".join(body), encoding="utf-8")


def _instruction_text(blind: bool) -> str:
    if blind:
        return (
            "<p>Edit only the annotator label, failure-type, and notes columns in the CSV. "
            "This blind view hides expected labels, source answerability labels, and model scores.</p>"
        )
    return (
        "<p>Edit only the auditor/adjudication label, failure-type, and notes columns in the CSV. "
        "Use this HTML as read-only evidence context.</p>"
    )


def _render_item(index: int, item: dict, *, blind: bool) -> str:
    rows = [
        _row("Split", item.get("split")),
        _row("Answer / label", item.get("answer")),
        _row("Source", item.get("source")),
    ]
    if not blind:
        rows.insert(
            1,
            _row("Expected answerable", _label_to_text(item.get("expected_label_answerable"))),
        )
    parts = [
        f"<section class='orbit' id='{html.escape(str(item.get('orbit_id')))}'>",
        f"<h3>{index}. {html.escape(str(item.get('orbit_id')))}</h3>",
        "<table>",
        *rows,
        "</table>",
        _render_set("Clean", item.get("clean") or {}, blind=blind),
    ]
    for pert_index, perturbation in enumerate(item.get("perturbations", []), start=1):
        parts.append(_render_set(f"Perturbation {pert_index}", perturbation, blind=blind))
    parts.append("</section>")
    return "\n".join(parts)


def _render_set(title: str, evidence_set: dict, *, blind: bool) -> str:
    rows = [
        _row("Query", evidence_set.get("query")),
        _row("Support key", evidence_set.get("support_key")),
        _row("Perturbation type", evidence_set.get("perturbation_type")),
    ]
    if not blind:
        rows.insert(
            1,
            _row("Original label_answerable", _label_to_text(evidence_set.get("label_answerable"))),
        )
    parts = [
        "<div class='set'>",
        f"<h4>{html.escape(title)}</h4>",
        "<table>",
        *rows,
        "</table>",
    ]
    for doc in evidence_set.get("docs", []):
        parts.append(_render_doc(doc, blind=blind))
    parts.append("</div>")
    return "\n".join(parts)


def _render_doc(doc: dict, *, blind: bool) -> str:
    title = doc.get("title") or doc.get("doc_id") or ""
    if blind:
        meta = f"rank={doc.get('rank')}"
    else:
        meta = (
            f"rank={doc.get('rank')} | corm={_fmt(doc.get('corm_score'))} | "
            f"support={_fmt(doc.get('support'))} | conflict={_fmt(doc.get('conflict'))} | "
            f"missing={_fmt(doc.get('missing'))}"
        )
    return (
        "<div class='doc'>"
        f"<div><b>{html.escape(str(title))}</b></div>"
        f"<div class='meta'>{html.escape(meta)}</div>"
        f"<div>{html.escape(str(doc.get('text') or ''))}</div>"
        "</div>"
    )


def _row(label: str, value: object) -> str:
    return (
        f"<tr><th>{html.escape(label)}</th>"
        f"<td>{html.escape('' if value is None else str(value))}</td></tr>"
    )


def _label_to_text(value: object) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return ""
    return str(value)


def _fmt(value: object) -> str:
    try:
        return f"{float(value):.4f}"
    except (TypeError, ValueError):
        return ""


def _editable_columns(blind: bool, annotator: str) -> list[str]:
    if blind:
        return [column for column in ANNOTATOR_COLUMNS[annotator] if column not in {"orbit_id", "split"}]
    return [
        "auditor_label_answerable",
        "auditor_failure_type",
        "auditor_notes",
        "auditor2_label_answerable",
        "auditor2_failure_type",
        "auditor2_notes",
        "adjudicated_label_answerable",
        "adjudication_notes",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--blind", action="store_true")
    parser.add_argument("--shuffle-seed", type=int)
    parser.add_argument(
        "--annotator",
        choices=sorted(ANNOTATOR_COLUMNS),
        default="auditor1",
        help="Annotator columns to expose when --blind is set.",
    )
    args = parser.parse_args()

    manifest = export_audit_pack(
        args.input,
        args.output_prefix,
        blind=args.blind,
        shuffle_seed=args.shuffle_seed,
        annotator=args.annotator,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
