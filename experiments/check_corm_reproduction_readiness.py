#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


REQUIRED_REPO_FILES = [
    "README.md",
    "src/run_eval.sh",
    "src/run_evaluation.py",
    "src/train_critic.py",
]
REQUIRED_DATA_FILES = [
    "wiki.faiss",
    "wiki_passages.jsonl",
    "biased_nq_test.jsonl",
]
REQUIRED_MODULES = [
    ("numpy", "numpy"),
    ("scipy", "scipy"),
    ("sklearn", "scikit-learn"),
    ("torch", "torch"),
    ("transformers", "transformers"),
    ("datasets", "datasets"),
    ("huggingface_hub", "huggingface_hub"),
    ("faiss", "faiss"),
    ("vllm", "vllm"),
]
DEFAULT_CHECKPOINT = Path("checkpoints/hf/critic-v12-mixed/checkpoint-latest/state.pt")


def check_corm_reproduction_readiness(
    repo: Path,
    data_src: Path,
    checkpoint: Path | None = None,
    *,
    require_cuda: bool = True,
) -> dict[str, Any]:
    repo = repo.resolve()
    data_src = data_src.resolve()
    checkpoint_path = (checkpoint or DEFAULT_CHECKPOINT).resolve()

    repo_checks = _check_files(repo, REQUIRED_REPO_FILES)
    data_checks = _check_files(data_src, REQUIRED_DATA_FILES)
    checkpoint_check = _file_check(checkpoint_path)
    module_checks = [_module_check(import_name, package_name) for import_name, package_name in REQUIRED_MODULES]
    cuda_check = _cuda_check(require_cuda=require_cuda)

    blockers = []
    blockers.extend(_missing_messages("repo", repo_checks))
    blockers.extend(_missing_messages("data", data_checks))
    if not checkpoint_check["exists"]:
        blockers.append(f"missing checkpoint: {checkpoint_check['path']}")
    for module in module_checks:
        if not module["available"]:
            blockers.append(f"missing python module: {module['package']}")
    if not cuda_check["satisfied"]:
        blockers.append(cuda_check["message"])

    return {
        "ready": not blockers,
        "repo": str(repo),
        "data_src": str(data_src),
        "checkpoint": checkpoint_check,
        "required_repo_files": repo_checks,
        "required_data_files": data_checks,
        "python_modules": module_checks,
        "cuda": cuda_check,
        "missing_required_artifacts": len(blockers),
        "blockers": blockers,
        "reproduction_command": _reproduction_command(data_src, checkpoint_path),
        "claim_policy": (
            "Full CoRM-RAG NQ/Biased-NQ/TruthfulQA reproduction claims are allowed "
            "only when ready is true and the evaluation command has produced matching metrics."
        ),
    }


def _check_files(root: Path, relative_paths: list[str]) -> list[dict[str, Any]]:
    return [_file_check(root / relative_path, relative_path=relative_path) for relative_path in relative_paths]


def _file_check(path: Path, *, relative_path: str | None = None) -> dict[str, Any]:
    exists = path.is_file()
    return {
        "name": relative_path or path.name,
        "path": str(path),
        "exists": exists,
        "size_bytes": path.stat().st_size if exists else None,
    }


def _missing_messages(kind: str, checks: list[dict[str, Any]]) -> list[str]:
    return [
        f"missing {kind} file: {check['name']} ({check['path']})"
        for check in checks
        if not check["exists"]
    ]


def _module_check(import_name: str, package_name: str) -> dict[str, Any]:
    return {
        "import_name": import_name,
        "package": package_name,
        "available": importlib.util.find_spec(import_name) is not None,
    }


def _cuda_check(*, require_cuda: bool) -> dict[str, Any]:
    if not require_cuda:
        return {
            "required": False,
            "available": None,
            "satisfied": True,
            "message": "CUDA check skipped.",
        }
    if importlib.util.find_spec("torch") is None:
        return {
            "required": True,
            "available": False,
            "satisfied": False,
            "message": "CUDA required but torch is unavailable.",
        }
    try:
        import torch

        available = bool(torch.cuda.is_available())
    except Exception as exc:  # pragma: no cover - depends on local torch build
        return {
            "required": True,
            "available": False,
            "satisfied": False,
            "message": f"CUDA required but torch CUDA check failed: {exc}",
        }
    return {
        "required": True,
        "available": available,
        "satisfied": available,
        "message": "CUDA available." if available else "CUDA required but unavailable.",
    }


def _reproduction_command(data_src: Path, checkpoint_path: Path) -> str:
    return (
        f"$env:DATA_SRC='{data_src}'; "
        f"$env:CRITIC_PATH='{checkpoint_path}'; "
        "$env:OUTPUT_DIR='results/corm_original_eval'; "
        "Push-Location external_repos/CoRM-RAG/src; "
        "bash run_eval.sh; "
        "Pop-Location"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("external_repos/CoRM-RAG"))
    parser.add_argument(
        "--data-src",
        type=Path,
        default=Path(os.environ.get("DATA_SRC", "external_repos/CoRM-RAG/data")),
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path(os.environ.get("CRITIC_PATH", DEFAULT_CHECKPOINT)),
    )
    parser.add_argument("--no-require-cuda", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report = check_corm_reproduction_readiness(
        args.repo,
        args.data_src,
        args.checkpoint,
        require_cuda=not args.no_require_cuda,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
