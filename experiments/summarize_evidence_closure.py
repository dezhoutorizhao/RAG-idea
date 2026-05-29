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
    human_audit_v4_eval_status = _human_audit_v4_eval_status(results)
    current_reproduction_status = _current_reproduction_status(results)
    fever_cp_sweep = _fever_cp_transfer_sweep_status(results)
    end2end_proxy = _end2end_proxy_status(results)
    v4_strong_baselines = _v4_strong_baseline_status(results)
    v4_failure_taxonomy = _v4_failure_taxonomy_status(results)
    v4_case_gallery = _v4_case_gallery_status(results)
    clean_sufficiency_figure = _clean_sufficiency_figure_status(results)
    v4_anti_shortcut = _v4_anti_shortcut_status(results)
    mechanism_ablation = _mechanism_ablation_status(results)
    neurips_readiness = _neurips_readiness_status(results)
    results_provenance = _results_provenance_status(results)
    reproducibility_bundle = _reproducibility_bundle_status(root)

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
            "human_audit_v4_eval": human_audit_v4_eval_status,
            "failure_taxonomy": v4_failure_taxonomy,
            "case_gallery": v4_case_gallery,
            "clean_sufficiency_figure": clean_sufficiency_figure,
            "anti_shortcut": v4_anti_shortcut,
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
                "transfer_sweep": fever_cp_sweep,
            },
        },
        "structural_audits": structural,
        "claim_verification": {
            "total_claims": claims.get("total_claims"),
            "passed_claims": claims.get("passed_claims"),
            "failed_claims": claims.get("failed_claims"),
        },
        "current_evidence_reproduction": current_reproduction_status,
        "results_provenance": results_provenance,
        "reproducibility_bundle": reproducibility_bundle,
        "neurips_readiness": neurips_readiness,
        "mechanism_ablation": mechanism_ablation,
        "end2end_selective_rag_proxy": end2end_proxy,
        "v4_strong_baselines": v4_strong_baselines,
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
            "The v4 failure taxonomy and case gallery are machine-readable diagnostics across FEVER and Hotpot variants, with heuristic/private-label status until human audit v4 is complete.",
            "A paper-facing v4 case-study gallery has been exported from failure-analysis top cases for qualitative inspection.",
            "A private-label diagnostic figure shows that high clean text-only sufficiency still contains many v4 orbit failures; this supports the qualitative motivation but not a human-audited claim.",
            "The primary v4 anti-shortcut suite passes raw-firewall, structural-only, group-split, and random-label sanity checks across six n100 variants.",
            "Mechanism ablations strongly support orbit alignment as necessary; shuffled perturbations collapse across Hotpot and FEVER bridge settings.",
        ],
        "disallowed_claims": [
            "Full original CoRM-RAG retrieval-generation reproduction is complete.",
            "A general formal risk-control guarantee is established.",
            "The results are human-audited.",
            "The method solves robust RAG generally across tasks.",
            "CSRM significantly beats the strongest learned orbit baseline on Hotpot semantic-swap v4.",
            "The v4 failure taxonomy is human-adjudicated evidence.",
        ],
        "remaining_non_human_blockers": [
            "Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts; an ext4 cleanup path exists but needs explicit approval before deleting logs/caches.",
            "FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.",
            "Independent external review has not been rerun after the latest storage-status update.",
            "End-to-end selective RAG evidence is currently proxy-only and mixed on some Hotpot v4 variants; it is not a full CoRM-RAG reproduction.",
            "V4 strong baselines are present, but CSRM-Rule loses or ties the strongest learned/context baselines; main claims must use calibrated/proxy wording with caveats.",
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


def _fever_cp_transfer_sweep_status(results: Path) -> dict[str, Any] | None:
    path = results / "fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    first_supported = payload.get("primary_method_first_supported_target")
    target_020 = payload.get("primary_method_target_020")
    return {
        "artifact": str(path.as_posix()),
        "primary_method": payload.get("primary_method"),
        "risk_targets": payload.get("risk_targets"),
        "negative_evidence_for_main_risk_claim": payload.get(
            "negative_evidence_for_main_risk_claim"
        ),
        "target_020_supported": None
        if target_020 is None
        else target_020.get("empirical_transfer_supported"),
        "target_020_misses": None if target_020 is None else target_020.get("target_miss_count"),
        "first_supported_target": None
        if first_supported is None
        else first_supported.get("risk_target"),
        "first_supported_max_test_risk": None
        if first_supported is None
        else first_supported.get("test_empirical_risk_max"),
        "claim_implication": payload.get("claim_implication"),
    }


def _end2end_proxy_status(results: Path) -> dict[str, Any] | None:
    path = results / "end2end_selective_rag_proxy_summary_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    aggregate = payload.get("aggregate", {})
    return {
        "artifact": str(path.as_posix()),
        "primary_method": payload.get("primary_method"),
        "row_count": aggregate.get("row_count"),
        "risk30_wins": aggregate.get("risk30_wins"),
        "risk30_ties": aggregate.get("risk30_ties"),
        "risk30_losses": aggregate.get("risk30_losses"),
        "risk50_wins": aggregate.get("risk50_wins"),
        "risk50_ties": aggregate.get("risk50_ties"),
        "risk50_losses": aggregate.get("risk50_losses"),
        "aurc_wins": aggregate.get("aurc_wins"),
        "aurc_ties": aggregate.get("aurc_ties"),
        "aurc_losses": aggregate.get("aurc_losses"),
        "mean_risk30_reduction": aggregate.get("mean_risk30_reduction"),
        "mean_risk50_reduction": aggregate.get("mean_risk50_reduction"),
        "mean_aurc_reduction": aggregate.get("mean_aurc_reduction"),
        "all_win": aggregate.get("all_win"),
        "has_losses": aggregate.get("has_losses"),
        "claim_implication": payload.get("claim_implication"),
    }


def _v4_strong_baseline_status(results: Path) -> dict[str, Any] | None:
    path = results / "v4_strong_baseline_summary_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    aggregate = payload.get("aggregate", {})
    rule = aggregate.get("csrm_rule_vs_strongest", {})
    calibrated = aggregate.get("calibrated_targets_vs_all_baselines", {})
    logistic = calibrated.get("csrm_calibrated_logistic", {})
    return {
        "artifact": str(path.as_posix()),
        "baseline_file_count": aggregate.get("baseline_file_count"),
        "comparison_file_count": aggregate.get("comparison_file_count"),
        "method_union": aggregate.get("method_union"),
        "rule_by_auroc_losses": get(rule, "by_auroc", "losses"),
        "rule_by_risk30_losses": get(rule, "by_risk_at_30", "losses"),
        "rule_by_aurc_losses": get(rule, "by_aurc", "losses"),
        "logistic_risk30_robust_wins": get(logistic, "risk_at_30_reduction", "robust_wins"),
        "logistic_risk30_losses": get(logistic, "risk_at_30_reduction", "losses"),
        "logistic_aurc_robust_wins": get(logistic, "aurc_reduction", "robust_wins"),
        "logistic_aurc_losses": get(logistic, "aurc_reduction", "losses"),
        "claim_implication": payload.get("claim_implication"),
    }


def _v4_failure_taxonomy_status(results: Path) -> dict[str, Any] | None:
    path = results / "v4_failure_taxonomy_summary_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    metrics = payload.get("metric_aggregate", {})
    return {
        "artifact": str(path.as_posix()),
        "dataset_count": payload.get("dataset_count"),
        "taxonomy_count": len(payload.get("taxonomy", [])),
        "case_gallery_coverage": payload.get("case_gallery_coverage"),
        "auroc_wins": get(metrics, "auroc", "wins"),
        "auroc_ties": get(metrics, "auroc", "ties"),
        "auroc_losses": get(metrics, "auroc", "losses"),
        "risk30_wins": get(metrics, "risk_at_30", "wins"),
        "risk30_ties": get(metrics, "risk_at_30", "ties"),
        "risk30_losses": get(metrics, "risk_at_30", "losses"),
        "risk50_wins": get(metrics, "risk_at_50", "wins"),
        "risk50_ties": get(metrics, "risk_at_50", "ties"),
        "risk50_losses": get(metrics, "risk_at_50", "losses"),
        "top_feature_gaps": payload.get("feature_frequency", [])[:5],
        "claim_implication": payload.get("claim_implication"),
    }


def _v4_case_gallery_status(results: Path) -> dict[str, Any] | None:
    path = results / "v4_case_gallery_summary_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    return {
        "artifact": str(path.as_posix()),
        "input_count": payload.get("input_count"),
        "case_count": payload.get("case_count"),
        "bucket_counts": payload.get("bucket_counts"),
        "dataset_counts": payload.get("dataset_counts"),
        "construction_type_counts": payload.get("construction_type_counts"),
        "outputs": payload.get("outputs"),
        "claim_boundary": payload.get("claim_boundary"),
    }


