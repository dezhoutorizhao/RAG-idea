#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


TRUE_VALUES = {"true", "yes", "1", "answerable", "supported"}
FALSE_VALUES = {"false", "no", "0", "fragile", "unanswerable", "unsupported", "insufficient"}
UNSURE_VALUES = {"", "unsure", "unknown", "unclear"}
SEMANTIC_VALUES = {
    "",
    "stable_answerable",
    "fragile",
    "unanswerable",
    "ambiguous",
    "annotation_error",
}


def summarize_human_audit_v4_status(audit_dir: Path) -> dict[str, Any]:
    manifests = sorted(audit_dir.glob("*.manifest.json"))
    packs = [summarize_pack(manifest) for manifest in manifests]
    total_items = sum(pack["selected_items"] for pack in packs)
    adjudicated_labeled = sum(pack["adjudication"]["labeled"] for pack in packs)
    pending = sum(pack["adjudication"]["pending"] for pack in packs)
    return {
        "audit_dir": str(audit_dir),
        "pack_count": len(packs),
        "total_items": total_items,
        "adjudicated_labeled": adjudicated_labeled,
        "pending": pending,
        "semantic_label_schema_ready": bool(packs)
        and all(pack["semantic_label_schema_ready"] for pack in packs),
        "ready": bool(packs) and all(pack["ready"] for pack in packs),
        "packs": packs,
        "claim_policy": (
            "This report tracks human-audit readiness only. Empty or pending labels do not support "
            "human-audited claims."
        ),
    }


