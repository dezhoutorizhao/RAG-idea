#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_ARTIFACTS = [
    Path("results/current_evidence_reproduction_20260529.json"),
    Path("results/current_evidence_reproduction_20260529.md"),
    Path("CLAIMS_LEDGER.json"),
    Path("CLAIMS_LEDGER.md"),
    Path("results/claims_verification.json"),
    Path("results/claims_ledger_markdown_summary_20260529.json"),
    Path("results/evidence_closure_status_v4.json"),
    Path("results/evidence_closure_status_v4.md"),
    Path("results/results_provenance_manifest_20260529.json"),
    Path("results/README.md"),
    Path("results/neurips_readiness_matrix_20260529.json"),
    Path("results/neurips_readiness_matrix_20260529.md"),
    Path("results/neurips_unblock_plan_20260529.json"),
    Path("results/neurips_unblock_plan_20260529.md"),
    Path("results/remote_storage_status_20260529.json"),
    Path("results/remote_home_storage_status_20260529.json"),
    Path("results/remote_ext4_prepare_dryrun_20260529.json"),
    Path("results/remote_ext4_prepare_dryrun_20260529.md"),
    Path("results/remote_storage_cleanup_plan_20260529.md"),
    Path("results/remote_cleanup_candidates_20260529.json"),
    Path("results/remote_cleanup_candidates_20260529.md"),
    Path("results/remote_ext4_cleanup_guarded_plan_20260529.json"),
    Path("results/remote_ext4_cleanup_guarded_plan_20260529.md"),
    Path("results/corm_reconstruction_plan_ext4_20260529.json"),
    Path("results/corm_remote_scripts_ext4_manifest.json"),
    Path("results/corm_remote_scripts_ext4/00_env.sh"),
    Path("results/corm_remote_scripts_ext4/01_prepare_env.sh"),
    Path("results/corm_remote_scripts_ext4/02_build_wikipedia_and_faiss.sh"),
    Path("results/corm_remote_scripts_ext4/03_prepare_biased_nq.sh"),
    Path("results/corm_remote_scripts_ext4/04_run_reconstructed_eval.sh"),
    Path("results/corm_remote_scripts_ext4/README.md"),
    Path("results/external_review_packet_status_20260529.json"),
    Path("results/external_review_packet_20260529.md"),
    Path("results/human_audit_v4_paper_pack_status_20260529.json"),
    Path("results/human_audit_v4_paper_pack_status_20260529.md"),
    Path("results/human_audit_v4_assignment_batches_20260529.json"),
    Path("results/human_audit_v4_assignment_batches_20260529.md"),
    Path("results/human_audit_v4_batch_collection_20260529.json"),
    Path("results/human_audit_v4_batch_collection_20260529.md"),
    Path("results/human_audit_v4_status_20260529.json"),
    Path("results/human_audit_v4_status_20260529.md"),
    Path("results/human_audit_v4_disagreement_taxonomy_20260529.json"),
    Path("results/human_audit_v4_disagreement_taxonomy_20260529.md"),
    Path("results/human_audit_v4_mismatch_20260529.json"),
    Path("results/human_audit_v4_mismatch_20260529.md"),
    Path("results/human_audit_v4_eval_status_20260529.json"),
    Path("results/human_audit_v4_eval_status_20260529.md"),
    Path("results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json"),
    Path("results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.md"),
    Path("results/end2end_selective_rag_proxy_summary_20260529.json"),
    Path("results/end2end_selective_rag_proxy_summary_20260529.md"),
    Path("results/end2end_retriever_generator_matrix_20260529.json"),
    Path("results/end2end_retriever_generator_matrix_20260529.md"),
    Path("results/end2end_risk_coverage_curves_20260529.json"),
    Path("results/end2end_risk_coverage_curves_20260529.md"),
    Path("results/end2end_target_risk_coverage_20260529.json"),
    Path("results/end2end_target_risk_coverage_20260529.md"),
    Path("paper/figures/end2end_risk_coverage_curves_20260529.svg"),
    Path("results/llm_judge_v4_requests_20260529.jsonl"),
    Path("results/llm_judge_v4_request_status_20260529.json"),
    Path("results/llm_judge_v4_request_status_20260529.md"),
    Path("results/llm_judge_nli_probe_requests_20260529.jsonl"),
    Path("results/llm_judge_nli_probe_request_status_20260529.json"),
    Path("results/llm_judge_nli_probe_request_status_20260529.md"),
    Path("results/llm_judge_nli_probe_batch_run_status_20260529.json"),
    Path("results/llm_judge_nli_probe_batch_run_status_20260529.md"),
    Path("results/llm_judge_nli_probe_score_status_20260529.json"),
    Path("results/llm_judge_nli_probe_score_status_20260529.md"),
    Path("results/llm_nli_correlation_status_20260529.json"),
    Path("results/llm_nli_correlation_status_20260529.md"),
    Path("results/text_only_verifier_status_20260529.json"),
    Path("results/text_only_verifier_status_20260529.md"),
    Path("results/audit_sample_paper_1000_v3_nli_set_eval.json"),
    Path("results/audit_sample_paper_1000_v3_nli_set.jsonl"),
    Path("results/mechanism_ablation_summary_20260529.json"),
    Path("results/mechanism_ablation_summary_20260529.md"),
    Path("results/theory_formalization_status_20260529.json"),
    Path("results/theory_formalization_status_20260529.md"),
    Path("results/novelty_audit_20260529.json"),
    Path("results/novelty_audit_20260529.md"),
    Path("results/v4_strong_baseline_summary_20260529.json"),
    Path("results/v4_strong_baseline_summary_20260529.md"),
    Path("results/v4_baseline_coverage_matrix_20260529.json"),
    Path("results/v4_baseline_coverage_matrix_20260529.md"),
    Path("results/v4_baseline_budget_parity_20260529.json"),
    Path("results/v4_baseline_budget_parity_20260529.md"),
    Path("results/v4_shared_threshold_selection_20260529.json"),
    Path("results/v4_shared_threshold_selection_20260529.md"),
    Path("results/risk_control_abstention_baselines_20260529.json"),
    Path("results/risk_control_abstention_baselines_20260529.md"),
    Path("results/calibration_fever_v4_n100_structbalanced.json"),
    Path("results/calibration_hotpot_v4_hardneg_n100.json"),
    Path("results/calibration_hotpot_v4_n100_hardmatched.json"),
    Path("results/calibration_hotpot_v4_n100_structbalanced.json"),
    Path("results/calibration_hotpot_v4_semanticswap_n100.json"),
    Path("results/calibration_hotpot_v4_supportpreserve_n100.json"),
    Path("results/compare_calibrated_fever_v4_n100_structbalanced.json"),
    Path("results/compare_calibrated_hotpot_v4_hardneg_n100.json"),
    Path("results/compare_calibrated_hotpot_v4_n100_hardmatched.json"),
    Path("results/compare_calibrated_hotpot_v4_n100_structbalanced.json"),
    Path("results/compare_calibrated_hotpot_v4_semanticswap_n100.json"),
    Path("results/compare_calibrated_hotpot_v4_supportpreserve_n100.json"),
    Path("results/v4_split_threshold_protocol_20260529.json"),
    Path("results/v4_split_threshold_protocol_20260529.md"),
    Path("results/v4_calibration_quality_20260529.json"),
    Path("results/v4_calibration_quality_20260529.md"),
    Path("results/v4_claim_safe_target_selection_20260529.json"),
    Path("results/v4_claim_safe_target_selection_20260529.md"),
    Path("results/v4_anti_shortcut_summary_20260529.json"),
    Path("results/v4_anti_shortcut_summary_20260529.md"),
    Path("results/v4_failure_taxonomy_summary_20260529.json"),
    Path("results/v4_failure_taxonomy_summary_20260529.md"),
    Path("results/v4_case_gallery_summary_20260529.json"),
    Path("results/clean_sufficiency_misleading_v4_20260529.json"),
    Path("paper/case_studies/v4_case_gallery_20260529.jsonl"),
    Path("paper/case_studies/v4_case_gallery_20260529.md"),
    Path("paper/figures/clean_sufficiency_misleading_v4_20260529.csv"),
    Path("paper/figures/clean_sufficiency_misleading_v4_20260529.svg"),
    Path("paper/figures/clean_sufficiency_misleading_v4_20260529.md"),
    Path("paper/sections/formalization.tex"),
    Path("paper/sections/theory.tex"),
    Path("reproducibility/checksums.json"),
    Path("reproducibility/seeds.json"),
    Path("reproducibility/hardware.md"),
    Path("reproducibility/artifact_manifest.md"),
    Path("reproducibility/hidden_local_path_audit.json"),
    Path("reproducibility/hidden_local_path_audit.md"),
    Path("reproducibility/reproduction_commands.md"),
    Path("reproducibility/bundle_summary_20260529.json"),
    Path("scripts/run_smoke.ps1"),
    Path("scripts/run_main_tables.ps1"),
    Path(".github/workflows/ci.yml"),
    Path("annotation/README.md"),
    Path("annotation/guidelines_v4.md"),
    Path("annotation/audit_card_template.md"),
    Path("annotation/label_schema_v4.json"),
    Path("annotation/export_blind_audit_pack_v4.py"),
    Path("annotation/merge_audit_labels_v4.py"),
    Path("annotation/adjudicate_labels_v4.py"),
    Path("annotation/compute_agreement_v4.py"),
    Path("experiments/reproduce_current_evidence_v4.py"),
    Path("experiments/materialize_human_audit_v4_paper_pack.py"),
    Path("experiments/materialize_human_audit_v4_assignment_batches.py"),
    Path("experiments/collect_human_audit_v4_assignment_batches.py"),
    Path("experiments/verify_claims.py"),
    Path("experiments/build_results_provenance_readme.py"),
    Path("experiments/build_claims_ledger_markdown.py"),
    Path("experiments/build_reproducibility_bundle.py"),
    Path("experiments/summarize_evidence_closure.py"),
    Path("experiments/build_external_review_packet.py"),
    Path("experiments/summarize_neurips_readiness.py"),
    Path("experiments/summarize_neurips_unblock_plan.py"),
    Path("experiments/audit_remote_cleanup_candidates.py"),
    Path("experiments/guarded_remote_ext4_cleanup.py"),
    Path("experiments/relocate_corm_remote_plan.py"),
    Path("experiments/materialize_llm_judge_requests_v4.py"),
    Path("experiments/materialize_llm_judge_requests_nli_probe.py"),
    Path("experiments/manage_openai_llm_judge_batch.py"),
    Path("experiments/normalize_llm_judge_batch_responses.py"),
    Path("experiments/compute_llm_nli_correlation.py"),
    Path("experiments/summarize_text_only_verifier_status.py"),
    Path("experiments/run_end2end_retriever_generator_matrix_v4.py"),
    Path("experiments/plot_end2end_risk_coverage_curves.py"),
    Path("experiments/summarize_end2end_target_risk_coverage.py"),
    Path("experiments/summarize_v4_baseline_coverage.py"),
    Path("experiments/summarize_v4_calibration_quality.py"),
    Path("experiments/summarize_v4_claim_safe_target_selection.py"),
    Path("experiments/summarize_risk_control_abstention_baselines.py"),
    Path("experiments/train_csrm_calibrated_v4.py"),
    Path("experiments/compare_calibrated_vs_baselines_v4.py"),
    Path("src/csrm_rag/verifiers/__init__.py"),
    Path("src/csrm_rag/verifiers/llm_judge.py"),
    Path("experiments/summarize_v4_baseline_budget_parity.py"),
    Path("experiments/compare_equal_budget_thresholds_v4.py"),
    Path("experiments/summarize_v4_split_threshold_protocol.py"),
    Path("experiments/summarize_mechanism_ablation.py"),
    Path("experiments/summarize_theory_formalization.py"),
    Path("experiments/summarize_novelty_audit.py"),
    Path("experiments/summarize_v4_failure_taxonomy.py"),
    Path("experiments/summarize_v4_anti_shortcut.py"),
    Path("experiments/export_v4_case_gallery.py"),
    Path("experiments/build_clean_sufficiency_misleading_figure.py"),
    Path("experiments/summarize_human_audit_v4_status.py"),
    Path("experiments/summarize_human_audit_v4_disagreements.py"),
    Path("experiments/summarize_human_audit_v4_mismatch.py"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.manifest.json"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.items.jsonl"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.review.html"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.auditor1.labels.csv"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.auditor2.labels.csv"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.merged_labels.jsonl"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.adjudicated_labels.jsonl"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.adjudication_template.csv"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.agreement.json"),
    Path("results/human_audit_v4/hotpot_v4_semanticswap_n100_blind200.readiness.json"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.manifest.json"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.items.jsonl"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.review.html"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.auditor1.labels.csv"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.auditor2.labels.csv"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.merged_labels.jsonl"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.adjudicated_labels.jsonl"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.adjudication_template.csv"),
    Path("results/human_audit_v4/fever_v4_n100_structbalanced_blind100.agreement.json"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.sources.raw.jsonl"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.sources.private_eval.jsonl"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.sources.textonly_scored.jsonl"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.manifest.json"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.items.jsonl"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.review.html"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.auditor1.labels.csv"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.auditor2.labels.csv"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.merged_labels.jsonl"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.adjudicated_labels.jsonl"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.adjudication_template.csv"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.agreement.json"),
    Path("results/human_audit_v4/v4_paper1000_mixed_blind1000.readiness.json"),
    Path("results/human_audit_v4_batches/v4_paper1000_mixed_blind1000.assignment_manifest.json"),
    Path("results/human_audit_v4_collection/v4_paper1000_mixed_blind1000.merged_labels.jsonl"),
    Path("results/human_audit_v4_collection/v4_paper1000_mixed_blind1000.adjudicated_labels.jsonl"),
    Path("results/human_audit_v4_collection/v4_paper1000_mixed_blind1000.readiness.json"),
]


