#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import stat
from pathlib import Path
from typing import Any


SECRET_LITERAL_PATTERNS = [
    re.compile(r"20030729"),
    re.compile(r"(?i)(password|passwd)\s*[:=]\s*['\"]?[^\s`'\"]+"),
    re.compile(r"OPENAI_API_KEY=(?!\$OPENAI_API_KEY|\$\{OPENAI_API_KEY[:}])\S+"),
    re.compile(r"OPENAI_BASE_URL=(?!\$OPENAI_BASE_URL|\$\{OPENAI_BASE_URL[:}])https?://\S+"),
]


def materialize_remote_scripts(plan_path: Path, output_dir: Path) -> dict[str, Any]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    remote_root = plan["remote"]["remote_root"]
    output_dir.mkdir(parents=True, exist_ok=True)

    scripts = {
        "00_env.sh": _env_script(plan),
        "01_prepare_env.sh": _step_script(
            "Prepare remote directories and Python environment.",
            [
                _command(plan, "prepare_remote_dirs"),
                _command(plan, "create_remote_venv"),
                _command(plan, "install_runtime"),
            ],
        ),
        "02_build_wikipedia_and_faiss.sh": _step_script(
            "Build Wikipedia passages, embeddings, and supplemental FAISS index.",
            [
                _command(plan, "build_passages_and_embeddings"),
                _command(plan, "build_faiss_index"),
            ],
        ),
        "03_prepare_biased_nq.sh": _step_script(
            "Generate or stage perturbations, then materialize biased_nq_test.jsonl.",
            [
                _command(plan, "generate_or_stage_perturbations"),
                _command(plan, "materialize_biased_nq"),
            ],
        ),
        "03_prepare_biased_nq_template_smoke.sh": _step_script(
            "Generate deterministic template perturbations and materialize a smoke Biased-NQ file.",
            [
                _optional_command(plan, "generate_template_perturbations_smoke"),
                _optional_command(plan, "materialize_template_biased_nq_smoke"),
            ],
        ),
        "04_run_reconstructed_eval.sh": _step_script(
            "Run reconstructed CoRM evaluation from the upstream src directory.",
            [_command(plan, "run_reconstructed_eval")],
        ),
        "04_run_template_biased_nq_smoke_eval.sh": _step_script(
            "Run a small template Biased-NQ reconstructed-eval smoke from the upstream src directory.",
            [_command(plan, "run_template_biased_nq_smoke_eval")],
        ),
        "05_watch_and_run_template_smoke_eval.sh": _watch_template_smoke_script(plan),
        "README.md": _readme(plan),
    }

    written = []
    for name, content in scripts.items():
        path = output_dir / name
        path.write_text(content, encoding="utf-8", newline="\n")
        if path.suffix == ".sh":
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        written.append(path)

    contains_secrets = any(_contains_secret(path.read_text(encoding="utf-8")) for path in written)
    manifest = {
        "status": "materialized",
        "plan": str(plan_path),
        "output_dir": str(output_dir),
        "remote_root": remote_root,
        "scripts": [path.name for path in written],
        "script_count": len(written),
        "contains_secret_markers": contains_secrets,
        "execution_order": [
            "00_env.sh",
            "01_prepare_env.sh",
            "02_build_wikipedia_and_faiss.sh",
            "03_prepare_biased_nq.sh",
            "03_prepare_biased_nq_template_smoke.sh",
            "04_run_template_biased_nq_smoke_eval.sh",
            "04_run_reconstructed_eval.sh",
            "05_watch_and_run_template_smoke_eval.sh",
        ],
        "claim_policy": plan["claim_policy"],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def _command(plan: dict[str, Any], name: str) -> str:
    for step in plan["remote_steps"]:
        if step["name"] == name:
            return step["command"]
    raise KeyError(f"missing remote step: {name}")


def _optional_command(plan: dict[str, Any], name: str) -> str:
    for step in plan["remote_steps"]:
        if step["name"] == name:
            return step["command"]
    return f'echo "optional step {name} is not present in this plan"'


def _env_script(plan: dict[str, Any]) -> str:
    remote_root = plan["remote"]["remote_root"]
    return f"""#!/usr/bin/env bash
set -euo pipefail

export REMOTE_ROOT="{remote_root}"
export CORM_RECON_DATA="$REMOTE_ROOT/data"
export CORM_RECON_WORKSPACE="$REMOTE_ROOT/workspace"
export CORM_RECON_OUTPUTS="$REMOTE_ROOT/outputs"
export CORM_RUNTIME_ROOT="${{CORM_RUNTIME_ROOT:-/dev/shm/csrm_corm_runtime}}"
export HF_ENDPOINT="${{HF_ENDPOINT:-{plan['remote'].get('hf_endpoint_default', 'https://hf-mirror.com')}}}"
export HF_HOME="${{HF_HOME:-$CORM_RUNTIME_ROOT/hf_cache}}"
export HF_HUB_CACHE="${{HF_HUB_CACHE:-$HF_HOME/hub}}"
export HF_DATASETS_CACHE="${{HF_DATASETS_CACHE:-$HF_HOME/datasets}}"
export HF_HUB_ETAG_TIMEOUT="${{HF_HUB_ETAG_TIMEOUT:-60}}"
export HF_HUB_DOWNLOAD_TIMEOUT="${{HF_HUB_DOWNLOAD_TIMEOUT:-180}}"
export PIP_CACHE_DIR="$CORM_RUNTIME_ROOT/pip_cache"
export TMPDIR="$CORM_RUNTIME_ROOT/tmp"
export TEMP="$CORM_RUNTIME_ROOT/tmp"
export TMP="$CORM_RUNTIME_ROOT/tmp"
export XDG_CACHE_HOME="$CORM_RUNTIME_ROOT/xdg_cache"
export VLLM_CACHE_ROOT="$CORM_RUNTIME_ROOT/vllm_cache"
export MAMBA_ROOT_PREFIX="$CORM_RUNTIME_ROOT/mamba_root"
export CONDA_PKGS_DIRS="$CORM_RUNTIME_ROOT/mamba_pkgs"
export CORM_RECON_ENV="$CORM_RUNTIME_ROOT/py_runtime"
export CORM_RECON_PYTHON="$CORM_RECON_ENV/bin/python"
export CORM_RECON_PIP="$CORM_RECON_ENV/bin/pip"

echo "REMOTE_ROOT=$REMOTE_ROOT"
echo "CORM_RUNTIME_ROOT=$CORM_RUNTIME_ROOT"
echo "HF_ENDPOINT=$HF_ENDPOINT"
echo "HF_HOME=$HF_HOME"
echo "HF_HUB_CACHE=$HF_HUB_CACHE"
echo "HF_DATASETS_CACHE=$HF_DATASETS_CACHE"
echo "PIP_CACHE_DIR=$PIP_CACHE_DIR"
echo "TMPDIR=$TMPDIR"
echo "CORM_RECON_ENV=$CORM_RECON_ENV"
"""


def _step_script(description: str, commands: list[str]) -> str:
    body = "\n\n".join(commands)
    return f"""#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
source "$SCRIPT_DIR/00_env.sh"

echo "{description}"

{body}
"""


def _readme(plan: dict[str, Any]) -> str:
    remote = plan["remote"]
    missing = "\n".join(f"- `{name}`" for name in plan["missing_local_reconstruction_inputs"])
    return f"""# CoRM Reconstructed Remote Runbook

Status: `planned_not_executed`

Remote target: `{remote['user']}@{remote['host']}:{remote['ssh_port']}`

Remote root: `{remote['remote_root']}`

Storage policy: {remote['storage_policy']}

Runtime root: `{remote.get('runtime_root', '/dev/shm/csrm_corm_runtime')}`

HuggingFace cache: `{remote.get('hf_home', '/dev/shm/csrm_corm_runtime/hf_cache')}`

Default HuggingFace endpoint: `{remote.get('hf_endpoint_default', 'https://hf-mirror.com')}`

Password/API policy: {remote['password_policy']}

Run order:

1. `bash 01_prepare_env.sh`
2. `bash 02_build_wikipedia_and_faiss.sh`
3. `bash 03_prepare_biased_nq.sh`
4. Optional fallback only: `bash 03_prepare_biased_nq_template_smoke.sh`
5. Optional smoke only: `bash 04_run_template_biased_nq_smoke_eval.sh`
6. `bash 04_run_reconstructed_eval.sh`
7. Optional watcher: `bash 05_watch_and_run_template_smoke_eval.sh`

Current missing local reconstruction inputs:

{missing}

Claim policy:

{plan['claim_policy']}
"""


def _watch_template_smoke_script(plan: dict[str, Any]) -> str:
    remote_root = plan["remote"]["remote_root"]
    data_dir = f"{remote_root}/data"
    outputs_dir = f"{remote_root}/outputs/template_smoke_watcher"
    smoke_results = f"{remote_root}/outputs/corm_reconstructed_eval_template_smoke/evaluation_results.json"
    return f"""#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
source "$SCRIPT_DIR/00_env.sh"

WATCH_TIMEOUT_SECONDS="${{WATCH_TIMEOUT_SECONDS:-21600}}"
WATCH_INTERVAL_SECONDS="${{WATCH_INTERVAL_SECONDS:-300}}"
WATCH_OUTPUT_DIR="{outputs_dir}"
mkdir -p "$WATCH_OUTPUT_DIR"

echo "Watch for reconstructed CoRM artifacts, then run the bounded template Biased-NQ smoke eval."
echo "timeout=$WATCH_TIMEOUT_SECONDS interval=$WATCH_INTERVAL_SECONDS"

START=$(date +%s)
while true; do
    NOW=$(date +%s)
    if [ "$((NOW - START))" -gt "$WATCH_TIMEOUT_SECONDS" ]; then
        cat > "$WATCH_OUTPUT_DIR/status.json" <<JSON
{{"status":"timeout","observed_at":"$(date -Iseconds)","reason":"wiki.faiss or required smoke inputs were not ready before timeout"}}
JSON
        exit 2
    fi

    if [ -f "{data_dir}/wiki.faiss" ] && [ -f "{data_dir}/wiki_passages.jsonl" ] && [ -f "{data_dir}/biased_nq_test.template_smoke.jsonl" ]; then
        if [ -f "{smoke_results}" ]; then
            cat > "$WATCH_OUTPUT_DIR/status.json" <<JSON
{{"status":"already_completed","observed_at":"$(date -Iseconds)","evaluation_results":"{smoke_results}"}}
JSON
            exit 0
        fi
        echo "Required artifacts are ready; launching bounded template smoke eval."
        bash "$SCRIPT_DIR/04_run_template_biased_nq_smoke_eval.sh" > "$WATCH_OUTPUT_DIR/template_smoke_eval.log" 2>&1
        cat > "$WATCH_OUTPUT_DIR/status.json" <<JSON
{{"status":"completed","observed_at":"$(date -Iseconds)","evaluation_results":"{smoke_results}","log":"$WATCH_OUTPUT_DIR/template_smoke_eval.log"}}
JSON
        exit 0
    fi

    echo "$(date -Iseconds) waiting for wiki.faiss, wiki_passages.jsonl, and biased_nq_test.template_smoke.jsonl"
    sleep "$WATCH_INTERVAL_SECONDS"
done
"""


def _contains_secret(text: str) -> bool:
    for pattern in SECRET_LITERAL_PATTERNS:
        if pattern.search(text):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=Path("results/corm_reconstruction_plan.json"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    manifest = materialize_remote_scripts(args.plan, args.output_dir)
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
