#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_REMOTE_ROOT = "/mnt/ntfs-disk/csrm_corm_reconstruction"
DEFAULT_RUNTIME_ROOT = "/dev/shm/csrm_corm_runtime"
DEFAULT_HF_ENDPOINT = "https://hf-mirror.com"
DEFAULT_RECON_GENERATOR_MODEL = "Qwen/Qwen2.5-7B-Instruct"
DEFAULT_TEMPLATE_SMOKE_GENERATOR_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"


def plan_corm_reconstruction(
    *,
    workspace: Path,
    data_src: Path,
    checkpoint: Path,
    remote_root: str = DEFAULT_REMOTE_ROOT,
) -> dict[str, Any]:
    workspace = workspace.resolve()
    data_src = data_src.resolve()
    checkpoint = checkpoint.resolve()
    repo = workspace / "external_repos" / "CoRM-RAG"

    local_inputs = {
        "workspace": _path_status(workspace),
        "corm_repo": _path_status(repo),
        "checkpoint": _path_status(checkpoint),
        "wiki_passages": _path_status(data_src / "wiki_passages.jsonl"),
        "wiki_embeddings": _path_status(data_src / "wiki_embeddings.npy"),
        "wiki_faiss": _path_status(data_src / "wiki.faiss"),
        "perturbations": _path_status(data_src / "perturbations.jsonl"),
        "biased_nq_test": _path_status(data_src / "biased_nq_test.jsonl"),
        "faiss_builder": _path_status(workspace / "experiments" / "build_corm_faiss_index.py"),
        "biased_nq_builder": _path_status(workspace / "experiments" / "build_corm_biased_nq_test.py"),
        "template_perturbation_builder": _path_status(workspace / "experiments" / "build_corm_template_perturbations.py"),
        "streaming_wikipedia_encoder": _path_status(workspace / "experiments" / "encode_corm_wikipedia_streaming.py"),
    }
    missing_now = [
        name
        for name in ["wiki_passages", "wiki_embeddings", "wiki_faiss", "perturbations", "biased_nq_test"]
        if not local_inputs[name]["exists"]
    ]

    commands = _commands(remote_root=remote_root)
    return {
        "status": "planned_not_executed",
        "workspace": str(workspace),
        "data_src": str(data_src),
        "remote": {
            "host": "192.168.103.101",
            "user": "syk",
            "ssh_port": 22,
            "remote_root": remote_root,
            "runtime_root": DEFAULT_RUNTIME_ROOT,
            "hf_home": f"{DEFAULT_RUNTIME_ROOT}/hf_cache",
            "hf_endpoint_default": DEFAULT_HF_ENDPOINT,
            "storage_policy": (
                "Use /mnt/ntfs-disk for persistent workspace/data and /dev/shm/csrm_corm_runtime "
                "for the transient Python runtime and HuggingFace cache; root filesystem is effectively full "
                "and /mnt/ntfs-disk is an NTFS/fuseblk mount with limited POSIX permission support."
            ),
            "hf_policy": (
                "Default direct huggingface.co access timed out on the server, while process-start "
                "HF_ENDPOINT=https://hf-mirror.com with HF_HOME under /dev/shm successfully streamed "
                "Wikipedia and loaded facebook/contriever-msmarco in the remote smoke."
            ),
            "password_policy": "Do not write passwords into scripts or reports; use interactive SSH, SSH keys, or caller-provided secret handling.",
        },
        "local_inputs": local_inputs,
        "missing_local_reconstruction_inputs": missing_now,
        "supplemental_tools_ready": bool(
            local_inputs["faiss_builder"]["exists"] and local_inputs["biased_nq_builder"]["exists"]
            and local_inputs["template_perturbation_builder"]["exists"]
            and local_inputs["streaming_wikipedia_encoder"]["exists"]
        ),
        "remote_steps": commands,
        "claim_policy": (
            "A run using these steps is reconstructed-pipeline evidence, not exact CoRM-RAG "
            "original reproduction, unless original artifacts or equivalence checks are supplied."
        ),
    }


def _path_status(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "size_bytes": path.stat().st_size if path.is_file() else None,
    }


