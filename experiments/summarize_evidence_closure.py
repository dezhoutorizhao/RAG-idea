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
    semantic_swap = _semantic_swap_status(results)
    remote_storage_probe = _remote_storage_probe_status(results)
    ext4_prepare_dry_run = _ext4_prepare_dry_run_status(results)
    human_audit_v4_status = _human_audit_v4_status(results)

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
        "latest_v4_diagnostics": {
            "hotpot_semantic_swap_n100": semantic_swap,
            "human_audit_v4": human_audit_v4_status,
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
            "latest_storage_probe": remote_storage_probe,
            "latest_ext4_prepare_dry_run": ext4_prepare_dry_run,
        },
        "allowed_claims": [
            "CSRM has strong bridge evidence on HotpotQA-derived orbits with released CoRM critic scores.",
            "CSRM has secondary bridge evidence on FEVER v3 near-miss orbits.",
            "Orbit alignment is necessary under the implemented shuffled-perturbation ablation.",
            "The directional CSRM ranking survives an automated NLI cross-scorer sensitivity probe.",
            "Hotpot-only empirical risk-target transfer is supported under the conservative CP pressure test.",
            "Hotpot semantic-swap v4 is a leakage-controlled diagnostic where self-consistency and retrieval-stability shortcuts fail.",
        ],
        "disallowed_claims": [
            "Full original CoRM-RAG retrieval-generation reproduction is complete.",
            "A general formal risk-control guarantee is established.",
            "The results are human-audited.",
            "The method solves robust RAG generally across tasks.",
            "CSRM significantly beats the strongest learned orbit baseline on Hotpot semantic-swap v4.",
        ],
        "remaining_non_human_blockers": [
            "Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts; an ext4 cleanup path exists but needs explicit approval before deleting logs/caches.",
            "FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.",
            "Independent external review has not been rerun after the latest storage-status update.",
        ],
        "remaining_human_audit_blockers": [
            "Human audit v4 packs are prepared for Hotpot semantic-swap blind200 and FEVER structbalanced blind100, but adjudicated labels are pending for all 300 items.",
        ],
    }
    return closure


def _semantic_swap_status(results: Path) -> dict[str, Any]:
    construction = load_json(results / "hotpot_orbits_v4_semanticswap_n100.construction_audit.json")
    anti_shortcut = load_json(results / "hotpot_orbits_v4_semanticswap_n100.constant.anti_shortcut.json")
    baselines = load_json(results / "baselines_hotpot_v4_semanticswap_n100.json")
    calibration = load_json(results / "calibration_hotpot_v4_semanticswap_n100.json")
    compare = load_json(results / "compare_calibrated_hotpot_v4_semanticswap_n100.json")
    readiness = load_json(results / "human_audit_v4/hotpot_v4_semanticswap_n100_blind200.readiness.json")
    manifest = load_json(results / "human_audit_v4/hotpot_v4_semanticswap_n100_blind200.manifest.json")

    methods = baselines["methods"]
    csrm = methods["csrm_rule"]
    strongest = baselines["strongest_non_csrm"]["by_auroc"]
    strongest_name = strongest["method"]
    strongest_metrics = strongest["metrics"]
    logistic = calibration["aggregate"]["csrm_calibrated_logistic"]
    isotonic = calibration["aggregate"]["csrm_calibrated_isotonic"]
    against_orbit = compare["aggregate"]["csrm_calibrated_logistic"]["calibrated_logistic_orbit"]
    return {
        "construction_audit": {
            "passed": construction["passed"],
            "groups": construction["groups"],
            "failed_groups": construction["failed_groups"],
            "mean_clean_doc_overlap": get(construction, "aggregate", "mean_clean_doc_overlap"),
            "mean_perturbation_doc_overlap": get(construction, "aggregate", "mean_perturbation_doc_overlap"),
            "text_changed_rate": get(construction, "aggregate", "text_changed_rate"),
            "answer_mentions_reduced_rate": get(construction, "aggregate", "answer_mentions_reduced_rate"),
        },
        "anti_shortcut": {
            "max_single_feature_auroc": get(
                anti_shortcut,
                "structural_only_probe",
                "max_single_feature_auroc",
            ),
            "passed_0_55_threshold": get(
                anti_shortcut,
                "structural_only_probe",
                "passed_0_55_threshold",
            ),
            "random_label_auroc_median": get(
                anti_shortcut,
                "random_label_sanity",
                "auroc",
                "median",
            ),
            "group_split_no_overlap": get(
                anti_shortcut,
                "group_split_probe",
                "passed_no_group_overlap",
            ),
        },
        "rule_csrm": {
            "auroc": csrm["auroc"],
            "risk_at_30": csrm["risk_at_30"],
            "risk_at_50": csrm["risk_at_50"],
            "aurc": csrm["aurc"],
            "vs_strongest_non_csrm_by_auroc": baselines["csrm_vs_strongest_non_csrm"]["by_auroc"],
        },
        "strongest_non_csrm": {
            "name": strongest_name,
            "auroc": strongest_metrics["auroc"],
            "risk_at_30": strongest_metrics["risk_at_30"],
            "risk_at_50": strongest_metrics["risk_at_50"],
            "aurc": strongest_metrics["aurc"],
        },
        "calibrated": {
            "logistic": {
                "auroc_mean": get(logistic, "auroc", "mean"),
                "risk_at_30_mean": get(logistic, "risk_at_30", "mean"),
                "risk_at_50_mean": get(logistic, "risk_at_50", "mean"),
                "aurc_mean": get(logistic, "aurc", "mean"),
                "brier_mean": get(logistic, "brier", "mean"),
                "target_met_count": logistic["target_met_count"],
            },
            "isotonic": {
                "auroc_mean": get(isotonic, "auroc", "mean"),
                "risk_at_30_mean": get(isotonic, "risk_at_30", "mean"),
                "risk_at_50_mean": get(isotonic, "risk_at_50", "mean"),
                "aurc_mean": get(isotonic, "aurc", "mean"),
                "brier_mean": get(isotonic, "brier", "mean"),
                "target_met_count": isotonic["target_met_count"],
            },
            "logistic_vs_calibrated_logistic_orbit": {
                "auroc_delta_mean": get(against_orbit, "auroc_improvement", "mean"),
                "risk_at_30_reduction_mean": get(against_orbit, "risk_at_30_reduction", "mean"),
                "risk_at_50_reduction_mean": get(against_orbit, "risk_at_50_reduction", "mean"),
                "aurc_reduction_mean": get(against_orbit, "aurc_reduction", "mean"),
            },
        },
        "human_audit_pack": {
            "pack_name": manifest["pack_name"],
            "selected_items": manifest["selected_items"],
            "selected_label_counts": manifest["selected_label_counts"],
            "ready": readiness["ready"],
            "labeled": readiness["labeled"],
            "pending": readiness["pending"],
            "completion_rate": readiness["completion_rate"],
            "failed_gates": readiness["failed_gates"],
        },
        "claim_status": "diagnostic_positive_but_not_strongest_baseline_win",
    }