def _clean_sufficiency_figure_status(results: Path) -> dict[str, Any] | None:
    path = results / "clean_sufficiency_misleading_v4_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    clean = payload.get("high_sufficiency_failure", {}).get("clean_sufficiency", {})
    worst = payload.get("high_sufficiency_failure", {}).get("worst_sufficiency", {})
    return {
        "artifact": str(path.as_posix()),
        "row_count": payload.get("row_count"),
        "dataset_count": payload.get("dataset_count"),
        "failure_rate": payload.get("failure_rate"),
        "clean_top_quartile_threshold": clean.get("threshold"),
        "clean_top_quartile_failure_rate": clean.get("failure_rate"),
        "clean_top_quartile_n": clean.get("n"),
        "worst_top_quartile_threshold": worst.get("threshold"),
        "worst_top_quartile_failure_rate": worst.get("failure_rate"),
        "worst_top_quartile_n": worst.get("n"),
        "outputs": payload.get("outputs"),
        "claim_boundary": payload.get("claim_boundary"),
    }


def _v4_anti_shortcut_status(results: Path) -> dict[str, Any] | None:
    path = results / "v4_anti_shortcut_summary_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    aggregate = payload.get("aggregate", {})
    return {
        "artifact": str(path.as_posix()),
        "dataset_count": payload.get("dataset_count"),
        "all_raw_firewall_passed": aggregate.get("all_raw_firewall_passed"),
        "all_structural_only_passed_0_55": aggregate.get("all_structural_only_passed_0_55"),
        "max_single_feature_auroc_max": aggregate.get("max_single_feature_auroc_max"),
        "all_group_split_no_overlap": aggregate.get("all_group_split_no_overlap"),
        "random_label_median_min": aggregate.get("random_label_median_min"),
        "random_label_median_max": aggregate.get("random_label_median_max"),
        "random_label_median_all_near_half": aggregate.get("random_label_median_all_near_half"),
        "private_metadata_upper_bound_all_high": aggregate.get(
            "private_metadata_upper_bound_all_high"
        ),
        "pass_core_anti_shortcut_suite": aggregate.get("pass_core_anti_shortcut_suite"),
        "claim_implication": payload.get("claim_implication"),
    }


