#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from experiments.run_human_audit_eval_v4 import run_human_audit_eval_v4
from experiments.summarize_evidence_closure import evidence_closure, render_markdown as render_closure_markdown
from experiments.summarize_fever_cp_transfer_sweep import (
    DEFAULT_INPUTS as DEFAULT_FEVER_CP_SWEEP_INPUTS,
    render_markdown as render_fever_cp_sweep_markdown,
    summarize_fever_cp_transfer_sweep,
)
from experiments.summarize_human_audit_v4_status import (
    render_markdown as render_human_audit_markdown,
    summarize_human_audit_v4_status,
)


DEFAULT_MANIFESTS = [
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.manifest.json"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.manifest.json"),
]


def reproduce_current_evidence_v4(
    root: Path,
    output_json: Path,
    output_md: Path,
    *,
    strict: bool = False,
) -> dict[str, Any]:
    results = root / "results"
    commands: list[dict[str, Any]] = []

    human_status_json = results / "human_audit_v4_status_20260529.json"
    human_status_md = results / "human_audit_v4_status_20260529.md"
    human_status = summarize_human_audit_v4_status(results / "human_audit_v4")
    _write_json(human_status_json, human_status)
    human_status_md.write_text(render_human_audit_markdown(human_status), encoding="utf-8")
    commands.append(
        {
            "name": "summarize_human_audit_v4_status",
            "outputs": [str(human_status_json), str(human_status_md)],
            "ready": human_status["ready"],
        }
    )

    eval_status_json = results / "human_audit_v4_eval_status_20260529.json"
    eval_status_md = results / "human_audit_v4_eval_status_20260529.md"
    eval_status = run_human_audit_eval_v4(
        [root / path for path in DEFAULT_MANIFESTS],
        results / "human_audit_v4_eval",
        eval_status_json,
        summary_md=eval_status_md,
        allow_partial=False,
    )
    commands.append(
        {
            "name": "run_human_audit_eval_v4",
            "outputs": [str(eval_status_json), str(eval_status_md)],
            "ready": eval_status["ready"],
            "evaluated_pack_count": eval_status["evaluated_pack_count"],
        }
    )

    fever_cp_sweep_json = results / "fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json"
    fever_cp_sweep_md = results / "fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.md"
    fever_cp_sweep = summarize_fever_cp_transfer_sweep([root / path for path in DEFAULT_FEVER_CP_SWEEP_INPUTS])
    _write_json(fever_cp_sweep_json, fever_cp_sweep)
    fever_cp_sweep_md.write_text(render_fever_cp_sweep_markdown(fever_cp_sweep), encoding="utf-8")
    commands.append(
        {
            "name": "summarize_fever_cp_transfer_sweep",
            "outputs": [str(fever_cp_sweep_json), str(fever_cp_sweep_md)],
            "ready": not fever_cp_sweep["negative_evidence_for_main_risk_claim"],
        }
    )

    closure_json = results / "evidence_closure_status_v4.json"
    closure_md = results / "evidence_closure_status_v4.md"
    closure = evidence_closure(root)
    _write_json(closure_json, closure)
    closure_md.write_text(render_closure_markdown(closure), encoding="utf-8")
    commands.append(
        {
            "name": "summarize_evidence_closure",
            "outputs": [str(closure_json), str(closure_md)],
            "ready": _closure_ready(closure),
        }
    )

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "strict": strict,
        "ready_for_neurips_main_claim": False,
        "commands": commands,
        "gate_summary": {
            "human_audit_v4_ready": human_status["ready"],
            "human_audit_v4_eval_ready": eval_status["ready"],
            "human_audit_v4_pending": human_status["pending"],
            "human_audit_v4_evaluated_pack_count": eval_status["evaluated_pack_count"],
            "full_corm_reconstruction_ready": bool(closure["corm_reconstruction"]["preflight_ready"]),
            "remote_storage_ready": _remote_storage_ready(closure),
            "claim_verifier_passed": closure["claim_verification"]["failed_claims"] == 0,
        },
        "blockers": {
            "human_audit": closure["remaining_human_audit_blockers"],
            "non_human": closure["remaining_non_human_blockers"],
        },
        "claim_policy": (
            "This one-command reproduction rebuilds the current evidence gates and closure artifacts. "
            "It does not fabricate human labels, does not delete server data, and does not complete full CoRM-RAG reproduction."
        ),
    }
    _write_json(output_json, report)
    output_md.write_text(render_markdown(report), encoding="utf-8")

    # Refresh closure once more so it records the manifest generated by this run.
    closure = evidence_closure(root)
    _write_json(closure_json, closure)
    closure_md.write_text(render_closure_markdown(closure), encoding="utf-8")

    if strict and not report["ready_for_neurips_main_claim"]:
        raise SystemExit(1)
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Current Evidence V4 Reproduction",
        "",
        f"Generated: `{report['generated_at_utc']}`",
        "",
        f"Ready for NeurIPS main claim: `{report['ready_for_neurips_main_claim']}`",
        "",
        "## Commands",
        "",
        "| Step | Ready | Outputs |",
        "|---|---|---|",
    ]
    for command in report["commands"]:
        outputs = "<br>".join(f"`{path}`" for path in command["outputs"])
        lines.append(f"| {command['name']} | `{command['ready']}` | {outputs} |")
    gate = report["gate_summary"]
    lines.extend(
        [
            "",
            "## Gate Summary",
            "",
            f"- Human audit v4 ready: `{gate['human_audit_v4_ready']}`.",
            f"- Human audit v4 eval ready: `{gate['human_audit_v4_eval_ready']}`.",
            f"- Human audit v4 pending labels: `{gate['human_audit_v4_pending']}`.",
            f"- Human audit v4 evaluated packs: `{gate['human_audit_v4_evaluated_pack_count']}`.",
            f"- Full CoRM reconstruction ready: `{gate['full_corm_reconstruction_ready']}`.",
            f"- Remote storage ready: `{gate['remote_storage_ready']}`.",
            f"- Claim verifier passed: `{gate['claim_verifier_passed']}`.",
            "",
            "## Blockers",
            "",
            "Human audit:",
        ]
    )
    lines.extend(f"- {item}" for item in report["blockers"]["human_audit"])
    lines.extend(["", "Non-human:"])
    lines.extend(f"- {item}" for item in report["blockers"]["non_human"])
    lines.extend(["", "## Claim Policy", "", report["claim_policy"], ""])
    return "\n".join(lines)


def _closure_ready(closure: dict[str, Any]) -> bool:
    return not closure["remaining_human_audit_blockers"] and not closure["remaining_non_human_blockers"]


def _remote_storage_ready(closure: dict[str, Any]) -> bool:
    probe = closure["corm_reconstruction"].get("latest_storage_probe") or {}
    return bool(probe.get("ready_for_full_reproduction_storage"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    report = reproduce_current_evidence_v4(
        args.root,
        args.output_json,
        args.output_md,
        strict=args.strict,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
