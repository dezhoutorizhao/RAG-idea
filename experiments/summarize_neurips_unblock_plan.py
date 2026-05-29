#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_READINESS = Path("results/neurips_readiness_matrix_20260529.json")
DEFAULT_HUMAN_COLLECTION = Path("results/human_audit_v4_batch_collection_20260529.json")
DEFAULT_HUMAN_STATUS = Path("results/human_audit_v4_status_20260529.json")
DEFAULT_LLM_BATCH = Path("results/llm_judge_nli_probe_batch_run_status_20260529.json")
DEFAULT_LLM_SCORE = Path("results/llm_judge_nli_probe_score_status_20260529.json")
DEFAULT_LLM_CORRELATION = Path("results/llm_nli_correlation_status_20260529.json")
DEFAULT_REMOTE_STORAGE = Path("results/remote_storage_status_20260529.json")
DEFAULT_EXT4_DRYRUN = Path("results/remote_ext4_prepare_dryrun_20260529.json")
DEFAULT_EXTERNAL_REVIEW = Path("results/external_review_packet_status_20260529.json")


def summarize_neurips_unblock_plan(
    root: Path = Path("."),
    *,
    readiness_path: Path = DEFAULT_READINESS,
    human_collection_path: Path = DEFAULT_HUMAN_COLLECTION,
    human_status_path: Path = DEFAULT_HUMAN_STATUS,
    llm_batch_path: Path = DEFAULT_LLM_BATCH,
    llm_score_path: Path = DEFAULT_LLM_SCORE,
    llm_correlation_path: Path = DEFAULT_LLM_CORRELATION,
    remote_storage_path: Path = DEFAULT_REMOTE_STORAGE,
    ext4_dryrun_path: Path = DEFAULT_EXT4_DRYRUN,
    external_review_path: Path = DEFAULT_EXTERNAL_REVIEW,
) -> dict[str, Any]:
    readiness = _load_optional_json(root / readiness_path)
    human_collection = _load_optional_json(root / human_collection_path)
    human_status = _load_optional_json(root / human_status_path)
    llm_batch = _load_optional_json(root / llm_batch_path)
    llm_score = _load_optional_json(root / llm_score_path)
    llm_correlation = _load_optional_json(root / llm_correlation_path)
    remote_storage = _load_optional_json(root / remote_storage_path)
    ext4_dryrun = _load_optional_json(root / ext4_dryrun_path)
    external_review = _load_optional_json(root / external_review_path)

    blockers = [
        _human_audit_blocker(human_collection, human_status),
        _llm_judge_blocker(llm_batch, llm_score, llm_correlation),
        _full_corm_storage_blocker(remote_storage, ext4_dryrun),
        _external_review_blocker(external_review),
        _risk_control_boundary(),
    ]
    open_blockers = [item for item in blockers if item["status"] != "pass"]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_artifacts": {
            "readiness": str(readiness_path),
            "human_collection": str(human_collection_path),
            "human_status": str(human_status_path),
            "llm_batch": str(llm_batch_path),
            "llm_score": str(llm_score_path),
            "llm_correlation": str(llm_correlation_path),
            "remote_storage": str(remote_storage_path),
            "ext4_dryrun": str(ext4_dryrun_path),
            "external_review": str(external_review_path),
        },
        "readiness_status_counts": readiness.get("status_counts", {}),
        "ready_for_neurips_main_track": readiness.get("ready_for_neurips_main_track"),
        "blockers": blockers,
        "open_blocker_count": len(open_blockers),
        "external_action_required_count": sum(1 for item in open_blockers if item["requires_external_action"]),
        "requires_user_approval_count": sum(1 for item in open_blockers if item["requires_user_approval"]),
        "next_execution_order": [
            "complete_human_audit_labels",
            "run_api_backed_llm_judge_batch",
            "approve_and_execute_remote_ext4_cleanup",
            "rerun_full_corm_reproduction_after_storage_probe_passes",
            "obtain_independent_external_review_response",
            "rerun_main_tables_and_claim_verifier",
        ],
        "claim_policy": (
            "This is an unblock plan, not evidence that the blockers are solved. It records the "
            "minimum external actions and repository commands needed before NeurIPS main-track "
            "readiness can be re-evaluated."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# NeurIPS Evidence Unblock Plan",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Ready for NeurIPS main-track claim: `{summary['ready_for_neurips_main_track']}`",
        f"Open blockers: `{summary['open_blocker_count']}`",
        f"External actions required: `{summary['external_action_required_count']}`",
        f"User approvals required: `{summary['requires_user_approval_count']}`",
        "",
        "## Blockers",
        "",
        "| Blocker | Status | External action | User approval | Current evidence | Next command |",
        "|---|---|---:|---:|---|---|",
    ]
    for item in summary["blockers"]:
        evidence = item["current_evidence"].replace("|", "\\|")
        command = "<br>".join(f"`{command}`" for command in item["next_commands"])
        lines.append(
            f"| {item['id']} | `{item['status']}` | `{item['requires_external_action']}` | "
            f"`{item['requires_user_approval']}` | {evidence} | {command} |"
        )
    lines.extend(["", "## Execution Order", ""])
    lines.extend(f"{index}. `{step}`" for index, step in enumerate(summary["next_execution_order"], start=1))
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _human_audit_blocker(collection: dict[str, Any], status: dict[str, Any]) -> dict[str, Any]:
    complete = bool(collection.get("human_labels_complete")) and bool(status.get("ready"))
    pending_auditor = collection.get("pending_auditor_labels")
    pending_adjudicated = collection.get("pending_adjudicated_labels")
    return {
        "id": "complete_human_audit_v4",
        "status": "pass" if complete else "blocked",
        "requires_external_action": not complete,
        "requires_user_approval": False,
        "current_evidence": (
            f"human_labels_complete={collection.get('human_labels_complete')}; "
            f"pending_auditor_labels={pending_auditor}; "
            f"pending_adjudicated_labels={pending_adjudicated}; "
            f"aggregate_pending={status.get('pending')}."
        ),
        "required_external_action": (
            "Fill both auditor CSV batches and adjudication labels for the v4 paper audit pack."
        ),
        "next_commands": [
            (
                "python -m experiments.collect_human_audit_v4_assignment_batches "
                "--output-json results/human_audit_v4_batch_collection_20260529.json "
                "--output-md results/human_audit_v4_batch_collection_20260529.md"
            ),
            "powershell -ExecutionPolicy Bypass -File scripts\\run_main_tables.ps1",
        ],
    }