def verify_v4_evidence_package(root: Path, artifacts: Sequence[Path]) -> dict[str, Any]:
    artifact_rows = [_artifact_row(root / path, path) for path in artifacts]
    missing = [row["path"] for row in artifact_rows if not row["exists"]]
    closure = _load_json(root / "results/evidence_closure_status_v4.json")
    reproduction = _load_json(root / "results/current_evidence_reproduction_20260529.json")
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "artifact_count": len(artifact_rows),
        "missing_artifact_count": len(missing),
        "missing_artifacts": missing,
        "artifacts": artifact_rows,
        "gate_summary": reproduction.get("gate_summary", {}),
        "ready_for_neurips_main_claim": reproduction.get("ready_for_neurips_main_claim"),
        "claim_verification": closure.get("claim_verification", {}),
        "remaining_human_audit_blockers": closure.get("remaining_human_audit_blockers", []),
        "remaining_non_human_blockers": closure.get("remaining_non_human_blockers", []),
        "allowed_claim_count": len(closure.get("allowed_claims", [])),
        "disallowed_claim_count": len(closure.get("disallowed_claims", [])),
        "package_status": "complete_with_known_blockers" if not missing else "incomplete_missing_artifacts",
        "claim_boundary": (
            "This manifest verifies that the current evidence package is present and hashable. "
            "It does not convert pending human audit, failed storage, proxy-only end-to-end results, "
            "or negative strong-baseline evidence into NeurIPS-ready main-claim support."
        ),
    }


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# V4 Evidence Package Manifest",
        "",
        f"Generated: `{manifest['generated_at_utc']}`",
        "",
        f"Package status: `{manifest['package_status']}`",
        f"Ready for NeurIPS main claim: `{manifest['ready_for_neurips_main_claim']}`",
        f"Missing artifacts: `{manifest['missing_artifact_count']}`",
        "",
        "## Gate Summary",
        "",
    ]
    for key, value in manifest["gate_summary"].items():
        lines.append(f"- {key}: `{value}`")

    claims = manifest["claim_verification"]
    lines.extend(
        [
            "",
            "## Claim Verification",
            "",
            f"- Passed: `{claims.get('passed_claims')}/{claims.get('total_claims')}`.",
            f"- Failed: `{claims.get('failed_claims')}`.",
            f"- Allowed/disallowed claim counts: `{manifest['allowed_claim_count']}` / `{manifest['disallowed_claim_count']}`.",
            "",
            "## Artifacts",
            "",
            "| Path | Exists | Bytes | SHA256 |",
            "|---|---:|---:|---|",
        ]
    )
    for row in manifest["artifacts"]:
        lines.append(
            f"| `{row['path']}` | `{row['exists']}` | `{row['size_bytes']}` | `{row['sha256']}` |"
        )

    lines.extend(["", "## Remaining Human-Audit Blockers", ""])
    lines.extend(f"- {item}" for item in manifest["remaining_human_audit_blockers"])
    lines.extend(["", "## Remaining Non-Human Blockers", ""])
    lines.extend(f"- {item}" for item in manifest["remaining_non_human_blockers"])
    lines.extend(["", "## Claim Boundary", "", manifest["claim_boundary"], ""])
    return "\n".join(lines)


def _artifact_row(path: Path, display_path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(display_path),
            "exists": False,
            "size_bytes": None,
            "sha256": None,
        }
    return {
        "path": str(display_path),
        "exists": True,
        "size_bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, nargs="+", default=DEFAULT_ARTIFACTS)
    args = parser.parse_args()

    manifest = verify_v4_evidence_package(args.root, args.artifacts)
    _write_json(args.output_json, manifest)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(manifest), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