def summarize_pack(manifest_path: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pack_name = manifest.get("pack_name") or manifest_path.name.removesuffix(".manifest.json")
    audit_dir = manifest_path.parent
    selected_items = int(manifest.get("selected_items") or len(manifest.get("audit_items", [])))
    expected_counts = _expected_counts(manifest.get("audit_items", []))
    label_csvs = _label_csv_paths(manifest, audit_dir, pack_name)
    auditor_summaries = {path.stem: summarize_label_csv(path) for path in label_csvs}
    agreement_path = audit_dir / f"{pack_name}.agreement.json"
    adjudicated_path = audit_dir / f"{pack_name}.adjudicated_labels.jsonl"
    readiness_path = audit_dir / f"{pack_name}.readiness.json"
    agreement = _load_json_if_exists(agreement_path)
    adjudication = summarize_adjudicated_labels(adjudicated_path, selected_items)
    readiness = _load_json_if_exists(readiness_path)
    ready = adjudication["labeled"] >= selected_items and adjudication["pending"] == 0
    failed_gates = []
    if selected_items == 0:
        failed_gates.append({"gate": "non_empty_pack", "actual": selected_items})
    if adjudication["labeled"] < selected_items:
        failed_gates.append(
            {
                "gate": "all_items_adjudicated",
                "required": selected_items,
                "actual": adjudication["labeled"],
            }
        )
    if adjudication["invalid"] > 0:
        failed_gates.append({"gate": "valid_adjudicated_labels", "invalid": adjudication["invalid"]})
    if not all(auditor.get("has_label_semantic_column") for auditor in auditor_summaries.values()):
        failed_gates.append({"gate": "semantic_label_column_present", "actual": False})
    return {
        "pack_name": pack_name,
        "manifest": str(manifest_path),
        "selected_items": selected_items,
        "expected_label_counts": expected_counts,
        "auditors": auditor_summaries,
        "semantic_label_schema_ready": all(
            auditor.get("has_label_semantic_column") for auditor in auditor_summaries.values()
        ),
        "agreement": _agreement_summary(agreement),
        "adjudication": adjudication,
        "readiness_file": str(readiness_path) if readiness_path.exists() else None,
        "readiness_file_ready": None if readiness is None else readiness.get("ready"),
        "ready": ready,
        "failed_gates": failed_gates,
    }


def summarize_label_csv(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(path),
            "exists": False,
            "rows": 0,
            "labeled": 0,
            "pending": 0,
            "invalid": 0,
            "semantic_labeled": 0,
            "semantic_pending": 0,
            "semantic_invalid": 0,
            "has_label_semantic_column": False,
        }
    reader = csv.DictReader(path.open(newline="", encoding="utf-8-sig"))
    rows = list(reader)
    labeled = pending = invalid = 0
    semantic_labeled = semantic_pending = semantic_invalid = 0
    has_semantic = "label_semantic" in set(reader.fieldnames or [])
    for row in rows:
        parsed = _parse_label(row.get("label_answerable"))
        if parsed is None:
            pending += 1
        elif parsed in {True, False}:
            labeled += 1
        else:
            invalid += 1
        semantic = _parse_semantic_label(row.get("label_semantic"))
        if semantic is None:
            semantic_pending += 1
        elif semantic == "invalid":
            semantic_invalid += 1
        else:
            semantic_labeled += 1
    return {
        "path": str(path),
        "exists": True,
        "rows": len(rows),
        "labeled": labeled,
        "pending": pending,
        "invalid": invalid,
        "semantic_labeled": semantic_labeled,
        "semantic_pending": semantic_pending,
        "semantic_invalid": semantic_invalid,
        "has_label_semantic_column": has_semantic,
        "completion_rate": labeled / len(rows) if rows else None,
        "semantic_completion_rate": semantic_labeled / len(rows) if rows else None,
    }


def summarize_adjudicated_labels(path: Path, expected_items: int) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(path),
            "exists": False,
            "items": 0,
            "labeled": 0,
            "pending": expected_items,
            "invalid": 0,
            "by_status": {},
        }
    items = _load_jsonl(path)
    labeled = pending = invalid = 0
    by_status: dict[str, int] = {}
    for item in items:
        status = str(item.get("adjudication_status") or "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        parsed = _parse_label(item.get("adjudicated_label_answerable"))
        if parsed is None:
            pending += 1
        elif parsed in {True, False}:
            labeled += 1
        else:
            invalid += 1
    return {
        "path": str(path),
        "exists": True,
        "items": len(items),
        "labeled": labeled,
        "pending": pending,
        "invalid": invalid,
        "completion_rate": labeled / len(items) if items else None,
        "by_status": by_status,
    }


def render_markdown(status: dict[str, Any]) -> str:
    lines = [
        "# Human Audit V4 Status",
        "",
        f"Audit directory: `{status['audit_dir']}`",
        "",
        f"Ready: `{status['ready']}`",
        f"Pack count: `{status['pack_count']}`",
        f"Total items: `{status['total_items']}`",
        f"Adjudicated labels: `{status['adjudicated_labeled']}`",
        f"Pending: `{status['pending']}`",
        f"Semantic label schema ready: `{status['semantic_label_schema_ready']}`",
        "",
        "| Pack | Items | Auditor labeled | Adjudicated | Pending | Ready |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for pack in status["packs"]:
        auditor_labeled = sum(auditor["labeled"] for auditor in pack["auditors"].values())
        lines.append(
            f"| {pack['pack_name']} | {pack['selected_items']} | {auditor_labeled} | "
            f"{pack['adjudication']['labeled']} | {pack['adjudication']['pending']} | "
            f"`{pack['ready']}` |"
        )
    lines.extend(["", "## Failed Gates", ""])
    for pack in status["packs"]:
        if not pack["failed_gates"]:
            continue
        lines.append(f"{pack['pack_name']}:")
        lines.extend(f"- `{gate['gate']}`: {gate}" for gate in pack["failed_gates"])
        lines.append("")
    lines.extend(
        [
            "## Claim Policy",
            "",
            status["claim_policy"],
            "",
        ]
    )
    return "\n".join(lines)


def _label_csv_paths(manifest: dict[str, Any], audit_dir: Path, pack_name: str) -> list[Path]:
    label_csvs = manifest.get("label_csvs")
    if isinstance(label_csvs, dict):
        return [_resolve_path(path, audit_dir) for path in label_csvs.values()]
    return sorted(audit_dir.glob(f"{pack_name}.*.labels.csv"))


def _resolve_path(raw_path: str, audit_dir: Path) -> Path:
    path = Path(str(raw_path).replace("\\", "/"))
    if path.exists():
        return path
    candidate = audit_dir / path.name
    return candidate


def _expected_counts(items: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"true": 0, "false": 0, "unknown": 0}
    for item in items:
        parsed = _parse_label(item.get("expected_label_answerable"))
        if parsed is True:
            counts["true"] += 1
        elif parsed is False:
            counts["false"] += 1
        else:
            counts["unknown"] += 1
    return counts


def _agreement_summary(agreement: dict[str, Any] | None) -> dict[str, Any] | None:
    if agreement is None:
        return None
    return {
        "auditors": agreement.get("auditors"),
        "completion": agreement.get("completion"),
        "pairwise": agreement.get("pairwise"),
        "semantic_pairwise": agreement.get("semantic_pairwise"),
        "conflicts": len(agreement.get("conflicts", [])),
        "semantic_conflicts": len(agreement.get("semantic_conflicts", [])),
    }


def _load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line in src:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _parse_label(value: Any) -> bool | None | str:
    normalized = str(value if value is not None else "").strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    if normalized in UNSURE_VALUES:
        return None
    return "invalid"


def _parse_semantic_label(value: Any) -> str | None:
    normalized = str(value if value is not None else "").strip().lower()
    if normalized == "":
        return None
    if normalized in SEMANTIC_VALUES:
        return normalized
    return "invalid"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-dir", type=Path, default=Path("results/human_audit_v4"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    status = summarize_human_audit_v4_status(args.audit_dir)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(status, indent=2, sort_keys=True), encoding="utf-8")
    args.output_md.write_text(render_markdown(status), encoding="utf-8")
    print(json.dumps(status, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
