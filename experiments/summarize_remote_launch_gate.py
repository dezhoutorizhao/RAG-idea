#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_HOME_PROBE = Path("results/remote_home_storage_status_latest.json")
DEFAULT_NTFS_PROBE = Path("results/remote_ntfs_storage_status_latest.json")
DEFAULT_CORM_MANIFEST = Path("results/corm_remote_scripts_ext4_manifest.json")
DEFAULT_CLEANUP_PLAN = Path("results/remote_ext4_cleanup_guarded_plan_20260529.json")
DEFAULT_CLEANUP_CANDIDATES = Path("results/remote_cleanup_candidates_20260529.json")


def summarize_remote_launch_gate(
    root: Path = Path("."),
    *,
    home_probe_path: Path = DEFAULT_HOME_PROBE,
    ntfs_probe_path: Path = DEFAULT_NTFS_PROBE,
    corm_manifest_path: Path = DEFAULT_CORM_MANIFEST,
    cleanup_plan_path: Path = DEFAULT_CLEANUP_PLAN,
    cleanup_candidates_path: Path = DEFAULT_CLEANUP_CANDIDATES,
) -> dict[str, Any]:
    home_probe = _load_optional_json(root / home_probe_path)
    ntfs_probe = _load_optional_json(root / ntfs_probe_path)
    manifest = _load_optional_json(root / corm_manifest_path)
    cleanup_plan = _load_optional_json(root / cleanup_plan_path)
    cleanup_candidates = _load_optional_json(root / cleanup_candidates_path)

    home_ready = _storage_ready(home_probe)
    ntfs_ready = _storage_ready(ntfs_probe)
    manifest_ready = manifest.get("status") == "materialized" and not manifest.get("contains_secret_markers")
    ext4_root = manifest.get("remote_root")
    cleanup_reclaim_gib = cleanup_candidates.get("recommended_reclaim_gib_lower_bound")
    cleanup_preflight_passed = bool((cleanup_plan.get("preflight") or {}).get("passed"))
    cleanup_executed = bool(cleanup_plan.get("destructive_operations_executed"))

    blockers = []
    if not home_ready:
        blockers.append(
            "ext4_home_storage_not_ready: /home/syk is writable but does not meet the 180 GiB free-space gate"
        )
    if not manifest_ready:
        blockers.append("ext4_corm_script_manifest_not_ready")
    if not cleanup_executed:
        blockers.append("guarded_ext4_cleanup_not_executed")
    if not ntfs_ready:
        blockers.append("ntfs_target_not_usable_for_full_reproduction")

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_artifacts": {
            "home_probe": str(home_probe_path),
            "ntfs_probe": str(ntfs_probe_path),
            "corm_manifest": str(corm_manifest_path),
            "cleanup_plan": str(cleanup_plan_path),
            "cleanup_candidates": str(cleanup_candidates_path),
        },
        "gpu_summary": _gpu_summary(home_probe or ntfs_probe),
        "home_ext4_gate": _storage_gate(home_probe),
        "ntfs_gate": _storage_gate(ntfs_probe),
        "corm_script_gate": {
            "manifest_ready": manifest_ready,
            "remote_root": ext4_root,
            "script_count": manifest.get("script_count"),
            "contains_secret_markers": manifest.get("contains_secret_markers"),
            "claim_policy": manifest.get("claim_policy"),
        },
        "cleanup_gate": {
            "cleanup_preflight_passed": cleanup_preflight_passed,
            "destructive_operations_executed": cleanup_executed,
            "recommended_reclaim_gib_lower_bound": cleanup_reclaim_gib,
            "approval_token_required": cleanup_plan.get("confirm_token_required"),
        },
        "ready_to_launch_full_corm_reproduction": bool(home_ready and manifest_ready and cleanup_executed),
        "must_not_launch_reasons": blockers,
        "next_safe_actions": [
            "obtain explicit user approval before executing guarded ext4 cleanup",
            "after cleanup, rerun the /home/syk storage probe and require >=180 GiB plus write probe pass",
            "launch results/corm_remote_scripts_ext4/02_build_wikipedia_and_faiss.sh only after the post-cleanup gate passes",
        ],
        "claim_policy": (
            "This artifact is a launch gate only. It records whether Full CoRM-RAG may be started; "
            "it is not evidence that Full CoRM-RAG has completed."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    home = summary["home_ext4_gate"]
    ntfs = summary["ntfs_gate"]
    scripts = summary["corm_script_gate"]
    cleanup = summary["cleanup_gate"]
    lines = [
        "# Remote Full CoRM-RAG Launch Gate",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Ready to launch Full CoRM-RAG: `{summary['ready_to_launch_full_corm_reproduction']}`",
        "",
        "## Storage Gates",
        "",
        "| Target | Ready | Free GiB | Min-free met | Write probe |",
        "|---|---:|---:|---:|---:|",
        (
            f"| `{home.get('target')}` | `{home.get('ready')}` | `{_fmt(home.get('available_gib'))}` | "
            f"`{home.get('min_free_met')}` | `{home.get('write_probe_passed')}` |"
        ),
        (
            f"| `{ntfs.get('target')}` | `{ntfs.get('ready')}` | `{_fmt(ntfs.get('available_gib'))}` | "
            f"`{ntfs.get('min_free_met')}` | `{ntfs.get('write_probe_passed')}` |"
        ),
        "",
        "## Script Gate",
        "",
        f"- Manifest ready: `{scripts.get('manifest_ready')}`.",
        f"- Remote root: `{scripts.get('remote_root')}`.",
        f"- Script count: `{scripts.get('script_count')}`.",
        f"- Contains secret markers: `{scripts.get('contains_secret_markers')}`.",
        "",
        "## Cleanup Gate",
        "",
        f"- Cleanup preflight passed: `{cleanup.get('cleanup_preflight_passed')}`.",
        f"- Destructive operations executed: `{cleanup.get('destructive_operations_executed')}`.",
        "- Recommended reclaim lower bound: "
        f"`{_fmt(cleanup.get('recommended_reclaim_gib_lower_bound'))} GiB`.",
        "",
        "## Must Not Launch Reasons",
        "",
    ]
    lines.extend(f"- {reason}" for reason in summary["must_not_launch_reasons"])
    lines.extend(["", "## Next Safe Actions", ""])
    lines.extend(f"- {action}" for action in summary["next_safe_actions"])
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _storage_ready(payload: dict[str, Any]) -> bool:
    return bool(payload.get("ready_for_full_reproduction_storage"))


def _storage_gate(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "target": payload.get("target"),
        "observed_at_utc": payload.get("observed_at_utc"),
        "ready": payload.get("ready_for_full_reproduction_storage"),
        "available_gib": payload.get("target_available_gib"),
        "min_free_met": payload.get("target_min_free_met"),
        "write_probe_passed": payload.get("target_write_probe_passed"),
    }


def _gpu_summary(payload: dict[str, Any]) -> dict[str, Any]:
    gpu = payload.get("gpu_query") or {}
    rows = []
    for line in (gpu.get("stdout") or "").splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) >= 4:
            rows.append(
                {
                    "index": parts[0],
                    "name": parts[1],
                    "memory_total_mib": _int_or_none(parts[2]),
                    "memory_free_mib": _int_or_none(parts[3]),
                }
            )
    return {"query_exit_status": gpu.get("exit_status"), "gpus": rows}


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _fmt(value: Any) -> str:
    if value is None:
        return "unknown"
    return f"{float(value):.1f}"


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_remote_launch_gate(args.root)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
