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


def check_remote_storage_status(
    *,
    host: str,
    user: str,
    port: int,
    password: str,
    target: str,
    output: Path,
    min_free_gib: float = 180.0,
    timeout: int = 30,
) -> dict[str, Any]:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=user, password=password, timeout=timeout)
    try:
        df = _run(client, f"df -PT / {shlex.quote(target)} /dev/shm 2>&1")
        findmnt = _run(client, f"findmnt -no SOURCE,FSTYPE,OPTIONS {shlex.quote(target)} 2>&1 || true")
        gpu = _run(
            client,
            "nvidia-smi --query-gpu=index,name,memory.total,memory.free "
            "--format=csv,noheader,nounits 2>&1 || true",
        )
        write_probe = _run(client, _write_probe_command(target))
    finally:
        client.close()

    filesystems = parse_df_pt(df["stdout"])
    target_fs = _find_mount(filesystems, target)
    available_gib = None if target_fs is None else target_fs["available_1k_blocks"] / (1024**2)
    writable = write_probe["exit_status"] == 0
    min_free_met = available_gib is not None and available_gib >= min_free_gib
    ready = bool(min_free_met and writable)
    report = {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "remote": {"host": host, "user": user, "port": port},
        "target": target,
        "min_free_gib": min_free_gib,
        "ready_for_full_reproduction_storage": ready,
        "target_available_gib": available_gib,
        "target_min_free_met": min_free_met,
        "target_write_probe_passed": writable,
        "filesystems": filesystems,
        "target_findmnt": findmnt,
        "gpu_query": gpu,
        "write_probe": write_probe,
        "claim_policy": (
            "This checks storage writability and free space only; it is not a completed "
            "CoRM-RAG reproduction result."
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def parse_df_pt(output: str) -> list[dict[str, Any]]:
    rows = []
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("Filesystem"):
            continue
        parts = stripped.split()
        if len(parts) < 7:
            continue
        blocks = _int_or_none(parts[2])
        used = _int_or_none(parts[3])
        available = _int_or_none(parts[4])
        if blocks is None or used is None or available is None:
            continue
        rows.append(
            {
                "filesystem": parts[0],
                "type": parts[1],
                "blocks_1k": blocks,
                "used_1k_blocks": used,
                "available_1k_blocks": available,
                "capacity": parts[5],
                "mount": " ".join(parts[6:]),
            }
        )
    return rows


def _find_mount(filesystems: list[dict[str, Any]], target: str) -> dict[str, Any] | None:
    exact = [item for item in filesystems if item["mount"] == target]
    if exact:
        return exact[0]
    prefix = [item for item in filesystems if target.startswith(str(item["mount"]).rstrip("/") + "/")]
    return max(prefix, key=lambda item: len(str(item["mount"])), default=None)


def _write_probe_command(target: str) -> str:
    quoted = shlex.quote(target.rstrip("/") + "/csrm_write_probe.XXXXXX")
    python = (
        "import os,pathlib;"
        "p=pathlib.Path(os.environ['TESTFILE']);"
        "data=b'csrm_remote_write_probe\\n';"
        "f=open(p,'wb');"
        "f.write(data);"
        "f.flush();"
        "os.fsync(f.fileno());"
        "f.close();"
        "assert p.read_bytes()==data"
    )
    return (
        "set -e; "
        f"TESTDIR=$(mktemp -d {quoted}); "
        "trap 'rm -rf \"$TESTDIR\"' EXIT; "
        f"TESTFILE=\"$TESTDIR/probe.bin\" python3 -c {shlex.quote(python)}"
    )


def _run(client: paramiko.SSHClient, command: str) -> dict[str, Any]:
    stdin, stdout, stderr = client.exec_command(command)
    del stdin
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    return {
        "command": command,
        "exit_status": stdout.channel.recv_exit_status(),
        "stdout": out,
        "stderr": err,
    }


def _int_or_none(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--target", default="/mnt/ntfs-disk")
    parser.add_argument("--min-free-gib", type=float, default=180.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    password = os.environ.get("CORM_REMOTE_PASSWORD")
    if not password:
        raise SystemExit("CORM_REMOTE_PASSWORD is required")
    report = check_remote_storage_status(
        host=args.host,
        user=args.user,
        port=args.port,
        password=password,
        target=args.target,
        output=args.output,
        min_free_gib=args.min_free_gib,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["ready_for_full_reproduction_storage"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
