#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_NLI_EVAL = Path("results/audit_sample_paper_1000_v3_nli_set_eval.json")
DEFAULT_NLI_SCORED = Path("results/audit_sample_paper_1000_v3_nli_set.jsonl")
DEFAULT_LLM_JUDGE_STATUS = Path("results/llm_judge_v4_request_status_20260529.json")
DEFAULT_LLM_JUDGE_SCORES = Path("results/llm_judge_v4_scores_20260529.jsonl")
DEFAULT_PAIRED_LLM_JUDGE_STATUS = Path("results/llm_judge_nli_probe_request_status_20260529.json")
DEFAULT_PAIRED_LLM_JUDGE_SCORES = Path("results/llm_judge_nli_probe_scores_20260529.jsonl")
DEFAULT_PAIRED_LLM_SCORE_STATUS = Path("results/llm_judge_nli_probe_score_status_20260529.json")
DEFAULT_LLM_NLI_CORRELATION_STATUS = Path("results/llm_nli_correlation_status_20260529.json")
DEFAULT_HUMAN_AUDIT_STATUS = Path("results/human_audit_v4_status_20260529.json")
REQUIRED_NLI_BASELINES = [
    "naive_orbit_average",
    "single_set_sure_style",
    "corm_max_clean",
    "corm_mean_clean",
]


