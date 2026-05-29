#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from experiments.materialize_corm_remote_scripts import materialize_remote_scripts
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from experiments.materialize_corm_remote_scripts import materialize_remote_scripts


DEFAULT_INPUT = Path("results/corm_reconstruction_plan.json")
DEFAULT_OUTPUT = Path("results/corm_reconstruction_plan_ext4_20260529.json")
DEFAULT_SCRIPT_DIR = Path("results/corm_remote_scripts_ext4")
DEFAULT_NEW_ROOT = "/home/syk/csrm_corm_reconstruction"


def relocate_corm_remote_plan(
    plan: dict[str, Any],
    *,
    new_remote_root: str,
) -> dict[str, Any]:
    output = deepcopy(plan)
    old_root = str(output["remote"]["remote_root"])
    output = _replace_strings(output, old_root, new_remote_root)
    output["remote"]["remote_root"] = new_remote_root
    output["remote"]["storage_policy"] = (
        "Use the repaired ext4 home filesystem for persistent workspace/data and "
        "/dev/shm/csrm_corm_runtime for the transient Python runtime and HuggingFace cache. "
        "Do not use /mnt/ntfs-disk for full reproduction until an independent write probe passes."
    )
    output["status"] = "planned_not_executed_ext4_relocation"
    output["relocation"] = {
        "old_remote_root": old_root,
        "new_remote_root": new_remote_root,
        "reason": (
            "The previous /mnt/ntfs-disk target reports free space but fails create/write probes. "
            "The ext4 /home/syk path is writable but must pass the 180 GiB post-cleanup probe before launch."
        ),
        "requires_post_cleanup_probe": True,
        "post_cleanup_probe_artifact": "results/remote_storage_status_after_ext4_cleanup.json",
    }
    output["claim_policy"] = (
        output.get("claim_policy", "")
        + " The ext4 relocation is a launch plan only; it is not evidence that full CoRM-RAG reproduction has run."
    ).strip()
    return output


def validate_relocated_plan(plan: dict[str, Any], *, old_root: str, new_root: str) -> dict[str, Any]:
    checked = deepcopy(plan)
    checked.pop("relocation", None)
    text = json.dumps(checked, ensure_ascii=False, sort_keys=True)
    return {
        "old_root_absent": old_root not in text,
        "new_root_present": new_root in text,
        "remote_root": plan.get("remote", {}).get("remote_root"),
        "status": plan.get("status"),
        "passed": old_root not in text and new_root in text and plan.get("remote", {}).get("remote_root") == new_root,
    }


def _replace_strings(value: Any, old: str, new: str) -> Any:
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [_replace_strings(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: _replace_strings(item, old, new) for key, item in value.items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--new-remote-root", default=DEFAULT_NEW_ROOT)
    parser.add_argument("--script-dir", type=Path, default=DEFAULT_SCRIPT_DIR)
    parser.add_argument("--manifest", type=Path, default=Path("results/corm_remote_scripts_ext4_manifest.json"))
    args = parser.parse_args()

    source = json.loads(args.input.read_text(encoding="utf-8"))
    old_root = source["remote"]["remote_root"]
    relocated = relocate_corm_remote_plan(source, new_remote_root=args.new_remote_root)
    validation = validate_relocated_plan(relocated, old_root=old_root, new_root=args.new_remote_root)
    relocated["relocation"]["validation"] = validation
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(relocated, indent=2, sort_keys=True), encoding="utf-8")
    manifest = materialize_remote_scripts(args.output, args.script_dir)
    if args.manifest:
        args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    result = {"plan": str(args.output), "manifest": str(args.manifest), "validation": validation}
    print(json.dumps(result, indent=2, sort_keys=True))
    if not validation["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
