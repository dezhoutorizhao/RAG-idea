import json

from experiments.summarize_evidence_closure import (
    _clean_sufficiency_figure_status,
    _ext4_prepare_dry_run_status,
    _human_audit_v4_eval_status,
    _human_audit_v4_status,
    _current_reproduction_status,
    _end2end_proxy_status,
    _fever_cp_transfer_sweep_status,
    _remote_storage_probe_status,
    _mechanism_ablation_status,
    _semantic_swap_status,
    _v4_case_gallery_status,
    _v4_anti_shortcut_status,
    _v4_failure_taxonomy_status,
    _v4_strong_baseline_status,
)


def test_semantic_swap_status_reads_latest_v4_diagnostic(tmp_path):
    results = tmp_path
    _write_json(
        results / "hotpot_orbits_v4_semanticswap_n100.construction_audit.json",
        {
            "passed": True,
            "groups": 2,
            "failed_groups": 0,
            "aggregate": {
                "mean_clean_doc_overlap": 1.0,
                "mean_perturbation_doc_overlap": 1.0,
                "text_changed_rate": 1.0,
                "answer_mentions_reduced_rate": 1.0,
            },
        },
    )
    _write_json(
        results / "hotpot_orbits_v4_semanticswap_n100.constant.anti_shortcut.json",
        {
            "structural_only_probe": {
                "max_single_feature_auroc": 0.5,
                "passed_0_55_threshold": True,
            },
            "random_label_sanity": {"auroc": {"median": 0.49}},
            "group_split_probe": {"passed_no_group_overlap": True},
        },
    )
    _write_json(
        results / "baselines_hotpot_v4_semanticswap_n100.json",
        {
            "methods": {
                "csrm_rule": {"auroc": 0.9, "risk_at_30": 0.1, "risk_at_50": 0.2, "aurc": 0.3}
            },
            "strongest_non_csrm": {
                "by_auroc": {
                    "method": "calibrated_logistic_orbit",
                    "metrics": {"auroc": 0.95, "risk_at_30": 0.05, "risk_at_50": 0.1, "aurc": 0.2},
                }
            },
            "csrm_vs_strongest_non_csrm": {
                "by_auroc": {
                    "auroc_improvement": -0.05,
                    "risk_at_30_reduction": -0.05,
                    "risk_at_50_reduction": -0.1,
                    "aurc_reduction": -0.1,
                }
            },
        },
    )
    _write_json(
        results / "calibration_hotpot_v4_semanticswap_n100.json",
        {
            "aggregate": {
                "csrm_calibrated_logistic": _calibrated(0.96, 2),
                "csrm_calibrated_isotonic": _calibrated(0.92, 3),
            }
        },
    )
    _write_json(
        results / "compare_calibrated_hotpot_v4_semanticswap_n100.json",
        {
            "aggregate": {
                "csrm_calibrated_logistic": {
                    "calibrated_logistic_orbit": {
                        "auroc_improvement": {"mean": 0.0},
                        "risk_at_30_reduction": {"mean": 0.0},
                        "risk_at_50_reduction": {"mean": 0.0},
                        "aurc_reduction": {"mean": 0.01},
                    }
                }
            }
        },
    )
    audit_dir = results / "human_audit_v4"
    audit_dir.mkdir()
    _write_json(
        audit_dir / "hotpot_v4_semanticswap_n100_blind200.manifest.json",
        {
            "pack_name": "pack",
            "selected_items": 2,
            "selected_label_counts": {"true": 1, "false": 1, "unknown": 0},
        },
    )
    _write_json(
        audit_dir / "hotpot_v4_semanticswap_n100_blind200.readiness.json",
        {
            "ready": False,
            "labeled": 0,
            "pending": 2,
            "completion_rate": 0.0,
            "failed_gates": [{"gate": "min_labeled_total"}],
        },
    )

    status = _semantic_swap_status(results)

    assert status["construction_audit"]["passed"] is True
    assert status["anti_shortcut"]["max_single_feature_auroc"] == 0.5
    assert status["strongest_non_csrm"]["name"] == "calibrated_logistic_orbit"
    assert status["calibrated"]["logistic"]["target_met_count"] == 2
    assert status["human_audit_pack"]["pending"] == 2