def summarize_text_only_verifier_status(
    root: Path,
    *,
    nli_eval_path: Path = DEFAULT_NLI_EVAL,
    nli_scored_path: Path = DEFAULT_NLI_SCORED,
    llm_judge_status_path: Path = DEFAULT_LLM_JUDGE_STATUS,
    llm_judge_scores_path: Path = DEFAULT_LLM_JUDGE_SCORES,
    paired_llm_judge_status_path: Path = DEFAULT_PAIRED_LLM_JUDGE_STATUS,
    paired_llm_judge_scores_path: Path = DEFAULT_PAIRED_LLM_JUDGE_SCORES,
    paired_llm_score_status_path: Path = DEFAULT_PAIRED_LLM_SCORE_STATUS,
    llm_nli_correlation_status_path: Path = DEFAULT_LLM_NLI_CORRELATION_STATUS,
    human_audit_status_path: Path = DEFAULT_HUMAN_AUDIT_STATUS,
) -> dict[str, Any]:
    nli_eval_abs = root / nli_eval_path
    nli_scored_abs = root / nli_scored_path
    llm_status_abs = root / llm_judge_status_path
    llm_scores_abs = root / llm_judge_scores_path
    paired_llm_status_abs = root / paired_llm_judge_status_path
    paired_llm_scores_abs = root / paired_llm_judge_scores_path
    paired_score_status_abs = root / paired_llm_score_status_path
    correlation_status_abs = root / llm_nli_correlation_status_path
    human_status_abs = root / human_audit_status_path

    nli_eval = _load_optional_json(nli_eval_abs)
    llm_status = _load_optional_json(llm_status_abs)
    paired_llm_status = _load_optional_json(paired_llm_status_abs)
    paired_score_status = _load_optional_json(paired_score_status_abs)
    correlation_status = _load_optional_json(correlation_status_abs)
    human_status = _load_optional_json(human_status_abs)

    nli_comparisons = _nli_comparisons(nli_eval)
    nli_directional = bool(nli_comparisons) and all(item["passes_all_metrics"] for item in nli_comparisons)
    llm_score_ready = bool(
        llm_status
        and llm_status.get("score_artifact_ready")
        and llm_scores_abs.exists()
        and llm_scores_abs.stat().st_size > 0
    )
    paired_request_pack_ready = bool(
        paired_llm_status
        and paired_llm_status.get("request_pack_ready")
        and paired_llm_status.get("paired_to_nli_probe")
    )
    paired_score_ready = bool(
        paired_llm_status
        and paired_llm_status.get("score_artifact_ready")
        and paired_llm_scores_abs.exists()
        and paired_llm_scores_abs.stat().st_size > 0
    )
    paired_score_space_ready = bool(nli_scored_abs.exists() and paired_score_ready)
    correlation_ready = bool(
        correlation_status
        and correlation_status.get("ready_for_nli_llm_correlation_claim")
    )
    human_ready = bool(human_status and human_status.get("ready"))

    criteria = [
        {
            "criterion": "NLI/text-only scorer beats required weak baselines",
            "status": "pass" if nli_directional else "fail",
            "evidence": str(nli_eval_path),
            "detail": (
                "CSRM has higher AUROC and lower Risk@30/AURC than naive orbit average, "
                "single-set SURE-style, and clean-only CoRM reducers."
                if nli_directional
                else "NLI comparison is missing or not directionally positive across required metrics."
            ),
        },
        {
            "criterion": "LLM judge and NLI ranking correlation",
            "status": "blocked" if not correlation_ready else "pass",
            "evidence": str(llm_judge_scores_path),
            "detail": (
                "Correlation can be computed from paired LLM and NLI scores."
                if correlation_ready
                else "The NLI-paired LLM judge request pack exists, but no API-backed paired score artifact exists yet."
            ),
        },
        {
            "criterion": "Human-label text-only CSRM evaluation",
            "status": "blocked" if not human_ready else "pass",
            "evidence": str(human_audit_status_path),
            "detail": (
                "Human audit labels are ready for text-only evaluation."
                if human_ready
                else "Human audit v4 adjudicated labels are still pending, so human-label text-only Risk@30/50 cannot be claimed."
            ),
        },
    ]

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "nli_probe": {
            "eval_path": str(nli_eval_path),
            "scored_path": str(nli_scored_path),
            "eval_exists": nli_eval is not None,
            "scored_exists": nli_scored_abs.exists(),
            "n": _get(nli_eval, "summary", "csrm", "n"),
            "csrm_metrics": _method_metrics(nli_eval, "csrm"),
            "required_baseline_comparisons": nli_comparisons,
            "directional_advantage_ready": nli_directional,
        },
        "llm_judge": {
            "status_path": str(llm_judge_status_path),
            "score_path": str(llm_judge_scores_path),
            "request_pack_ready": bool(llm_status and llm_status.get("request_pack_ready")),
            "request_count": _get(llm_status, "request_count"),
            "score_artifact_ready": llm_score_ready,
            "paired_request_status_path": str(paired_llm_judge_status_path),
            "paired_request_pack_ready": paired_request_pack_ready,
            "paired_request_count": _get(paired_llm_status, "request_count"),
            "paired_score_path": str(paired_llm_judge_scores_path),
            "paired_score_artifact_ready": paired_score_ready,
            "paired_score_space_ready": paired_score_space_ready,
            "paired_score_status_path": str(paired_llm_score_status_path),
            "paired_score_status": _get(paired_score_status, "status"),
            "paired_score_blocker_reason": _get(paired_score_status, "blocker_reason"),
            "paired_score_parsed_count": _get(paired_score_status, "parsed_score_count"),
            "correlation_status_path": str(llm_nli_correlation_status_path),
            "correlation_status": _get(correlation_status, "status"),
            "correlation_blocker_reason": _get(correlation_status, "blocker_reason"),
            "nli_llm_correlation_ready": correlation_ready,
        },
        "human_audit": {
            "status_path": str(human_audit_status_path),
            "ready": human_ready,
            "pending": _get(human_status, "pending"),
        },
        "success_criteria": criteria,
        "ready_for_text_only_main_claim": all(item["status"] == "pass" for item in criteria),
        "claim_policy": (
            "This audits the text-only verifier evidence from RAG-idea Section 5.2. "
            "It supports only the NLI bridge/probe claim until LLM judge scores and "
            "human adjudicated labels are available."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Text-Only Verifier Status",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Ready for text-only main claim: `{summary['ready_for_text_only_main_claim']}`",
        "",
        "## NLI Probe",
        "",
        f"- Eval artifact: `{summary['nli_probe']['eval_path']}`.",
        f"- Scored artifact: `{summary['nli_probe']['scored_path']}`.",
        f"- N: `{summary['nli_probe']['n']}`.",
        f"- Directional advantage ready: `{summary['nli_probe']['directional_advantage_ready']}`.",
        "",
        "| Baseline | AUROC delta | Risk@30 reduction | AURC reduction | Pass |",
        "|---|---:|---:|---:|---|",
    ]
    for item in summary["nli_probe"]["required_baseline_comparisons"]:
        lines.append(
            "| {baseline} | {auroc_delta:.4f} | {risk30_reduction:.4f} | "
            "{aurc_reduction:.4f} | `{passes_all_metrics}` |".format(**item)
        )
    lines.extend(
        [
            "",
            "## LLM Judge Correlation",
            "",
            f"- Request pack ready: `{summary['llm_judge']['request_pack_ready']}`.",
            f"- Request count: `{summary['llm_judge']['request_count']}`.",
            f"- Score artifact ready: `{summary['llm_judge']['score_artifact_ready']}`.",
            f"- NLI-paired request pack ready: `{summary['llm_judge']['paired_request_pack_ready']}`.",
            f"- NLI-paired request count: `{summary['llm_judge']['paired_request_count']}`.",
            f"- NLI-paired score artifact ready: `{summary['llm_judge']['paired_score_artifact_ready']}`.",
            f"- Paired score space ready: `{summary['llm_judge']['paired_score_space_ready']}`.",
            f"- Paired score normalization status: `{summary['llm_judge']['paired_score_status']}`.",
            f"- Paired score blocker: `{summary['llm_judge']['paired_score_blocker_reason']}`.",
            f"- Paired parsed scores: `{summary['llm_judge']['paired_score_parsed_count']}`.",
            f"- Correlation status: `{summary['llm_judge']['correlation_status']}`.",
            f"- Correlation blocker: `{summary['llm_judge']['correlation_blocker_reason']}`.",
            f"- NLI/LLM correlation ready: `{summary['llm_judge']['nli_llm_correlation_ready']}`.",
            "",
            "## Success Criteria",
            "",
            "| Criterion | Status | Detail |",
            "|---|---|---|",
        ]
    )
    for item in summary["success_criteria"]:
        lines.append(f"| {item['criterion']} | `{item['status']}` | {item['detail']} |")
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _nli_comparisons(nli_eval: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not nli_eval:
        return []
    csrm = _method_metrics(nli_eval, "csrm")
    if not csrm:
        return []
    comparisons = []
    for baseline in REQUIRED_NLI_BASELINES:
        base = _method_metrics(nli_eval, baseline)
        if not base:
            continue
        auroc_delta = csrm["auroc"] - base["auroc"]
        risk30_reduction = base["risk_at_30"] - csrm["risk_at_30"]
        aurc_reduction = base["aurc"] - csrm["aurc"]
        comparisons.append(
            {
                "baseline": baseline,
                "auroc_delta": auroc_delta,
                "risk30_reduction": risk30_reduction,
                "aurc_reduction": aurc_reduction,
                "passes_all_metrics": auroc_delta > 0 and risk30_reduction > 0 and aurc_reduction > 0,
            }
        )
    return comparisons


def _method_metrics(nli_eval: dict[str, Any] | None, method: str) -> dict[str, float] | None:
    if not nli_eval:
        return None
    row = nli_eval.get("summary", {}).get(method)
    if not row:
        return None
    risk30 = row.get("risk_at_30_coverage", {}).get("risk")
    metrics = {"auroc": row.get("auroc"), "aurc": row.get("aurc"), "risk_at_30": risk30, "n": row.get("n")}
    if any(value is None for value in metrics.values()):
        return None
    return metrics


def _load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _get(payload: dict[str, Any] | None, *path: str) -> Any:
    cursor: Any = payload
    for part in path:
        if not isinstance(cursor, dict):
            return None
        cursor = cursor.get(part)
    return cursor


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, default=Path("results/text_only_verifier_status_20260529.json"))
    parser.add_argument("--output-md", type=Path, default=Path("results/text_only_verifier_status_20260529.md"))
    args = parser.parse_args()
    summary = summarize_text_only_verifier_status(args.root)
    _write_json(args.output_json, summary)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