def _remote_storage_probe_status(results: Path) -> dict[str, Any] | None:
    path = results / "remote_storage_status_20260529.json"
    if not path.exists():
        return None

    payload = load_json(path)
    target = payload.get("target")
    target_fs = None
    for filesystem in payload.get("filesystems", []):
        if filesystem.get("mount") == target:
            target_fs = filesystem
            break

    return {
        "artifact": str(path.as_posix()),
        "observed_at_utc": payload.get("observed_at_utc"),
        "target": target,
        "ready_for_full_reproduction_storage": payload.get("ready_for_full_reproduction_storage"),
        "target_available_gib": payload.get("target_available_gib"),
        "target_min_free_met": payload.get("target_min_free_met"),
        "target_write_probe_passed": payload.get("target_write_probe_passed"),
        "target_filesystem_type": None if target_fs is None else target_fs.get("type"),
        "target_capacity": None if target_fs is None else target_fs.get("capacity"),
        "target_findmnt": get(payload, "target_findmnt", "stdout"),
        "gpu_query": get(payload, "gpu_query", "stdout"),
        "write_probe_error": get(payload, "write_probe", "stderr"),
    }


def _ext4_prepare_dry_run_status(results: Path) -> dict[str, Any] | None:
    path = results / "remote_ext4_prepare_dryrun_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    return {
        "artifact": str(path.as_posix()),
        "mode": payload.get("mode"),
        "target": payload.get("target"),
        "destructive_operations_executed": payload.get("destructive_operations_executed"),
        "min_free_gib": payload.get("min_free_gib"),
        "cleanup_step_count": len(payload.get("cleanup_plan", [])),
        "docker_json_logs_bytes": get(payload, "before", "docker_json_logs_bytes", "stdout"),
        "root_cache": get(payload, "before", "root_cache", "stdout"),
        "user_cache": get(payload, "before", "user_cache", "stdout"),
        "user_conda_pkg_cache": get(payload, "before", "user_conda_pkg_cache", "stdout"),
        "df_target": get(payload, "before", "df_target", "stdout"),
        "next_probe_command": payload.get("next_probe_command"),
    }


def _human_audit_v4_status(results: Path) -> dict[str, Any] | None:
    path = results / "human_audit_v4_status_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    return {
        "artifact": str(path.as_posix()),
        "ready": payload.get("ready"),
        "pack_count": payload.get("pack_count"),
        "total_items": payload.get("total_items"),
        "adjudicated_labeled": payload.get("adjudicated_labeled"),
        "pending": payload.get("pending"),
        "packs": [
            {
                "pack_name": pack.get("pack_name"),
                "selected_items": pack.get("selected_items"),
                "ready": pack.get("ready"),
                "adjudicated_labeled": get(pack, "adjudication", "labeled"),
                "pending": get(pack, "adjudication", "pending"),
            }
            for pack in payload.get("packs", [])
        ],
    }