def _mechanism_ablation_status(results: Path) -> dict[str, Any] | None:
    path = results / "mechanism_ablation_summary_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    by_method = payload.get("aggregate", {}).get("by_method", {})
    shuffled = by_method.get("csrm_shuffled_perturbations", {})
    no_answer = by_method.get("csrm_no_answer_consistency", {})
    no_worst = by_method.get("csrm_no_worst_sufficiency", {})
    return {
        "artifact": str(path.as_posix()),
        "dataset_count": payload.get("dataset_count"),
        "strong_alignment_evidence": get(payload, "aggregate", "strong_alignment_evidence"),
        "weak_or_negative_methods": get(payload, "aggregate", "methods_with_negative_or_weak_evidence"),
        "shuffled_auroc_drop_mean": shuffled.get("auroc_drop_mean"),
        "shuffled_risk30_increase_mean": shuffled.get("risk30_increase_mean"),
        "shuffled_aurc_increase_mean": shuffled.get("aurc_increase_mean"),
        "no_answer_auroc_drop_mean": no_answer.get("auroc_drop_mean"),
        "no_answer_risk30_increase_mean": no_answer.get("risk30_increase_mean"),
        "no_worst_auroc_drop_mean": no_worst.get("auroc_drop_mean"),
        "no_worst_risk30_increase_mean": no_worst.get("risk30_increase_mean"),
        "claim_implication": payload.get("claim_implication"),
    }


