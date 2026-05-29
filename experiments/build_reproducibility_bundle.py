#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from experiments.build_clean_sufficiency_misleading_figure import (
    DEFAULT_INPUTS as CLEAN_FIGURE_INPUTS,
)
from experiments.summarize_end2end_selective_rag_proxy import (
    DEFAULT_INPUTS as END2END_PROXY_INPUTS,
)
from experiments.summarize_mechanism_ablation import DEFAULT_INPUTS as MECHANISM_INPUTS
from experiments.summarize_v4_anti_shortcut import DEFAULT_INPUTS as ANTI_SHORTCUT_INPUTS
from experiments.summarize_v4_failure_taxonomy import DEFAULT_INPUTS as FAILURE_TAXONOMY_INPUTS
from experiments.summarize_v4_strong_baselines import (
    DEFAULT_BASELINES as STRONG_BASELINE_INPUTS,
    DEFAULT_COMPARISONS as STRONG_BASELINE_COMPARISONS,
)


DATASET_CONSTRUCTION_ARTIFACTS = [
    Path("results/hotpot_orbits_v4_semanticswap_n100.construction_audit.json"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.manifest.json"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.manifest.json"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.manifest.json"),
    *FAILURE_TAXONOMY_INPUTS,
    *ANTI_SHORTCUT_INPUTS,
    *END2END_PROXY_INPUTS,
    *CLEAN_FIGURE_INPUTS,
    *MECHANISM_INPUTS,
    *STRONG_BASELINE_INPUTS,
    *STRONG_BASELINE_COMPARISONS,
]

SEED_SOURCE_FILES = [
    Path("results/hotpot_corm_calibration_multiseed.json"),
    Path("results/hotpot_corm_risk_control_cp_multiseed.json"),
    Path("results/fever_nearmiss_corm_v3_calibration_multiseed.json"),
    Path("results/fever_nearmiss_corm_v3_risk_control_cp_multiseed.json"),
    Path("results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json"),
    Path("results/v4_strong_baseline_summary_20260529.json"),
]

HIDDEN_LOCAL_PATH_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:(?:\\\\|\\)[A-Za-z0-9_. -]"),
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/(?!syk\b)[^/\s]+"),
]


def build_reproducibility_bundle(root: Path) -> dict[str, Any]:
    reproducibility = root / "reproducibility"
    reproducibility.mkdir(parents=True, exist_ok=True)

    manifest = _load_json(root / "results/v4_evidence_package_manifest_20260529.json")
    closure = _load_json(root / "results/evidence_closure_status_v4.json")
    claims_summary = _load_optional_json(root / "results/claims_ledger_markdown_summary_20260529.json")
    checkpoint = _load_optional_json(root / "results/corm_remote_checkpoint_status.json")
    release = _load_optional_json(root / "results/corm_release_manifest.json")
    remote_storage = _load_optional_json(root / "results/remote_storage_status_20260529.json")

    checksums = _checksums(root, manifest, checkpoint, release)
    seeds = _seeds(root)
    hidden_path_audit = _hidden_path_audit(root, manifest)
    hardware = _hardware(root, closure, remote_storage)

    outputs = {
        "checksums": reproducibility / "checksums.json",
        "seeds": reproducibility / "seeds.json",
        "hidden_local_path_audit_json": reproducibility / "hidden_local_path_audit.json",
        "hidden_local_path_audit_md": reproducibility / "hidden_local_path_audit.md",
        "hardware": reproducibility / "hardware.md",
        "artifact_manifest": reproducibility / "artifact_manifest.md",
        "reproduction_commands": reproducibility / "reproduction_commands.md",
    }
    _write_json(outputs["checksums"], checksums)
    _write_json(outputs["seeds"], seeds)
    _write_json(outputs["hidden_local_path_audit_json"], hidden_path_audit)
    outputs["hidden_local_path_audit_md"].write_text(
        _render_hidden_path_audit(hidden_path_audit),
        encoding="utf-8",
    )
    outputs["hardware"].write_text(_render_hardware(hardware), encoding="utf-8")
    outputs["artifact_manifest"].write_text(
        _render_artifact_manifest(manifest, checksums),
        encoding="utf-8",
    )
    outputs["reproduction_commands"].write_text(_render_reproduction_commands(), encoding="utf-8")

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "outputs": {name: _display_path(root, path) for name, path in outputs.items()},
        "artifact_count": manifest.get("artifact_count"),
        "manifest_missing_artifact_count": manifest.get("missing_artifact_count"),
        "artifact_checksum_count": len(checksums["artifacts"]),
        "dataset_construction_hash_count": len(checksums["dataset_construction_artifacts"]),
        "checkpoint_hash_available": bool(checksums["checkpoints"]),
        "claims_ledger_markdown_ready": claims_summary.get("failed_claims") == 0
        if claims_summary
        else False,
        "claims_ledger_total_claims": claims_summary.get("total_claims"),
        "seed_source_count": len(seeds["sources"]),
        "unique_seed_count": len(seeds["unique_seeds"]),
        "hidden_local_path_finding_count": hidden_path_audit["finding_count"],
        "hidden_local_path_passed": hidden_path_audit["passed"],
        "remote_storage_ready": _remote_storage_ready(closure),
        "ready_for_neurips_main_claim": closure.get("current_evidence_reproduction", {}).get(
            "ready_for_neurips_main_claim"
        ),
        "claim_boundary": (
            "This reproducibility bundle documents the current evidence package. "
            "It does not complete human audit labels, full CoRM-RAG reproduction, "
            "or general formal risk-control support."
        ),
    }
    _write_json(reproducibility / "bundle_summary_20260529.json", summary)
    return summary


