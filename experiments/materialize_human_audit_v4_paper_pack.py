#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
from annotation.export_blind_audit_pack_v4 import export_blind_audit_pack_v4
from annotation.merge_audit_labels_v4 import merge_audit_labels_v4
from experiments.check_audit_readiness import check_audit_readiness


DEFAULT_SOURCES = [
    {
        "name": "hotpot_v4_base_n100",
        "raw": Path("results/hotpot_orbits_v4_n100.constant.raw.jsonl"),
        "private": Path("results/hotpot_orbits_v4_n100.private_eval.jsonl"),
        "scored": Path("results/hotpot_orbits_v4_n100.constant.textonly_scored.jsonl"),
    },
    {
        "name": "fever_v4_base_n100",
        "raw": Path("results/fever_orbits_v4_n100.constant.raw.jsonl"),
        "private": Path("results/fever_orbits_v4_n100.private_eval.jsonl"),
        "scored": Path("results/fever_orbits_v4_n100.constant.textonly_scored.jsonl"),
    },
]

DEFAULT_PACK_NAME = "v4_paper1000_mixed_blind1000"


def materialize_human_audit_v4_paper_pack(
    root: Path,
    output_dir: Path,
    *,
    pack_name: str = DEFAULT_PACK_NAME,
    seed: int = 20260529,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    combined_raw = output_dir / f"{pack_name}.sources.raw.jsonl"
    combined_private = output_dir / f"{pack_name}.sources.private_eval.jsonl"
    combined_scored = output_dir / f"{pack_name}.sources.textonly_scored.jsonl"

    source_summaries = _write_combined_sources(root, combined_raw, combined_private, combined_scored)
    expected_total = sum(item["row_count"] for item in source_summaries)

    manifest = export_blind_audit_pack_v4(
        combined_raw,
        combined_private,
        output_dir,
        pack_name=pack_name,
        max_items=None,
        seed=seed,
        annotator_ids=["auditor1", "auditor2"],
        audit_id_prefix=pack_name,
    )
    label_csvs = [Path(path) for path in manifest["label_csvs"].values()]
    manifest_path = output_dir / f"{pack_name}.manifest.json"
    merged_path = output_dir / f"{pack_name}.merged_labels.jsonl"
    agreement_path = output_dir / f"{pack_name}.agreement.json"
    adjudicated_path = output_dir / f"{pack_name}.adjudicated_labels.jsonl"
    template_path = output_dir / f"{pack_name}.adjudication_template.csv"
    readiness_path = output_dir / f"{pack_name}.readiness.json"

    merge_summary = merge_audit_labels_v4(manifest_path, label_csvs, merged_path)
    agreement = compute_agreement_v4(merged_path)
    _write_json(agreement_path, agreement)
    adjudication = adjudicate_labels_v4(
        merged_path,
        adjudicated_path,
        template_csv=template_path,
    )
    readiness = check_audit_readiness(
        adjudicated_path,
        min_labeled_total=manifest["selected_items"],
        min_labeled_per_split=max(1, manifest["selected_items"] // 2),
        label_field="adjudicated_label_answerable",
        require_disagreement_notes=False,
    )
    _write_json(readiness_path, readiness)

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pack_name": pack_name,
        "output_dir": str(output_dir),
        "source_summaries": source_summaries,
        "expected_total_items": expected_total,
        "selected_items": manifest["selected_items"],
        "selected_label_counts": manifest["selected_label_counts"],
        "paper_pack_ready_for_labeling": manifest["selected_items"] == expected_total,
        "human_labels_complete": readiness["ready"],
        "pending_adjudicated_labels": readiness["pending"],
        "artifacts": {
            "combined_raw": str(combined_raw),
            "combined_private": str(combined_private),
            "combined_scored": str(combined_scored),
            "manifest": str(manifest_path),
            "items_jsonl": manifest["items_jsonl"],
            "review_html": manifest["review_html"],
            "label_csvs": manifest["label_csvs"],
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
            "This materializes a paper-grade 1000-item Human Audit v4 blind pack. "
            "It is ready for human labeling but contains no completed human labels yet, "
            "so it does not support human-audited result claims."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Human Audit V4 Paper Pack Status",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Pack name: `{summary['pack_name']}`",
        f"Selected items: `{summary['selected_items']}`",
        f"Paper pack ready for labeling: `{summary['paper_pack_ready_for_labeling']}`",
        f"Human labels complete: `{summary['human_labels_complete']}`",
        f"Pending adjudicated labels: `{summary['pending_adjudicated_labels']}`",
        f"Selected label counts: `{summary['selected_label_counts']}`",
        "",
        "## Sources",
        "",
        "| Source | Rows | Raw | Private | Scored |",
        "|---|---:|---|---|---|",
    ]
    for source in summary["source_summaries"]:
        lines.append(
            f"| {source['name']} | `{source['row_count']}` | `{source['raw']}` | "
            f"`{source['private']}` | `{source['scored']}` |"
        )
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
        ]
    )
    artifacts = summary["artifacts"]
    for name, path in artifacts.items():
        if isinstance(path, dict):
            for sub_name, sub_path in path.items():
                lines.append(f"- {name}.{sub_name}: `{sub_path}`")
        else:
            lines.append(f"- {name}: `{path}`")
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _write_combined_sources(
    root: Path,
    combined_raw: Path,
    combined_private: Path,
    combined_scored: Path,
) -> list[dict[str, Any]]:
    seen_orbits: set[str] = set()
    summaries = []
    raw_rows: list[dict[str, Any]] = []
    private_rows: list[dict[str, Any]] = []
    scored_rows: list[dict[str, Any]] = []
    for source in DEFAULT_SOURCES:
        raw_path = root / source["raw"]
        private_path = root / source["private"]
        scored_path = root / source["scored"]
        raw = _load_jsonl(raw_path)
        private = _load_jsonl(private_path)
        scored = _load_jsonl(scored_path)
        raw_by_id = _by_orbit(raw, raw_path)
        private_by_id = _by_orbit(private, private_path)
        scored_by_id = _by_orbit(scored, scored_path)
        ids = sorted(raw_by_id)
        if set(ids) != set(private_by_id) or set(ids) != set(scored_by_id):
            raise ValueError(f"{source['name']} raw/private/scored orbit ids are misaligned")
        duplicate = seen_orbits.intersection(ids)
        if duplicate:
            raise ValueError(f"{source['name']} duplicates orbit ids: {sorted(duplicate)[:5]}")
        seen_orbits.update(ids)
        raw_rows.extend(raw_by_id[orbit_id] for orbit_id in ids)
        private_rows.extend(private_by_id[orbit_id] for orbit_id in ids)
        scored_rows.extend(scored_by_id[orbit_id] for orbit_id in ids)
        summaries.append(
            {
                "name": source["name"],
                "row_count": len(ids),
                "raw": str(source["raw"]),
                "private": str(source["private"]),
                "scored": str(source["scored"]),
            }
        )
    _write_jsonl(combined_raw, raw_rows)
    _write_jsonl(combined_private, private_rows)
    _write_jsonl(combined_scored, scored_rows)
    return summaries


def _by_orbit(rows: list[dict[str, Any]], path: Path) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        orbit_id = str(row.get("orbit_id") or "").strip()
        if not orbit_id:
            raise ValueError(f"{path} has a row without orbit_id")
        if orbit_id in by_id:
            raise ValueError(f"{path} duplicates orbit_id {orbit_id}")
        by_id[orbit_id] = row
    return by_id


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line in src:
            if line.strip():
                rows.append(json.loads(line))
    if not rows:
        raise ValueError(f"{path} contains no rows")
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as dst:
        for row in rows:
            dst.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=Path("results/human_audit_v4"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--pack-name", default=DEFAULT_PACK_NAME)
    parser.add_argument("--seed", type=int, default=20260529)
    args = parser.parse_args()

    summary = materialize_human_audit_v4_paper_pack(
        args.root,
        args.output_dir,
        pack_name=args.pack_name,
        seed=args.seed,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
