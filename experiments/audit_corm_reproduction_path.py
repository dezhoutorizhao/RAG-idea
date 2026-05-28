#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_RUNTIME_ARTIFACTS = [
    "wiki.faiss",
    "wiki_passages.jsonl",
    "biased_nq_test.jsonl",
]


def audit_reproduction_path(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    workspace = repo.parent.parent.resolve()
    files = _python_and_shell_files(repo)
    source_by_path = {str(path.relative_to(repo)).replace("\\", "/"): path.read_text(encoding="utf-8", errors="replace") for path in files}
    supplemental = _supplemental_reconstruction_report(workspace)

    artifact_reports = []
    for artifact in REQUIRED_RUNTIME_ARTIFACTS:
        artifact_reports.append(_artifact_report(artifact, source_by_path))

    run_eval = source_by_path.get("src/run_eval.sh", "")
    run_evaluation = source_by_path.get("src/run_evaluation.py", "")
    encode_wikipedia = source_by_path.get("src/encode_wikipedia.py", "")

    blockers = []
    for item in artifact_reports:
        if item["required_by_runtime"] and not item["producer_detected"]:
            blockers.append(f"no detected producer for required runtime artifact: {item['name']}")
    if "faiss.read_index" in run_evaluation and "faiss.write_index" not in "\n".join(source_by_path.values()):
        blockers.append("runtime reads a FAISS index but repository source does not call faiss.write_index")
    if "wiki_embeddings.npy" in encode_wikipedia and "wiki.faiss" not in encode_wikipedia:
        blockers.append("encode_wikipedia.py saves embeddings but does not build the wiki.faiss file expected by run_eval.sh")
    if "biased_nq_test.jsonl" in run_evaluation and not _has_writer_for("biased_nq_test.jsonl", source_by_path):
        blockers.append("Biased-NQ evaluation file is consumed but no exact builder is present in the repository")
    if "vllm" in run_evaluation:
        blockers.append("full generation evaluation requires vLLM in addition to retrieval/scoring dependencies")

    return {
        "repo": str(repo),
        "source_file_count": len(files),
        "required_runtime_artifacts": artifact_reports,
        "run_eval_requires_data_src": "DATA_SRC" in run_eval,
        "run_evaluation_reads_faiss": "faiss.read_index" in run_evaluation,
        "repository_calls_faiss_write_index": "faiss.write_index" in "\n".join(source_by_path.values()),
        "encode_wikipedia_outputs_passages": "wiki_passages.jsonl" in encode_wikipedia,
        "encode_wikipedia_outputs_embeddings": "wiki_embeddings.npy" in encode_wikipedia,
        "encode_wikipedia_outputs_faiss": "wiki.faiss" in encode_wikipedia,
        "biased_nq_exact_builder_detected": _has_writer_for("biased_nq_test.jsonl", source_by_path),
        "supplemental_reconstruction": supplemental,
        "reconstructability_status": "blocked" if blockers else "scripted",
        "supplemental_reconstructability_status": (
            "available" if supplemental["faiss_builder_available"] and supplemental["biased_nq_builder_available"] else "missing"
        ),
        "blockers": blockers,
        "minimal_reconstruction_steps": _minimal_steps(),
        "interpretation": (
            "This audit inspects the released repository for a direct path from source scripts "
            "to the runtime artifacts required by run_eval.sh. It does not claim the artifacts "
            "cannot be rebuilt manually; it records whether the current repository scripts expose "
            "a complete, exact, automated reproduction path."
        ),
    }


def _python_and_shell_files(repo: Path) -> list[Path]:
    if not repo.exists():
        raise FileNotFoundError(f"repository not found: {repo}")
    patterns = ["*.py", "*.sh", "README.md"]
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(path for path in repo.rglob(pattern) if path.is_file())
    return sorted(set(paths))


def _artifact_report(artifact: str, source_by_path: dict[str, str]) -> dict[str, Any]:
    required_by = []
    mentioned_by = []
    producers = []
    for rel_path, text in source_by_path.items():
        if artifact not in text:
            continue
        mentioned_by.append(rel_path)
        if _looks_like_reader(artifact, text):
            required_by.append(rel_path)
        if _looks_like_writer(artifact, text):
            producers.append(rel_path)
    return {
        "name": artifact,
        "mentioned_by": sorted(mentioned_by),
        "required_by_runtime": bool(required_by),
        "required_by": sorted(required_by),
        "producer_detected": bool(producers),
        "producer_files": sorted(producers),
    }


def _looks_like_reader(artifact: str, text: str) -> bool:
    escaped = re.escape(artifact)
    reader_patterns = [
        rf"open\([^)]*{escaped}[^)]*\)",
        rf"read_index\([^)]*{escaped}[^)]*\)",
        rf"ln -sf [^\n]*{escaped}",
        rf"stage_file [^\n]*{escaped}",
    ]
    return any(re.search(pattern, text) for pattern in reader_patterns)


def _looks_like_writer(artifact: str, text: str) -> bool:
    escaped = re.escape(artifact)
    writer_patterns = [
        rf"open\([^)]*{escaped}[^)]*,\s*['\"]w",
        rf"write_index\([^)]*{escaped}",
        rf"to_json\([^)]*{escaped}",
        rf"json.dump\([^)]*{escaped}",
    ]
    if any(re.search(pattern, text) for pattern in writer_patterns):
        return True
    if artifact == "wiki_passages.jsonl":
        return (
            "wiki_passages.jsonl" in text
            and re.search(r"open\(\s*passages_path\s*,\s*['\"]w", text) is not None
        )
    return False


def _has_writer_for(artifact: str, source_by_path: dict[str, str]) -> bool:
    return any(_looks_like_writer(artifact, text) for text in source_by_path.values())


def _minimal_steps() -> list[dict[str, str]]:
    return [
        {
            "step": "build_wikipedia_passages",
            "status": "partially_scripted",
            "evidence": "src/encode_wikipedia.py writes wiki_passages.jsonl and wiki_embeddings.npy.",
        },
        {
            "step": "build_faiss_index",
            "status": "missing_exact_script",
            "evidence": "run_evaluation.py reads wiki.faiss, but no faiss.write_index call is present.",
        },
        {
            "step": "build_biased_nq_test",
            "status": "missing_exact_script",
            "evidence": "run_evaluation.py consumes biased_nq_test.jsonl; perturbation scripts write different files.",
        },
        {
            "step": "install_runtime",
            "status": "required",
            "evidence": "run_evaluation.py imports faiss and vllm during full retrieval-generation evaluation.",
        },
    ]


def _supplemental_reconstruction_report(workspace: Path) -> dict[str, Any]:
    faiss_builder = workspace / "experiments" / "build_corm_faiss_index.py"
    biased_builder = workspace / "experiments" / "build_corm_biased_nq_test.py"
    return {
        "workspace": str(workspace),
        "faiss_builder": str(faiss_builder),
        "biased_nq_builder": str(biased_builder),
        "faiss_builder_available": faiss_builder.is_file(),
        "biased_nq_builder_available": biased_builder.is_file(),
        "interpretation": (
            "Supplemental scripts can support a documented reconstruction attempt, "
            "but they are not part of the upstream released CoRM-RAG source and do "
            "not prove equivalence to the authors' original artifacts."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("external_repos/CoRM-RAG"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report = audit_reproduction_path(args.repo)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["reconstructability_status"] != "scripted":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
