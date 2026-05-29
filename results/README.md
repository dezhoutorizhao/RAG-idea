# Results Provenance

Generated: `2026-05-29T06:12:35.640939+00:00`

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
| summarize_fever_cp_transfer_sweep | `False` | `experiments/summarize_fever_cp_transfer_sweep.py` | `results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`ee2779aa9b71`)<br>`results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`78ad9e70a8d3`) |
| summarize_end2end_selective_rag_proxy | `False` | `experiments/summarize_end2end_selective_rag_proxy.py` | `results/end2end_selective_rag_proxy_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`d31c88762fc8`)<br>`results/end2end_selective_rag_proxy_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`dcd52493e2e3`) |
| run_end2end_retriever_generator_matrix_v4 | `False` | `experiments/run_end2end_retriever_generator_matrix_v4.py` | `results/end2end_retriever_generator_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`a190a8d353b8`)<br>`results/end2end_retriever_generator_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`32dcf6fb709b`) |
| plot_end2end_risk_coverage_curves | `True` | `experiments/plot_end2end_risk_coverage_curves.py` | `results/end2end_risk_coverage_curves_20260529.json` (exists=`True`, tracked=`True`, sha256=`88229abbc22b`)<br>`results/end2end_risk_coverage_curves_20260529.md` (exists=`True`, tracked=`True`, sha256=`63e7ad65bafd`)<br>`paper/figures/end2end_risk_coverage_curves_20260529.svg` (exists=`True`, tracked=`True`, sha256=`e24141090458`) |
| summarize_end2end_target_risk_coverage | `True` | `experiments/summarize_end2end_target_risk_coverage.py` | `results/end2end_target_risk_coverage_20260529.json` (exists=`True`, tracked=`True`, sha256=`9d4d7659652b`)<br>`results/end2end_target_risk_coverage_20260529.md` (exists=`True`, tracked=`True`, sha256=`99de3e0a6eb7`) |
| materialize_llm_judge_requests_v4 | `False` | `experiments/materialize_llm_judge_requests_v4.py` | `results/llm_judge_v4_requests_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`7863764d362f`)<br>`results/llm_judge_v4_request_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`235dbf180d62`)<br>`results/llm_judge_v4_request_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`5e2a62710d65`) |
| materialize_llm_judge_requests_nli_probe | `False` | `experiments/materialize_llm_judge_requests_nli_probe.py` | `results/llm_judge_nli_probe_requests_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`74ed598cbdcf`)<br>`results/llm_judge_nli_probe_request_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`01ed2efa10aa`)<br>`results/llm_judge_nli_probe_request_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`9c67f2e0d449`) |
| manage_openai_llm_judge_batch_preflight | `False` | `experiments/manage_openai_llm_judge_batch.py` | `results/llm_judge_nli_probe_batch_run_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`38d6fa6fa3d3`)<br>`results/llm_judge_nli_probe_batch_run_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`31a02fa1cd82`) |
| normalize_llm_judge_batch_responses | `False` | `experiments/normalize_llm_judge_batch_responses.py` | `results/llm_judge_nli_probe_score_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`97bda3343c55`)<br>`results/llm_judge_nli_probe_score_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`6ffceb531c27`) |
| compute_llm_nli_correlation | `False` | `experiments/compute_llm_nli_correlation.py` | `results/llm_nli_correlation_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`e2f9fa7b2452`)<br>`results/llm_nli_correlation_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`01322e39918d`) |
| summarize_text_only_verifier_status | `False` | `experiments/summarize_text_only_verifier_status.py` | `results/text_only_verifier_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`df72c0a24cfb`)<br>`results/text_only_verifier_status_20260529.md` (exists=`True`, tracked=`True`, sha256=`24351edb1b55`) |
| summarize_v4_strong_baselines | `False` | `experiments/summarize_v4_strong_baselines.py` | `results/v4_strong_baseline_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`210f1f1862fe`)<br>`results/v4_strong_baseline_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`1d244edb2de8`) |
| summarize_v4_baseline_coverage | `False` | `experiments/summarize_v4_baseline_coverage.py` | `results/v4_baseline_coverage_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`84260dcc6583`)<br>`results/v4_baseline_coverage_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`61c66e951906`) |
| summarize_v4_baseline_budget_parity | `False` | `experiments/summarize_v4_baseline_budget_parity.py` | `results/v4_baseline_budget_parity_20260529.json` (exists=`True`, tracked=`True`, sha256=`2d1e8d4864be`)<br>`results/v4_baseline_budget_parity_20260529.md` (exists=`True`, tracked=`True`, sha256=`09af2850decc`) |
| compare_equal_budget_thresholds_v4 | `True` | `experiments/compare_equal_budget_thresholds_v4.py` | `results/v4_shared_threshold_selection_20260529.json` (exists=`True`, tracked=`True`, sha256=`99919a9075cb`)<br>`results/v4_shared_threshold_selection_20260529.md` (exists=`True`, tracked=`True`, sha256=`5a47da60451f`) |
| summarize_v4_split_threshold_protocol | `True` | `experiments/summarize_v4_split_threshold_protocol.py` | `results/v4_split_threshold_protocol_20260529.json` (exists=`True`, tracked=`True`, sha256=`d6d9b786c9a6`)<br>`results/v4_split_threshold_protocol_20260529.md` (exists=`True`, tracked=`True`, sha256=`34dcbc929b63`) |
| summarize_risk_control_abstention_baselines | `True` | `experiments/summarize_risk_control_abstention_baselines.py` | `results/risk_control_abstention_baselines_20260529.json` (exists=`True`, tracked=`True`, sha256=`5cfd6803bd73`)<br>`results/risk_control_abstention_baselines_20260529.md` (exists=`True`, tracked=`True`, sha256=`ef6e2dc03e22`) |
| summarize_v4_calibration_quality | `False` | `experiments/summarize_v4_calibration_quality.py` | `results/v4_calibration_quality_20260529.json` (exists=`True`, tracked=`True`, sha256=`df206187ef3f`)<br>`results/v4_calibration_quality_20260529.md` (exists=`True`, tracked=`True`, sha256=`eeb61f1db265`) |
| summarize_v4_failure_taxonomy | `True` | `experiments/summarize_v4_failure_taxonomy.py` | `results/v4_failure_taxonomy_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`cf768f11c2d5`)<br>`results/v4_failure_taxonomy_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`35c8d557ebd1`) |
| export_v4_case_gallery | `True` | `experiments/export_v4_case_gallery.py` | `paper/case_studies/v4_case_gallery_20260529.jsonl` (exists=`True`, tracked=`True`, sha256=`f03232de577d`)<br>`paper/case_studies/v4_case_gallery_20260529.md` (exists=`True`, tracked=`True`, sha256=`32243fcbcedf`)<br>`results/v4_case_gallery_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`2c0b0bf7eed0`) |
| build_clean_sufficiency_misleading_figure | `True` | `experiments/build_clean_sufficiency_misleading_figure.py` | `paper/figures/clean_sufficiency_misleading_v4_20260529.csv` (exists=`True`, tracked=`True`, sha256=`ded3232932e8`)<br>`results/clean_sufficiency_misleading_v4_20260529.json` (exists=`True`, tracked=`True`, sha256=`b2928d84aaba`)<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.svg` (exists=`True`, tracked=`True`, sha256=`a354e94977a8`)<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.md` (exists=`True`, tracked=`True`, sha256=`70e90c508998`) |
| summarize_v4_anti_shortcut | `True` | `experiments/summarize_v4_anti_shortcut.py` | `results/v4_anti_shortcut_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`f3b3506ab908`)<br>`results/v4_anti_shortcut_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`98f05bee97f5`) |
| summarize_mechanism_ablation | `True` | `experiments/summarize_mechanism_ablation.py` | `results/mechanism_ablation_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`255740a0ee6f`)<br>`results/mechanism_ablation_summary_20260529.md` (exists=`True`, tracked=`True`, sha256=`a9e5095ed9c8`) |
| verify_claims | `True` | `experiments/verify_claims.py` | `results/claims_verification.json` (exists=`True`, tracked=`True`, sha256=`b3051aff04cf`) |
| summarize_evidence_closure | `False` | `experiments/summarize_evidence_closure.py` | `results/evidence_closure_status_v4.json` (exists=`True`, tracked=`True`, sha256=`18deb7fac767`)<br>`results/evidence_closure_status_v4.md` (exists=`True`, tracked=`True`, sha256=`e9faa7cf417a`) |
| build_external_review_packet | `False` | `experiments/build_external_review_packet.py` | `results/external_review_packet_status_20260529.json` (exists=`True`, tracked=`True`, sha256=`6d4d6d367419`)<br>`results/external_review_packet_20260529.md` (exists=`True`, tracked=`True`, sha256=`f72d076381ee`) |
| summarize_neurips_readiness | `False` | `experiments/summarize_neurips_readiness.py` | `results/neurips_readiness_matrix_20260529.json` (exists=`True`, tracked=`True`, sha256=`1296a59c0a8b`)<br>`results/neurips_readiness_matrix_20260529.md` (exists=`True`, tracked=`True`, sha256=`049694b97609`) |
| build_results_provenance_readme | `True` | `experiments/build_results_provenance_readme.py` | `results/results_provenance_manifest_20260529.json` (exists=`True`, tracked=`True`, sha256=`03def3e22547`)<br>`results/README.md` (exists=`True`, tracked=`True`, sha256=`cf60831d0fc6`) |
| build_claims_ledger_markdown | `True` | `experiments/build_claims_ledger_markdown.py` | `CLAIMS_LEDGER.md` (exists=`True`, tracked=`True`, sha256=`bd57b2d57ad0`)<br>`results/claims_ledger_markdown_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`3c130434d153`) |
| build_reproducibility_bundle | `True` | `experiments/build_reproducibility_bundle.py` | `reproducibility/checksums.json` (exists=`True`, tracked=`True`, sha256=`d3ef4886ffb4`)<br>`reproducibility/seeds.json` (exists=`True`, tracked=`True`, sha256=`8015546e9949`)<br>`reproducibility/hardware.md` (exists=`True`, tracked=`True`, sha256=`558ba47b8f3f`)<br>`reproducibility/artifact_manifest.md` (exists=`True`, tracked=`True`, sha256=`7b3b728b7b00`)<br>`reproducibility/hidden_local_path_audit.json` (exists=`True`, tracked=`True`, sha256=`2936c9619fb5`)<br>`reproducibility/hidden_local_path_audit.md` (exists=`True`, tracked=`True`, sha256=`6b199d3fbf49`)<br>`reproducibility/reproduction_commands.md` (exists=`True`, tracked=`True`, sha256=`3f3f3099efd9`)<br>`reproducibility/bundle_summary_20260529.json` (exists=`True`, tracked=`True`, sha256=`0867741f8086`) |

## Reproduce Current Package

```bash
python -m experiments.reproduce_current_evidence_v4 --output-json results/current_evidence_reproduction_20260529.json --output-md results/current_evidence_reproduction_20260529.md
python -m experiments.verify_v4_evidence_package --output-json results/v4_evidence_package_manifest_20260529.json --output-md results/v4_evidence_package_manifest_20260529.md
python -m experiments.build_results_provenance_readme --output-json results/results_provenance_manifest_20260529.json --output-md results/README.md
```

## Artifact Status

- Evidence manifest artifact count: `161`.
- Evidence manifest missing artifacts: `0`.
- Missing current-step outputs: `0`.
- Current-step outputs not listed in evidence manifest: `0`.
- Readiness status counts: `{'blocked': 3, 'fail': 1, 'partial': 4, 'pass': 4}`.

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