def _llm_judge_blocker(
    batch: dict[str, Any],
    score: dict[str, Any],
    correlation: dict[str, Any],
) -> dict[str, Any]:
    ready = bool(correlation.get("ready_for_nli_llm_correlation_claim"))
    followup = batch.get("execution_commands") or batch.get("followup_commands") or []
    commands = [item.get("command") for item in followup if item.get("command")]
    if not commands:
        commands = [
            "$env:OPENAI_API_KEY='<set locally>'; python -m experiments.manage_openai_llm_judge_batch --action submit",
            "$env:OPENAI_API_KEY='<set locally>'; python -m experiments.manage_openai_llm_judge_batch --action retrieve --batch-id <batch_id>",
            "python -m experiments.normalize_llm_judge_batch_responses --batch-output-jsonl results\\llm_judge_nli_probe_batch_output_20260529.jsonl --scores-jsonl results\\llm_judge_nli_probe_scores_20260529.jsonl",
            "python -m experiments.compute_llm_nli_correlation --output-json results\\llm_nli_correlation_status_20260529.json --output-md results\\llm_nli_correlation_status_20260529.md",
        ]
    return {
        "id": "run_api_backed_llm_judge",
        "status": "pass" if ready else "blocked",
        "requires_external_action": not ready,
        "requires_user_approval": False,
        "current_evidence": (
            f"batch_status={batch.get('status')}; "
            f"ready_for_batch_submission={batch.get('ready_for_batch_submission')}; "
            f"score_status={score.get('status')}; "
            f"correlation_ready={correlation.get('ready_for_nli_llm_correlation_claim')}."
        ),
        "required_external_action": "Provide a real API key and run the OpenAI-compatible batch flow.",
        "next_commands": commands,
    }


