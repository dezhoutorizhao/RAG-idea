#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import paramiko

from experiments.prepare_remote_ext4_storage import sudo_command


DEFAULT_OUTPUT_JSON = Path("results/remote_cleanup_candidates_20260529.json")
DEFAULT_OUTPUT_MD = Path("results/remote_cleanup_candidates_20260529.md")


def audit_remote_cleanup_candidates(
    *,
    host: str,
    user: str,
    port: int,
    password: str,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
    top_n: int = 30,
    timeout: int = 30,
) -> dict[str, Any]:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=user, password=password, timeout=timeout)
    try:
        raw = {
            "df_root": _run(client, "df -PT / 2>&1 || true"),
            "docker_ps": _run(
                client,
                sudo_command(
                    "docker ps --no-trunc --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}' 2>&1 || true",
                    password,
                ),
                display_command=sudo_command(
                    "docker ps --no-trunc --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}' 2>&1 || true",
                    "***",
                ),
            ),
            "docker_logs": _run(
                client,
                sudo_command(
                    (
                        "find /var/lib/docker/containers -name '*-json.log' -type f "
                        "-printf '%s\\t%p\\n' 2>/dev/null | sort -nr | head "
                        f"-n {int(top_n)}"
                    ),
                    password,
                ),
                display_command=sudo_command(
                    (
                        "find /var/lib/docker/containers -name '*-json.log' -type f "
                        "-printf '%s\\t%p\\n' 2>/dev/null | sort -nr | head "
                        f"-n {int(top_n)}"
                    ),
                    "***",
                ),
            ),
            "root_cache_total": _run(
                client,
                sudo_command("du -sb /root/.cache 2>/dev/null || true", password),
                display_command=sudo_command("du -sb /root/.cache 2>/dev/null || true", "***"),
            ),
            "root_cache_entries": _run(
                client,
                sudo_command(
                    f"du -sb /root/.cache/* 2>/dev/null | sort -nr | head -n {int(top_n)}",
                    password,
                ),
                display_command=sudo_command(
                    f"du -sb /root/.cache/* 2>/dev/null | sort -nr | head -n {int(top_n)}",
                    "***",
                ),
            ),
            "user_cache_total": _run(client, f"du -sb /home/{shlex.quote(user)}/.cache 2>/dev/null || true"),
            "user_cache_entries": _run(
                client,
                f"du -sb /home/{shlex.quote(user)}/.cache/* 2>/dev/null | sort -nr | head -n {int(top_n)}",
            ),
            "conda_pkg_total": _run(
                client,
                f"du -sb /home/{shlex.quote(user)}/miniconda3/pkgs 2>/dev/null || true",
            ),
            "home_top_entries": _run(
                client,
                (
                    f"du -sb /home/{shlex.quote(user)}/* /home/{shlex.quote(user)}/.[!.]* "
                    f"2>/dev/null | sort -nr | head -n {int(top_n)}"
                ),
            ),
        }
    finally:
        client.close()

    running_containers = parse_docker_ps(raw["docker_ps"]["stdout"])
    docker_logs = annotate_docker_logs(
        parse_size_path_lines(raw["docker_logs"]["stdout"]),
        running_containers,
    )
    root_cache_total = first_size(raw["root_cache_total"]["stdout"])
    user_cache_total = first_size(raw["user_cache_total"]["stdout"])
    conda_pkg_total = first_size(raw["conda_pkg_total"]["stdout"])
    docker_log_total_top_n = sum(item["size_bytes"] for item in docker_logs)
    recommended_reclaim_bytes = docker_log_total_top_n + root_cache_total + user_cache_total

    report = {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "remote": {"host": host, "user": user, "port": port},
        "top_n": top_n,
        "destructive_operations_executed": False,
        "recommended_cleanup_scope": [
            "truncate_docker_json_logs",
            "clear_root_cache_contents",
            "clear_user_cache_contents",
        ],
        "recommended_reclaim_bytes_lower_bound": recommended_reclaim_bytes,
        "recommended_reclaim_gib_lower_bound": bytes_to_gib(recommended_reclaim_bytes),
        "docker": {
            "running_container_count": len(running_containers),
            "top_log_count": len(docker_logs),
            "top_log_bytes": docker_log_total_top_n,
            "top_log_gib": bytes_to_gib(docker_log_total_top_n),
            "top_logs": docker_logs,
        },
        "caches": {
            "root_cache_total_bytes": root_cache_total,
            "root_cache_total_gib": bytes_to_gib(root_cache_total),
            "root_cache_entries": parse_size_path_lines(raw["root_cache_entries"]["stdout"]),
            "user_cache_total_bytes": user_cache_total,
            "user_cache_total_gib": bytes_to_gib(user_cache_total),
            "user_cache_entries": parse_size_path_lines(raw["user_cache_entries"]["stdout"]),
            "conda_pkg_total_bytes": conda_pkg_total,
            "conda_pkg_total_gib": bytes_to_gib(conda_pkg_total),
        },
        "home_top_entries": parse_size_path_lines(raw["home_top_entries"]["stdout"]),
        "raw_commands": raw,
        "claim_policy": (
            "This is a read-only cleanup candidate audit. It does not delete, truncate, prune, "
            "unmount, or modify server files. It supports cleanup approval decisions only."
        ),
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    return report


def parse_docker_ps(stdout: str) -> dict[str, dict[str, str]]:
    containers: dict[str, dict[str, str]] = {}
    for line in stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 4 or len(parts[0]) < 12:
            continue
        containers[parts[0]] = {
            "container_id": parts[0],
            "name": parts[1],
            "image": parts[2],
            "status": parts[3],
        }
    return containers


def annotate_docker_logs(
    logs: list[dict[str, Any]],
    running_containers: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    output = []
    for item in logs:
        container_id = container_id_from_log_path(item["path"])
        running = running_containers.get(container_id or "")
        output.append(
            {
                **item,
                "size_gib": bytes_to_gib(item["size_bytes"]),
                "container_id": container_id,
                "container_running": running is not None,
                "container_name": None if running is None else running["name"],
                "container_image": None if running is None else running["image"],
                "container_status": None if running is None else running["status"],
            }
        )
    return output


def container_id_from_log_path(path: str) -> str | None:
    parts = Path(path).parts
    try:
        index = parts.index("containers")
    except ValueError:
        return None
    if index + 1 >= len(parts):
        return None
    candidate = parts[index + 1]
    return candidate if len(candidate) >= 12 else None


def parse_size_path_lines(stdout: str) -> list[dict[str, Any]]:
    items = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split(maxsplit=1)
        if len(parts) != 2:
            continue
        try:
            size = int(parts[0])
        except ValueError:
            continue
        items.append({"size_bytes": size, "size_gib": bytes_to_gib(size), "path": parts[1]})
    return items


def first_size(stdout: str) -> int:
    items = parse_size_path_lines(stdout)
    return 0 if not items else int(items[0]["size_bytes"])


def bytes_to_gib(value: int | float | None) -> float:
    if not value:
        return 0.0
    return float(value) / float(1024**3)


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Remote Cleanup Candidate Audit",
        "",
        f"Generated: `{report['observed_at_utc']}`",
        f"Remote: `{report['remote']['user']}@{report['remote']['host']}:{report['remote']['port']}`",
        f"Destructive operations executed: `{report['destructive_operations_executed']}`",
        "",
        "## Summary",
        "",
        f"- Recommended reclaim lower bound: `{report['recommended_reclaim_gib_lower_bound']:.1f} GiB`.",
        f"- Running Docker containers observed: `{report['docker']['running_container_count']}`.",
        f"- Top Docker log bytes scanned: `{report['docker']['top_log_gib']:.1f} GiB`.",
        f"- Root cache: `{report['caches']['root_cache_total_gib']:.1f} GiB`.",
        f"- User cache: `{report['caches']['user_cache_total_gib']:.1f} GiB`.",
        f"- Conda package cache: `{report['caches']['conda_pkg_total_gib']:.1f} GiB`.",
        "",
        "## Recommended Cleanup Scope",
        "",
    ]
    lines.extend(f"- `{item}`" for item in report["recommended_cleanup_scope"])
    lines.extend(
        [
            "",
            "## Largest Docker JSON Logs",
            "",
            "| Size GiB | Running | Container | Image | Path |",
            "|---:|---:|---|---|---|",
        ]
    )
    for item in report["docker"]["top_logs"][:10]:
        lines.append(
            f"| {item['size_gib']:.2f} | `{item['container_running']}` | "
            f"{_md(item.get('container_name'))} | {_md(item.get('container_image'))} | `{item['path']}` |"
        )
    lines.extend(
        [
            "",
            "## Largest Root Cache Entries",
            "",
            "| Size GiB | Path |",
            "|---:|---|",
        ]
    )
    for item in report["caches"]["root_cache_entries"][:10]:
        lines.append(f"| {item['size_gib']:.2f} | `{item['path']}` |")
    lines.extend(
        [
            "",
            "## Largest User Cache Entries",
            "",
            "| Size GiB | Path |",
            "|---:|---|",
        ]
    )
    for item in report["caches"]["user_cache_entries"][:10]:
        lines.append(f"| {item['size_gib']:.2f} | `{item['path']}` |")
    lines.extend(["", "## Claim Policy", "", report["claim_policy"], ""])
    return "\n".join(lines)


def _md(value: Any) -> str:
    if value in {None, ""}:
        return "`not_running_or_unknown`"
    return f"`{str(value).replace('|', '/')}`"


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
    parser.add_argument("--top-n", type=int, default=30)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    password = os.environ.get("CORM_REMOTE_PASSWORD")
    if not password:
        raise SystemExit("CORM_REMOTE_PASSWORD is required")

    report = audit_remote_cleanup_candidates(
        host=args.host,
        user=args.user,
        port=args.port,
        password=password,
        output_json=args.output_json,
        output_md=args.output_md,
        top_n=args.top_n,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