def test_remote_storage_probe_status_marks_write_failure(tmp_path):
    _write_json(
        tmp_path / "remote_storage_status_20260529.json",
        {
            "observed_at_utc": "2026-05-28T18:09:53+00:00",
            "target": "/mnt/ntfs-disk",
            "ready_for_full_reproduction_storage": False,
            "target_available_gib": 322.14,
            "target_min_free_met": True,
            "target_write_probe_passed": False,
            "filesystems": [
                {
                    "mount": "/mnt/ntfs-disk",
                    "type": "fuseblk",
                    "capacity": "84%",
                }
            ],
            "target_findmnt": {"stdout": "/dev/nvme1n1p1 fuseblk rw\n"},
            "gpu_query": {"stdout": "0, NVIDIA GeForce RTX 4090, 24564, 24076\n"},
            "write_probe": {"stderr": "No space left on device\n"},
        },
    )

    status = _remote_storage_probe_status(tmp_path)

    assert status["target_min_free_met"] is True
    assert status["target_write_probe_passed"] is False
    assert status["ready_for_full_reproduction_storage"] is False
    assert status["target_filesystem_type"] == "fuseblk"
    assert "No space left" in status["write_probe_error"]


def test_ext4_prepare_dry_run_status_is_non_destructive(tmp_path):
    _write_json(
        tmp_path / "remote_ext4_prepare_dryrun_20260529.json",
        {
            "mode": "dry_run",
            "target": "/home/syk",
            "destructive_operations_executed": False,
            "min_free_gib": 180.0,
            "cleanup_plan": [{"name": "truncate_logs"}, {"name": "clear_root_cache"}],
            "before": {
                "docker_json_logs_bytes": {"stdout": "123\n"},
                "root_cache": {"stdout": "31G\t/root/.cache\n"},
                "user_cache": {"stdout": "19G\t/home/syk/.cache\n"},
                "user_conda_pkg_cache": {"stdout": "5.0G\t/home/syk/miniconda3/pkgs\n"},
                "df_target": {"stdout": "ext4 13G /\n"},
            },
            "next_probe_command": "python experiments/check_remote_storage_status.py ...",
        },
    )

    status = _ext4_prepare_dry_run_status(tmp_path)

    assert status["mode"] == "dry_run"
    assert status["destructive_operations_executed"] is False
    assert status["cleanup_step_count"] == 2
    assert status["docker_json_logs_bytes"] == "123\n"


def test_human_audit_v4_status_is_aggregated(tmp_path):
    _write_json(
        tmp_path / "human_audit_v4_status_20260529.json",
        {
            "ready": False,
            "pack_count": 1,
            "total_items": 2,
            "adjudicated_labeled": 1,
            "pending": 1,
            "packs": [
                {
                    "pack_name": "pack",
                    "selected_items": 2,
                    "ready": False,
                    "adjudication": {"labeled": 1, "pending": 1},
                }
            ],
        },
    )

    status = _human_audit_v4_status(tmp_path)

    assert status["ready"] is False
    assert status["pack_count"] == 1
    assert status["packs"][0]["adjudicated_labeled"] == 1
    assert status["packs"][0]["pending"] == 1


def test_human_audit_v4_eval_status_is_aggregated(tmp_path):
    _write_json(
        tmp_path / "human_audit_v4_eval_status_20260529.json",
        {
            "ready": False,
            "pack_count": 1,
            "evaluated_pack_count": 0,
            "allow_partial": False,
            "packs": [
                {
                    "pack_name": "pack",
                    "selected_items": 2,
                    "labeled": 0,
                    "pending": 2,
                    "evaluation_ready": False,
                    "evaluated": False,
                }
            ],
        },
    )

    status = _human_audit_v4_eval_status(tmp_path)

    assert status["ready"] is False
    assert status["evaluated_pack_count"] == 0
    assert status["packs"][0]["evaluation_ready"] is False


def test_fever_cp_transfer_sweep_status_marks_boundary(tmp_path):
    _write_json(
        tmp_path / "fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json",
        {
            "primary_method": "csrm_logreg_calibrated",
            "risk_targets": [0.2, 0.25, 0.3, 0.35],
            "negative_evidence_for_main_risk_claim": True,
            "primary_method_target_020": {
                "empirical_transfer_supported": False,
                "target_miss_count": 2,
            },
            "primary_method_first_supported_target": {
                "risk_target": 0.35,
                "test_empirical_risk_max": 0.3442,
            },
            "claim_implication": "negative evidence",
        },
    )

    status = _fever_cp_transfer_sweep_status(tmp_path)

    assert status["primary_method"] == "csrm_logreg_calibrated"
    assert status["target_020_supported"] is False
    assert status["target_020_misses"] == 2
    assert status["first_supported_target"] == 0.35
    assert status["negative_evidence_for_main_risk_claim"] is True


