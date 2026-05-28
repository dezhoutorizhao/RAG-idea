#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from experiments.run_all_baselines_v4 import run_all_baselines_v4


TRUE_VALUES = {"true", "yes", "1", "answerable", "supported"}
FALSE_VALUES = {"false", "no", "0", "fragile", "unanswerable", "unsupported", "insufficient"}
UNSURE_VALUES = {"", "unsure", "unknown", "unclear"}


def run_human_audit_eval_v4(
    manifest_paths: list[Path],
    output_dir: Path,
    summary_json: Path,
    *,
    summary_md: Path | None = None,
    allow_partial: bool = False,
) -> dict[str, Any]:
    pack_reports = []
    for manifest_path in manifest_paths:
        pack_reports.append(run_pack(manifest_path, output_dir, allow_partial=allow_partial))

    ready = bool(pack_reports) and all(report["evaluation_ready"] for report in pack_reports)
    summary = {
        "manifest_paths": [str(path) for path in manifest_paths],
        "output_dir": str(output_dir),
        "allow_partial": allow_partial,
        "ready": ready,
        "pack_count": len(pack_reports),
        "evaluated_pack_count": sum(report["evaluated"] for report in pack_reports),
        "packs": pack_reports,
        "claim_policy": (
            "Only packs with adjudicated human labels are evaluated. Pending labels block "
            "human-audited claims unless allow_partial is explicitly used for diagnostics."
        ),
    }
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    if summary_md:
        summary_md.parent.mkdir(parents=True, exist_ok=True)
        summary_md.write_text(render_markdown(summary), encoding="utf-8")
    return summary


def run_pack(manifest_path: Path, output_dir: Path, *, allow_partial: bool) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pack_name = str(manifest.get("pack_name") or manifest_path.name.removesuffix(".manifest.json"))
    audit_dir = manifest_path.parent
    adjudicated_path = audit_dir / f"{pack_name}.adjudicated_labels.jsonl"
    raw_path = _resolve_path(manifest["raw_input"], manifest_path.parent)
    private_path = _resolve_path(manifest["private_input"], manifest_path.parent)
    scored_path = infer_scored_path(raw_path)
    selected = int(manifest.get("selected_items") or len(manifest.get("audit_items", [])))
    labels = load_adjudicated_labels(adjudicated_path)
    labeled = sum(label is not None for label in labels.values())
    pending = selected - labeled
    invalid = max(0, len(labels) - selected)
    failed_gates = []
    if not adjudicated_path.exists():
        failed_gates.append({"gate": "adjudicated_labels_exists", "path": str(adjudicated_path)})
    if labeled == 0:
        failed_gates.append({"gate": "non_empty_human_labels", "actual": labeled})
    if not allow_partial and labeled < selected:
        failed_gates.append({"gate": "all_selected_items_adjudicated", "required": selected, "actual": labeled})
    if not scored_path.exists():
        failed_gates.append({"gate": "scored_input_exists", "path": str(scored_path)})

    report: dict[str, Any] = {
        "pack_name": pack_name,
        "manifest": str(manifest_path),
        "raw_input": str(raw_path),
        "private_input": str(private_path),
        "scored_input": str(scored_path),
        "adjudicated_labels": str(adjudicated_path),
        "selected_items": selected,
        "labeled": labeled,
        "pending": max(0, pending),
        "allow_partial": allow_partial,
        "evaluation_ready": not failed_gates,
        "evaluated": False,
        "failed_gates": failed_gates,
    }
    if failed_gates:
        return report

    materialized = materialize_human_labeled_inputs(
        manifest=manifest,
        labels=labels,
        raw_path=raw_path,
        private_path=private_path,
        scored_path=scored_path,
        output_dir=output_dir,
        pack_name=pack_name,
        allow_partial=allow_partial,
    )
    eval_output = output_dir / f"{pack_name}.human_audited_baselines.json"
    eval_result = run_all_baselines_v4(
        materialized["raw_output"],
        materialized["private_output"],
        materialized["scored_output"],
        eval_output,
    )
    report.update(
        {
            "evaluated": True,
            "materialized": {key: str(value) for key, value in materialized.items()},
            "evaluation_output": str(eval_output),
            "evaluation_n": eval_result["n"],
            "strongest_non_csrm": {
                metric: item["method"] for metric, item in eval_result["strongest_non_csrm"].items()
            },
            "csrm_vs_strongest_non_csrm": eval_result["csrm_vs_strongest_non_csrm"],
        }
    )
    return report


