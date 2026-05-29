# Results Provenance

Generated: `2026-05-29T06:22:57.081768+00:00`

Ready for NeurIPS main-track claim: `False`.

This package is complete only as a current-evidence snapshot with known blockers; it is not a NeurIPS main-track-ready evidence closure.

## Source Reports

- current_evidence_reproduction: `results\current_evidence_reproduction_20260529.json`
- v4_evidence_package_manifest: `results\v4_evidence_package_manifest_20260529.json`
- neurips_readiness_matrix: `results\neurips_readiness_matrix_20260529.json`

## Step Provenance

| Step | Ready | Source script | Outputs |
|---|---:|---|---|
| summarize_human_audit_v4_status | `False` | `experiments/summarize_human_audit_v4_status.py` | `results/human_audit_v4_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`9382df70b54b`)<br>`results/human_audit_v4_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`f88c4716924c`) |
| summarize_human_audit_v4_disagreements | `True` | `experiments/summarize_human_audit_v4_disagreements.py` | `results/human_audit_v4_disagreement_taxonomy_20260529.json` (exists=`True`, tracked=`True`, sha256=`4bd730559c17`)<br>`results/human_audit_v4_disagreement_taxonomy_20260529.md` (exists=`True`, tracked=`True`, sha256=`3846043b4555`) |
| summarize_human_audit_v4_mismatch | `True` | `experiments/summarize_human_audit_v4_mismatch.py` | `results/human_audit_v4_mismatch_20260529.json` (exists=`True`, tracked=`True`, sha256=`3382f45f2441`)<br>`results/human_audit_v4_mismatch_20260529.md` (exists=`True`, tracked=`True`, sha256=`715cbb880435`) |
| run_human_audit_eval_v4 | `False` | `experiments/run_human_audit_eval_v4.py` | `results/human_audit_v4_eval_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`3703442aa638`)<br>`results/human_audit_v4_eval_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`631763b47c09`) |
| summarize_fever_cp_transfer_sweep | `False` | `experiments/summarize_fever_cp_transfer_sweep.py` | `results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`11a8d2f93cec`)<br>`results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`520b79abb99e`) |
| summarize_end2end_selective_rag_proxy | `False` | `experiments/summarize_end2end_selective_rag_proxy.py` | `results/end2end_selective_rag_proxy_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`08174414f74a`)<br>`results/end2end_selective_rag_proxy_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`74c721a1f30e`) |
| run_end2end_retriever_generator_matrix_v4 | `False` | `experiments/run_end2end_retriever_generator_matrix_v4.py` | `results/end2end_retriever_generator_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`d917416f107d`)<br>`results/end2end_retriever_generator_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`0ae6b67586db`) |
| plot_end2end_risk_coverage_curves | `True` | `experiments/plot_end2end_risk_coverage_curves.py` | `results/end2end_risk_coverage_curves_20260529.json` (exists=`True`, tracked=`True`, sha256=`be420a5a4b83`)<br>`results/end2end_risk_coverage_curves_20260529.md` (exists=`True`, tracked=`True`, sha256=`aac5f54d05da`)<br>`paper/figures/end2end_risk_coverage_curves_20260529.svg` (exists=`True`, tracked=`True`, sha256=`e24141090458`) |
| summarize_end2end_target_risk_coverage | `True` | `experiments/summarize_end2end_target_risk_coverage.py` | `results/end2end_target_risk_coverage_20260529.json` (exists=`True`, tracked=`True`, sha256=`2c5576db5c61`)<br>`results/end2end_target_risk_coverage_20260529.md` (exists=`True`, tracked=`True`, sha256=`0e3fde3a30d1`) |
| materialize_llm_judge_requests_v4 | `False` | `experiments/materialize_llm_judge_requests_v4.py` | `results/llm_judge_v4_requests_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`7863764d362f`)<br>`results/llm_judge_v4_request_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`ae97cb94f01b`)<br>`results/llm_judge_v4_request_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`2eb8c9f90d46`) |
| materialize_llm_judge_requests_nli_probe | `False` | `experiments/materialize_llm_judge_requests_nli_probe.py` | `results/llm_judge_nli_probe_requests_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`74ed598cbdcf`)<br>`results/llm_judge_nli_probe_request_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`f651cb1753c4`)<br>`results/llm_judge_nli_probe_request_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`2db4b535640f`) |
| manage_openai_llm_judge_batch_preflight | `False` | `experiments/manage_openai_llm_judge_batch.py` | `results/llm_judge_nli_probe_batch_run_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`d64fb64778c9`)<br>`results/llm_judge_nli_probe_batch_run_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`37a63fc46f8f`) |
| normalize_llm_judge_batch_responses | `False` | `experiments/normalize_llm_judge_batch_responses.py` | `results/llm_judge_nli_probe_score_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`9d8421eebd9f`)<br>`results/llm_judge_nli_probe_score_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`5a7865520d6a`) |
| compute_llm_nli_correlation | `False` | `experiments/compute_llm_nli_correlation.py` | `results/llm_nli_correlation_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`84e48e723b96`)<br>`results/llm_nli_correlation_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`245c1aae3d81`) |
| summarize_text_only_verifier_status | `False` | `experiments/summarize_text_only_verifier_status.py` | `results/text_only_verifier_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`af14a12ac7b3`)<br>`results/text_only_verifier_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`6c279c9bcf83`) |
| summarize_v4_strong_baselines | `False` | `experiments/summarize_v4_strong_baselines.py` | `results/v4_strong_baseline_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`e8c61f4e7870`)<br>`results/v4_strong_baseline_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`7c302aae0a15`) |
| summarize_v4_baseline_coverage | `False` | `experiments/summarize_v4_baseline_coverage.py` | `results/v4_baseline_coverage_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`9f6d33d80c3f`)<br>`results/v4_baseline_coverage_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`2c98f387483b`) |
| summarize_v4_baseline_budget_parity | `False` | `experiments/summarize_v4_baseline_budget_parity.py` | `results/v4_baseline_budget_parity_20260529.json` (exists=`True`, tracked=`True`, sha256=`d367e39b3c29`)<br>`results/v4_baseline_budget_parity_20260529.md` (exists=`True`, tracked=`True`, sha256=`8899fc5ed627`) |
| compare_equal_budget_thresholds_v4 | `True` | `experiments/compare_equal_budget_thresholds_v4.py` | `results/v4_shared_threshold_selection_20260529.json` (exists=`True`, tracked=`True`, sha256=`9f4e1510adef`)<br>`results/v4_shared_threshold_selection_20260529.md` (exists=`True`, tracked=`True`, sha256=`021bcbf7c9de`) |
| summarize_v4_split_threshold_protocol | `True` | `experiments/summarize_v4_split_threshold_protocol.py` | `results/v4_split_threshold_protocol_20260529.json` (exists=`True`, tracked=`True`, sha256=`5fe1e80ad629`)<br>`results/v4_split_threshold_protocol_20260529.md` (exists=`True`, tracked=`True`, sha256=`099838da2358`) |
| summarize_risk_control_abstention_baselines | `True` | `experiments/summarize_risk_control_abstention_baselines.py` | `results/risk_control_abstention_baselines_20260529.json` (exists=`True`, tracked=`True`, sha256=`e0f246f12e8f`)<br>`results/risk_control_abstention_baselines_20260529.md` (exists=`True`, tracked=`True`, sha256=`9cc38787e1eb`) |
| summarize_v4_calibration_quality | `False` | `experiments/summarize_v4_calibration_quality.py` | `results/v4_calibration_quality_20260529.json` (exists=`True`, tracked=`True`, sha256=`e6f7a0d4040a`)<br>`results/v4_calibration_quality_20260529.md` (exists=`True`, tracked=`True`, sha256=`59915a0e3856`) |
| summarize_v4_failure_taxonomy | `True` | `experiments/summarize_v4_failure_taxonomy.py` | `results/v4_failure_taxonomy_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`e13514910223`)<br>`results/v4_failure_taxonomy_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`aa340ed25212`) |
| export_v4_case_gallery | `True` | `experiments/export_v4_case_gallery.py` | `paper/case_studies/v4_case_gallery_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`f03232de577d`)<br>`paper/case_studies/v4_case_gallery_20260529.md` (exists=`True`, tracked=`True`, sha256=`c16142e76014`)<br>`results/v4_case_gallery_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`8a5567d0bf35`) |
| build_clean_sufficiency_misleading_figure | `True` | `experiments/build_clean_sufficiency_misleading_figure.py` | `paper/figures/clean_sufficiency_misleading_v4_20260529.csv` (exists=`True`, tracked=`True`, sha256=`ded3232932e8`)<br>`results/clean_sufficiency_misleading_v4_20260529.json` (exists=`True`, tracked=`True`, sha256=`1d35c5693090`)<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.svg` (exists=`True`, tracked=`True`, sha256=`a354e94977a8`)<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.md` (exists=`True`, tracked=`True`, sha256=`a3b248aa6c93`) |
| summarize_v4_anti_shortcut | `True` | `experiments/summarize_v4_anti_shortcut.py` | `results/v4_anti_shortcut_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`6deaf920972c`)<br>`results/v4_anti_shortcut_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`492438cc842e`) |
| summarize_mechanism_ablation | `True` | `experiments/summarize_mechanism_ablation.py` | `results/mechanism_ablation_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`ca0d49b37338`)<br>`results/mechanism_ablation_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`20d71e99ae95`) |
| summarize_theory_formalization | `True` | `experiments/summarize_theory_formalization.py` | `results/theory_formalization_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`4f0113b01597`)<br>`results/theory_formalization_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`bdd404d9f260`) |
| verify_claims | `True` | `experiments/verify_claims.py` | `results/claims_verification.json` (exists=`True`, tracked=`True`, sha256=`b3051aff04cf`) |
| summarize_evidence_closure | `False` | `experiments/summarize_evidence_closure.py` | `results/evidence_closure_status_v4.json` (exists=`True`, tracked=`True`, sha256=`b12f4dcace57`)<br>`results/evidence_closure_status_v4.md` (exists=`True`, tracked=`True`, sha256=`df24be5db93e`) |
| build_external_review_packet | `False` | `experiments/build_external_review_packet.py` | `results/external_review_packet_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`4473d383d461`)<br>`results/external_review_packet_20260529.md` (exists=`True`, tracked=`True`, sha256=`9ceda8647a47`) |
| summarize_neurips_readiness | `False` | `experiments/summarize_neurips_readiness.py` | `results/neurips_readiness_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`8cb2c377cef7`)<br>`results/neurips_readiness_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`d5fa63b64a12`) |
| build_results_provenance_readme | `True` | `experiments/build_results_provenance_readme.py` | `results/results_provenance_manifest_20260529.json` (exists=`True`, tracked=`True`, sha256=`15e1ed8fda2e`)<br>`results/README.md` (exists=`True`, tracked=`True`, sha256=`5dec70742358`) |
| build_claims_ledger_markdown | `True` | `experiments/build_claims_ledger_markdown.py` | `CLAIMS_LEDGER.md` (exists=`True`, tracked=`True`, sha256=`23eab1a243be`)<br>`results/claims_ledger_markdown_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`3646ab885cb2`) |
| build_reproducibility_bundle | `True` | `experiments/build_reproducibility_bundle.py` | `reproducibility/checksums.json` (exists=`True`, tracked=`True`, sha256=`82d6b9bbf659`)<br>`reproducibility/seeds.json` (exists=`True`, tracked=`True`, sha256=`e16552f0c023`)<br>`reproducibility/hardware.md` (exists=`True`, tracked=`True`, sha256=`c5c80a0b41b9`)<br>`reproducibility/artifact_manifest.md` (exists=`True`, tracked=`True`, sha256=`f805a718c869`)<br>`reproducibility/hidden_local_path_audit.json` (exists=`True`, tracked=`True`, sha256=`482e144b56e8`)<br>`reproducibility/hidden_local_path_audit.md` (exists=`True`, tracked=`True`, sha256=`b686eedb01c3`)<br>`reproducibility/reproduction_commands.md` (exists=`True`, tracked=`True`, sha256=`3f3f3099efd9`)<br>`reproducibility/bundle_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`eba1650ddc82`) |

## Reproduce Current Package

```bash
python -m experiments.reproduce_current_evidence_v4 --output-json results/current_evidence_reproduction_20260529.json --output-md results/current_evidence_reproduction_20260529.md
python -m experiments.verify_v4_evidence_package --output-json results/v4_evidence_package_manifest_20260529.json --output-md results/v4_evidence_package_manifest_20260529.md
python -m experiments.build_results_provenance_readme --output-json results/results_provenance_manifest_20260529.json --output-md results/README.md
```

## Artifact Status

- Evidence manifest artifact count: `166`.
- Evidence manifest missing artifacts: `0`.
- Missing current-step outputs: `0`.
- Current-step outputs not listed in evidence manifest: `0`.
- Readiness status counts: `{'blocked': 3, 'fail': 1, 'partial': 4, 'pass': 5}`.

## Known Blockers

Human audit:
- Human audit v4 packs are prepared for Hotpot semantic-swap blind200 and FEVER structbalanced blind100, but adjudicated labels are pending for all 300 items.

Non-human:
- Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts; an ext4 cleanup path exists but needs explicit approval before deleting logs/caches.
- FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.
- External review packet is ready, but independent review remains pending; place the response at results\external_review_response_20260529.md.
- End-to-end selective RAG evidence is currently proxy-only: fixed-coverage and fixed-risk views are directionally positive, but some Hotpot v4 variants remain mixed and this is not a full CoRM-RAG reproduction.
- V4 strong baselines are present, but CSRM-Rule loses or ties the strongest learned/context baselines; main claims must use calibrated/proxy wording with caveats.
- V4 calibrated orbit risk improves Brier on all current calibration artifacts, but ECE is mixed, so calibration remains partial evidence rather than a closed formal-risk claim.

Readiness matrix hard blockers:
- Human-audited orbit labels (`blocked`): Pending labels: 300; cannot claim human-audited results.
- Full CoRM-RAG reproduction (`blocked`): Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts. Latest storage probe shows 322.1 GiB available and target_write_probe_passed=False; 6 target-dir file probes failed while writable fallback dirs are ['/home/syk', '/tmp', '/dev/shm'].
- Independent external review (`blocked`): External review packet is ready, but no independent review response is present; place the response at `results\external_review_response_20260529.md`.

## Claim Boundary

This README records artifact provenance for the current evidence package. It does not complete pending human audit labels, full CoRM-RAG reproduction, or unsupported formal/general risk-control claims.
