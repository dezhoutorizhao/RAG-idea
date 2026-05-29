#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from experiments.prepare_remote_ext4_storage import prepare_remote_ext4_storage
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from experiments.prepare_remote_ext4_storage import prepare_remote_ext4_storage


CONFIRM_TOKEN = "APPROVE_EXT4_LOG_CACHE_CLEANUP_FOR_FULL_CORM_RAG_REPRO"
DEFAULT_CANDIDATES = Path("results/remote_cleanup_candidates_20260529.json")
DEFAULT_OUTPUT_JSON = Path("results/remote_ext4_cleanup_guarded_plan_20260529.json")
DEFAULT_OUTPUT_MD = Path("results/remote_ext4_cleanup_guarded_plan_20260529.md")


def build_guarded_cleanup_plan(
    *,
    candidates: dict[str, Any],
    host: str,
    user: str,
    port: int,
    target: str,
    min_free_gib: float,
    execute: bool,
    confirm_token: str | None,
) -> dict[str, Any]:
    confirmation_valid = confirm_token == CONFIRM_TOKEN
    preflight = validate_cleanup_candidates(candidates, min_reclaim_gib=min_free_gib)
    can_execute = bool(execute and confirmation_valid and preflight["passed"])
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "remote": {"host": host, "user": user, "port": port},
        "target": target,
        "min_free_gib": min_free_gib,
        "execute_requested": execute,
        "destructive_operations_executed": False,
        "confirm_token_required": CONFIRM_TOKEN,
        "confirmation_valid": confirmation_valid,
        "preflight": preflight,
        "can_execute": can_execute,
        "cleanup_scope": [
            "truncate Docker json-file logs only",
            "delete immediate contents of /root/.cache",
            f"delete immediate contents of /home/{user}/.cache",
        ],
        "explicit_non_scope": [
            "no docker system prune",
            "no Docker volume deletion",
            "no container/image deletion",
            "no /mnt/ntfs-disk deletion",
            "no other users' home directory deletion",
        ],
        "execute_command": (
            "$env:CORM_REMOTE_PASSWORD='<set locally>'; "
            "python -m experiments.guarded_remote_ext4_cleanup "
            f"--host {host} --user {user} --port {port} --target {target} "
            f"--min-free-gib {min_free_gib:g} --execute --confirm-token {CONFIRM_TOKEN}"
        ),
        "post_execute_probe_required": (
            "$env:CORM_REMOTE_PASSWORD='<set locally>'; "
            "python -m experiments.check_remote_storage_status "
            f"--host {host} --user {user} --port {port} --target {target} "
            "--output results/remote_storage_status_after_ext4_cleanup.json "
            f"--min-free-gib {min_free_gib:g}"
        ),
        "claim_policy": (
            "This guarded plan is not a cleanup result. It exists to prevent accidental remote "
            "deletion and to make the required approval token and cleanup scope auditable."
        ),
    }


def validate_cleanup_candidates(candidates: dict[str, Any], *, min_reclaim_gib: float) -> dict[str, Any]:
    reclaim = float(candidates.get("recommended_reclaim_gib_lower_bound") or 0.0)
    read_only = candidates.get("destructive_operations_executed") is False
    scope = set(candidates.get("recommended_cleanup_scope") or [])
    expected_scope = {
        "truncate_docker_json_logs",
        "clear_root_cache_contents",
        "clear_user_cache_contents",
    }
    scope_ok = expected_scope.issubset(scope)
    return {
        "passed": bool(read_only and scope_ok and reclaim >= min_reclaim_gib),
        "candidate_audit_read_only": read_only,
        "recommended_reclaim_gib_lower_bound": reclaim,
        "min_reclaim_gib_required": min_reclaim_gib,
        "recommended_reclaim_met": reclaim >= min_reclaim_gib,
        "required_scope_present": scope_ok,
        "required_scope": sorted(expected_scope),
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Guarded Remote Ext4 Cleanup Plan",
        "",
        f"Generated: `{plan['generated_at_utc']}`",
        f"Remote: `{plan['remote']['user']}@{plan['remote']['host']}:{plan['remote']['port']}`",
        f"Target: `{plan['target']}`",
        f"Execute requested: `{plan['execute_requested']}`",
        f"Destructive operations executed: `{plan['destructive_operations_executed']}`",
        f"Can execute now: `{plan['can_execute']}`",
        "",
        "## Preflight",
        "",
        f"- Passed: `{plan['preflight']['passed']}`.",
        "- Recommended reclaim lower bound: "
        f"`{plan['preflight']['recommended_reclaim_gib_lower_bound']:.1f} GiB`.",
        f"- Required reclaim lower bound: `{plan['preflight']['min_reclaim_gib_required']:.1f} GiB`.",
        f"- Candidate audit read-only: `{plan['preflight']['candidate_audit_read_only']}`.",
        f"- Required scope present: `{plan['preflight']['required_scope_present']}`.",
        "",
        "## Cleanup Scope",
        "",
    ]
    lines.extend(f"- {item}" for item in plan["cleanup_scope"])
    lines.extend(["", "## Explicit Non-Scope", ""])
    lines.extend(f"- {item}" for item in plan["explicit_non_scope"])
    lines.extend(
        [
            "",
            "## Execute Command",
            "",
            "Run this only after explicit user approval:",
            "",
            "```powershell",
            plan["execute_command"],
            "```",
            "",
            "Then run the independent post-cleanup probe:",
            "",
            "```powershell",
            plan["post_execute_probe_required"],
            "```",
            "",
            "## Claim Policy",
            "",
            plan["claim_policy"],
            "",
        ]
    )
    return "\n".join(lines)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--target", default="/home/syk")
    parser.add_argument("--min-free-gib", type=float, default=180.0)
    parser.add_argument("--candidate-audit", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-token")
    args = parser.parse_args()

    candidates = load_json(args.candidate_audit)
    plan = build_guarded_cleanup_plan(
        candidates=candidates,
        host=args.host,
        user=args.user,
        port=args.port,
        target=args.target,
        min_free_gib=args.min_free_gib,
        execute=args.execute,
        confirm_token=args.confirm_token,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
    args.output_md.write_text(render_markdown(plan), encoding="utf-8")
    print(json.dumps(plan, indent=2, sort_keys=True))

    if args.execute and not plan["can_execute"]:
        raise SystemExit("Refusing cleanup: confirmation token or candidate preflight failed")

    if plan["can_execute"]:
        password = os.environ.get("CORM_REMOTE_PASSWORD")
        if not password:
            raise SystemExit("CORM_REMOTE_PASSWORD is required")
        execution = prepare_remote_ext4_storage(
            host=args.host,
            user=args.user,
            port=args.port,
            password=password,
            target=args.target,
            output=Path("results/remote_ext4_prepare_execute_20260529.json"),
            execute=True,
            min_free_gib=args.min_free_gib,
        )
        plan["destructive_operations_executed"] = True
        plan["execution_report"] = execution
        args.output_json.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
        args.output_md.write_text(render_markdown(plan), encoding="utf-8")


if __name__ == "__main__":
    main()