def _neurips_readiness_status(results: Path) -> dict[str, Any] | None:
    path = results / "neurips_readiness_matrix_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    return {
        "artifact": str(path.as_posix()),
        "ready_for_neurips_main_track": payload.get("ready_for_neurips_main_track"),
        "status_counts": payload.get("status_counts"),
        "hard_blocker_count": len(payload.get("hard_blockers", [])),
        "negative_or_partial_count": len(payload.get("negative_or_partial_evidence", [])),
        "hard_blockers": [
            {
                "requirement": row.get("requirement"),
                "status": row.get("status"),
                "boundary_or_next_action": row.get("boundary_or_next_action"),
            }
            for row in payload.get("hard_blockers", [])
        ],
        "negative_or_partial_evidence": [
            {
                "requirement": row.get("requirement"),
                "status": row.get("status"),
                "boundary_or_next_action": row.get("boundary_or_next_action"),
            }
            for row in payload.get("negative_or_partial_evidence", [])
        ],
    }


def _results_provenance_status(results: Path) -> dict[str, Any] | None:
    path = results / "results_provenance_manifest_20260529.json"
    readme = results / "README.md"
    if not path.exists():
        return None
    payload = load_json(path)
    return {
        "artifact": str(path.as_posix()),
        "readme_artifact": str(readme.as_posix()),
        "readme_exists": readme.exists(),
        "step_count": payload.get("step_count"),
        "artifact_count": payload.get("artifact_count"),
        "manifest_missing_artifact_count": payload.get("manifest_missing_artifact_count"),
        "missing_output_count": payload.get("missing_output_count"),
        "untracked_output_count": payload.get("untracked_output_count"),
        "readiness_status_counts": payload.get("readiness_status_counts"),
        "claim_boundary": payload.get("claim_boundary"),
    }


def _reproducibility_bundle_status(root: Path) -> dict[str, Any] | None:
    path = root / "reproducibility/bundle_summary_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    return {
        "artifact": "reproducibility/bundle_summary_20260529.json",
        "artifact_checksum_count": payload.get("artifact_checksum_count"),
        "dataset_construction_hash_count": payload.get("dataset_construction_hash_count"),
        "checkpoint_hash_available": payload.get("checkpoint_hash_available"),
        "unique_seed_count": payload.get("unique_seed_count"),
        "hidden_local_path_passed": payload.get("hidden_local_path_passed"),
        "hidden_local_path_finding_count": payload.get("hidden_local_path_finding_count"),
        "remote_storage_ready": payload.get("remote_storage_ready"),
        "claim_boundary": payload.get("claim_boundary"),
        "outputs": payload.get("outputs", {}),
    }


def _human_audit_v4_eval_status(results: Path) -> dict[str, Any] | None:
    path = results / "human_audit_v4_eval_status_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    return {
        "artifact": str(path.as_posix()),
        "ready": payload.get("ready"),
        "pack_count": payload.get("pack_count"),
        "evaluated_pack_count": payload.get("evaluated_pack_count"),
        "allow_partial": payload.get("allow_partial"),
        "packs": [
            {
                "pack_name": pack.get("pack_name"),
                "selected_items": pack.get("selected_items"),
                "labeled": pack.get("labeled"),
                "pending": pack.get("pending"),
                "evaluation_ready": pack.get("evaluation_ready"),
                "evaluated": pack.get("evaluated"),
            }
            for pack in payload.get("packs", [])
        ],
    }