def _checksums(
    root: Path,
    manifest: dict[str, Any],
    checkpoint: dict[str, Any],
    release: dict[str, Any],
) -> dict[str, Any]:
    artifact_rows = [
        {
            "path": _normalize(row.get("path", "")),
            "exists": row.get("exists"),
            "size_bytes": row.get("size_bytes"),
            "sha256": row.get("sha256"),
        }
        for row in manifest.get("artifacts", [])
    ]
    dataset_rows = [
        _hash_row(root, path)
        for path in _unique_paths(DATASET_CONSTRUCTION_ARTIFACTS)
        if (root / path).exists()
    ]
    checkpoints = []
    local_checkpoint = checkpoint.get("local", {})
    if local_checkpoint.get("sha256"):
        checkpoints.append(
            {
                "name": "CoRM critic checkpoint",
                "path": local_checkpoint.get("path"),
                "size_bytes": local_checkpoint.get("size_bytes"),
                "sha256": local_checkpoint.get("sha256"),
                "remote_sha256": checkpoint.get("remote_sha256"),
                "sha256_match": checkpoint.get("sha256_match"),
                "source": "results/corm_remote_checkpoint_status.json",
            }
        )
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifacts": artifact_rows,
        "dataset_construction_artifacts": dataset_rows,
        "checkpoints": checkpoints,
        "release_status": {
            "source": "results/corm_release_manifest.json",
            "hf_repo": release.get("hf_repo"),
            "release_status": release.get("release_status"),
            "checkpoint_available": release.get("checkpoint_available"),
            "missing_public_data_artifacts": release.get("missing_public_data_artifacts", []),
        },
        "claim_boundary": (
            "Checksums prove artifact identity only; they do not prove human-label validity "
            "or completed full CoRM-RAG reproduction."
        ),
    }


def _seeds(root: Path) -> dict[str, Any]:
    sources = []
    unique: set[int] = set()
    for path in SEED_SOURCE_FILES:
        absolute = root / path
        if not absolute.exists():
            continue
        payload = _load_json(absolute)
        seeds = sorted(_extract_ints_by_key(payload, "seeds"))
        if not seeds:
            seeds = sorted(_extract_seed_suffixes(payload))
        for seed in seeds:
            unique.add(seed)
        sources.append({"path": str(path), "seeds": seeds})
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
        "unique_seeds": sorted(unique),
        "fixed_seed_policy": (
            "Current bridge/calibration evidence uses explicit data or split seeds recorded "
            "in result JSON files. Regeneration scripts should preserve these seeds unless "
            "a new preregistered sweep is added."
        ),
    }