def test_end2end_proxy_status_marks_mixed_results(tmp_path):
    _write_json(
        tmp_path / "end2end_selective_rag_proxy_summary_20260529.json",
        {
            "primary_method": "csrm",
            "aggregate": {
                "row_count": 2,
                "risk30_wins": 1,
                "risk30_ties": 0,
                "risk30_losses": 1,
                "risk50_wins": 2,
                "risk50_ties": 0,
                "risk50_losses": 0,
                "aurc_wins": 1,
                "aurc_ties": 0,
                "aurc_losses": 1,
                "mean_risk30_reduction": 0.1,
                "mean_risk50_reduction": 0.2,
                "mean_aurc_reduction": 0.05,
                "all_win": False,
                "has_losses": True,
            },
            "claim_implication": "proxy-only",
        },
    )

    status = _end2end_proxy_status(tmp_path)

    assert status["primary_method"] == "csrm"
    assert status["row_count"] == 2
    assert status["risk30_losses"] == 1
    assert status["all_win"] is False
    assert status["has_losses"] is True


def test_v4_strong_baseline_status_marks_rule_losses(tmp_path):
    _write_json(
        tmp_path / "v4_strong_baseline_summary_20260529.json",
        {
            "aggregate": {
                "baseline_file_count": 6,
                "comparison_file_count": 6,
                "method_union": ["csrm_rule", "calibrated_logistic_orbit"],
                "csrm_rule_vs_strongest": {
                    "by_auroc": {"losses": 6},
                    "by_risk_at_30": {"losses": 6},
                    "by_aurc": {"losses": 6},
                },
                "calibrated_targets_vs_all_baselines": {
                    "csrm_calibrated_logistic": {
                        "risk_at_30_reduction": {"robust_wins": 1, "losses": 1},
                        "aurc_reduction": {"robust_wins": 1, "losses": 5},
                    }
                },
            },
            "claim_implication": "baseline caveat",
        },
    )

    status = _v4_strong_baseline_status(tmp_path)

    assert status["baseline_file_count"] == 6
    assert status["rule_by_auroc_losses"] == 6
    assert status["logistic_risk30_robust_wins"] == 1
    assert status["logistic_aurc_losses"] == 5


def test_v4_failure_taxonomy_status_summarizes_diagnostic(tmp_path):
    _write_json(
        tmp_path / "v4_failure_taxonomy_summary_20260529.json",
        {
            "dataset_count": 6,
            "taxonomy": [{"construction_type": "stable"}, {"construction_type": "semantic_swap"}],
            "case_gallery_coverage": {"target_high_false_positive": 48},
            "metric_aggregate": {
                "auroc": {"wins": 0, "ties": 3, "losses": 3},
                "risk_at_30": {"wins": 1, "ties": 4, "losses": 1},
                "risk_at_50": {"wins": 0, "ties": 4, "losses": 2},
            },
            "feature_frequency": [
                {"feature": "min_sufficiency", "top3_count": 4},
                {"feature": "clean_to_worst_gap", "top3_count": 4},
                {"feature": "verifier_entropy", "top3_count": 3},
                {"feature": "retrieval_overlap", "top3_count": 3},
                {"feature": "answer_consistency", "top3_count": 1},
                {"feature": "unused", "top3_count": 0},
            ],
            "claim_implication": "heuristic/private-label until human audit v4",
        },
    )

    status = _v4_failure_taxonomy_status(tmp_path)

    assert status["dataset_count"] == 6
    assert status["taxonomy_count"] == 2
    assert status["auroc_losses"] == 3
    assert status["risk30_wins"] == 1
    assert len(status["top_feature_gaps"]) == 5
    assert "human audit v4" in status["claim_implication"]


def test_v4_case_gallery_status_summarizes_outputs(tmp_path):
    _write_json(
        tmp_path / "v4_case_gallery_summary_20260529.json",
        {
            "input_count": 6,
            "case_count": 192,
            "bucket_counts": {"target_high_false_positive": 48},
            "dataset_counts": {"hotpot": 32},
            "construction_type_counts": {"stable": 96},
            "outputs": {
                "jsonl": "paper/case_studies/v4_case_gallery_20260529.jsonl",
                "markdown": "paper/case_studies/v4_case_gallery_20260529.md",
            },
            "claim_boundary": "not human-adjudicated evidence",
        },
    )

    status = _v4_case_gallery_status(tmp_path)

    assert status["case_count"] == 192
    assert status["bucket_counts"]["target_high_false_positive"] == 48
    assert status["outputs"]["markdown"].endswith(".md")
    assert "not human-adjudicated" in status["claim_boundary"]


