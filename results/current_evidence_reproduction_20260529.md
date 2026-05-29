# Current Evidence V4 Reproduction

Generated: `2026-05-29T06:12:34.703851+00:00`

Ready for NeurIPS main claim: `False`

## Commands

| Step | Ready | Outputs |
|---|---|---|
| summarize_human_audit_v4_status | `False` | `results\human_audit_v4_status_20260529.json`<br>`results\human_audit_v4_status_20260529.md` |
| summarize_human_audit_v4_disagreements | `True` | `results\human_audit_v4_disagreement_taxonomy_20260529.json`<br>`results\human_audit_v4_disagreement_taxonomy_20260529.md` |
| summarize_human_audit_v4_mismatch | `True` | `results\human_audit_v4_mismatch_20260529.json`<br>`results\human_audit_v4_mismatch_20260529.md` |
| run_human_audit_eval_v4 | `False` | `results\human_audit_v4_eval_status_20260529.json`<br>`results\human_audit_v4_eval_status_20260529.md` |
| summarize_fever_cp_transfer_sweep | `False` | `results\fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json`<br>`results\fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.md` |
| summarize_end2end_selective_rag_proxy | `False` | `results\end2end_selective_rag_proxy_summary_20260529.json`<br>`results\end2end_selective_rag_proxy_summary_20260529.md` |
| run_end2end_retriever_generator_matrix_v4 | `False` | `results\end2end_retriever_generator_matrix_20260529.json`<br>`results\end2end_retriever_generator_matrix_20260529.md` |
| plot_end2end_risk_coverage_curves | `True` | `results\end2end_risk_coverage_curves_20260529.json`<br>`results\end2end_risk_coverage_curves_20260529.md`<br>`paper\figures\end2end_risk_coverage_curves_20260529.svg` |
| summarize_end2end_target_risk_coverage | `True` | `results\end2end_target_risk_coverage_20260529.json`<br>`results\end2end_target_risk_coverage_20260529.md` |
| materialize_llm_judge_requests_v4 | `False` | `results\llm_judge_v4_requests_20260529.jsonl`<br>`results\llm_judge_v4_request_status_20260529.json`<br>`results\llm_judge_v4_request_status_20260529.md` |
| materialize_llm_judge_requests_nli_probe | `False` | `results\llm_judge_nli_probe_requests_20260529.jsonl`<br>`results\llm_judge_nli_probe_request_status_20260529.json`<br>`results\llm_judge_nli_probe_request_status_20260529.md` |
| manage_openai_llm_judge_batch_preflight | `False` | `results\llm_judge_nli_probe_batch_run_status_20260529.json`<br>`results\llm_judge_nli_probe_batch_run_status_20260529.md` |
| normalize_llm_judge_batch_responses | `False` | `results\llm_judge_nli_probe_score_status_20260529.json`<br>`results\llm_judge_nli_probe_score_status_20260529.md` |
| compute_llm_nli_correlation | `False` | `results\llm_nli_correlation_status_20260529.json`<br>`results\llm_nli_correlation_status_20260529.md` |
| summarize_text_only_verifier_status | `False` | `results\text_only_verifier_status_20260529.json`<br>`results\text_only_verifier_status_20260529.md` |
| summarize_v4_strong_baselines | `False` | `results\v4_strong_baseline_summary_20260529.json`<br>`results\v4_strong_baseline_summary_20260529.md` |
| summarize_v4_baseline_coverage | `False` | `results\v4_baseline_coverage_matrix_20260529.json`<br>`results\v4_baseline_coverage_matrix_20260529.md` |
| summarize_v4_baseline_budget_parity | `False` | `results\v4_baseline_budget_parity_20260529.json`<br>`results\v4_baseline_budget_parity_20260529.md` |
| compare_equal_budget_thresholds_v4 | `True` | `results\v4_shared_threshold_selection_20260529.json`<br>`results\v4_shared_threshold_selection_20260529.md` |
| summarize_v4_split_threshold_protocol | `True` | `results\v4_split_threshold_protocol_20260529.json`<br>`results\v4_split_threshold_protocol_20260529.md` |
| summarize_risk_control_abstention_baselines | `True` | `results\risk_control_abstention_baselines_20260529.json`<br>`results\risk_control_abstention_baselines_20260529.md` |
| summarize_v4_calibration_quality | `False` | `results\v4_calibration_quality_20260529.json`<br>`results\v4_calibration_quality_20260529.md` |
| summarize_v4_failure_taxonomy | `True` | `results\v4_failure_taxonomy_summary_20260529.json`<br>`results\v4_failure_taxonomy_summary_20260529.md` |
| export_v4_case_gallery | `True` | `paper\case_studies\v4_case_gallery_20260529.jsonl`<br>`paper\case_studies\v4_case_gallery_20260529.md`<br>`results\v4_case_gallery_summary_20260529.json` |
| build_clean_sufficiency_misleading_figure | `True` | `paper\figures\clean_sufficiency_misleading_v4_20260529.csv`<br>`results\clean_sufficiency_misleading_v4_20260529.json`<br>`paper\figures\clean_sufficiency_misleading_v4_20260529.svg`<br>`paper\figures\clean_sufficiency_misleading_v4_20260529.md` |
| summarize_v4_anti_shortcut | `True` | `results\v4_anti_shortcut_summary_20260529.json`<br>`results\v4_anti_shortcut_summary_20260529.md` |
| summarize_mechanism_ablation | `True` | `results\mechanism_ablation_summary_20260529.json`<br>`results\mechanism_ablation_summary_20260529.md` |
| verify_claims | `True` | `results\claims_verification.json` |
| summarize_evidence_closure | `False` | `results\evidence_closure_status_v4.json`<br>`results\evidence_closure_status_v4.md` |
| build_external_review_packet | `False` | `results\external_review_packet_status_20260529.json`<br>`results\external_review_packet_20260529.md` |
| summarize_neurips_readiness | `False` | `results\neurips_readiness_matrix_20260529.json`<br>`results\neurips_readiness_matrix_20260529.md` |
| build_results_provenance_readme | `True` | `results\results_provenance_manifest_20260529.json`<br>`results\README.md` |
| build_claims_ledger_markdown | `True` | `CLAIMS_LEDGER.md`<br>`results\claims_ledger_markdown_summary_20260529.json` |
| build_reproducibility_bundle | `True` | `reproducibility/checksums.json`<br>`reproducibility/seeds.json`<br>`reproducibility/hardware.md`<br>`reproducibility/artifact_manifest.md`<br>`reproducibility/hidden_local_path_audit.json`<br>`reproducibility/hidden_local_path_audit.md`<br>`reproducibility/reproduction_commands.md`<br>`reproducibility/bundle_summary_20260529.json` |

