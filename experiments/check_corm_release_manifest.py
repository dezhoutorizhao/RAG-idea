#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_HF_REPO = "PeiyangLiu/CoRM-RAG"
DEFAULT_GITHUB_TREE_URL = "https://api.github.com/repos/PeiYangLiu/CoRM-RAG/git/trees/main?recursive=1"

REQUIRED_PUBLIC_ARTIFACTS = [
    "critic-v12-mixed/checkpoint-latest/state.pt",
    "wiki.faiss",
    "wiki_passages.jsonl",
    "biased_nq_test.jsonl",
]


def analyze_release_manifest(
    *,
    hf_files: list[str] | None,
    github_files: list[str] | None,
    hf_error: str | None = None,
    github_error: str | None = None,
) -> dict[str, Any]:
    hf_files = sorted(hf_files or [])
    github_files = sorted(github_files or [])
    required = []
    for artifact in REQUIRED_PUBLIC_ARTIFACTS:
        required.append(
            {
                "name": artifact,
                "available_on_hf": _contains_artifact(hf_files, artifact),
                "available_on_github": _contains_artifact(github_files, artifact),
            }
        )

    missing_data = [
        item["name"]
        for item in required
        if item["name"] != "critic-v12-mixed/checkpoint-latest/state.pt"
        and not item["available_on_hf"]
        and not item["available_on_github"]
    ]
    checkpoint_available = any(
        item["name"] == "critic-v12-mixed/checkpoint-latest/state.pt"
        and (item["available_on_hf"] or item["available_on_github"])
        for item in required
    )
    release_status = (
        "checkpoint_plus_data"
        if checkpoint_available and not missing_data
        else "checkpoint_only_or_data_missing"
        if checkpoint_available
        else "checkpoint_and_data_missing_or_unverified"
    )
    return {
        "hf_repo": DEFAULT_HF_REPO,
        "github_tree_url": DEFAULT_GITHUB_TREE_URL,
        "hf_query_ok": hf_error is None,
        "github_query_ok": github_error is None,
        "hf_error": hf_error,
        "github_error": github_error,
        "hf_file_count": len(hf_files),
        "github_file_count": len(github_files),
        "hf_files": hf_files,
        "github_files": github_files,
        "required_public_artifacts": required,
        "checkpoint_available": checkpoint_available,
        "missing_public_data_artifacts": missing_data,
        "missing_public_data_count": len(missing_data),
        "release_status": release_status,
        "interpretation": (
            "Full CoRM-RAG reproduction remains blocked unless wiki.faiss, "
            "wiki_passages.jsonl, and biased_nq_test.jsonl are obtained or rebuilt. "
            "The released checkpoint alone is sufficient for critic-scoring bridge studies, "
            "but not for the original retrieval-generation evaluation."
        ),
    }


def _contains_artifact(paths: list[str], artifact: str) -> bool:
    normalized_artifact = artifact.replace("\\", "/")
    artifact_name = normalized_artifact.rsplit("/", 1)[-1]
    for path in paths:
        normalized_path = path.replace("\\", "/")
        if normalized_path == normalized_artifact or normalized_path.endswith("/" + normalized_artifact):
            return True
        if normalized_path.rsplit("/", 1)[-1] == artifact_name:
            return True
    return False


def query_hf_files(repo_id: str) -> tuple[list[str] | None, str | None]:
    try:
        from huggingface_hub import list_repo_files

        return list_repo_files(repo_id, repo_type="model"), None
    except Exception as exc:  # pragma: no cover - network and optional dependency
        return None, f"{type(exc).__name__}: {exc}"


def query_github_tree(url: str) -> tuple[list[str] | None, str | None]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "csrm-rag-reproduction-check",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
        files = [
            item["path"]
            for item in payload.get("tree", [])
            if item.get("type") == "blob" and item.get("path")
        ]
        return files, None
    except Exception as exc:  # pragma: no cover - network dependent
        return None, f"{type(exc).__name__}: {exc}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hf-repo", default=DEFAULT_HF_REPO)
    parser.add_argument("--github-tree-url", default=DEFAULT_GITHUB_TREE_URL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-github", action="store_true")
    args = parser.parse_args()

    hf_files, hf_error = query_hf_files(args.hf_repo)
    if args.skip_github:
        github_files, github_error = [], "skipped"
    else:
        github_files, github_error = query_github_tree(args.github_tree_url)
    report = analyze_release_manifest(
        hf_files=hf_files,
        github_files=github_files,
        hf_error=hf_error,
        github_error=github_error,
    )
    report["hf_repo"] = args.hf_repo
    report["github_tree_url"] = args.github_tree_url
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
