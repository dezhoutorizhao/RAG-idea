#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROVENANCE_BY_STEP = {
    "summarize_human_audit_v4_status": "experiments/summarize_human_audit_v4_status.py",
    "run_human_audit_eval_v4": "experiments/run_human_audit_eval_v4.py",
    "summarize_fever_cp_transfer_sweep": "experiments/summarize_fever_cp_transfer_sweep.py",
    "summarize_end2end_selective_rag_proxy": "experiments/summarize_end2end_selective_rag_proxy.py",
    "summarize_v4_strong_baselines": "experiments/summarize_v4_strong_baselines.py",
    "summarize_v4_failure_taxonomy": "experiments/summarize_v4_failure_taxonomy.py",
    "export_v4_case_gallery": "experiments/export_v4_case_gallery.py",
    "build_clean_sufficiency_misleading_figure": "experiments/build_clean_sufficiency_misleading_figure.py",
    "summarize_v4_anti_shortcut": "experiments/summarize_v4_anti_shortcut.py",
    "summarize_mechanism_ablation": "experiments/summarize_mechanism_ablation.py",
    "verify_claims": "experiments/verify_claims.py",
    "summarize_evidence_closure": "experiments/summarize_evidence_closure.py",
    "summarize_neurips_readiness": "experiments/summarize_neurips_readiness.py",
    "build_results_provenance_readme": "experiments/build_results_provenance_readme.py",
    "build_claims_ledger_markdown": "experiments/build_claims_ledger_markdown.py",
    "build_reproducibility_bundle": "experiments/build_reproducibility_bundle.py",
}


def build_results_provenance_readme(
    root: Path,
    reproduction_path: Path,
    evidence_manifest_path: Path,
    readiness_path: Path,
) -> dict[str, Any]:
    reproduction = _load_json(reproduction_path)
    evidence_manifest = _load_json(evidence_manifest_path) if evidence_manifest_path.exists() else {}
    readiness = _load_json(readiness_path) if readiness_path.exists() else {}
    artifact_index = _artifact_index(evidence_manifest)

    steps = []
    for command in reproduction.get("commands", []):
        outputs = [
            _output_row(root, Path(raw_output), artifact_index)
            for raw_output in command.get("outputs", [])
        ]
        steps.append(
            {
                "step": command.get("name"),
                "ready": command.get("ready"),
                "source_script": PROVENANCE_BY_STEP.get(command.get("name"), "unknown"),
                "reproduction_entrypoint": "experiments/reproduce_current_evidence_v4.py",
                "outputs": outputs,
                "all_outputs_present": all(row["exists"] for row in outputs),
            }
        )

    missing_outputs = [
        row["path"]
        for step in steps
        for row in step["outputs"]
        if not row["exists"]
    ]
    untracked_outputs = [
        row["path"]
        for step in steps
        for row in step["outputs"]
        if row["exists"] and not row["manifest_tracked"]
    ]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "source_reports": {
            "current_evidence_reproduction": _display_path(root, reproduction_path),
            "v4_evidence_package_manifest": _display_path(root, evidence_manifest_path),
            "neurips_readiness_matrix": _display_path(root, readiness_path),
        },
        "reproduction_ready_for_neurips_main_claim": reproduction.get(
            "ready_for_neurips_main_claim"
        ),
        "step_count": len(steps),
        "steps": steps,
        "artifact_count": evidence_manifest.get("artifact_count"),
        "manifest_missing_artifact_count": evidence_manifest.get("missing_artifact_count"),
        "missing_output_count": len(missing_outputs),
        "missing_outputs": missing_outputs,
        "untracked_output_count": len(untracked_outputs),
        "untracked_outputs": untracked_outputs,
        "untracked_or_missing_output_count": len(missing_outputs),
        "untracked_or_missing_outputs": missing_outputs,
        "readiness_status_counts": readiness.get("status_counts", {}),
        "known_blockers": {
            "human_audit": reproduction.get("blockers", {}).get("human_audit", []),
            "non_human": reproduction.get("blockers", {}).get("non_human", []),
            "hard_readiness_blockers": [
                {
                    "requirement": row.get("requirement"),
                    "status": row.get("status"),
                    "boundary_or_next_action": row.get("boundary_or_next_action"),
                }
                for row in readiness.get("hard_blockers", [])
            ],
        },
        "claim_boundary": (
            "This README records artifact provenance for the current evidence package. "
            "It does not complete pending human audit labels, full CoRM-RAG reproduction, "
            "or unsupported formal/general risk-control claims."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Results Provenance",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Ready for NeurIPS main-track claim: "
        f"`{summary['reproduction_ready_for_neurips_main_claim']}`.",
        "",
        "This package is complete only as a current-evidence snapshot with known blockers; "
        "it is not a NeurIPS main-track-ready evidence closure.",
        "",
        "## Source Reports",
        "",
    ]
    for name, path in summary["source_reports"].items():
        lines.append(f"- {name}: `{path}`")

    lines.extend(
        [
            "",
            "## Step Provenance",
            "",
            "| Step | Ready | Source script | Outputs |",
            "|---|---:|---|---|",
        ]
    )
    for step in summary["steps"]:
        outputs = "<br>".join(
            (
                f"`{row['path']}` "
                f"(exists=`{row['exists']}`, tracked=`{row['manifest_tracked']}`, "
                f"sha256=`{_short_hash(row['sha256'])}`)"
            )
            for row in step["outputs"]
        )
        lines.append(
            f"| {step['step']} | `{step['ready']}` | "
            f"`{step['source_script']}` | {outputs} |"
        )

    lines.extend(
        [
            "",
            "## Reproduce Current Package",
            "",
            "```bash",
            "python -m experiments.reproduce_current_evidence_v4 "
            "--output-json results/current_evidence_reproduction_20260529.json "
            "--output-md results/current_evidence_reproduction_20260529.md",
            "python -m experiments.verify_v4_evidence_package "
            "--output-json results/v4_evidence_package_manifest_20260529.json "
            "--output-md results/v4_evidence_package_manifest_20260529.md",
            "python -m experiments.build_results_provenance_readme "
            "--output-json results/results_provenance_manifest_20260529.json "
            "--output-md results/README.md",
            "```",
            "",
            "## Artifact Status",
            "",
            f"- Evidence manifest artifact count: `{summary['artifact_count']}`.",
            f"- Evidence manifest missing artifacts: "
            f"`{summary['manifest_missing_artifact_count']}`.",
            f"- Missing current-step outputs: `{summary['missing_output_count']}`.",
            f"- Current-step outputs not listed in evidence manifest: "
            f"`{summary['untracked_output_count']}`.",
            f"- Readiness status counts: `{summary['readiness_status_counts']}`.",
            "",
            "## Known Blockers",
            "",
            "Human audit:",
        ]
    )
    lines.extend(f"- {item}" for item in summary["known_blockers"]["human_audit"])
    lines.extend(["", "Non-human:"])
    lines.extend(f"- {item}" for item in summary["known_blockers"]["non_human"])
    lines.extend(["", "Readiness matrix hard blockers:"])
    lines.extend(
        f"- {item['requirement']} (`{item['status']}`): {item['boundary_or_next_action']}"
        for item in summary["known_blockers"]["hard_readiness_blockers"]
    )
    lines.extend(["", "## Claim Boundary", "", summary["claim_boundary"], ""])
    return "\n".join(lines)


