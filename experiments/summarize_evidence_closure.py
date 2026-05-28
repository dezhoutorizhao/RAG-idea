#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def get(payload: dict[str, Any], *path: str, default: Any = None) -> Any:
    cursor: Any = payload
    for part in path:
        if not isinstance(cursor, dict) or part not in cursor:
            return default
        cursor = cursor[part]
    return cursor


def metric_table(summary: dict[str, Any], methods: list[str]) -> dict[str, dict[str, float | None]]:
    aggregate = summary.get("aggregate", summary.get("summary", {}))
    output: dict[str, dict[str, float | None]] = {}
    for method in methods:
        item = aggregate.get(method, {})
        risk = item.get("risk_at_30", item.get("risk_at_30_coverage", {}))
        output[method] = {
            "auroc": _metric_value(item.get("auroc")),
            "risk_at_30": _risk_value(risk),
            "aurc": _metric_value(item.get("aurc")),
        }
    return output


def _metric_value(value: Any) -> float | None:
    if isinstance(value, dict):
        value = value.get("mean")
    if value is None:
        return None
    return float(value)


def _risk_value(value: Any) -> float | None:
    if isinstance(value, dict):
        if "risk" in value:
            value = value["risk"]
        else:
            value = value.get("mean")
    return _metric_value(value)


def evidence_closure(root: Path) -> dict[str, Any]:
    results = root / "results"
    methods = [
        "csrm",
        "naive_orbit_average",
        "corm_max_clean",
        "single_set_sure_style",
        "csrm_shuffled_perturbations",
    ]

    hotpot = load_json(results / "hotpot_corm_multiseed_summary_fullabl.json")
    fever = load_json(results / "fever_nearmiss_corm_v3_multiseed_summary.json")
    nli = load_json(results / "audit_sample_paper_1000_v3_nli_set_eval.json")
    hotpot_cp = load_json(results / "hotpot_corm_risk_control_cp_multiseed.json")
    fever_cp = load_json(results / "fever_nearmiss_corm_v3_risk_control_cp_multiseed.json")
    preflight = load_json(results / "corm_reproduction_preflight.json")
    remote = load_json(results / "corm_full_wikipedia_job_status.json")
    claims = load_json(results / "claims_verification.json")

    structural_paths = [
        results / "hotpot_orbit_consistency_audit.json",
        results / "fever_nearmiss_corm_v3_orbit_consistency_audit.json",
        results / "fever_nearmiss_corm_v3_seed31_orbit_consistency_audit.json",
        results / "fever_nearmiss_corm_v3_seed47_orbit_consistency_audit.json",
    ]
    structural = {
        path.name: {
            "passed": bool(load_json(path).get("passed")),
            "error_count": int(load_json(path).get("error_count", 0)),
        }
        for path in structural_paths
    }

    closure = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "verdict": "non_human_bridge_closed_except_full_corm_reconstruction_and_formal_risk",
        "human_audit_v3_excluded_by_user": True,
        "main_bridge_results": {
            "hotpot_corm_multiseed": metric_table(hotpot, methods),
            "fever_nearmiss_corm_v3_multiseed": metric_table(fever, methods),
            "nli_cross_scorer_paper_1000": metric_table(nli, methods),
        },
        "risk_control": {
            "hotpot_cp": {
                "empirical_transfer_supported": get(
                    hotpot_cp,
                    "aggregate",
                    "csrm_logreg_calibrated",
                    "empirical_transfer_supported",
                ),
                "formal_risk_guarantee_supported": get(
                    hotpot_cp,
                    "aggregate",
                    "csrm_logreg_calibrated",
                    "formal_risk_guarantee_supported",
                ),
                "target_miss_count": get(
                    hotpot_cp,
                    "aggregate",
                    "csrm_logreg_calibrated",
                    "target_miss_count",
                ),
            },
            "fever_cp": {
                "empirical_transfer_supported": get(
                    fever_cp,
                    "aggregate",
                    "csrm_logreg_calibrated",
                    "empirical_transfer_supported",
                ),
                "formal_risk_guarantee_supported": get(
                    fever_cp,
                    "aggregate",
                    "csrm_logreg_calibrated",
                    "formal_risk_guarantee_supported",
                ),
                "target_miss_count": get(
                    fever_cp,
                    "aggregate",
                    "csrm_logreg_calibrated",
                    "target_miss_count",
                ),
            },
        },
        "structural_audits": structural,
        "claim_verification": {
            "total_claims": claims.get("total_claims"),
            "passed_claims": claims.get("passed_claims"),
            "failed_claims": claims.get("failed_claims"),
        },
        "corm_reconstruction": {
            "preflight_ready": preflight.get("ready"),
            "missing_required_artifacts": preflight.get("missing_required_artifacts"),
            "remote_status": remote.get("status"),
            "latest_observed_at": remote.get("observed_at"),
            "complete_embedding_shards": get(
                remote,
                "observed_outputs",
                "complete_embedding_shard_count",
            ),
            "latest_complete_embedding_shard": get(
                remote,
                "observed_outputs",
                "latest_complete_embedding_shard",
            ),
            "wiki_faiss_exists": get(remote, "observed_outputs", "wiki_faiss_exists"),
            "terminal_failure": get(remote, "terminal_failure", "summary"),
        },
        "allowed_claims": [
            "CSRM has strong bridge evidence on HotpotQA-derived orbits with released CoRM critic scores.",
            "CSRM has secondary bridge evidence on FEVER v3 near-miss orbits.",
            "Orbit alignment is necessary under the implemented shuffled-perturbation ablation.",
            "The directional CSRM ranking survives an automated NLI cross-scorer sensitivity probe.",
            "Hotpot-only empirical risk-target transfer is supported under the conservative CP pressure test.",
        ],
        "disallowed_claims": [
            "Full original CoRM-RAG retrieval-generation reproduction is complete.",
            "A general formal risk-control guarantee is established.",
            "The results are human-audited.",
            "The method solves robust RAG generally across tasks.",
        ],
        "remaining_non_human_blockers": [
            "Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts.",
            "FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.",
            "Independent external review has not been rerun after the latest storage-status update.",
        ],
    }
    return closure