def _hidden_path_audit(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    findings = []
    for row in manifest.get("artifacts", []):
        artifact_name = _normalize(row.get("path", ""))
        if _skip_hidden_path_scan(artifact_name):
            continue
        path = root / row.get("path", "")
        if not path.exists() or path.stat().st_size > 2_000_000:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in HIDDEN_LOCAL_PATH_PATTERNS:
            for match in pattern.finditer(text):
                findings.append(
                    {
                        "artifact": artifact_name,
                        "pattern": pattern.pattern,
                        "match": match.group(0),
                    }
                )
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scanned_artifact_count": len(manifest.get("artifacts", [])),
        "finding_count": len(findings),
        "passed": len(findings) == 0,
        "findings": findings,
        "allowed_remote_path_note": (
            "Remote /mnt/ntfs-disk and /home/syk paths are documented operational paths, "
            "not hidden local dependencies."
        ),
    }


def _skip_hidden_path_scan(path: str) -> bool:
    return path in {
        "reproducibility/hidden_local_path_audit.json",
        "reproducibility/hidden_local_path_audit.md",
        "experiments/build_reproducibility_bundle.py",
    }


def _hardware(root: Path, closure: dict[str, Any], remote_storage: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "local": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "processor": platform.processor(),
        },
        "remote": {
            "storage_probe": _display_path(root, root / "results/remote_storage_status_20260529.json"),
            "gpu_query_stdout": _get(remote_storage, "gpu_query", "stdout"),
            "target": remote_storage.get("target"),
            "target_filesystem_type": _target_filesystem_type(remote_storage),
            "target_available_gib": remote_storage.get("target_available_gib"),
            "target_write_probe_passed": remote_storage.get("target_write_probe_passed"),
            "ready_for_full_reproduction_storage": remote_storage.get(
                "ready_for_full_reproduction_storage"
            ),
        },
        "corm_reconstruction": closure.get("corm_reconstruction", {}),
    }


def _render_hardware(hardware: dict[str, Any]) -> str:
    remote = hardware["remote"]
    reconstruction = hardware["corm_reconstruction"]
    return "\n".join(
        [
            "# Hardware And Storage",
            "",
            f"Generated: `{hardware['generated_at_utc']}`",
            "",
            "## Local",
            "",
            f"- Python: `{hardware['local']['python']}`",
            f"- Platform: `{hardware['local']['platform']}`",
            f"- Processor: `{hardware['local']['processor']}`",
            "",
            "## Remote GPU / Storage Snapshot",
            "",
            f"- Storage probe: `{remote['storage_probe']}`",
            f"- GPU query: `{(remote['gpu_query_stdout'] or '').strip()}`",
            f"- Target: `{remote['target']}`; filesystem: `{remote['target_filesystem_type']}`.",
            f"- Available GiB: `{remote['target_available_gib']}`.",
            f"- Write probe passed: `{remote['target_write_probe_passed']}`.",
            f"- Ready for full reproduction storage: "
            f"`{remote['ready_for_full_reproduction_storage']}`.",
            "",
            "## CoRM Reconstruction Boundary",
            "",
            f"- Preflight ready: `{reconstruction.get('preflight_ready')}`.",
            f"- Remote status: `{reconstruction.get('remote_status')}`.",
            f"- Complete embedding shards: `{reconstruction.get('complete_embedding_shards')}`.",
            f"- wiki.faiss exists: `{reconstruction.get('wiki_faiss_exists')}`.",
            "",
        ]
    )


def _render_artifact_manifest(manifest: dict[str, Any], checksums: dict[str, Any]) -> str:
    lines = [
        "# Reproducibility Artifact Manifest",
        "",
        f"Manifest artifacts: `{manifest.get('artifact_count')}`.",
        f"Missing artifacts: `{manifest.get('missing_artifact_count')}`.",
        f"Dataset construction hashes: `{len(checksums['dataset_construction_artifacts'])}`.",
            f"Checkpoint hashes: `{len(checksums['checkpoints'])}`.",
            f"Claims ledger markdown: `CLAIMS_LEDGER.md`.",
            "",
        "## Current Evidence Artifacts",
        "",
        "| Path | Bytes | SHA256 |",
        "|---|---:|---|",
    ]
    for row in checksums["artifacts"]:
        lines.append(f"| `{row['path']}` | `{row['size_bytes']}` | `{row['sha256']}` |")
    lines.extend(["", "## Dataset Construction Artifacts", "", "| Path | Bytes | SHA256 |", "|---|---:|---|"])
    for row in checksums["dataset_construction_artifacts"]:
        lines.append(f"| `{row['path']}` | `{row['size_bytes']}` | `{row['sha256']}` |")
    lines.append("")
    return "\n".join(lines)