def _current_reproduction_status(results: Path) -> dict[str, Any] | None:
    path = results / "current_evidence_reproduction_20260529.json"
    if not path.exists():
        return None
    payload = load_json(path)
    return {
        "artifact": str(path.as_posix()),
        "ready_for_neurips_main_claim": payload.get("ready_for_neurips_main_claim"),
        "human_audit_v4_ready": get(payload, "gate_summary", "human_audit_v4_ready"),
        "human_audit_v4_eval_ready": get(payload, "gate_summary", "human_audit_v4_eval_ready"),
        "human_audit_v4_pending": get(payload, "gate_summary", "human_audit_v4_pending"),
        "full_corm_reconstruction_ready": get(
            payload,
            "gate_summary",
            "full_corm_reconstruction_ready",
        ),
        "remote_storage_ready": get(payload, "gate_summary", "remote_storage_ready"),
        "claim_verifier_passed": get(payload, "gate_summary", "claim_verifier_passed"),
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
    reproduction = status.get("current_evidence_reproduction")
    results_provenance = status.get("results_provenance")
    reproducibility_bundle = status.get("reproducibility_bundle")
    neurips_readiness = status.get("neurips_readiness")
    mechanism_ablation = status.get("mechanism_ablation")
    end2end_proxy = status.get("end2end_selective_rag_proxy")
    strong_baselines = status.get("v4_strong_baselines")
    semantic = status["latest_v4_diagnostics"]["hotpot_semantic_swap_n100"]
    human_v4 = status["latest_v4_diagnostics"].get("human_audit_v4")
    human_v4_eval = status["latest_v4_diagnostics"].get("human_audit_v4_eval")
    failure_taxonomy = status["latest_v4_diagnostics"].get("failure_taxonomy")
    case_gallery = status["latest_v4_diagnostics"].get("case_gallery")
    clean_sufficiency_figure = status["latest_v4_diagnostics"].get("clean_sufficiency_figure")
    v4_anti_shortcut = status["latest_v4_diagnostics"].get("anti_shortcut")

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
        ]
    )
    fever_sweep = risk["fever_cp"].get("transfer_sweep")
    if fever_sweep:
        lines.extend(
            [
                f"- FEVER CP target sweep: 0.20 supported `{fever_sweep['target_020_supported']}` "
                f"with `{fever_sweep['target_020_misses']}` misses; first observed all-seed pass "
                f"at `{_fmt(fever_sweep['first_supported_target'])}` with max test risk "
                f"`{_fmt(fever_sweep['first_supported_max_test_risk'])}`.",
                f"- FEVER CP claim implication: {fever_sweep['claim_implication']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Current Evidence Reproduction",
            "",
        ]
    )
    if reproduction:
        lines.extend(
            [
                f"- Ready for NeurIPS main claim: `{reproduction['ready_for_neurips_main_claim']}`.",
                f"- Human audit pending: `{reproduction['human_audit_v4_pending']}`; "
                f"human eval ready: `{reproduction['human_audit_v4_eval_ready']}`.",
                f"- Full CoRM reconstruction ready: `{reproduction['full_corm_reconstruction_ready']}`; "
                f"remote storage ready: `{reproduction['remote_storage_ready']}`.",
                f"- Claim verifier passed: `{reproduction['claim_verifier_passed']}`.",
                "",
            ]
        )
    else:
        lines.extend(["- Not recorded.", ""])
    lines.extend(["## Results Provenance", ""])
    if results_provenance:
        lines.extend(
            [
                f"- README artifact: `{results_provenance['readme_artifact']}`; "
                f"exists: `{results_provenance['readme_exists']}`.",
                f"- Provenance steps: `{results_provenance['step_count']}`; "
                f"tracked artifacts: `{results_provenance['artifact_count']}`.",
                f"- Manifest missing artifacts: "
                f"`{results_provenance['manifest_missing_artifact_count']}`; "
                f"missing current-step outputs: `{results_provenance['missing_output_count']}`; "
                f"untracked current-step outputs: `{results_provenance['untracked_output_count']}`.",
                f"- Claim boundary: {results_provenance['claim_boundary']}",
                "",
            ]
        )
    else:
        lines.extend(["- Not recorded.", ""])
    lines.extend(["## Reproducibility Bundle", ""])
    if reproducibility_bundle:
        lines.extend(
            [
                f"- Artifact checksums: `{reproducibility_bundle['artifact_checksum_count']}`; "
                f"dataset construction hashes: "
                f"`{reproducibility_bundle['dataset_construction_hash_count']}`.",
                f"- Checkpoint hash available: "
                f"`{reproducibility_bundle['checkpoint_hash_available']}`; "
                f"unique seeds: `{reproducibility_bundle['unique_seed_count']}`.",
                f"- Hidden local path audit passed: "
                f"`{reproducibility_bundle['hidden_local_path_passed']}`; "
                f"findings: `{reproducibility_bundle['hidden_local_path_finding_count']}`.",
                f"- Remote storage ready: `{reproducibility_bundle['remote_storage_ready']}`.",
                f"- Claim boundary: {reproducibility_bundle['claim_boundary']}",
                "",
            ]
        )
    else:
        lines.extend(["- Not recorded.", ""])
    lines.extend(["## NeurIPS Readiness Matrix", ""])
    if neurips_readiness:
        lines.extend(
            [
                f"- Ready for NeurIPS main-track claim: "
                f"`{neurips_readiness['ready_for_neurips_main_track']}`.",
                f"- Status counts: `{neurips_readiness['status_counts']}`.",
                f"- Hard blockers: `{neurips_readiness['hard_blocker_count']}`; "
                f"negative/partial evidence items: `{neurips_readiness['negative_or_partial_count']}`.",
                "",
                "Hard blockers:",
            ]
        )
        lines.extend(
            f"- {item['requirement']}: {item['boundary_or_next_action']}"
            for item in neurips_readiness["hard_blockers"]
        )
        lines.extend(["", "Negative or partial evidence:"])
        lines.extend(
            f"- {item['requirement']} (`{item['status']}`): {item['boundary_or_next_action']}"
            for item in neurips_readiness["negative_or_partial_evidence"]
        )
        lines.append("")
    else:
        lines.extend(["- Not recorded.", ""])
    lines.extend(["## V4 Strong Baselines", ""])
    if strong_baselines:
        lines.extend(
            [
                f"- Baseline files: `{strong_baselines['baseline_file_count']}`; "
                f"comparison files: `{strong_baselines['comparison_file_count']}`.",
                f"- Method union: `{', '.join(strong_baselines['method_union'] or [])}`.",
                f"- CSRM-Rule losses vs strongest by AUROC/Risk@30/AURC: "
                f"`{strong_baselines['rule_by_auroc_losses']}` / "
                f"`{strong_baselines['rule_by_risk30_losses']}` / "
                f"`{strong_baselines['rule_by_aurc_losses']}`.",
                f"- CSRM-Calibrated-Logistic robust Risk@30 wins/losses: "
                f"`{strong_baselines['logistic_risk30_robust_wins']}` / "
                f"`{strong_baselines['logistic_risk30_losses']}`; AURC robust wins/losses: "
                f"`{strong_baselines['logistic_aurc_robust_wins']}` / "
                f"`{strong_baselines['logistic_aurc_losses']}`.",
                f"- Claim implication: {strong_baselines['claim_implication']}",
                "",
            ]
        )
    else:
        lines.extend(["- Not recorded.", ""])
    lines.extend(["## V4 Failure Taxonomy", ""])
    if failure_taxonomy:
        feature_names = ", ".join(
            str(item.get("feature")) for item in failure_taxonomy["top_feature_gaps"]
        )
        lines.extend(
            [
                f"- Datasets: `{failure_taxonomy['dataset_count']}`; "
                f"construction buckets: `{failure_taxonomy['taxonomy_count']}`.",
                f"- AUROC wins/ties/losses vs calibrated logistic orbit: "
                f"`{failure_taxonomy['auroc_wins']}` / `{failure_taxonomy['auroc_ties']}` / "
                f"`{failure_taxonomy['auroc_losses']}`.",
                f"- Risk@30 wins/ties/losses vs calibrated logistic orbit: "
                f"`{failure_taxonomy['risk30_wins']}` / `{failure_taxonomy['risk30_ties']}` / "
                f"`{failure_taxonomy['risk30_losses']}`.",
                f"- Risk@50 wins/ties/losses vs calibrated logistic orbit: "
                f"`{failure_taxonomy['risk50_wins']}` / `{failure_taxonomy['risk50_ties']}` / "
                f"`{failure_taxonomy['risk50_losses']}`.",
                f"- Case gallery coverage: `{failure_taxonomy['case_gallery_coverage']}`.",
                f"- Recurring top feature gaps: `{feature_names}`.",
                f"- Claim implication: {failure_taxonomy['claim_implication']}",
                "",
            ]
        )
    else:
        lines.extend(["- Not recorded.", ""])
    if case_gallery:
        outputs = case_gallery.get("outputs") or {}
        lines.extend(
            [
                "V4 case-study gallery:",
                f"- Cases: `{case_gallery['case_count']}` from `{case_gallery['input_count']}` inputs.",
                f"- Bucket coverage: `{case_gallery['bucket_counts']}`.",
                f"- Outputs: `{outputs.get('jsonl')}` and `{outputs.get('markdown')}`.",
                f"- Claim boundary: {case_gallery['claim_boundary']}",
                "",
            ]
        )
    else:
        lines.extend(["V4 case-study gallery:", "- Not recorded.", ""])
    if clean_sufficiency_figure:
        outputs = clean_sufficiency_figure.get("outputs") or {}
        lines.extend(
            [
                "Clean-sufficiency misleading diagnostic:",
                f"- Rows: `{clean_sufficiency_figure['row_count']}` across "
                f"`{clean_sufficiency_figure['dataset_count']}` datasets; overall private-label "
                f"failure rate: `{_fmt(clean_sufficiency_figure['failure_rate'])}`.",
                f"- Top-quartile clean sufficiency threshold/failure rate/n: "
                f"`{_fmt(clean_sufficiency_figure['clean_top_quartile_threshold'])}` / "
                f"`{_fmt(clean_sufficiency_figure['clean_top_quartile_failure_rate'])}` / "
                f"`{clean_sufficiency_figure['clean_top_quartile_n']}`.",
                f"- Top-quartile worst sufficiency threshold/failure rate/n: "
                f"`{_fmt(clean_sufficiency_figure['worst_top_quartile_threshold'])}` / "
                f"`{_fmt(clean_sufficiency_figure['worst_top_quartile_failure_rate'])}` / "
                f"`{clean_sufficiency_figure['worst_top_quartile_n']}`.",
                f"- Outputs: `{outputs.get('svg')}` and `{outputs.get('csv')}`.",
                f"- Claim boundary: {clean_sufficiency_figure['claim_boundary']}",
                "",
            ]
        )
    else:
        lines.extend(["Clean-sufficiency misleading diagnostic:", "- Not recorded.", ""])
    if v4_anti_shortcut:
        lines.extend(
            [
                "V4 anti-shortcut suite:",
                f"- Datasets: `{v4_anti_shortcut['dataset_count']}`; core suite passed: "
                f"`{v4_anti_shortcut['pass_core_anti_shortcut_suite']}`.",
                f"- Raw firewall all passed: `{v4_anti_shortcut['all_raw_firewall_passed']}`; "
                f"group split no-overlap all passed: `{v4_anti_shortcut['all_group_split_no_overlap']}`.",
                f"- Structural-only all passed <= 0.55: "
                f"`{v4_anti_shortcut['all_structural_only_passed_0_55']}`; max single-feature AUROC: "
                f"`{_fmt(v4_anti_shortcut['max_single_feature_auroc_max'])}`.",
                f"- Random-label median AUROC range: "
                f"`{_fmt(v4_anti_shortcut['random_label_median_min'])}` to "
                f"`{_fmt(v4_anti_shortcut['random_label_median_max'])}`.",
                f"- Private metadata upper bound all high: "
                f"`{v4_anti_shortcut['private_metadata_upper_bound_all_high']}`.",
                f"- Claim implication: {v4_anti_shortcut['claim_implication']}",
                "",
            ]
        )
    else:
        lines.extend(["V4 anti-shortcut suite:", "- Not recorded.", ""])
    lines.extend(["## Mechanism Ablation", ""])
    if mechanism_ablation:
        lines.extend(
            [
                f"- Datasets: `{mechanism_ablation['dataset_count']}`; strong alignment evidence: "
                f"`{mechanism_ablation['strong_alignment_evidence']}`.",
                f"- Shuffled perturbations mean AUROC drop / Risk@30 increase / AURC increase: "
                f"`{_fmt(mechanism_ablation['shuffled_auroc_drop_mean'])}` / "
                f"`{_fmt(mechanism_ablation['shuffled_risk30_increase_mean'])}` / "
                f"`{_fmt(mechanism_ablation['shuffled_aurc_increase_mean'])}`.",
                f"- No-answer-consistency mean AUROC drop / Risk@30 increase: "
                f"`{_fmt(mechanism_ablation['no_answer_auroc_drop_mean'])}` / "
                f"`{_fmt(mechanism_ablation['no_answer_risk30_increase_mean'])}`.",
                f"- No-worst-sufficiency mean AUROC drop / Risk@30 increase: "
                f"`{_fmt(mechanism_ablation['no_worst_auroc_drop_mean'])}` / "
                f"`{_fmt(mechanism_ablation['no_worst_risk30_increase_mean'])}`.",
                f"- Weak or negative standalone component evidence: "
                f"`{mechanism_ablation['weak_or_negative_methods']}`.",
                f"- Claim implication: {mechanism_ablation['claim_implication']}",
                "",
            ]
        )
    else:
        lines.extend(["- Not recorded.", ""])
    lines.extend(["## End-to-End Selective RAG Proxy", ""])
    if end2end_proxy:
        lines.extend(
            [
                f"- Rows: `{end2end_proxy['row_count']}`; all-win: `{end2end_proxy['all_win']}`; "
                f"has losses/mixed rows: `{end2end_proxy['has_losses']}`.",
                f"- Risk@30 wins/ties/losses vs strongest non-CSRM: "
                f"`{end2end_proxy['risk30_wins']}` / `{end2end_proxy['risk30_ties']}` / "
                f"`{end2end_proxy['risk30_losses']}`.",
                f"- Risk@50 wins/ties/losses vs strongest non-CSRM: "
                f"`{end2end_proxy['risk50_wins']}` / `{end2end_proxy['risk50_ties']}` / "
                f"`{end2end_proxy['risk50_losses']}`.",
                f"- AURC wins/ties/losses vs strongest non-CSRM: "
                f"`{end2end_proxy['aurc_wins']}` / `{end2end_proxy['aurc_ties']}` / "
                f"`{end2end_proxy['aurc_losses']}`.",
                f"- Mean Risk@30/Risk@50/AURC reduction: "
                f"`{_fmt(end2end_proxy['mean_risk30_reduction'])}` / "
                f"`{_fmt(end2end_proxy['mean_risk50_reduction'])}` / "
                f"`{_fmt(end2end_proxy['mean_aurc_reduction'])}`.",
                f"- Claim implication: {end2end_proxy['claim_implication']}",
                "",
            ]
        )
    else:
        lines.extend(["- Not recorded.", ""])
    lines.extend(
        [
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
    if human_v4_eval:
        lines.extend(
            [
                "Human audit v4 evaluation gate:",
                f"- Ready: `{human_v4_eval['ready']}`; evaluated packs: "
                f"`{human_v4_eval['evaluated_pack_count']}/{human_v4_eval['pack_count']}`; "
                f"allow partial: `{human_v4_eval['allow_partial']}`.",
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