def render_markdown(status: dict[str, Any]) -> str:
    hotpot = status["main_bridge_results"]["hotpot_corm_multiseed"]
    fever = status["main_bridge_results"]["fever_nearmiss_corm_v3_multiseed"]
    nli = status["main_bridge_results"]["nli_cross_scorer_paper_1000"]
    reconstruction = status["corm_reconstruction"]
    terminal_failure = str(reconstruction["terminal_failure"] or "not recorded").rstrip(".")
    risk = status["risk_control"]
    claims = status["claim_verification"]

    def row(method: str, item: dict[str, float | None]) -> str:
        return (
            f"| {method} | {_fmt(item['auroc'])} | "
            f"{_fmt(item['risk_at_30'])} | {_fmt(item['aurc'])} |"
        )

    lines = [
        "# Evidence Closure Status",
        "",
        f"Generated: `{status['generated_at_utc']}`",
        "",
        "Verdict: non-human bridge evidence is substantially closed, but full CoRM reconstruction "
        "and general formal risk control remain unsupported. Human audit v3 is explicitly excluded "
        "from this closure by user request.",
        "",
        "## HotpotQA Bridge",
        "",
        "| Method | AUROC | Risk@30 | AURC |",
        "|---|---:|---:|---:|",
    ]
    lines.extend(row(method, hotpot[method]) for method in hotpot)
    lines.extend(
        [
            "",
            "## FEVER v3 Near-Miss Bridge",
            "",
            "| Method | AUROC | Risk@30 | AURC |",
            "|---|---:|---:|---:|",
        ]
    )
    lines.extend(row(method, fever[method]) for method in fever)
    lines.extend(
        [
            "",
            "## NLI Cross-Scorer Probe",
            "",
            "| Method | AUROC | Risk@30 | AURC |",
            "|---|---:|---:|---:|",
        ]
    )
    lines.extend(row(method, nli[method]) for method in nli)
    lines.extend(
        [
            "",
            "## Risk Control",
            "",
            f"- Hotpot CP empirical transfer: `{risk['hotpot_cp']['empirical_transfer_supported']}`; "
            f"formal guarantee: `{risk['hotpot_cp']['formal_risk_guarantee_supported']}`; "
            f"target misses: `{risk['hotpot_cp']['target_miss_count']}`.",
            f"- FEVER CP empirical transfer: `{risk['fever_cp']['empirical_transfer_supported']}`; "
            f"formal guarantee: `{risk['fever_cp']['formal_risk_guarantee_supported']}`; "
            f"target misses: `{risk['fever_cp']['target_miss_count']}`.",
            "",
            "## CoRM Reconstruction",
            "",
            f"- Preflight ready: `{reconstruction['preflight_ready']}`.",
            f"- Missing required artifacts: `{reconstruction['missing_required_artifacts']}`.",
            f"- Remote status: `{reconstruction['remote_status']}`.",
            f"- Complete embedding shards: `{reconstruction['complete_embedding_shards']}`; "
            f"latest: `{reconstruction['latest_complete_embedding_shard']}`.",
            f"- FAISS exists: `{reconstruction['wiki_faiss_exists']}`.",
            f"- Terminal failure: {terminal_failure}.",
            "",
            "## Claim Boundary",
            "",
            "Allowed claims:",
        ]
    )
    lines.extend(f"- {item}" for item in status["allowed_claims"])
    lines.extend(["", "Disallowed claims:"])
    lines.extend(f"- {item}" for item in status["disallowed_claims"])
    lines.extend(["", "Remaining non-human blockers:"])
    lines.extend(f"- {item}" for item in status["remaining_non_human_blockers"])
    lines.extend(
        [
            "",
            "## Verification",
            "",
            f"Claim verifier: `{claims['passed_claims']}/{claims['total_claims']}` passed, "
            f"`{claims['failed_claims']}` failed.",
            "",
        ]
    )
    return "\n".join(lines)


def _fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.4f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    status = evidence_closure(args.root)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(status, indent=2, sort_keys=True), encoding="utf-8")
    args.output_md.write_text(render_markdown(status), encoding="utf-8")
    print(json.dumps(status, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