def materialize_human_labeled_inputs(
    *,
    manifest: dict[str, Any],
    labels: dict[str, bool | None],
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_dir: Path,
    pack_name: str,
    allow_partial: bool,
) -> dict[str, Path]:
    audit_to_orbit = {str(item["audit_id"]): str(item["orbit_id"]) for item in manifest.get("audit_items", [])}
    orbit_labels = {
        audit_to_orbit[audit_id]: label
        for audit_id, label in labels.items()
        if audit_id in audit_to_orbit and label is not None
    }
    if not allow_partial:
        missing = sorted(set(audit_to_orbit.values()) - set(orbit_labels))
        if missing:
            raise ValueError(f"{pack_name} has {len(missing)} selected orbits without human labels")

    raw_rows = _filter_rows(raw_path, orbit_labels)
    private_rows = _filter_rows(private_path, orbit_labels)
    scored_rows = _filter_rows(scored_path, orbit_labels)
    if not (len(raw_rows) == len(private_rows) == len(scored_rows) == len(orbit_labels)):
        raise ValueError(f"{pack_name} raw/private/scored selected rows are misaligned")
    for raw, private, scored in zip(raw_rows, private_rows, scored_rows):
        orbit_id = str(raw["orbit_id"])
        if orbit_id != str(private["orbit_id"]) or orbit_id != str(scored["orbit_id"]):
            raise ValueError(f"{pack_name} has misaligned orbit_id {orbit_id}")
        private["heuristic_label_answerable"] = private.get("label_answerable")
        private["label_answerable"] = bool(orbit_labels[orbit_id])
        private["label_source"] = "human_adjudicated_v4"
        private["human_label"] = bool(orbit_labels[orbit_id])
        private["adjudicated_label"] = bool(orbit_labels[orbit_id])

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_output = output_dir / f"{pack_name}.human.raw.jsonl"
    private_output = output_dir / f"{pack_name}.human.private_eval.jsonl"
    scored_output = output_dir / f"{pack_name}.human.textonly_scored.jsonl"
    _write_jsonl(raw_output, raw_rows)
    _write_jsonl(private_output, private_rows)
    _write_jsonl(scored_output, scored_rows)
    return {"raw_output": raw_output, "private_output": private_output, "scored_output": scored_output}


def load_adjudicated_labels(path: Path) -> dict[str, bool | None]:
    if not path.exists():
        return {}
    labels = {}
    for row in _read_jsonl(path):
        labels[str(row["audit_id"])] = _parse_label(row.get("adjudicated_label_answerable"))
    return labels


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Human Audit V4 Evaluation Status",
        "",
        f"Ready: `{summary['ready']}`",
        f"Pack count: `{summary['pack_count']}`",
        f"Evaluated pack count: `{summary['evaluated_pack_count']}`",
        f"Allow partial: `{summary['allow_partial']}`",
        "",
        "| Pack | Selected | Labeled | Pending | Evaluation ready | Evaluated |",
        "|---|---:|---:|---:|---|---|",
    ]
    for pack in summary["packs"]:
        lines.append(
            f"| {pack['pack_name']} | {pack['selected_items']} | {pack['labeled']} | "
            f"{pack['pending']} | `{pack['evaluation_ready']}` | `{pack['evaluated']}` |"
        )
    lines.extend(["", "## Failed Gates", ""])
    for pack in summary["packs"]:
        if not pack["failed_gates"]:
            continue
        lines.append(f"{pack['pack_name']}:")
        lines.extend(f"- `{gate['gate']}`: {gate}" for gate in pack["failed_gates"])
        lines.append("")
    lines.extend(["## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def infer_scored_path(raw_path: Path) -> Path:
    name = raw_path.name
    if name.endswith(".raw.jsonl"):
        return raw_path.with_name(name[: -len(".raw.jsonl")] + ".textonly_scored.jsonl")
    raise ValueError(f"cannot infer scored path from {raw_path}")


def _resolve_path(raw_path: str, base: Path) -> Path:
    path = Path(str(raw_path).replace("\\", "/"))
    if path.exists():
        return path
    candidate = base / path.name
    if candidate.exists():
        return candidate
    return path


def _filter_rows(path: Path, orbit_labels: dict[str, bool]) -> list[dict[str, Any]]:
    rows = []
    for row in _read_jsonl(path):
        if str(row.get("orbit_id")) in orbit_labels:
            rows.append(row)
    rows.sort(key=lambda row: str(row["orbit_id"]))
    return rows


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no} is not valid JSON") from exc
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as dst:
        for row in rows:
            dst.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _parse_label(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    if normalized in UNSURE_VALUES:
        return None
    raise ValueError(f"invalid adjudicated label {value!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--summary-md", type=Path)
    parser.add_argument("--allow-partial", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when any pack is not evaluation-ready.")
    args = parser.parse_args()

    summary = run_human_audit_eval_v4(
        args.manifest,
        args.output_dir,
        args.summary_json,
        summary_md=args.summary_md,
        allow_partial=args.allow_partial,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.strict and not summary["ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