def render_markdown(status: dict[str, Any]) -> str:
    hotpot = status["main_bridge_results"]["hotpot_corm_multiseed"]
    fever = status["main_bridge_results"]["fever_nearmiss_corm_v3_multiseed"]
    nli = status["main_bridge_results"]["nli_cross_scorer_paper_1000"]
    reconstruction = status["corm_reconstruction"]
    terminal_failure = str(reconstruction["terminal_failure"] or "not recorded").rstrip(".")
    storage_probe = reconstruction.get("latest_storage_probe")
    ext4_dry_run = reconstruction.get("latest_ext4_prepare_dry_run")
    risk = status["risk_control"]
    claims = status["claim_verification"]
    semantic = status["latest_v4_diagnostics"]["hotpot_semantic_swap_n100"]
    human_v4 = status["latest_v4_diagnostics"].get("human_audit_v4")

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
        ]
    )
    if storage_probe:
        write_error = str(storage_probe.get("write_probe_error") or "not recorded").strip()
        gpu_query = "; ".join(str(storage_probe.get("gpu_query") or "").splitlines())
        lines.extend(
            [
                "Latest storage probe:",
                f"- Target: `{storage_probe['target']}` "
                f"({storage_probe['target_filesystem_type']}, capacity `{storage_probe['target_capacity']}`).",
                f"- Reported available: `{_fmt(storage_probe['target_available_gib'])}` GiB; "
                f"minimum met: `{storage_probe['target_min_free_met']}`.",
                f"- Write probe passed: `{storage_probe['target_write_probe_passed']}`; "
                f"storage-ready: `{storage_probe['ready_for_full_reproduction_storage']}`.",
                f"- Write probe error: `{write_error}`.",
                f"- GPU query: `{gpu_query}`.",
                "",
            ]
        )
    if ext4_dry_run:
        lines.extend(
            [
                "Latest ext4 cleanup dry run:",
                f"- Target: `{ext4_dry_run['target']}`; mode: `{ext4_dry_run['mode']}`; "
                f"destructive operations executed: `{ext4_dry_run['destructive_operations_executed']}`.",
                f"- Cleanup steps planned: `{ext4_dry_run['cleanup_step_count']}`; "
                f"minimum free required: `{ext4_dry_run['min_free_gib']}` GiB.",
                f"- Docker JSON logs bytes: `{str(ext4_dry_run.get('docker_json_logs_bytes') or '').strip()}`.",
                f"- Root cache: `{str(ext4_dry_run.get('root_cache') or '').strip()}`; "
                f"user cache: `{str(ext4_dry_run.get('user_cache') or '').strip()}`.",
                "",
            ]
        )
    lines.extend(
        [
            "## Latest V4 Hotpot Diagnostic",
            "",
            "Semantic-swap n100:",
            f"- Construction audit passed: `{semantic['construction_audit']['passed']}`; "
            f"failed groups: `{semantic['construction_audit']['failed_groups']}`.",
            f"- Perturbation doc overlap: `{_fmt(semantic['construction_audit']['mean_perturbation_doc_overlap'])}`; "
            f"text changed rate: `{_fmt(semantic['construction_audit']['text_changed_rate'])}`; "
            f"answer-mention reduced rate: `{_fmt(semantic['construction_audit']['answer_mentions_reduced_rate'])}`.",
            f"- Structural-only max AUROC: `{_fmt(semantic['anti_shortcut']['max_single_feature_auroc'])}`.",
            f"- CSRM-Rule AUROC/Risk@30/AURC: "
            f"`{_fmt(semantic['rule_csrm']['auroc'])}` / "
            f"`{_fmt(semantic['rule_csrm']['risk_at_30'])}` / "
            f"`{_fmt(semantic['rule_csrm']['aurc'])}`.",
            f"- Strongest non-CSRM: `{semantic['strongest_non_csrm']['name']}` "
            f"with AUROC `{_fmt(semantic['strongest_non_csrm']['auroc'])}`.",
            f"- CSRM-Calibrated-Logistic AUROC mean: "
            f"`{_fmt(semantic['calibrated']['logistic']['auroc_mean'])}`; "
            f"vs calibrated logistic orbit AUROC delta mean: "
            f"`{_fmt(semantic['calibrated']['logistic_vs_calibrated_logistic_orbit']['auroc_delta_mean'])}`.",
            f"- Human-audited labels complete: `{semantic['human_audit_pack']['ready']}` "
            f"(labeled `{semantic['human_audit_pack']['labeled']}`, pending `{semantic['human_audit_pack']['pending']}`).",
            "",
        ]
    )
    if human_v4:
        lines.extend(
            [
                "Human audit v4 aggregate:",
                f"- Ready: `{human_v4['ready']}`; packs: `{human_v4['pack_count']}`; "
                f"items: `{human_v4['total_items']}`.",
                f"- Adjudicated labels: `{human_v4['adjudicated_labeled']}`; "
                f"pending: `{human_v4['pending']}`.",
                "",
            ]
        )
    lines.extend(
        [
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
    lines.extend(["", "Remaining human-audit blockers:"])
    lines.extend(f"- {item}" for item in status["remaining_human_audit_blockers"])
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
