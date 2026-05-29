#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SECTION_FILES = [
    Path("paper/sections/formalization.tex"),
    Path("paper/sections/theory.tex"),
]

REQUIRED_LABELS = [
    "sec:formalization",
    "sec:theory",
    "prop:clean-not-orbit",
    "prop:single-set-not-orbit",
    "prop:orbit-alignment-necessary",
]

REQUIRED_CONCEPTS = [
    "orbit risk",
    "clean-only selector",
    "single-set sufficiency",
    "orbit alignment",
    "Scope and non-claims",
]


def summarize_theory_formalization(root: Path) -> dict[str, Any]:
    files = [_file_status(root, path) for path in DEFAULT_SECTION_FILES]
    combined_text = "\n".join(row.get("text", "") for row in files)
    labels = [
        {"label": label, "present": f"\\label{{{label}}}" in combined_text}
        for label in REQUIRED_LABELS
    ]
    concepts = [
        {"concept": concept, "present": concept.lower() in combined_text.lower()}
        for concept in REQUIRED_CONCEPTS
    ]
    all_files_present = all(row["exists"] for row in files)
    all_labels_present = all(row["present"] for row in labels)
    all_concepts_present = all(row["present"] for row in concepts)
    ready = all_files_present and all_labels_present and all_concepts_present
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "section_files": [
            {key: value for key, value in row.items() if key != "text"} for row in files
        ],
        "required_labels": labels,
        "required_concepts": concepts,
        "all_files_present": all_files_present,
        "all_labels_present": all_labels_present,
        "all_concepts_present": all_concepts_present,
        "theory_module_ready": ready,
        "claim_implication": (
            "The formalization supports the mechanism-level information-structure claim that "
            "clean-only, single-set, and unaligned evidence are insufficient for item-level "
            "counterfactual orbit risk. It does not prove empirical all-win behavior, human "
            "validity, or a formal risk-control guarantee."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Theory Formalization Status",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Theory module ready: `{summary['theory_module_ready']}`",
        f"All files present: `{summary['all_files_present']}`",
        f"All labels present: `{summary['all_labels_present']}`",
        f"All concepts present: `{summary['all_concepts_present']}`",
        "",
        "## Section Files",
        "",
        "| Path | Exists | Bytes | SHA256 |",
        "|---|---:|---:|---|",
    ]
    for row in summary["section_files"]:
        lines.append(
            f"| `{row['path']}` | `{row['exists']}` | `{row['size_bytes']}` | `{row['sha256']}` |"
        )

    lines.extend(["", "## Required Labels", ""])
    lines.extend(f"- `{row['label']}`: `{row['present']}`" for row in summary["required_labels"])
    lines.extend(["", "## Required Concepts", ""])
    lines.extend(
        f"- {row['concept']}: `{row['present']}`" for row in summary["required_concepts"]
    )
    lines.extend(["", "## Claim Implication", "", summary["claim_implication"], ""])
    return "\n".join(lines)


def _file_status(root: Path, path: Path) -> dict[str, Any]:
    abs_path = root / path
    if not abs_path.exists():
        return {
            "path": str(path),
            "exists": False,
            "size_bytes": None,
            "sha256": None,
            "text": "",
        }
    text = abs_path.read_text(encoding="utf-8")
    return {
        "path": str(path),
        "exists": True,
        "size_bytes": abs_path.stat().st_size,
        "sha256": _sha256(abs_path),
        "text": text,
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_theory_formalization(args.root)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
