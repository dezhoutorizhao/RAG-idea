#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def summarize_human_audit_v4_mismatch(audit_dir: Path) -> dict[str, Any]:
    packs = [summarize_pack(path) for path in sorted(audit_dir.glob("*.manifest.json"))]
    binary_comparable = sum(pack["binary_comparable"] for pack in packs)
    binary_mismatches = sum(pack["binary_mismatches"] for pack in packs)
    semantic_comparable = sum(pack["semantic_comparable"] for pack in packs)
    semantic_mismatches = sum(pack["semantic_mismatches"] for pack in packs)
    return {
        "audit_dir": str(audit_dir),
        "pack_count": len(packs),
        "binary_comparable": binary_comparable,
        "binary_mismatches": binary_mismatches,
        "binary_mismatch_rate": _rate(binary_mismatches, binary_comparable),
        "semantic_comparable": semantic_comparable,
        "semantic_mismatches": semantic_mismatches,
        "semantic_mismatch_rate": _rate(semantic_mismatches, semantic_comparable),
        "packs": packs,
        "mismatch_artifact_ready": bool(packs),
        "human_audit_complete": bool(packs)
        and all(pack["pending_adjudications"] == 0 for pack in packs)
        and binary_comparable > 0,
        "claim_policy": (
            "This artifact compares heuristic labels with adjudicated human labels only when "
            "adjudicated labels exist. Pending labels are excluded from mismatch rates."
        ),
    }


def summarize_pack(manifest_path: Path) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    pack_name = manifest.get("pack_name") or manifest_path.name.removesuffix(".manifest.json")
    audit_dir = manifest_path.parent
    heuristic_by_audit_id = {
        str(item["audit_id"]): {
            "expected_label_answerable": item.get("expected_label_answerable"),
            "heuristic_label": str(item.get("heuristic_label") or "").strip(),
            "construction_type": item.get("construction_type"),
            "dataset": item.get("dataset"),
            "orbit_id": item.get("orbit_id"),
        }
        for item in manifest.get("audit_items", [])
    }
    adjudicated = _load_jsonl_if_exists(audit_dir / f"{pack_name}.adjudicated_labels.jsonl")
    pending = 0
    binary_comparable = binary_mismatches = 0
    semantic_comparable = semantic_mismatches = 0
    binary_by_construction: Counter[str] = Counter()
    semantic_by_construction: Counter[str] = Counter()
    examples = []
    for row in adjudicated:
        status = str(row.get("adjudication_status") or "unknown")
        if status == "pending":
            pending += 1
            continue
        audit_id = str(row.get("audit_id") or "")
        expected = heuristic_by_audit_id.get(audit_id, {})
        expected_binary = _parse_bool(expected.get("expected_label_answerable"))
        human_binary = _parse_bool(row.get("adjudicated_label_answerable"))
        construction = str(expected.get("construction_type") or row.get("construction_type") or "unknown")
        if expected_binary is not None and human_binary is not None:
            binary_comparable += 1
            if expected_binary != human_binary:
                binary_mismatches += 1
                binary_by_construction[construction] += 1
                examples.append(_example(row, expected, "binary"))
        expected_semantic = str(expected.get("heuristic_label") or "").strip()
        human_semantic = str(row.get("adjudicated_label_semantic") or "").strip()
        if expected_semantic and human_semantic:
            semantic_comparable += 1
            if expected_semantic != human_semantic:
                semantic_mismatches += 1
                semantic_by_construction[construction] += 1
                examples.append(_example(row, expected, "semantic"))
    return {
        "pack_name": pack_name,
        "manifest": str(manifest_path),
        "selected_items": int(manifest.get("selected_items") or len(manifest.get("audit_items", []))),
        "pending_adjudications": pending,
        "binary_comparable": binary_comparable,
        "binary_mismatches": binary_mismatches,
        "binary_mismatch_rate": _rate(binary_mismatches, binary_comparable),
        "semantic_comparable": semantic_comparable,
        "semantic_mismatches": semantic_mismatches,
        "semantic_mismatch_rate": _rate(semantic_mismatches, semantic_comparable),
        "binary_mismatches_by_construction": dict(sorted(binary_by_construction.items())),
        "semantic_mismatches_by_construction": dict(sorted(semantic_by_construction.items())),
        "mismatch_examples": examples[:20],
        "claim_boundary": (
            "Mismatch counts are undefined until adjudicated human labels exist. "
            "A zero mismatch count with zero comparable rows is not positive evidence."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Human Audit V4 Heuristic-Human Mismatch",
        "",
        f"Audit directory: `{summary['audit_dir']}`",
        "",
        f"Mismatch artifact ready: `{summary['mismatch_artifact_ready']}`",
        f"Human audit complete: `{summary['human_audit_complete']}`",
        "",
        "## Aggregate",
        "",
        f"- Binary comparable labels: `{summary['binary_comparable']}`",
        f"- Binary mismatches: `{summary['binary_mismatches']}`",
        f"- Binary mismatch rate: `{summary['binary_mismatch_rate']}`",
        f"- Semantic comparable labels: `{summary['semantic_comparable']}`",
        f"- Semantic mismatches: `{summary['semantic_mismatches']}`",
        f"- Semantic mismatch rate: `{summary['semantic_mismatch_rate']}`",
        "",
        "## Packs",
        "",
        "| Pack | Items | Pending | Binary comparable | Binary mismatch rate | Semantic comparable | Semantic mismatch rate |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for pack in summary["packs"]:
        lines.append(
            f"| {pack['pack_name']} | {pack['selected_items']} | {pack['pending_adjudications']} | "
            f"{pack['binary_comparable']} | {pack['binary_mismatch_rate']} | "
            f"{pack['semantic_comparable']} | {pack['semantic_mismatch_rate']} |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _example(row: dict[str, Any], expected: dict[str, Any], mismatch_type: str) -> dict[str, Any]:
    return {
        "audit_id": row.get("audit_id"),
        "mismatch_type": mismatch_type,
        "dataset": expected.get("dataset") or row.get("dataset"),
        "construction_type": expected.get("construction_type") or row.get("construction_type"),
        "orbit_id": expected.get("orbit_id") or row.get("orbit_id"),
        "heuristic_label": expected.get("heuristic_label"),
        "expected_label_answerable": expected.get("expected_label_answerable"),
        "adjudicated_label_semantic": row.get("adjudicated_label_semantic"),
        "adjudicated_label_answerable": row.get("adjudicated_label_answerable"),
        "adjudication_status": row.get("adjudication_status"),
    }


def _parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    normalized = str(value if value is not None else "").strip().lower()
    if normalized in {"true", "yes", "1", "answerable", "supported", "stable_answerable"}:
        return True
    if normalized in {"false", "no", "0", "fragile", "unanswerable", "unsupported", "insufficient"}:
        return False
    return None


def _rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl_if_exists(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line in src:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-dir", type=Path, default=Path("results/human_audit_v4"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_human_audit_v4_mismatch(args.audit_dir)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
