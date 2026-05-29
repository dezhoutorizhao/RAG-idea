#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_ARTIFACTS = [
    Path("results/current_evidence_reproduction_20260529.json"),
    Path("results/current_evidence_reproduction_20260529.md"),
    Path("results/evidence_closure_status_v4.json"),
    Path("results/evidence_closure_status_v4.md"),
    Path("results/results_provenance_manifest_20260529.json"),
    Path("results/README.md"),
    Path("results/neurips_readiness_matrix_20260529.json"),
    Path("results/neurips_readiness_matrix_20260529.md"),
    Path("results/human_audit_v4_status_20260529.json"),
    Path("results/human_audit_v4_status_20260529.md"),
    Path("results/human_audit_v4_eval_status_20260529.json"),
    Path("results/human_audit_v4_eval_status_20260529.md"),
    Path("results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json"),
    Path("results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.md"),
    Path("results/end2end_selective_rag_proxy_summary_20260529.json"),
    Path("results/end2end_selective_rag_proxy_summary_20260529.md"),
    Path("results/mechanism_ablation_summary_20260529.json"),
    Path("results/mechanism_ablation_summary_20260529.md"),
    Path("results/v4_strong_baseline_summary_20260529.json"),
    Path("results/v4_strong_baseline_summary_20260529.md"),
    Path("results/v4_anti_shortcut_summary_20260529.json"),
    Path("results/v4_anti_shortcut_summary_20260529.md"),
    Path("results/v4_failure_taxonomy_summary_20260529.json"),
    Path("results/v4_failure_taxonomy_summary_20260529.md"),
    Path("results/v4_case_gallery_summary_20260529.json"),
    Path("results/clean_sufficiency_misleading_v4_20260529.json"),
    Path("paper/case_studies/v4_case_gallery_20260529.jsonl"),
    Path("paper/case_studies/v4_case_gallery_20260529.md"),
    Path("paper/figures/clean_sufficiency_misleading_v4_20260529.csv"),
    Path("paper/figures/clean_sufficiency_misleading_v4_20260529.svg"),
    Path("paper/figures/clean_sufficiency_misleading_v4_20260529.md"),
    Path("reproducibility/checksums.json"),
    Path("reproducibility/seeds.json"),
    Path("reproducibility/hardware.md"),
    Path("reproducibility/artifact_manifest.md"),
    Path("reproducibility/hidden_local_path_audit.json"),
    Path("reproducibility/hidden_local_path_audit.md"),
    Path("reproducibility/reproduction_commands.md"),
    Path("reproducibility/bundle_summary_20260529.json"),
    Path("scripts/run_smoke.ps1"),
    Path("scripts/run_main_tables.ps1"),
    Path(".github/workflows/ci.yml"),
    Path("experiments/reproduce_current_evidence_v4.py"),
    Path("experiments/build_results_provenance_readme.py"),
    Path("experiments/build_reproducibility_bundle.py"),
    Path("experiments/summarize_evidence_closure.py"),
    Path("experiments/summarize_neurips_readiness.py"),
    Path("experiments/summarize_mechanism_ablation.py"),
    Path("experiments/summarize_v4_failure_taxonomy.py"),
    Path("experiments/summarize_v4_anti_shortcut.py"),
    Path("experiments/export_v4_case_gallery.py"),
    Path("experiments/build_clean_sufficiency_misleading_figure.py"),
]


def verify_v4_evidence_package(root: Path, artifacts: Sequence[Path]) -> dict[str, Any]:
    artifact_rows = [_artifact_row(root / path, path) for path in artifacts]
    missing = [row["path"] for row in artifact_rows if not row["exists"]]
    closure = _load_json(root / "results/evidence_closure_status_v4.json")
    reproduction = _load_json(root / "results/current_evidence_reproduction_20260529.json")
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "artifact_count": len(artifact_rows),
        "missing_artifact_count": len(missing),
        "missing_artifacts": missing,
        "artifacts": artifact_rows,
        "gate_summary": reproduction.get("gate_summary", {}),
        "ready_for_neurips_main_claim": reproduction.get("ready_for_neurips_main_claim"),
        "claim_verification": closure.get("claim_verification", {}),
        "remaining_human_audit_blockers": closure.get("remaining_human_audit_blockers", []),
        "remaining_non_human_blockers": closure.get("remaining_non_human_blockers", []),
        "allowed_claim_count": len(closure.get("allowed_claims", [])),
        "disallowed_claim_count": len(closure.get("disallowed_claims", [])),
        "package_status": "complete_with_known_blockers" if not missing else "incomplete_missing_artifacts",
        "claim_boundary": (
            "This manifest verifies that the current evidence package is present and hashable. "
            "It does not convert pending human audit, failed storage, proxy-only end-to-end results, "
            "or negative strong-baseline evidence into NeurIPS-ready main-claim support."
        ),
    }


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# V4 Evidence Package Manifest",
        "",
        f"Generated: `{manifest['generated_at_utc']}`",
        "",
        f"Package status: `{manifest['package_status']}`",
        f"Ready for NeurIPS main claim: `{manifest['ready_for_neurips_main_claim']}`",
        f"Missing artifacts: `{manifest['missing_artifact_count']}`",
        "",
        "## Gate Summary",
        "",
    ]
    for key, value in manifest["gate_summary"].items():
        lines.append(f"- {key}: `{value}`")

    claims = manifest["claim_verification"]
    lines.extend(
        [
            "",
            "## Claim Verification",
            "",
            f"- Passed: `{claims.get('passed_claims')}/{claims.get('total_claims')}`.",
            f"- Failed: `{claims.get('failed_claims')}`.",
            f"- Allowed/disallowed claim counts: `{manifest['allowed_claim_count']}` / `{manifest['disallowed_claim_count']}`.",
            "",
            "## Artifacts",
            "",
            "| Path | Exists | Bytes | SHA256 |",
            "|---|---:|---:|---|",
        ]
    )
    for row in manifest["artifacts"]:
        lines.append(
            f"| `{row['path']}` | `{row['exists']}` | `{row['size_bytes']}` | `{row['sha256']}` |"
        )

    lines.extend(["", "## Remaining Human-Audit Blockers", ""])
    lines.extend(f"- {item}" for item in manifest["remaining_human_audit_blockers"])
    lines.extend(["", "## Remaining Non-Human Blockers", ""])
    lines.extend(f"- {item}" for item in manifest["remaining_non_human_blockers"])
    lines.extend(["", "## Claim Boundary", "", manifest["claim_boundary"], ""])
    return "\n".join(lines)


def _artifact_row(path: Path, display_path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(display_path),
            "exists": False,
            "size_bytes": None,
            "sha256": None,
        }
    return {
        "path": str(display_path),
        "exists": True,
        "size_bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }


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
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, nargs="+", default=DEFAULT_ARTIFACTS)
    args = parser.parse_args()

    manifest = verify_v4_evidence_package(args.root, args.artifacts)
    _write_json(args.output_json, manifest)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(manifest), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
