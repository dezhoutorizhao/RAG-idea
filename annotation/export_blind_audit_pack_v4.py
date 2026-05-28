#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import json
import random
from pathlib import Path
from typing import Any


CSV_COLUMNS = [
    "audit_id",
    "dataset",
    "auditor_id",
    "label_answerable",
    "failure_type",
    "confidence",
    "notes",
]


def export_blind_audit_pack_v4(
    raw_path: Path,
    private_path: Path,
    output_dir: Path,
    *,
    pack_name: str,
    max_items: int | None = None,
    seed: int = 13,
    annotator_ids: list[str] | None = None,
    audit_id_prefix: str | None = None,
) -> dict[str, Any]:
    raw_items = _load_jsonl_by_orbit(raw_path)
    private_items = _load_jsonl_by_orbit(private_path)
    if not raw_items:
        raise ValueError(f"{raw_path} contains no raw records")
    if not private_items:
        raise ValueError(f"{private_path} contains no private records")

    joined = []
    for orbit_id, raw in raw_items.items():
        private = private_items.get(orbit_id)
        if private is None:
            continue
        joined.append({"raw": raw, "private": private})
    if not joined:
        raise ValueError("raw and private files do not share any orbit_id values")

    selected = _sample_items(joined, max_items=max_items, seed=seed)
    prefix = audit_id_prefix or pack_name
    rng = random.Random(seed)
    rng.shuffle(selected)
    audit_items = [
        _make_audit_item(index, pair["raw"], pair["private"], prefix=prefix)
        for index, pair in enumerate(selected, start=1)
    ]

    output_dir.mkdir(parents=True, exist_ok=True)
    items_path = output_dir / f"{pack_name}.items.jsonl"
    review_path = output_dir / f"{pack_name}.review.html"
    manifest_path = output_dir / f"{pack_name}.manifest.json"

    _write_jsonl(items_path, [item["public"] for item in audit_items])
    _write_review_html(review_path, audit_items, pack_name=pack_name)

    annotator_ids = annotator_ids or ["auditor1", "auditor2"]
    label_csvs = {}
    for annotator_id in annotator_ids:
        label_path = output_dir / f"{pack_name}.{annotator_id}.labels.csv"
        _write_label_csv(label_path, audit_items, annotator_id)
        label_csvs[annotator_id] = str(label_path)

    labels = [_parse_bool(item.get("label_answerable")) for item in private_items.values()]
    selected_labels = [_parse_bool(item["hidden"]["expected_label_answerable"]) for item in audit_items]
    manifest = {
        "pack_name": pack_name,
        "raw_input": str(raw_path),
        "private_input": str(private_path),
        "items_jsonl": str(items_path),
        "review_html": str(review_path),
        "label_csvs": label_csvs,
        "manifest": str(manifest_path),
        "seed": seed,
        "max_items": max_items,
        "total_joined_items": len(joined),
        "selected_items": len(audit_items),
        "source_label_counts": _count_bool(labels),
        "selected_label_counts": _count_bool(selected_labels),
        "hidden_fields": [
            "orbit_id",
            "source_item_group_id",
            "label_answerable",
            "construction_type",
            "label_source",
            "heuristic_label",
            "support_key",
            "retrieval_scores",
            "retrieval_score",
            "generator_outputs",
            "verifier_outputs",
            "model_scores",
        ],
        "audit_items": [
            {
                "audit_id": item["public"]["audit_id"],
                **item["hidden"],
            }
            for item in audit_items
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def _load_jsonl_by_orbit(path: Path) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            item = json.loads(line)
            orbit_id = str(item.get("orbit_id") or "").strip()
            if not orbit_id:
                raise ValueError(f"{path}:{line_no} is missing orbit_id")
            if orbit_id in items:
                raise ValueError(f"{path}:{line_no} duplicates orbit_id {orbit_id}")
            items[orbit_id] = item
    return items


def _sample_items(
    items: list[dict[str, dict[str, Any]]],
    *,
    max_items: int | None,
    seed: int,
) -> list[dict[str, dict[str, Any]]]:
    ordered = sorted(items, key=lambda pair: str(pair["raw"].get("orbit_id") or ""))
    if max_items is None or max_items >= len(ordered):
        return ordered

    rng = random.Random(seed)
    by_label: dict[bool, list[dict[str, dict[str, Any]]]] = {True: [], False: []}
    unlabeled = []
    for pair in ordered:
        label = _parse_bool(pair["private"].get("label_answerable"))
        if label is None:
            unlabeled.append(pair)
        else:
            by_label[label].append(pair)
    for bucket in [by_label[True], by_label[False], unlabeled]:
        rng.shuffle(bucket)

    if by_label[True] and by_label[False]:
        per_class = max_items // 2
        selected = by_label[True][:per_class] + by_label[False][:per_class]
        remainder = max_items - len(selected)
        leftovers = by_label[True][per_class:] + by_label[False][per_class:] + unlabeled
        rng.shuffle(leftovers)
        selected.extend(leftovers[:remainder])
        return selected

    rng.shuffle(ordered)
    return ordered[:max_items]


def _make_audit_item(
    index: int,
    raw: dict[str, Any],
    private: dict[str, Any],
    *,
    prefix: str,
) -> dict[str, Any]:
    audit_id = f"{prefix}-{index:05d}"
    public = {
        "audit_id": audit_id,
        "dataset": raw.get("dataset") or private.get("dataset") or "",
        "query": raw.get("query") or "",
        "candidate_answer": raw.get("candidate_answer") or private.get("gold_answer") or "",
        "clean_evidence": _public_docs(raw.get("clean_evidence") or []),
        "perturbations": [
            {
                "query": perturbation.get("query") or raw.get("query") or "",
                "candidate_answer": perturbation.get("candidate_answer")
                or raw.get("candidate_answer")
                or private.get("gold_answer")
                or "",
                "evidence": _public_docs(perturbation.get("evidence") or []),
            }
            for perturbation in raw.get("perturbations", [])
        ],
    }
    hidden = {
        "orbit_id": raw.get("orbit_id"),
        "source_item_group_id": raw.get("source_item_group_id") or private.get("source_item_group_id"),
        "dataset": public["dataset"],
        "expected_label_answerable": _parse_bool(private.get("label_answerable")),
        "construction_type": private.get("construction_type"),
        "label_source": private.get("label_source"),
        "heuristic_label": private.get("heuristic_label"),
        "support_key": private.get("support_key"),
        "gold_answer": private.get("gold_answer"),
    }
    return {"public": public, "hidden": hidden, "private": private}


def _public_docs(docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "rank": doc.get("rank"),
            "title": doc.get("title") or "",
            "doc_id": doc.get("doc_id") or "",
            "text": doc.get("text") or "",
        }
        for doc in docs
    ]


def _write_jsonl(path: Path, items: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as dst:
        for item in items:
            dst.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def _write_label_csv(path: Path, audit_items: list[dict[str, Any]], annotator_id: str) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(dst, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for item in audit_items:
            writer.writerow(
                {
                    "audit_id": item["public"]["audit_id"],
                    "dataset": item["public"]["dataset"],
                    "auditor_id": annotator_id,
                    "label_answerable": "",
                    "failure_type": "",
                    "confidence": "",
                    "notes": "",
                }
            )


def _write_review_html(path: Path, audit_items: list[dict[str, Any]], *, pack_name: str) -> None:
    body = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'>",
        f"<title>{html.escape(pack_name)} Human Audit v4</title>",
        "<style>",
        "body{font-family:Arial,sans-serif;line-height:1.45;margin:24px;max-width:1200px}",
        "table{border-collapse:collapse;width:100%;margin:10px 0}",
        "th,td{border:1px solid #ccc;padding:6px;vertical-align:top}",
        "th{background:#f2f2f2;width:160px}",
        ".item{border-top:3px solid #333;margin-top:24px;padding-top:16px}",
        ".set{border:1px solid #bbb;margin:12px 0;padding:10px}",
        ".doc{margin:8px 0;padding:8px;background:#fafafa;border-left:3px solid #bbb}",
        ".meta{color:#555;font-size:0.92em}",
        "code{background:#f4f4f4;padding:1px 3px}",
        "</style></head><body>",
        f"<h1>{html.escape(pack_name)} Human Audit v4</h1>",
        "<p>Use only the evidence text shown here. Hidden labels, construction metadata, "
        "retrieval scores, and model scores are intentionally omitted.</p>",
    ]
    for index, item in enumerate(audit_items, start=1):
        public = item["public"]
        body.extend(
            [
                f"<section class='item' id='{html.escape(public['audit_id'])}'>",
                f"<h2>{index}. {html.escape(public['audit_id'])}</h2>",
                "<table>",
                _row("Dataset", public.get("dataset")),
                _row("Query", public.get("query")),
                _row("Candidate answer", public.get("candidate_answer")),
                "</table>",
                _render_evidence_set("Clean evidence", public.get("clean_evidence") or []),
            ]
        )
        for pert_index, perturbation in enumerate(public.get("perturbations") or [], start=1):
            body.extend(
                [
                    "<div class='set'>",
                    f"<h3>Perturbation evidence {pert_index}</h3>",
                    "<table>",
                    _row("Query", perturbation.get("query")),
                    _row("Candidate answer", perturbation.get("candidate_answer")),
                    "</table>",
                    _render_docs(perturbation.get("evidence") or []),
                    "</div>",
                ]
            )
        body.append("</section>")
    body.append("</body></html>")
    path.write_text("\n".join(body), encoding="utf-8")


def _render_evidence_set(title: str, docs: list[dict[str, Any]]) -> str:
    return "\n".join(["<div class='set'>", f"<h3>{html.escape(title)}</h3>", _render_docs(docs), "</div>"])


def _render_docs(docs: list[dict[str, Any]]) -> str:
    rendered = []
    for doc in docs:
        title = str(doc.get("title") or doc.get("doc_id") or "")
        meta = f"rank={doc.get('rank')}"
        rendered.append(
            "<div class='doc'>"
            f"<div><b>{html.escape(title)}</b></div>"
            f"<div class='meta'>{html.escape(meta)}</div>"
            f"<div>{html.escape(str(doc.get('text') or ''))}</div>"
            "</div>"
        )
    return "\n".join(rendered)


def _row(label: str, value: Any) -> str:
    return (
        f"<tr><th>{html.escape(label)}</th>"
        f"<td>{html.escape('' if value is None else str(value))}</td></tr>"
    )


def _parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "answerable", "supported"}:
        return True
    if normalized in {"false", "0", "no", "fragile", "unanswerable", "unsupported"}:
        return False
    return None


def _count_bool(values: list[bool | None]) -> dict[str, int]:
    counts = {"true": 0, "false": 0, "unknown": 0}
    for value in values:
        if value is True:
            counts["true"] += 1
        elif value is False:
            counts["false"] += 1
        else:
            counts["unknown"] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--pack-name", required=True)
    parser.add_argument("--max-items", type=int)
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--annotator-id", action="append", dest="annotator_ids")
    parser.add_argument("--audit-id-prefix")
    args = parser.parse_args()

    manifest = export_blind_audit_pack_v4(
        args.raw,
        args.private,
        args.output_dir,
        pack_name=args.pack_name,
        max_items=args.max_items,
        seed=args.seed,
        annotator_ids=args.annotator_ids,
        audit_id_prefix=args.audit_id_prefix,
    )
    print(json.dumps({k: v for k, v in manifest.items() if k != "audit_items"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
