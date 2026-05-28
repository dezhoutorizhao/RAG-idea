#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import paramiko

try:
    from experiments.check_remote_storage_status import check_remote_storage_status
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from experiments.check_remote_storage_status import check_remote_storage_status


DEFAULT_TARGET = "/home/syk"


def prepare_remote_ext4_storage(
    *,
    host: str,
    user: str,
    port: int,
    password: str,
    target: str,
    output: Path,
    execute: bool = False,
    min_free_gib: float = 180.0,
    timeout: int = 30,
) -> dict[str, Any]:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=user, password=password, timeout=timeout)
    try:
        before = collect_space_snapshot(client, target, password)
        cleanup_results = []
        if execute:
            cleanup_results = run_cleanup(client, password, user)
        after = collect_space_snapshot(client, target, password)
    finally:
        client.close()

    report = {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "remote": {"host": host, "user": user, "port": port},
        "target": target,
        "min_free_gib": min_free_gib,
        "mode": "execute" if execute else "dry_run",
        "destructive_operations_executed": bool(execute),
        "before": before,
        "cleanup_plan": cleanup_plan(user),
        "cleanup_results": cleanup_results,
        "after": after,
        "next_probe_command": (
            "python experiments/check_remote_storage_status.py "
            f"--host {host} --user {user} --port {port} "
            f"--target {shlex.quote(target)} --min-free-gib {min_free_gib:g} "
            "--output results/remote_storage_status_after_ext4_cleanup.json"
        ),
        "claim_policy": (
            "Dry-run output is only an execution plan. Execute mode must be followed by an "
            "independent write/fsync/read/delete storage probe before launching full CoRM-RAG reproduction."
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def collect_space_snapshot(client: paramiko.SSHClient, target: str, password: str) -> dict[str, Any]:
    user = target_user_from_home(target)
    user_home = f"/home/{shlex.quote(_shell_path_component(user))}"
    commands = {
        "df_target": f"df -hT {shlex.quote(target)} 2>&1 || true",
        "df_root_machine": "df -PT / 2>&1 || true",
        "user_cache": f"du -sh {user_home}/.cache 2>&1 || true",
        "user_conda_pkg_cache": f"du -sh {user_home}/miniconda3/pkgs 2>&1 || true",
    }
    snapshot = {name: _run(client, command) for name, command in commands.items()}

    sudo_commands = {
        "docker_json_logs_bytes": (
            "find /var/lib/docker/containers -name '*-json.log' -type f "
            "-printf '%s\\n' 2>/dev/null | awk '{s+=$1} END{print s+0}'"
        ),
        "root_cache": "du -sh /root/.cache 2>&1 || true",
        "docker_system_df": "docker system df 2>&1 || true",
    }
    for name, command in sudo_commands.items():
        snapshot[name] = _run(
            client,
            sudo_command(command, password),
            display_command=sudo_command(command, "***"),
        )
    return snapshot


def cleanup_plan(user: str) -> list[dict[str, str]]:
    return [
        {
            "name": "truncate_docker_json_logs",
            "risk": "medium",
            "description": "Truncate Docker json-file logs; preserves containers/images/volumes but deletes logs.",
            "command": docker_log_truncate_command(),
        },
        {
            "name": "clear_root_cache",
            "risk": "medium",
            "description": "Delete immediate contents of /root/.cache; may require re-downloading cached assets.",
            "command": clear_directory_contents_command("/root/.cache"),
        },
        {
            "name": "clear_user_cache",
            "risk": "low_to_medium",
            "description": f"Delete immediate contents of /home/{user}/.cache.",
            "command": clear_directory_contents_command(f"/home/{user}/.cache"),
        },
    ]


def run_cleanup(client: paramiko.SSHClient, password: str, user: str) -> list[dict[str, Any]]:
    results = []
    for item in cleanup_plan(user):
        result = _run(
            client,
            sudo_command(item["command"], password),
            display_command=sudo_command(item["command"], "***"),
        )
        results.append({**item, "result": result})
    return results


def docker_log_truncate_command() -> str:
    return (
        "find /var/lib/docker/containers -name '*-json.log' -type f "
        "-exec sh -c 'for path do : > \"$path\"; done' sh {} +"
    )


def clear_directory_contents_command(path: str) -> str:
    quoted = shlex.quote(path)
    return f"test -d {quoted} && find {quoted} -mindepth 1 -maxdepth 1 -exec rm -rf -- {{}} + || true"


def sudo_command(command: str, password: str) -> str:
    quoted_password = shlex.quote(password)
    return f"printf '%s\\n' {quoted_password} | sudo -S -p '' bash -lc {shlex.quote(command)}"


def target_user_from_home(target: str) -> str:
    parts = Path(target).parts
    if len(parts) >= 3 and parts[1] == "home":
        return parts[2]
    return "syk"


def _shell_path_component(value: str) -> str:
    if "/" in value or value in {"", ".", ".."}:
        raise ValueError(f"unsafe path component: {value!r}")
    return value


def _run(client: paramiko.SSHClient, command: str, *, display_command: str | None = None) -> dict[str, Any]:
    stdin, stdout, stderr = client.exec_command(command)
    del stdin
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    return {
        "command": command if display_command is None else display_command,
        "exit_status": stdout.channel.recv_exit_status(),
        "stdout": out,
        "stderr": err,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--target", default=DEFAULT_TARGET)
    parser.add_argument("--min-free-gib", type=float, default=180.0)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    password = os.environ.get("CORM_REMOTE_PASSWORD")
    if not password:
        raise SystemExit("CORM_REMOTE_PASSWORD is required")

    report = prepare_remote_ext4_storage(
        host=args.host,
        user=args.user,
        port=args.port,
        password=password,
        target=args.target,
        output=args.output,
        execute=args.execute,
        min_free_gib=args.min_free_gib,
    )
    print(json.dumps(report, indent=2, sort_keys=True))

    if args.execute:
        probe_output = args.output.with_name("remote_storage_status_after_ext4_cleanup.json")
        probe = check_remote_storage_status(
            host=args.host,
            user=args.user,
            port=args.port,
            password=password,
            target=args.target,
            output=probe_output,
            min_free_gib=args.min_free_gib,
        )
        print(json.dumps({"post_cleanup_probe": probe}, indent=2, sort_keys=True))
        if not probe["ready_for_full_reproduction_storage"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