def _full_corm_storage_blocker(storage: dict[str, Any], ext4: dict[str, Any]) -> dict[str, Any]:
    ready = bool(storage.get("ready_for_full_reproduction_storage"))
    cleanup_commands = [
        (
            "$env:CORM_REMOTE_PASSWORD='<set locally>'; python -m experiments.prepare_remote_ext4_storage "
            "--host 192.168.103.101 --user syk --port 22 --target /home/syk "
            "--output results/remote_ext4_prepare_execute_20260529.json --min-free-gib 180 --execute"
        ),
        (
            "$env:CORM_REMOTE_PASSWORD='<set locally>'; python -m experiments.check_remote_storage_status "
            "--host 192.168.103.101 --user syk --port 22 --target /home/syk "
            "--output results/remote_storage_status_after_ext4_cleanup.json --min-free-gib 180"
        ),
        "run results/corm_remote_scripts/02_build_wikipedia_and_faiss.sh only after the post-cleanup probe passes",
    ]
    return {
        "id": "repair_storage_for_full_corm_reproduction",
        "status": "pass" if ready else "blocked",
        "requires_external_action": not ready,
        "requires_user_approval": not ready,
        "current_evidence": (
            f"target={storage.get('target')}; "
            f"target_available_gib={_fmt(storage.get('target_available_gib'))}; "
            f"target_write_probe_passed={storage.get('target_write_probe_passed')}; "
            f"ext4_mode={ext4.get('mode')}; "
            f"destructive_operations_executed={ext4.get('destructive_operations_executed')}."
        ),
        "required_external_action": (
            "Approve the minimal ext4 cleanup plan, then verify write/fsync/read/delete on /home/syk."
        ),
        "next_commands": cleanup_commands,
    }


def _external_review_blocker(review: dict[str, Any]) -> dict[str, Any]:
    ready = bool(review.get("ready_for_independent_external_review_claim"))
    response = review.get("review_response_path") or "results/external_review_response_20260529.md"
    return {
        "id": "obtain_independent_external_review",
        "status": "pass" if ready else "blocked",
        "requires_external_action": not ready,
        "requires_user_approval": False,
        "current_evidence": (
            f"packet_ready={review.get('packet_ready')}; "
            f"external_review_completed={review.get('external_review_completed')}; "
            f"response_path={response}."
        ),
        "required_external_action": "Have an independent reviewer inspect the packet and write the response file.",
        "next_commands": [
            f"place independent review response at {response}",
            "powershell -ExecutionPolicy Bypass -File scripts\\run_main_tables.ps1",
        ],
    }


def _risk_control_boundary() -> dict[str, Any]:
    return {
        "id": "risk_control_claim_boundary",
        "status": "fail",
        "requires_external_action": False,
        "requires_user_approval": False,
        "current_evidence": (
            "FEVER 0.20 CP transfer remains negative; this is scientific negative evidence, "
            "not an operational blocker."
        ),
        "required_external_action": (
            "Keep risk-control wording as Hotpot-only empirical pressure-test evidence unless "
            "new experiments overturn the FEVER failure."
        ),
        "next_commands": [
            "do not claim a general formal risk-control guarantee",
            "use results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json as boundary evidence",
        ],
    }


def _fmt(value: Any) -> str:
    return "unknown" if value is None else f"{float(value):.1f}"


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_neurips_unblock_plan(args.root)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