## Gate Summary

- Human audit v4 ready: `False`.
- Human audit v4 eval ready: `False`.
- Human audit v4 pending labels: `300`.
- Human audit v4 evaluated packs: `0`.
- Full CoRM reconstruction ready: `False`.
- Remote storage ready: `False`.
- Claim verifier passed: `True`.

## Blockers

Human audit:
- Human audit v4 packs are prepared for Hotpot semantic-swap blind200 and FEVER structbalanced blind100, but adjudicated labels are pending for all 300 items.

Non-human:
- Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts; an ext4 cleanup path exists but needs explicit approval before deleting logs/caches.
- FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.
- External review packet is ready, but independent review remains pending; place the response at results\external_review_response_20260529.md.
- End-to-end selective RAG evidence is currently proxy-only: fixed-coverage and fixed-risk views are directionally positive, but some Hotpot v4 variants remain mixed and this is not a full CoRM-RAG reproduction.
- V4 strong baselines are present, but CSRM-Rule loses or ties the strongest learned/context baselines; main claims must use calibrated/proxy wording with caveats.
- V4 calibrated orbit risk improves Brier on all current calibration artifacts, but ECE is mixed, so calibration remains partial evidence rather than a closed formal-risk claim.

## Claim Policy

This one-command reproduction rebuilds the current evidence gates and closure artifacts. It does not fabricate human labels, does not delete server data, and does not complete full CoRM-RAG reproduction.