def test_clean_sufficiency_figure_status_summarizes_private_label_boundary(tmp_path):
    _write_json(
        tmp_path / "clean_sufficiency_misleading_v4_20260529.json",
        {
            "row_count": 1200,
            "dataset_count": 6,
            "failure_rate": 0.5,
            "high_sufficiency_failure": {
                "clean_sufficiency": {
                    "threshold": 0.24,
                    "failure_rate": 0.51,
                    "n": 303,
                },
                "worst_sufficiency": {
                    "threshold": 0.22,
                    "failure_rate": 0.36,
                    "n": 302,
                },
            },
            "outputs": {
                "svg": "paper/figures/clean.svg",
                "csv": "paper/figures/clean.csv",
            },
            "claim_boundary": "not human-adjudicated labels",
        },
    )

    status = _clean_sufficiency_figure_status(tmp_path)

    assert status["row_count"] == 1200
    assert status["clean_top_quartile_failure_rate"] == 0.51
    assert status["worst_top_quartile_n"] == 302
    assert "not human-adjudicated" in status["claim_boundary"]


def test_v4_anti_shortcut_status_summarizes_passed_suite(tmp_path):
    _write_json(
        tmp_path / "v4_anti_shortcut_summary_20260529.json",
        {
            "dataset_count": 6,
            "aggregate": {
                "all_raw_firewall_passed": True,
                "all_structural_only_passed_0_55": True,
                "max_single_feature_auroc_max": 0.51875,
                "all_group_split_no_overlap": True,
                "random_label_median_min": 0.4961,
                "random_label_median_max": 0.50545,
                "random_label_median_all_near_half": True,
                "private_metadata_upper_bound_all_high": True,
                "pass_core_anti_shortcut_suite": True,
            },
            "claim_implication": "supports leakage-control claims",
        },
    )

    status = _v4_anti_shortcut_status(tmp_path)

    assert status["dataset_count"] == 6
    assert status["pass_core_anti_shortcut_suite"] is True
    assert status["max_single_feature_auroc_max"] == 0.51875
    assert status["random_label_median_all_near_half"] is True


def test_mechanism_ablation_status_summarizes_alignment_and_boundaries(tmp_path):
    _write_json(
        tmp_path / "mechanism_ablation_summary_20260529.json",
        {
            "dataset_count": 2,
            "aggregate": {
                "strong_alignment_evidence": True,
                "methods_with_negative_or_weak_evidence": ["csrm_no_worst_sufficiency"],
                "by_method": {
                    "csrm_shuffled_perturbations": {
                        "auroc_drop_mean": 0.9,
                        "risk30_increase_mean": 0.6,
                        "aurc_increase_mean": 0.5,
                    },
                    "csrm_no_answer_consistency": {
                        "auroc_drop_mean": 0.1,
                        "risk30_increase_mean": 0.2,
                    },
                    "csrm_no_worst_sufficiency": {
                        "auroc_drop_mean": -0.01,
                        "risk30_increase_mean": 0.0,
                    },
                },
            },
            "claim_implication": "alignment is necessary",
        },
    )

    status = _mechanism_ablation_status(tmp_path)

    assert status["strong_alignment_evidence"] is True
    assert status["shuffled_auroc_drop_mean"] == 0.9
    assert status["no_worst_risk30_increase_mean"] == 0.0
    assert status["weak_or_negative_methods"] == ["csrm_no_worst_sufficiency"]


def test_current_reproduction_status_is_aggregated(tmp_path):
    _write_json(
        tmp_path / "current_evidence_reproduction_20260529.json",
        {
            "ready_for_neurips_main_claim": False,
            "gate_summary": {
                "human_audit_v4_ready": False,
                "human_audit_v4_eval_ready": False,
                "human_audit_v4_pending": 300,
                "full_corm_reconstruction_ready": False,
                "remote_storage_ready": False,
                "claim_verifier_passed": True,
            },
        },
    )

    status = _current_reproduction_status(tmp_path)

    assert status["ready_for_neurips_main_claim"] is False
    assert status["human_audit_v4_pending"] == 300
    assert status["claim_verifier_passed"] is True


def _calibrated(auroc, target_met_count):
    return {
        "auroc": {"mean": auroc},
        "risk_at_30": {"mean": 0.0},
        "risk_at_50": {"mean": 0.1},
        "aurc": {"mean": 0.2},
        "brier": {"mean": 0.05},
        "target_met_count": target_met_count,
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
