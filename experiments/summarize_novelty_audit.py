#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PAPERS = [
    {
        "paper": "Beyond Semantic Relevance: Counterfactual Risk Minimization for Robust Retrieval-Augmented Generation",
        "year": 2026,
        "venue_or_status": "arXiv 2605.01302",
        "url": "https://arxiv.org/abs/2605.01302",
        "overlap": "Direct parent paper: counterfactual risk minimization for robust RAG and risk-aware abstention.",
        "difference": "CSRM-RAG must be framed as a selective risk detector and audit protocol over aligned evidence-set orbits, not as a new CoRM-RAG retriever.",
        "risk_level": "high",
    },
    {
        "paper": "SURE-RAG: Sufficiency and Uncertainty-Aware Evidence Verification for Selective Retrieval-Augmented Generation",
        "year": 2026,
        "venue_or_status": "arXiv 2605.03534",
        "url": "https://arxiv.org/abs/2605.03534",
        "overlap": "Closest sufficiency-verifier and selective-RAG abstention work.",
        "difference": "SURE-RAG focuses on sufficiency/uncertainty verification; CSRM-RAG novelty must come from counterfactual orbit stability and aligned perturbation evidence.",
        "risk_level": "high",
    },
    {
        "paper": "Sufficient Context: A New Lens on Retrieval Augmented Generation Systems",
        "year": 2025,
        "venue_or_status": "ICLR 2025",
        "url": "https://research.google/pubs/sufficient-context-a-new-lens-on-retrieval-augmented-generation-systems-2/",
        "overlap": "Defines sufficient context and uses sufficiency for guided abstention.",
        "difference": "It does not provide item-level counterfactual evidence-orbit risk estimation or aligned orbit ablations.",
        "risk_level": "medium",
    },
    {
        "paper": "Counterfactual Reasoning for Retrieval-Augmented Generation",
        "year": 2026,
        "venue_or_status": "ICLR 2026",
        "url": "https://openreview.net/forum?id=9U51rOnGko",
        "overlap": "Counterfactual queries and arbitration for robust RAG.",
        "difference": "CF-RAG uses counterfactual query reasoning; CSRM-RAG must emphasize evidence-set orbit stability and selective risk under equal verifier budget.",
        "risk_level": "high",
    },
    {
        "paper": "Causal-Counterfactual RAG: The Integration of Causal-Counterfactual Reasoning into RAG",
        "year": 2025,
        "venue_or_status": "arXiv 2509.14435",
        "url": "https://arxiv.org/abs/2509.14435",
        "overlap": "Causal and counterfactual reasoning integrated into RAG.",
        "difference": "Broader causal-counterfactual answer generation; not the same as calibrated orbit-level selective risk detection.",
        "risk_level": "medium",
    },
    {
        "paper": "Is Conformal Factuality for RAG-based LLMs Robust? Novel Metrics and Systematic Insights",
        "year": 2026,
        "venue_or_status": "arXiv 2603.16817",
        "url": "https://arxiv.org/abs/2603.16817",
        "overlap": "Robust factuality and calibration-style guarantees for RAG.",
        "difference": "Relevant to risk-control claims; current CSRM-RAG evidence is empirical and must not claim formal conformal coverage.",
        "risk_level": "medium",
    },
]

CORE_CLAIMS = [
    {
        "claim": "Aligned evidence-set orbits expose fragile RAG items that clean sufficiency misses.",
        "novelty": "medium",
        "closest_prior": "CoRM-RAG; Sufficient Context; SURE-RAG",
        "assessment": "Plausible if positioned as orbit-level counterfactual stability rather than plain sufficiency.",
    },
    {
        "claim": "CSRM estimates selective item risk from orbit statistics under equal verifier-call budgets.",
        "novelty": "medium",
        "closest_prior": "SURE-RAG; CoRM-RAG",
        "assessment": "Novelty depends on human-audited orbit labels and strong equal-budget baselines; current evidence is partial.",
    },
    {
        "claim": "Orbit alignment is a necessary mechanism for counterfactual selective RAG.",
        "novelty": "medium-high",
        "closest_prior": "CF-RAG; CoRM-RAG",
        "assessment": "Mechanism is defensible after shuffled-alignment ablation and formalization, but needs careful distinction from counterfactual-query methods.",
    },
    {
        "claim": "CSRM provides formal/general risk control for robust RAG.",
        "novelty": "low",
        "closest_prior": "Conformal factuality for RAG; CoRM-RAG risk-aware abstention",
        "assessment": "Do not claim. Current FEVER evidence is negative at the 0.20 target.",
    },
]


def summarize_novelty_audit() -> dict[str, Any]:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "search_date": "2026-05-29",
        "method_under_review": (
            "CSRM-RAG: counterfactual sufficiency stability and calibrated selective risk "
            "over aligned evidence-set orbits for robust RAG."
        ),
        "core_claims": CORE_CLAIMS,
        "closest_prior_work": PAPERS,
        "overall_novelty_score_10": 6.5,
        "recommendation": "proceed_with_caution",
        "positioning": (
            "Frame the contribution as an audit-grade, leakage-controlled, aligned evidence-orbit "
            "selective-risk protocol built on top of CoRM-style critic scores. Avoid claiming a new "
            "retrieval paradigm, formal risk control, or all-win superiority."
        ),
        "required_to_upgrade": [
            "Complete the 1000-item Human Audit v4 labels and report human-label metrics.",
            "Obtain API-backed LLM-judge baseline/correlation scores or remove LLM-judge claims.",
            "Keep full CoRM-RAG reproduction unsupported until the storage/index artifacts are repaired.",
            "Write related work around SURE-RAG, Sufficient Context, CF-RAG, and CoRM-RAG as closest neighbors.",
        ],
        "novelty_ready_for_strong_claim": False,
        "claim_policy": (
            "This is a current literature-positioning audit, not proof of novelty. It supports a "
            "narrow proceed-with-caution framing and highlights prior-work risks that must be "
            "disclosed in any NeurIPS submission."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Novelty Audit Update",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Search date: `{summary['search_date']}`",
        "",
        f"Method: {summary['method_under_review']}",
        "",
        f"Overall novelty score: `{summary['overall_novelty_score_10']}/10`",
        f"Recommendation: `{summary['recommendation']}`",
        f"Ready for strong novelty claim: `{summary['novelty_ready_for_strong_claim']}`",
        "",
        "## Core Claims",
        "",
        "| Claim | Novelty | Closest prior | Assessment |",
        "|---|---|---|---|",
    ]
    for row in summary["core_claims"]:
        lines.append(
            f"| {row['claim']} | `{row['novelty']}` | {row['closest_prior']} | {row['assessment']} |"
        )
    lines.extend(
        [
            "",
            "## Closest Prior Work",
            "",
            "| Paper | Year | Venue/status | Overlap | Difference | Risk |",
            "|---|---:|---|---|---|---|",
        ]
    )
    for paper in summary["closest_prior_work"]:
        lines.append(
            f"| [{paper['paper']}]({paper['url']}) | {paper['year']} | "
            f"{paper['venue_or_status']} | {paper['overlap']} | {paper['difference']} | "
            f"`{paper['risk_level']}` |"
        )
    lines.extend(["", "## Positioning", "", summary["positioning"], ""])
    lines.extend(["## Required To Upgrade", ""])
    lines.extend(f"- {item}" for item in summary["required_to_upgrade"])
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_novelty_audit()
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