def _render_hidden_path_audit(audit: dict[str, Any]) -> str:
    lines = [
        "# Hidden Local Path Audit",
        "",
        f"Passed: `{audit['passed']}`.",
        f"Scanned artifacts: `{audit['scanned_artifact_count']}`.",
        f"Findings: `{audit['finding_count']}`.",
        "",
        audit["allowed_remote_path_note"],
        "",
    ]
    if audit["findings"]:
        lines.extend(["## Findings", "", "| Artifact | Pattern | Match |", "|---|---|---|"])
        lines.extend(
            f"| `{item['artifact']}` | `{item['pattern']}` | `{item['match']}` |"
            for item in audit["findings"]
        )
        lines.append("")
    return "\n".join(lines)


def _render_reproduction_commands() -> str:
    return "\n".join(
        [
            "# Reproduction Commands",
            "",
            "## Smoke Test",
            "",
            "```powershell",
            ".\\scripts\\run_smoke.ps1",
            "```",
            "",
            "Equivalent command:",
            "",
            "```powershell",
            "$env:PYTHONPATH='src'; python -m pytest tests/test_build_results_provenance_readme.py tests/test_build_claims_ledger_markdown.py tests/test_build_reproducibility_bundle.py tests/test_materialize_human_audit_v4_assignment_batches.py tests/test_collect_human_audit_v4_assignment_batches.py tests/test_summarize_v4_claim_safe_target_selection.py tests/test_summarize_neurips_unblock_plan.py tests/test_verify_v4_evidence_package.py -q",
            "```",
            "",
            "## Main Current-Evidence Tables",
            "",
            "```powershell",
            ".\\scripts\\run_main_tables.ps1",
            "```",
            "",
            "This rebuilds the current evidence package, provenance README, reproducibility bundle, and evidence manifest. It does not fabricate human labels or complete full CoRM-RAG reproduction.",
            "",
        ]
    )


def _hash_row(root: Path, path: Path) -> dict[str, Any]:
    absolute = root / path
    return {
        "path": _normalize(str(path)),
        "size_bytes": absolute.stat().st_size,
        "sha256": _sha256(absolute),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _extract_ints_by_key(value: Any, key: str) -> set[int]:
    found: set[int] = set()
    if isinstance(value, dict):
        for item_key, item_value in value.items():
            if item_key == key and isinstance(item_value, list):
                found.update(int(seed) for seed in item_value if isinstance(seed, int))
            else:
                found.update(_extract_ints_by_key(item_value, key))
    elif isinstance(value, list):
        for item in value:
            found.update(_extract_ints_by_key(item, key))
    return found


def _extract_seed_suffixes(value: Any) -> set[int]:
    text = json.dumps(value, ensure_ascii=True)
    return {int(seed) for seed in re.findall(r"seed(\d+)", text)}


def _unique_paths(paths: list[Path]) -> list[Path]:
    seen = set()
    output = []
    for path in paths:
        normalized = _normalize(str(path))
        if normalized not in seen:
            seen.add(normalized)
            output.append(path)
    return output


def _remote_storage_ready(closure: dict[str, Any]) -> bool:
    probe = closure.get("corm_reconstruction", {}).get("latest_storage_probe") or {}
    return bool(probe.get("ready_for_full_reproduction_storage"))


def _target_filesystem_type(remote_storage: dict[str, Any]) -> str | None:
    target = remote_storage.get("target")
    for filesystem in remote_storage.get("filesystems", []):
        if filesystem.get("mount") == target:
            return filesystem.get("type")
    return None


def _get(payload: dict[str, Any], *path: str) -> Any:
    cursor: Any = payload
    for part in path:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(part)
    return cursor


def _display_path(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def _normalize(path: str) -> str:
    return path.replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _load_json(path)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    summary = build_reproducibility_bundle(args.root)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