def _artifact_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index = {}
    for row in manifest.get("artifacts", []):
        normalized = _normalize_path(row.get("path", ""))
        index[normalized] = row
    return index


def _output_row(root: Path, output: Path, artifact_index: dict[str, dict[str, Any]]) -> dict[str, Any]:
    absolute = output if output.is_absolute() else root / output
    display = _display_path(root, absolute)
    normalized = _normalize_path(display)
    manifest_row = artifact_index.get(normalized)
    if manifest_row:
        return {
            "path": normalized,
            "exists": bool(manifest_row.get("exists")),
            "size_bytes": manifest_row.get("size_bytes"),
            "sha256": manifest_row.get("sha256"),
            "manifest_tracked": True,
        }

    exists = absolute.exists()
    return {
        "path": normalized,
        "exists": exists,
        "size_bytes": absolute.stat().st_size if exists else None,
        "sha256": _sha256(absolute) if exists else None,
        "manifest_tracked": False,
    }


def _display_path(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def _short_hash(value: str | None) -> str:
    if not value:
        return "None"
    return value[:12]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--reproduction-json",
        type=Path,
        default=Path("results/current_evidence_reproduction_20260529.json"),
    )
    parser.add_argument(
        "--evidence-manifest-json",
        type=Path,
        default=Path("results/v4_evidence_package_manifest_20260529.json"),
    )
    parser.add_argument(
        "--readiness-json",
        type=Path,
        default=Path("results/neurips_readiness_matrix_20260529.json"),
    )
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.root
    summary = build_results_provenance_readme(
        root,
        root / args.reproduction_json,
        root / args.evidence_manifest_json,
        root / args.readiness_json,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
