# Results Provenance

Generated: `2026-05-29T07:52:24.232321+00:00`

Ready for NeurIPS main-track claim: `False`.

This package is complete only as a current-evidence snapshot with known blockers; it is not a NeurIPS main-track-ready evidence closure.

## Source Reports

- current_evidence_reproduction: `results\current_evidence_reproduction_20260529.json`
- v4_evidence_package_manifest: `results\v4_evidence_package_manifest_20260529.json`
- neurips_readiness_matrix: `results\neurips_readiness_matrix_20260529.json`

## Step Provenance

| Step | Ready | Source script | Outputs |
|---|---:|---|---|
| materialize_human_audit_v4_paper_pack | `True` | `experiments/materialize_human_audit_v4_paper_pack.py` | `results/human_audit_v4_paper_pack_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`a178f167f64d`)<br>`results/human_audit_v4_paper_pack_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`3754f0427102`) |
| materialize_human_audit_v4_assignment_batches | `True` | `experiments/materialize_human_audit_v4_assignment_batches.py` | `results/human_audit_v4_assignment_batches_20260529.json` (exists=`True`, tracked=`True`, sha256=`6e73084ecd03`)<br>`results/human_audit_v4_assignment_batches_20260529.md` (exists=`True`, tracked=`True`, sha256=`ca2a095a9b54`)<br>`results/human_audit_v4_batches/v4_paper1000_mixed_blind1000.assignment_manifest.json` (exists=`True`, tracked=`True`, sha256=`76828b27a7cc`) |
| collect_human_audit_v4_assignment_batches | `False` | `experiments/collect_human_audit_v4_assignment_batches.py` | `results/human_audit_v4_batch_collection_20260529.json` (exists=`True`, tracked=`True`, sha256=`5fcc4d03f8a1`)<br>`results/human_audit_v4_batch_collection_20260529.md` (exists=`True`, tracked=`True`, sha256=`ebb8c5615ee5`)<br>`results/human_audit_v4_collection/v4_paper1000_mixed_blind1000.merged_labels.jsonl` (exists=`True`, tracked=`True`, sha256=`01a893122d46`)<br>`results/human_audit_v4_collection/v4_paper1000_mixed_blind1000.adjudicated_labels.jsonl` (exists=`True`, tracked=`True`, sha256=`6dab172b0c15`)<br>`results/human_audit_v4_collection/v4_paper1000_mixed_blind1000.readiness.json` (exists=`True`, tracked=`True`, sha256=`e9e7b4d14b81`) |
| summarize_human_audit_v4_status | `False` | `experiments/summarize_human_audit_v4_status.py` | `results/human_audit_v4_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`6c1147bdc32e`)<br>`results/human_audit_v4_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`7336e42957bb`) |
| summarize_human_audit_v4_disagreements | `True` | `experiments/summarize_human_audit_v4_disagreements.py` | `results/human_audit_v4_disagreement_taxonomy_20260529.json` (exists=`True`, tracked=`True`, sha256=`0ee3f3e91d75`)<br>`results/human_audit_v4_disagreement_taxonomy_20260529.md` (exists=`True`, tracked=`True`, sha256=`bbae4d358c93`) |
| summarize_human_audit_v4_mismatch | `True` | `experiments/summarize_human_audit_v4_mismatch.py` | `results/human_audit_v4_mismatch_20260529.json` (exists=`True`, tracked=`True`, sha256=`fcf134a8a7f3`)<br>`results/human_audit_v4_mismatch_20260529.md` (exists=`True`, tracked=`True`, sha256=`d345a1eeee8f`) |
| run_human_audit_eval_v4 | `False` | `experiments/run_human_audit_eval_v4.py` | `results/human_audit_v4_eval_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`c33cbaf7461e`)<br>`results/human_audit_v4_eval_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`51303ec57d86`) |
| summarize_fever_cp_transfer_sweep | `False` | `experiments/summarize_fever_cp_transfer_sweep.py` | `results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`0701a545fd94`)<br>`results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`fcc8413731dc`) |
| summarize_end2end_selective_rag_proxy | `False` | `experiments/summarize_end2end_selective_rag_proxy.py` | `results/end2end_selective_rag_proxy_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`4fb33ecc2e37`)<br>`results/end2end_selective_rag_proxy_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`a246310db04a`) |
| run_end2end_retriever_generator_matrix_v4 | `False` | `experiments/run_end2end_retriever_generator_matrix_v4.py` | `results/end2end_retriever_generator_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`d09bf3fbc06b`)<br>`results/end2end_retriever_generator_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`76b0432e7ffd`) |
| plot_end2end_risk_coverage_curves | `True` | `experiments/plot_end2end_risk_coverage_curves.py` | `results/end2end_risk_coverage_curves_20260529.json` (exists=`True`, tracked=`True`, sha256=`6d288e6e97e8`)<br>`results/end2end_risk_coverage_curves_20260529.md` (exists=`True`, tracked=`True`, sha256=`d4de7bf65ac4`)<br>`paper/figures/end2end_risk_coverage_curves_20260529.svg` (exists=`True`, tracked=`True`, sha256=`e24141090458`) |
| summarize_end2end_target_risk_coverage | `True` | `experiments/summarize_end2end_target_risk_coverage.py` | `results/end2end_target_risk_coverage_20260529.json` (exists=`True`, tracked=`True`, sha256=`c11ea3d86999`)<br>`results/end2end_target_risk_coverage_20260529.md` (exists=`True`, tracked=`True`, sha256=`c87c50481fdd`) |
| materialize_llm_judge_requests_v4 | `False` | `experiments/materialize_llm_judge_requests_v4.py` | `results/llm_judge_v4_requests_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`7863764d362f`)<br>`results/llm_judge_v4_request_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`9aa9318de478`)<br>`results/llm_judge_v4_request_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`c6930587d1d7`) |
| materialize_llm_judge_requests_nli_probe | `False` | `experiments/materialize_llm_judge_requests_nli_probe.py` | `results/llm_judge_nli_probe_requests_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`74ed598cbdcf`)<br>`results/llm_judge_nli_probe_request_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`ddd15ae7ccf8`)<br>`results/llm_judge_nli_probe_request_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`a394b24b47c8`) |
| manage_openai_llm_judge_batch_preflight | `False` | `experiments/manage_openai_llm_judge_batch.py` | `results/llm_judge_nli_probe_batch_run_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`6a234cc4a73d`)<br>`results/llm_judge_nli_probe_batch_run_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`b421c3f581a5`) |
| normalize_llm_judge_batch_responses | `False` | `experiments/normalize_llm_judge_batch_responses.py` | `results/llm_judge_nli_probe_score_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`c19a699dec39`)<br>`results/llm_judge_nli_probe_score_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`30e89f72ee52`) |
| compute_llm_nli_correlation | `False` | `experiments/compute_llm_nli_correlation.py` | `results/llm_nli_correlation_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`f0c7110500cc`)<br>`results/llm_nli_correlation_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`3f5c4a8d63e3`) |
| summarize_text_only_verifier_status | `False` | `experiments/summarize_text_only_verifier_status.py` | `results/text_only_verifier_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`635d4006e51f`)<br>`results/text_only_verifier_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`c2cf85912cfa`) |
| summarize_v4_strong_baselines | `False` | `experiments/summarize_v4_strong_baselines.py` | `results/v4_strong_baseline_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`fc21c48e1787`)<br>`results/v4_strong_baseline_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`581565e3da84`) |
| summarize_v4_baseline_coverage | `False` | `experiments/summarize_v4_baseline_coverage.py` | `results/v4_baseline_coverage_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`3da90cc4f946`)<br>`results/v4_baseline_coverage_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`ee3972502db1`) |
| summarize_v4_baseline_budget_parity | `False` | `experiments/summarize_v4_baseline_budget_parity.py` | `results/v4_baseline_budget_parity_20260529.json` (exists=`True`, tracked=`True`, sha256=`f311d8503527`)<br>`results/v4_baseline_budget_parity_20260529.md` (exists=`True`, tracked=`True`, sha256=`840c25b03b51`) |
| compare_equal_budget_thresholds_v4 | `True` | `experiments/compare_equal_budget_thresholds_v4.py` | `results/v4_shared_threshold_selection_20260529.json` (exists=`True`, tracked=`True`, sha256=`98390eaed1b3`)<br>`results/v4_shared_threshold_selection_20260529.md` (exists=`True`, tracked=`True`, sha256=`72bc691beba4`) |
| summarize_v4_split_threshold_protocol | `True` | `experiments/summarize_v4_split_threshold_protocol.py` | `results/v4_split_threshold_protocol_20260529.json` (exists=`True`, tracked=`True`, sha256=`4cfbac7cccd4`)<br>`results/v4_split_threshold_protocol_20260529.md` (exists=`True`, tracked=`True`, sha256=`134605c4f412`) |
| summarize_risk_control_abstention_baselines | `True` | `experiments/summarize_risk_control_abstention_baselines.py` | `results/risk_control_abstention_baselines_20260529.json` (exists=`True`, tracked=`True`, sha256=`108f2625b985`)<br>`results/risk_control_abstention_baselines_20260529.md` (exists=`True`, tracked=`True`, sha256=`0e0404aee3f5`) |
| summarize_v4_calibration_quality | `False` | `experiments/summarize_v4_calibration_quality.py` | `results/v4_calibration_quality_20260529.json` (exists=`True`, tracked=`True`, sha256=`efdc82ec6d8d`)<br>`results/v4_calibration_quality_20260529.md` (exists=`True`, tracked=`True`, sha256=`a68f2692a075`) |
| summarize_v4_claim_safe_target_selection | `False` | `experiments/summarize_v4_claim_safe_target_selection.py` | `results/v4_claim_safe_target_selection_20260529.json` (exists=`True`, tracked=`True`, sha256=`7c828c77d345`)<br>`results/v4_claim_safe_target_selection_20260529.md` (exists=`True`, tracked=`True`, sha256=`63a2c89caa23`) |
| summarize_v4_failure_taxonomy | `True` | `experiments/summarize_v4_failure_taxonomy.py` | `results/v4_failure_taxonomy_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`62b3e09138f0`)<br>`results/v4_failure_taxonomy_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`5fd95585f557`) |
| export_v4_case_gallery | `True` | `experiments/export_v4_case_gallery.py` | `paper/case_studies/v4_case_gallery_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`f03232de577d`)<br>`paper/case_studies/v4_case_gallery_20260529.md` (exists=`True`, tracked=`True`, sha256=`56f51823f907`)<br>`results/v4_case_gallery_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`7d1b230773c6`) |
| build_clean_sufficiency_misleading_figure | `True` | `experiments/build_clean_sufficiency_misleading_figure.py` | `paper/figures/clean_sufficiency_misleading_v4_20260529.csv` (exists=`True`, tracked=`True`, sha256=`ded3232932e8`)<br>`results/clean_sufficiency_misleading_v4_20260529.json` (exists=`True`, tracked=`True`, sha256=`3b16d332f426`)<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.svg` (exists=`True`, tracked=`True`, sha256=`a354e94977a8`)<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.md` (exists=`True`, tracked=`True`, sha256=`2cdf334f04b4`) |
| summarize_v4_anti_shortcut | `True` | `experiments/summarize_v4_anti_shortcut.py` | `results/v4_anti_shortcut_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`12e2ad69d79e`)<br>`results/v4_anti_shortcut_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`5916b85abb1d`) |
| summarize_mechanism_ablation | `True` | `experiments/summarize_mechanism_ablation.py` | `results/mechanism_ablation_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`458fce6630cf`)<br>`results/mechanism_ablation_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`9877f535a0ca`) |
| summarize_theory_formalization | `True` | `experiments/summarize_theory_formalization.py` | `results/theory_formalization_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`c941c4283585`)<br>`results/theory_formalization_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`2111665e86f8`) |
| summarize_novelty_audit | `True` | `experiments/summarize_novelty_audit.py` | `results/novelty_audit_20260529.json` (exists=`True`, tracked=`True`, sha256=`e7af4d4605c9`)<br>`results/novelty_audit_20260529.md` (exists=`True`, tracked=`True`, sha256=`e1fa1c5a2ad3`) |
| verify_claims | `True` | `experiments/verify_claims.py` | `results/claims_verification.json` (exists=`True`, tracked=`True`, sha256=`b3051aff04cf`) |
| summarize_evidence_closure | `False` | `experiments/summarize_evidence_closure.py` | `results/evidence_closure_status_v4.json` (exists=`True`, tracked=`True`, sha256=`98dfd6394edb`)<br>`results/evidence_closure_status_v4.md` (exists=`True`, tracked=`True`, sha256=`c6043a9c38e2`) |
| build_external_review_packet | `False` | `experiments/build_external_review_packet.py` | `results/external_review_packet_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`a18d5148cbce`)<br>`results/external_review_packet_20260529.md` (exists=`True`, tracked=`True`, sha256=`695343e8c53f`) |
| summarize_neurips_readiness | `False` | `experiments/summarize_neurips_readiness.py` | `results/neurips_readiness_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`bba994c53575`)<br>`results/neurips_readiness_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`2e58a6372f19`) |
| summarize_neurips_unblock_plan | `False` | `experiments/summarize_neurips_unblock_plan.py` | `results/neurips_unblock_plan_20260529.json` (exists=`True`, tracked=`True`, sha256=`937912ed936f`)<br>`results/neurips_unblock_plan_20260529.md` (exists=`True`, tracked=`True`, sha256=`65d683df8fbb`) |
| build_results_provenance_readme | `True` | `experiments/build_results_provenance_readme.py` | `results/results_provenance_manifest_20260529.json` (exists=`True`, tracked=`True`, sha256=`11c201a691cf`)<br>`results/README.md` (exists=`True`, tracked=`True`, sha256=`51694a062ac3`) |
| build_claims_ledger_markdown | `True` | `experiments/build_claims_ledger_markdown.py` | `CLAIMS_LEDGER.md` (exists=`True`, tracked=`True`, sha256=`88bc47d43cdb`)<br>`results/claims_ledger_markdown_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`0853cb3cc505`) |
| build_reproducibility_bundle | `True` | `experiments/build_reproducibility_bundle.py` | `reproducibility/checksums.json` (exists=`True`, tracked=`True`, sha256=`4c26e31d3171`)<br>`reproducibility/seeds.json` (exists=`True`, tracked=`True`, sha256=`6b98db901cf4`)<br>`reproducibility/hardware.md` (exists=`True`, tracked=`True`, sha256=`63aab60e5813`)<br>`reproducibility/artifact_manifest.md` (exists=`True`, tracked=`True`, sha256=`b51f542e992c`)<br>`reproducibility/hidden_local_path_audit.json` (exists=`True`, tracked=`True`, sha256=`79461df3ee34`)<br>`reproducibility/hidden_local_path_audit.md` (exists=`True`, tracked=`True`, sha256=`392ac67854b3`)<br>`reproducibility/reproduction_commands.md` (exists=`True`, tracked=`True`, sha256=`b48d193a931d`)<br>`reproducibility/bundle_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`379d7fde4768`) |

## Reproduce Current Package

```bash
python -m experiments.reproduce_current_evidence_v4 --output-json results/current_evidence_reproduction_20260529.json --output-md results/current_evidence_reproduction_20260529.md
python -m experiments.verify_v4_evidence_package --output-json results/v4_evidence_package_manifest_20260529.json --output-md results/v4_evidence_package_manifest_20260529.md
python -m experiments.build_results_provenance_readme --output-json results/results_provenance_manifest_20260529.json --output-md results/README.md
```

## Artifact Status

- Evidence manifest artifact count: `206`.
- Evidence manifest missing artifacts: `0`.
- Missing current-step outputs: `0`.
- Current-step outputs not listed in evidence manifest: `0`.
- Readiness status counts: `{'blocked': 3, 'fail': 1, 'partial': 5, 'pass': 5}`.

## Known Blockers

Human audit:
- Human audit v4 packs are prepared, including the paper-grade mixed blind1000 pack, but adjudicated labels are pending for all 1300 items.

Non-human:
- Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts; an ext4 cleanup path exists but needs explicit approval before deleting logs/caches.
- FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.
- External review packet is ready, but independent review remains pending; place the response at results\external_review_response_20260529.md.
- End-to-end selective RAG evidence is currently proxy-only: fixed-coverage and fixed-risk views are directionally positive, but some Hotpot v4 variants remain mixed and this is not a full CoRM-RAG reproduction.
- V4 strong baselines are present, but CSRM-Rule loses or ties the strongest learned/context baselines; main claims must use calibrated/proxy wording with caveats.
- Claim-safe target selection recommends csrm_calibrated_gbdt only with caveats; all-win support is False, and blockers remain: LLM-as-judge baseline is still missing.; Faithful/full CoRM-RAG baseline remains partial until full reproduction is complete.; Human audit labels are incomplete: pending auditor labels=2000, pending adjudicated labels=1000.; Text-only verifier main claim is blocked by missing LLM correlation and human labels.
- V4 calibrated orbit risk improves Brier on all current calibration artifacts, but ECE is mixed, so calibration remains partial evidence rather than a closed formal-risk claim.
- Novelty positioning remains proceed-with-caution because closely related 2025-2026 work exists; strong novelty claims require narrower wording and completed human-audit/baseline evidence.

Readiness matrix hard blockers:
- Human-audited orbit labels (`blocked`): Assignment batches ready: True; batch collection complete: False; pending labels: 1300; cannot claim human-audited results.
- Full CoRM-RAG reproduction (`blocked`): Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts. Latest storage probe shows 322.1 GiB available and target_write_probe_passed=False; 6 target-dir file probes failed while writable fallback dirs are ['/home/syk', '/tmp', '/dev/shm'].
- Independent external review (`blocked`): External review packet is ready, but no independent review response is present; place the response at `results\external_review_response_20260529.md`.

## Claim Boundary

This README records artifact provenance for the current evidence package. It does not complete pending human audit labels, full CoRM-RAG reproduction, or unsupported formal/general risk-control claims.
