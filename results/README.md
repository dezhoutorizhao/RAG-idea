# Results Provenance

Generated: `2026-05-29T08:13:59.819766+00:00`

Ready for NeurIPS main-track claim: `False`.

This package is complete only as a current-evidence snapshot with known blockers; it is not a NeurIPS main-track-ready evidence closure.

## Source Reports

- current_evidence_reproduction: `results\current_evidence_reproduction_20260529.json`
- v4_evidence_package_manifest: `results\v4_evidence_package_manifest_20260529.json`
- neurips_readiness_matrix: `results\neurips_readiness_matrix_20260529.json`

## Step Provenance

| Step | Ready | Source script | Outputs |
|---|---:|---|---|
| materialize_human_audit_v4_paper_pack | `True` | `experiments/materialize_human_audit_v4_paper_pack.py` | `results/human_audit_v4_paper_pack_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`500d4f5b1a24`)<br>`results/human_audit_v4_paper_pack_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`88dad58990f1`) |
| materialize_human_audit_v4_assignment_batches | `True` | `experiments/materialize_human_audit_v4_assignment_batches.py` | `results/human_audit_v4_assignment_batches_20260529.json` (exists=`True`, tracked=`True`, sha256=`c77b6169b1f3`)<br>`results/human_audit_v4_assignment_batches_20260529.md` (exists=`True`, tracked=`True`, sha256=`778f227a6582`)<br>`results/human_audit_v4_batches/v4_paper1000_mixed_blind1000.assignment_manifest.json` (exists=`True`, tracked=`True`, sha256=`89dc9c0bb850`) |
| collect_human_audit_v4_assignment_batches | `False` | `experiments/collect_human_audit_v4_assignment_batches.py` | `results/human_audit_v4_batch_collection_20260529.json` (exists=`True`, tracked=`True`, sha256=`f21036742afd`)<br>`results/human_audit_v4_batch_collection_20260529.md` (exists=`True`, tracked=`True`, sha256=`74ecebe35497`)<br>`results/human_audit_v4_collection/v4_paper1000_mixed_blind1000.merged_labels.jsonl` (exists=`True`, tracked=`True`, sha256=`01a893122d46`)<br>`results/human_audit_v4_collection/v4_paper1000_mixed_blind1000.adjudicated_labels.jsonl` (exists=`True`, tracked=`True`, sha256=`6dab172b0c15`)<br>`results/human_audit_v4_collection/v4_paper1000_mixed_blind1000.readiness.json` (exists=`True`, tracked=`True`, sha256=`e9e7b4d14b81`) |
| summarize_human_audit_v4_status | `False` | `experiments/summarize_human_audit_v4_status.py` | `results/human_audit_v4_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`6c1147bdc32e`)<br>`results/human_audit_v4_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`7336e42957bb`) |
| summarize_human_audit_v4_disagreements | `True` | `experiments/summarize_human_audit_v4_disagreements.py` | `results/human_audit_v4_disagreement_taxonomy_20260529.json` (exists=`True`, tracked=`True`, sha256=`0ee3f3e91d75`)<br>`results/human_audit_v4_disagreement_taxonomy_20260529.md` (exists=`True`, tracked=`True`, sha256=`bbae4d358c93`) |
| summarize_human_audit_v4_mismatch | `True` | `experiments/summarize_human_audit_v4_mismatch.py` | `results/human_audit_v4_mismatch_20260529.json` (exists=`True`, tracked=`True`, sha256=`fcf134a8a7f3`)<br>`results/human_audit_v4_mismatch_20260529.md` (exists=`True`, tracked=`True`, sha256=`d345a1eeee8f`) |
| run_human_audit_eval_v4 | `False` | `experiments/run_human_audit_eval_v4.py` | `results/human_audit_v4_eval_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`c33cbaf7461e`)<br>`results/human_audit_v4_eval_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`51303ec57d86`) |
| summarize_fever_cp_transfer_sweep | `False` | `experiments/summarize_fever_cp_transfer_sweep.py` | `results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`2e9255ca5cc0`)<br>`results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`8017c65cee49`) |
| summarize_end2end_selective_rag_proxy | `False` | `experiments/summarize_end2end_selective_rag_proxy.py` | `results/end2end_selective_rag_proxy_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`0a591acd41ce`)<br>`results/end2end_selective_rag_proxy_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`f9d515b98793`) |
| run_end2end_retriever_generator_matrix_v4 | `False` | `experiments/run_end2end_retriever_generator_matrix_v4.py` | `results/end2end_retriever_generator_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`8c13c7d5b739`)<br>`results/end2end_retriever_generator_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`a235500c150b`) |
| plot_end2end_risk_coverage_curves | `True` | `experiments/plot_end2end_risk_coverage_curves.py` | `results/end2end_risk_coverage_curves_20260529.json` (exists=`True`, tracked=`True`, sha256=`7d3da263d8f7`)<br>`results/end2end_risk_coverage_curves_20260529.md` (exists=`True`, tracked=`True`, sha256=`b20278a6fdca`)<br>`paper/figures/end2end_risk_coverage_curves_20260529.svg` (exists=`True`, tracked=`True`, sha256=`e24141090458`) |
| summarize_end2end_target_risk_coverage | `True` | `experiments/summarize_end2end_target_risk_coverage.py` | `results/end2end_target_risk_coverage_20260529.json` (exists=`True`, tracked=`True`, sha256=`ca430d7dd95d`)<br>`results/end2end_target_risk_coverage_20260529.md` (exists=`True`, tracked=`True`, sha256=`677eaf540cb9`) |
| materialize_llm_judge_requests_v4 | `False` | `experiments/materialize_llm_judge_requests_v4.py` | `results/llm_judge_v4_requests_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`7863764d362f`)<br>`results/llm_judge_v4_request_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`b30a1f2f3477`)<br>`results/llm_judge_v4_request_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`f0916117be72`) |
| materialize_llm_judge_requests_nli_probe | `False` | `experiments/materialize_llm_judge_requests_nli_probe.py` | `results/llm_judge_nli_probe_requests_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`74ed598cbdcf`)<br>`results/llm_judge_nli_probe_request_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`470f498af73c`)<br>`results/llm_judge_nli_probe_request_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`67fa34a50106`) |
| manage_openai_llm_judge_batch_preflight | `False` | `experiments/manage_openai_llm_judge_batch.py` | `results/llm_judge_nli_probe_batch_run_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`d401a2661226`)<br>`results/llm_judge_nli_probe_batch_run_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`07b33c70b7a9`) |
| normalize_llm_judge_batch_responses | `False` | `experiments/normalize_llm_judge_batch_responses.py` | `results/llm_judge_nli_probe_score_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`2f425bb21aa6`)<br>`results/llm_judge_nli_probe_score_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`c06f9b670a01`) |
| compute_llm_nli_correlation | `False` | `experiments/compute_llm_nli_correlation.py` | `results/llm_nli_correlation_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`1977b0c8dbab`)<br>`results/llm_nli_correlation_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`cd68133e1f7f`) |
| summarize_text_only_verifier_status | `False` | `experiments/summarize_text_only_verifier_status.py` | `results/text_only_verifier_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`1c6dc87d4258`)<br>`results/text_only_verifier_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`f52e9635187a`) |
| summarize_v4_strong_baselines | `False` | `experiments/summarize_v4_strong_baselines.py` | `results/v4_strong_baseline_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`217978c56afc`)<br>`results/v4_strong_baseline_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`ab0994b97df2`) |
| summarize_v4_baseline_coverage | `False` | `experiments/summarize_v4_baseline_coverage.py` | `results/v4_baseline_coverage_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`5fdfac95aa69`)<br>`results/v4_baseline_coverage_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`045b09e7f265`) |
| summarize_v4_baseline_budget_parity | `False` | `experiments/summarize_v4_baseline_budget_parity.py` | `results/v4_baseline_budget_parity_20260529.json` (exists=`True`, tracked=`True`, sha256=`ae8d2c2087d7`)<br>`results/v4_baseline_budget_parity_20260529.md` (exists=`True`, tracked=`True`, sha256=`e09e0022f0f3`) |
| compare_equal_budget_thresholds_v4 | `True` | `experiments/compare_equal_budget_thresholds_v4.py` | `results/v4_shared_threshold_selection_20260529.json` (exists=`True`, tracked=`True`, sha256=`c728ace3c266`)<br>`results/v4_shared_threshold_selection_20260529.md` (exists=`True`, tracked=`True`, sha256=`33a22e86eb7e`) |
| summarize_v4_split_threshold_protocol | `True` | `experiments/summarize_v4_split_threshold_protocol.py` | `results/v4_split_threshold_protocol_20260529.json` (exists=`True`, tracked=`True`, sha256=`543be955e8b8`)<br>`results/v4_split_threshold_protocol_20260529.md` (exists=`True`, tracked=`True`, sha256=`91b832425db6`) |
| summarize_risk_control_abstention_baselines | `True` | `experiments/summarize_risk_control_abstention_baselines.py` | `results/risk_control_abstention_baselines_20260529.json` (exists=`True`, tracked=`True`, sha256=`7f16f0ffc8e2`)<br>`results/risk_control_abstention_baselines_20260529.md` (exists=`True`, tracked=`True`, sha256=`f74f7520178d`) |
| summarize_v4_calibration_quality | `False` | `experiments/summarize_v4_calibration_quality.py` | `results/v4_calibration_quality_20260529.json` (exists=`True`, tracked=`True`, sha256=`3de0e7914e15`)<br>`results/v4_calibration_quality_20260529.md` (exists=`True`, tracked=`True`, sha256=`a196392fd276`) |
| summarize_v4_claim_safe_target_selection | `False` | `experiments/summarize_v4_claim_safe_target_selection.py` | `results/v4_claim_safe_target_selection_20260529.json` (exists=`True`, tracked=`True`, sha256=`0bd93a0aaee2`)<br>`results/v4_claim_safe_target_selection_20260529.md` (exists=`True`, tracked=`True`, sha256=`82eadddbae05`) |
| summarize_v4_failure_taxonomy | `True` | `experiments/summarize_v4_failure_taxonomy.py` | `results/v4_failure_taxonomy_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`bbade922e56c`)<br>`results/v4_failure_taxonomy_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`184a928bc723`) |
| export_v4_case_gallery | `True` | `experiments/export_v4_case_gallery.py` | `paper/case_studies/v4_case_gallery_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`f03232de577d`)<br>`paper/case_studies/v4_case_gallery_20260529.md` (exists=`True`, tracked=`True`, sha256=`60ad7f97e907`)<br>`results/v4_case_gallery_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`69ffcf3a01f8`) |
| build_clean_sufficiency_misleading_figure | `True` | `experiments/build_clean_sufficiency_misleading_figure.py` | `paper/figures/clean_sufficiency_misleading_v4_20260529.csv` (exists=`True`, tracked=`True`, sha256=`ded3232932e8`)<br>`results/clean_sufficiency_misleading_v4_20260529.json` (exists=`True`, tracked=`True`, sha256=`3f7a7303c689`)<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.svg` (exists=`True`, tracked=`True`, sha256=`a354e94977a8`)<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.md` (exists=`True`, tracked=`True`, sha256=`d865c54f4d55`) |
| summarize_v4_anti_shortcut | `True` | `experiments/summarize_v4_anti_shortcut.py` | `results/v4_anti_shortcut_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`78c8a96e0d71`)<br>`results/v4_anti_shortcut_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`bc9ea90bdb4d`) |
| summarize_mechanism_ablation | `True` | `experiments/summarize_mechanism_ablation.py` | `results/mechanism_ablation_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`28c4a98e0bb8`)<br>`results/mechanism_ablation_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`804b7402a266`) |
| summarize_theory_formalization | `True` | `experiments/summarize_theory_formalization.py` | `results/theory_formalization_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`78ad226d9fce`)<br>`results/theory_formalization_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`052e89195710`) |
| summarize_novelty_audit | `True` | `experiments/summarize_novelty_audit.py` | `results/novelty_audit_20260529.json` (exists=`True`, tracked=`True`, sha256=`1a9653a91c32`)<br>`results/novelty_audit_20260529.md` (exists=`True`, tracked=`True`, sha256=`0fc6c22000b4`) |
| verify_claims | `True` | `experiments/verify_claims.py` | `results/claims_verification.json` (exists=`True`, tracked=`True`, sha256=`b3051aff04cf`) |
| summarize_evidence_closure | `False` | `experiments/summarize_evidence_closure.py` | `results/evidence_closure_status_v4.json` (exists=`True`, tracked=`True`, sha256=`6ea980ebda6b`)<br>`results/evidence_closure_status_v4.md` (exists=`True`, tracked=`True`, sha256=`4b9f239b13dc`) |
| build_external_review_packet | `False` | `experiments/build_external_review_packet.py` | `results/external_review_packet_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`89dbe2bd6aaa`)<br>`results/external_review_packet_20260529.md` (exists=`True`, tracked=`True`, sha256=`3db469a749bc`) |
| summarize_neurips_readiness | `False` | `experiments/summarize_neurips_readiness.py` | `results/neurips_readiness_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`ddb7714de809`)<br>`results/neurips_readiness_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`bda3487934ce`) |
| summarize_neurips_unblock_plan | `False` | `experiments/summarize_neurips_unblock_plan.py` | `results/neurips_unblock_plan_20260529.json` (exists=`True`, tracked=`True`, sha256=`8b8e811a2403`)<br>`results/neurips_unblock_plan_20260529.md` (exists=`True`, tracked=`True`, sha256=`60e4e7925993`) |
| build_results_provenance_readme | `True` | `experiments/build_results_provenance_readme.py` | `results/results_provenance_manifest_20260529.json` (exists=`True`, tracked=`True`, sha256=`2044548eee88`)<br>`results/README.md` (exists=`True`, tracked=`True`, sha256=`4527e15cb7f7`) |
| build_claims_ledger_markdown | `True` | `experiments/build_claims_ledger_markdown.py` | `CLAIMS_LEDGER.md` (exists=`True`, tracked=`True`, sha256=`477b9aee51fd`)<br>`results/claims_ledger_markdown_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`866a795cf163`) |
| build_reproducibility_bundle | `True` | `experiments/build_reproducibility_bundle.py` | `reproducibility/checksums.json` (exists=`True`, tracked=`True`, sha256=`169b90c129cc`)<br>`reproducibility/seeds.json` (exists=`True`, tracked=`True`, sha256=`aa7caf65cb4a`)<br>`reproducibility/hardware.md` (exists=`True`, tracked=`True`, sha256=`b2de931353f4`)<br>`reproducibility/artifact_manifest.md` (exists=`True`, tracked=`True`, sha256=`adb4f70fc3b2`)<br>`reproducibility/hidden_local_path_audit.json` (exists=`True`, tracked=`True`, sha256=`55e4e7b4fa17`)<br>`reproducibility/hidden_local_path_audit.md` (exists=`True`, tracked=`True`, sha256=`7cc2c8e9fb57`)<br>`reproducibility/reproduction_commands.md` (exists=`True`, tracked=`True`, sha256=`b48d193a931d`)<br>`reproducibility/bundle_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`55b8f69d932d`) |

## Reproduce Current Package

```bash
python -m experiments.reproduce_current_evidence_v4 --output-json results/current_evidence_reproduction_20260529.json --output-md results/current_evidence_reproduction_20260529.md
python -m experiments.verify_v4_evidence_package --output-json results/v4_evidence_package_manifest_20260529.json --output-md results/v4_evidence_package_manifest_20260529.md
python -m experiments.build_results_provenance_readme --output-json results/results_provenance_manifest_20260529.json --output-md results/README.md
```

## Artifact Status

- Evidence manifest artifact count: `221`.
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
