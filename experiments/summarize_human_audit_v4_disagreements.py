#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def summarize_human_audit_v4_disagreements(audit_dir: Path) -> dict[str, Any]:
    manifests = sorted(audit_dir.glob("*.manifest.json"))
    packs = [summarize_pack(path) for path in manifests]
    aggregate = {
        "binary_conflict_count": sum(pack["binary_conflict_count"] for pack in packs),
        "semantic_conflict_count": sum(pack["semantic_conflict_count"] for pack in packs),
        "pending_adjudication_count": sum(pack["pending_adjudication_count"] for pack in packs),
        "manual_adjudication_count": sum(pack["manual_adjudication_count"] for pack in packs),
        "auto_agree_count": sum(pack["auto_agree_count"] for pack in packs),
        "failure_type_disagreement_count": sum(
            pack["failure_type_disagreement_count"] for pack in packs
        ),
    }
    return {
        "audit_dir": str(audit_dir),
        "pack_count": len(packs),
        "aggregate": aggregate,
        "packs": packs,
        "taxonomy_artifact_ready": bool(packs),
        "human_audit_complete": bool(packs)
        and aggregate["pending_adjudication_count"] == 0
        and aggregate["auto_agree_count"] + aggregate["manual_adjudication_count"] > 0,
        "claim_policy": (
            "This artifact exposes disagreement taxonomy and adjudication state only. "
            "It does not convert pending labels into human-audited evidence."
        ),
    }


def summarize_pack(manifest_path: Path) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    audit_dir = manifest_path.parent
    pack_name = manifest.get("pack_name") or manifest_path.name.removesuffix(".manifest.json")
    agreement = _load_json_if_exists(audit_dir / f"{pack_name}.agreement.json") or {}
    adjudicated = _load_jsonl_if_exists(audit_dir / f"{pack_name}.adjudicated_labels.jsonl")
    merged = _load_jsonl_if_exists(audit_dir / f"{pack_name}.merged_labels.jsonl")
    template_rows = _load_csv_if_exists(audit_dir / f"{pack_name}.adjudication_template.csv")

    binary_conflicts = list(agreement.get("conflicts", []))
    semantic_conflicts = list(agreement.get("semantic_conflicts", []))
    adjudication_status = Counter(
        str(row.get("adjudication_status") or "unknown") for row in adjudicated
    )
    failure_type_disagreements = _failure_type_disagreements(merged)
    return {
        "pack_name": pack_name,
        "manifest": str(manifest_path),
        "selected_items": int(manifest.get("selected_items") or len(manifest.get("audit_items", []))),
        "binary_conflict_count": len(binary_conflicts),
        "semantic_conflict_count": len(semantic_conflicts),
        "binary_conflict_taxonomy": _conflict_taxonomy(binary_conflicts),
        "semantic_conflict_taxonomy": _conflict_taxonomy(semantic_conflicts),
        "failure_type_disagreement_count": len(failure_type_disagreements),
        "failure_type_disagreement_taxonomy": _failure_type_taxonomy(failure_type_disagreements),
        "failure_type_disagreement_examples": failure_type_disagreements[:10],
        "pending_adjudication_count": adjudication_status.get("pending", 0),
        "manual_adjudication_count": adjudication_status.get("manual", 0),
        "auto_agree_count": adjudication_status.get("auto_agree", 0),
        "adjudication_status_counts": dict(sorted(adjudication_status.items())),
        "adjudication_template_rows": len(template_rows),
        "claim_boundary": (
            "Conflict and pending counts are audit workflow diagnostics. "
            "They are not human-audited result metrics until labels are complete."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    lines = [
        "# Human Audit V4 Disagreement Taxonomy",
        "",
        f"Audit directory: `{summary['audit_dir']}`",
        "",
        f"Taxonomy artifact ready: `{summary['taxonomy_artifact_ready']}`",
        f"Human audit complete: `{summary['human_audit_complete']}`",
        "",
        "## Aggregate",
        "",
        f"- Binary conflicts: `{aggregate['binary_conflict_count']}`",
        f"- Semantic conflicts: `{aggregate['semantic_conflict_count']}`",
        f"- Failure-type disagreements: `{aggregate['failure_type_disagreement_count']}`",
        f"- Pending adjudications: `{aggregate['pending_adjudication_count']}`",
        f"- Manual adjudications: `{aggregate['manual_adjudication_count']}`",
        f"- Auto-agree adjudications: `{aggregate['auto_agree_count']}`",
        "",
        "## Packs",
        "",
        "| Pack | Items | Binary conflicts | Semantic conflicts | Failure-type disagreements | Pending | Manual | Auto-agree |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for pack in summary["packs"]:
        lines.append(
            f"| {pack['pack_name']} | {pack['selected_items']} | "
            f"{pack['binary_conflict_count']} | {pack['semantic_conflict_count']} | "
            f"{pack['failure_type_disagreement_count']} | "
            f"{pack['pending_adjudication_count']} | {pack['manual_adjudication_count']} | "
            f"{pack['auto_agree_count']} |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _conflict_taxonomy(conflicts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    for row in conflicts:
        labels = [
            str(value)
            for key, value in row.items()
            if key != "audit_id" and value is not None and str(value) != ""
        ]
        if len(labels) < 2:
            continue
        counts[" vs ".join(labels)] += 1
    return [{"label_pair": key, "count": count} for key, count in sorted(counts.items())]


def _failure_type_disagreements(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_audit: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_audit[str(row.get("audit_id") or "")].append(row)
    disagreements = []
    for audit_id, labels in sorted(by_audit.items()):
        failure_types = {
            str(row.get("failure_type") or "").strip()
            for row in labels
            if str(row.get("failure_type") or "").strip()
        }
        if len(failure_types) <= 1:
            continue
        disagreements.append(
            {
                "audit_id": audit_id,
                "failure_types": sorted(failure_types),
                "auditor_labels": [
                    {
                        "auditor_id": row.get("auditor_id"),
                        "label_semantic": row.get("label_semantic"),
                        "label_answerable": row.get("label_answerable"),
                        "failure_type": row.get("failure_type"),
                    }
                    for row in labels
                ],
            }
        )
    return disagreements


def _failure_type_taxonomy(disagreements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    for item in disagreements:
        counts[" vs ".join(item["failure_types"])] += 1
    return [{"failure_type_pair": key, "count": count} for key, count in sorted(counts.items())]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return _load_json(path)


def _load_jsonl_if_exists(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line in src:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _load_csv_if_exists(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as src:
        return list(csv.DictReader(src))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-dir", type=Path, default=Path("results/human_audit_v4"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_human_audit_v4_disagreements(args.audit_dir)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