def _commands(*, remote_root: str) -> list[dict[str, Any]]:
    data_dir = f"{remote_root}/data"
    repo_dir = f"{remote_root}/workspace"
    output_dir = f"{remote_root}/outputs/corm_reconstructed_eval"
    smoke_output_dir = f"{remote_root}/outputs/corm_reconstructed_eval_template_smoke"
    stage_dir = f"{remote_root}/stage/eval_data"
    smoke_stage_dir = f"{remote_root}/stage/eval_data_template_smoke"
    smoke_data_dir = f"{remote_root}/stage/template_smoke_data"
    runtime_root = DEFAULT_RUNTIME_ROOT
    hf_cache = f"{runtime_root}/hf_cache"
    pip_cache = f"{runtime_root}/pip_cache"
    tmp_dir = f"{runtime_root}/tmp"
    xdg_cache = f"{runtime_root}/xdg_cache"
    vllm_cache = f"{runtime_root}/vllm_cache"
    mamba_root = f"{runtime_root}/mamba_root"
    mamba_pkgs = f"{runtime_root}/mamba_pkgs"
    micromamba_dir = f"{runtime_root}/micromamba"
    py_env = f"{runtime_root}/py_runtime"
    python = "$CORM_RECON_PYTHON"
    pip = "$CORM_RECON_PIP"
    return [
        {
            "name": "prepare_remote_dirs",
            "command": (
                f"mkdir -p {repo_dir} {data_dir} {output_dir} {smoke_output_dir} {stage_dir} "
                f"{smoke_stage_dir} {smoke_data_dir} {hf_cache} {hf_cache}/hub "
                f"{hf_cache}/datasets {pip_cache} {tmp_dir} {xdg_cache} {vllm_cache} "
                f"{mamba_root} {mamba_pkgs} {micromamba_dir}"
            ),
        },
        {
            "name": "create_remote_venv",
            "command": (
                f"if [ ! -x {micromamba_dir}/bin/micromamba ]; then "
                f"curl -L https://micro.mamba.pm/api/micromamba/linux-64/latest "
                f"| tar --touch -xvj -C {micromamba_dir} bin/micromamba; "
                f"fi && ("
                f"{micromamba_dir}/bin/micromamba create -y -p {py_env} -c conda-forge python=3.10 pip "
                f"|| (rm -rf {py_env} && python3 -m venv --copies {py_env})"
                f")"
            ),
            "caveat": (
                "The system Python is 3.8; the reconstructed evaluation uses an isolated Python 3.10 "
                "micromamba environment under /dev/shm when conda-forge is reachable, with a system "
                "Python 3.8 venv fallback if conda-forge metadata download fails. /dev/shm is used "
                "because the persistent /mnt/ntfs-disk mount does not support all POSIX permission "
                "operations required by micromamba."
            ),
        },
        {
            "name": "install_runtime",
            "command": (
                f"{pip} install --upgrade pip setuptools wheel && "
                f"if {python} -c \"import sys; raise SystemExit(0 if sys.version_info < (3, 9) else 1)\"; then "
                f"{pip} install numpy scipy scikit-learn datasets huggingface_hub transformers tokenizers==0.20.3 'torch>=2.1' faiss-cpu 'vllm==0.5.5'; "
                f"else {pip} install numpy scipy scikit-learn datasets huggingface_hub transformers 'torch>=2.1' faiss-cpu 'vllm>=0.5'; "
                "fi && "
                f"{python} -c \"import sysconfig; from pathlib import Path; "
                "p=Path(sysconfig.get_paths()['purelib'])/'pyairports'; "
                "p.mkdir(exist_ok=True); "
                "(p/'__init__.py').write_text('from .airports import AIRPORT_LIST\\\\n'); "
                "(p/'airports.py').write_text('AIRPORT_LIST = []\\\\n')\""
            ),
            "caveat": (
                "CUDA-specific torch/vLLM wheels may need adjustment for the server driver and Python version; "
                "Python 3.8 fallback pins vLLM to 0.5.5 and adds a minimal pyairports shim because the "
                "current pyairports 0.0.1 wheel lacks the module imported by outlines."
            ),
        },
        {
            "name": "build_passages_and_embeddings",
            "command": (
                f"cd {repo_dir} && HF_ENDPOINT=${{HF_ENDPOINT:-{DEFAULT_HF_ENDPOINT}}} "
                f"HF_HOME={hf_cache} HF_HUB_CACHE={hf_cache}/hub HF_DATASETS_CACHE={hf_cache}/datasets "
                f"HF_HUB_ETAG_TIMEOUT=${{HF_HUB_ETAG_TIMEOUT:-60}} "
                f"HF_HUB_DOWNLOAD_TIMEOUT=${{HF_HUB_DOWNLOAD_TIMEOUT:-180}} "
                f"{python} experiments/encode_corm_wikipedia_streaming.py "
                f"--output-dir {data_dir} --device cuda:0 --encode-batch-size 256 "
                f"--passages-per-shard 250000 --resume"
            ),
            "expected_outputs": [f"{data_dir}/wiki_passages.jsonl", f"{data_dir}/embeddings_shard_000000.npy"],
            "caveat": (
                "This supplemental streaming encoder avoids the upstream encode_wikipedia.py OOM risk by "
                "writing embeddings_shard_*.npy incrementally. For smoke tests, add --max-articles or "
                "--max-passages manually; full reconstruction should omit those limits."
            ),
        },
        {
            "name": "build_faiss_index",
            "command": (
                f"cd {repo_dir} && {python} experiments/build_corm_faiss_index.py "
                f"--embeddings {data_dir} "
                f"--output {data_dir}/wiki.faiss "
                f"--manifest {remote_root}/outputs/wiki_faiss_manifest.json"
            ),
            "expected_outputs": [f"{data_dir}/wiki.faiss"],
        },
        {
            "name": "generate_or_stage_perturbations",
            "command": (
                f"cd {repo_dir}/external_repos/CoRM-RAG && "
                f"OPENAI_API_KEY=$OPENAI_API_KEY OPENAI_BASE_URL=$OPENAI_BASE_URL "
                f"{python} src/gen_perturbations_api.py "
                f"--output {data_dir}/perturbations.jsonl --data nq_val"
            ),
            "caveat": "Requires an OpenAI-compatible API for original-style perturbations; alternatively stage an existing perturbations.jsonl file or use the template fallback step below for reconstructed-pipeline smoke only.",
            "expected_outputs": [f"{data_dir}/perturbations.jsonl"],
        },
        {
            "name": "generate_template_perturbations_smoke",
            "command": (
                f"cd {repo_dir} && HF_ENDPOINT=${{HF_ENDPOINT:-{DEFAULT_HF_ENDPOINT}}} "
                f"HF_HOME={hf_cache} HF_HUB_CACHE={hf_cache}/hub HF_DATASETS_CACHE={hf_cache}/datasets "
                f"{python} experiments/build_corm_template_perturbations.py "
                f"--output {data_dir}/perturbations.template_smoke.jsonl "
                f"--manifest {remote_root}/outputs/perturbations_template_smoke_manifest.json "
                f"--max-queries 100"
            ),
            "caveat": "Template fallback for smoke and plumbing tests only; do not report it as original Biased-NQ evidence.",
            "expected_outputs": [f"{data_dir}/perturbations.template_smoke.jsonl"],
        },
        {
            "name": "materialize_biased_nq",
            "command": (
                f"cd {repo_dir} && {python} experiments/build_corm_biased_nq_test.py "
                f"--perturbations {data_dir}/perturbations.jsonl "
                f"--output {data_dir}/biased_nq_test.jsonl "
                f"--manifest {remote_root}/outputs/biased_nq_manifest.json"
            ),
            "expected_outputs": [f"{data_dir}/biased_nq_test.jsonl"],
        },
        {
            "name": "materialize_template_biased_nq_smoke",
            "command": (
                f"cd {repo_dir} && {python} experiments/build_corm_biased_nq_test.py "
                f"--perturbations {data_dir}/perturbations.template_smoke.jsonl "
                f"--output {data_dir}/biased_nq_test.template_smoke.jsonl "
                f"--manifest {remote_root}/outputs/biased_nq_template_smoke_manifest.json"
            ),
            "caveat": "Template fallback for smoke and plumbing tests only; do not report it as original Biased-NQ evidence.",
            "expected_outputs": [f"{data_dir}/biased_nq_test.template_smoke.jsonl"],
        },
        {
            "name": "run_reconstructed_eval",
            "command": (
                f"cd {repo_dir}/external_repos/CoRM-RAG/src && "
                f"PATH={py_env}/bin:$PATH "
                f"HF_ENDPOINT=${{HF_ENDPOINT:-{DEFAULT_HF_ENDPOINT}}} HF_HOME={hf_cache} "
                f"HF_HUB_CACHE={hf_cache}/hub HF_DATASETS_CACHE={hf_cache}/datasets "
                f"HF_HUB_ETAG_TIMEOUT=${{HF_HUB_ETAG_TIMEOUT:-60}} "
                f"HF_HUB_DOWNLOAD_TIMEOUT=${{HF_HUB_DOWNLOAD_TIMEOUT:-180}} DATA_SRC={data_dir} "
                f"EVAL_STAGE_DIR={stage_dir} SKIP_FAISS_COPY=${{SKIP_FAISS_COPY:-1}} "
                f"CRITIC_PATH={repo_dir}/checkpoints/hf/critic-v12-mixed/checkpoint-latest/state.pt "
                f"OUTPUT_DIR={output_dir} "
                f"GENERATOR_MODEL=${{GENERATOR_MODEL:-{DEFAULT_RECON_GENERATOR_MODEL}}} "
                f"bash run_eval.sh"
            ),
            "expected_outputs": [f"{output_dir}/evaluation_results.json"],
        },
        {
            "name": "run_template_biased_nq_smoke_eval",
            "command": (
                f"SMOKE_DATA_SRC={smoke_data_dir} && mkdir -p \"$SMOKE_DATA_SRC\" && "
                f"ln -sf {data_dir}/wiki.faiss \"$SMOKE_DATA_SRC/wiki.faiss\" && "
                f"ln -sf {data_dir}/wiki_passages.jsonl \"$SMOKE_DATA_SRC/wiki_passages.jsonl\" && "
                f"ln -sf {data_dir}/biased_nq_test.template_smoke.jsonl \"$SMOKE_DATA_SRC/biased_nq_test.jsonl\" && "
                f"cd {repo_dir}/external_repos/CoRM-RAG/src && "
                f"PATH={py_env}/bin:$PATH "
                f"HF_ENDPOINT=${{HF_ENDPOINT:-{DEFAULT_HF_ENDPOINT}}} HF_HOME={hf_cache} "
                f"HF_HUB_CACHE={hf_cache}/hub HF_DATASETS_CACHE={hf_cache}/datasets "
                f"HF_HUB_ETAG_TIMEOUT=${{HF_HUB_ETAG_TIMEOUT:-60}} "
                f"HF_HUB_DOWNLOAD_TIMEOUT=${{HF_HUB_DOWNLOAD_TIMEOUT:-180}} DATA_SRC=\"$SMOKE_DATA_SRC\" "
                f"EVAL_STAGE_DIR={smoke_stage_dir} SKIP_FAISS_COPY=${{SKIP_FAISS_COPY:-1}} "
                f"EVAL_DATASETS=Biased_NQ EVAL_MAX_EXAMPLES=${{EVAL_MAX_EXAMPLES:-20}} "
                f"EVAL_RERANK_DEPTH=${{EVAL_RERANK_DEPTH:-10}} "
                f"EVAL_MAX_CONTEXT_DOCS=${{EVAL_MAX_CONTEXT_DOCS:-2}} "
                f"CRITIC_PATH={repo_dir}/checkpoints/hf/critic-v12-mixed/checkpoint-latest/state.pt "
                f"OUTPUT_DIR={smoke_output_dir} "
                f"GENERATOR_MODEL=${{GENERATOR_MODEL:-{DEFAULT_TEMPLATE_SMOKE_GENERATOR_MODEL}}} "
                f"bash run_eval.sh"
            ),
            "caveat": (
                "Template Biased-NQ smoke evaluation is for pipeline debugging only. It uses the "
                "deterministic template fallback and a small per-dataset cap; do not report it as "
                "original Biased-NQ or full CoRM-RAG reproduction evidence."
            ),
            "expected_outputs": [f"{smoke_output_dir}/evaluation_results.json"],
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument("--data-src", type=Path, default=Path("external_repos/CoRM-RAG/data"))
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("checkpoints/hf/critic-v12-mixed/checkpoint-latest/state.pt"),
    )
    parser.add_argument("--remote-root", default=DEFAULT_REMOTE_ROOT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report = plan_corm_reconstruction(
        workspace=args.workspace,
        data_src=args.data_src,
        checkpoint=args.checkpoint,
        remote_root=args.remote_root,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
