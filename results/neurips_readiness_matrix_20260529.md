# NeurIPS Readiness Matrix

Generated: `2026-05-29T07:52:23.773147+00:00`

Ready for NeurIPS main-track claim: `False`

## Status Counts

- pass: `5`
- partial: `5`
- fail: `1`
- blocked: `3`

## Checklist

| Requirement | Status | Evidence | Boundary / next action |
|---|---|---|---|
| Leakage-free v4 pipeline | `pass` | `results/v4_anti_shortcut_summary_20260529.json`<br>`results/evidence_closure_status_v4.json` | Core anti-shortcut suite passes; private construction metadata remains evaluator-only. |
| Human-audited orbit labels | `blocked` | `results/human_audit_v4_paper_pack_status_20260529.json`<br>`results/human_audit_v4_assignment_batches_20260529.json`<br>`results/human_audit_v4_batch_collection_20260529.json`<br>`results/human_audit_v4_status_20260529.json`<br>`results/human_audit_v4_disagreement_taxonomy_20260529.json`<br>`results/human_audit_v4_mismatch_20260529.json`<br>`results/human_audit_v4_eval_status_20260529.json` | Assignment batches ready: True; batch collection complete: False; pending labels: 1300; cannot claim human-audited results. |
| Text-only semantic verifier | `partial` | `results/text_only_verifier_status_20260529.json`<br>`results/audit_sample_paper_1000_v3_nli_set_eval.json`<br>`results/llm_judge_v4_request_status_20260529.json` | NLI cross-scorer evidence is directionally positive against required weak baselines, but LLM-NLI correlation and human-label text-only evaluation are not ready. |
| Strong baselines and equal-budget controls | `partial` | `results/v4_strong_baseline_summary_20260529.json`<br>`results/v4_baseline_coverage_matrix_20260529.json`<br>`results/v4_baseline_budget_parity_20260529.json`<br>`results/v4_shared_threshold_selection_20260529.json`<br>`results/v4_split_threshold_protocol_20260529.json`<br>`results/risk_control_abstention_baselines_20260529.json`<br>`results/v4_claim_safe_target_selection_20260529.json`<br>`results/llm_judge_v4_request_status_20260529.json` | Baseline package exists, but CSRM-Rule has losses/ties against strongest learned/context baselines; coverage/budget matrices still mark faithful CoRM as partial, clean-only controls as lower-budget, and LLM judge scores as missing. The LLM judge request pack is ready, but no API-backed score artifact exists. Template multi-sample self-consistency, risk-control abstention baselines, shared calibration-threshold selection, and claim-safe target selection are auditable, but test risk/coverage remains mixed rather than all-win. |
| End-to-end selective RAG | `partial` | `results/end2end_selective_rag_proxy_summary_20260529.json`<br>`results/end2end_retriever_generator_matrix_20260529.json`<br>`results/end2end_risk_coverage_curves_20260529.json`<br>`results/end2end_target_risk_coverage_20260529.json`<br>`paper/figures/end2end_risk_coverage_curves_20260529.svg` | Proxy evidence now covers two local retrievers and two generators, but remains mixed and is not a full CoRM-RAG Wikipedia retrieval-generation reproduction. The risk-coverage and target-risk coverage artifacts summarize lower accepted-error risk at fixed coverage and higher coverage at fixed target risk, but do not remove the full-reproduction boundary. |
| Full CoRM-RAG reproduction | `blocked` | `results/corm_reproduction_preflight.json`<br>`results/corm_full_wikipedia_job_status.json`<br>`results/remote_storage_status_20260529.json` | Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts. Latest storage probe shows 322.1 GiB available and target_write_probe_passed=False; 6 target-dir file probes failed while writable fallback dirs are ['/home/syk', '/tmp', '/dev/shm']. |
| Mechanism ablations | `pass` | `results/mechanism_ablation_summary_20260529.json` | Alignment evidence is strong; no-worst-sufficiency is weak/redundant in current bridge artifacts. |
| Theory and formalization | `pass` | `paper/sections/formalization.tex`<br>`paper/sections/theory.tex`<br>`results/theory_formalization_status_20260529.json` | Formalization now states the orbit-risk object and three information-structure propositions. This supports the mechanism rationale but does not imply empirical all-win behavior, human validity, or a formal risk-control guarantee. |
| Novelty and positioning | `partial` | `results/novelty_audit_20260529.json`<br>`results/novelty_audit_20260529.md` | Latest novelty audit recommends proceed-with-caution: closest risks are CoRM-RAG, SURE-RAG, Sufficient Context, CF-RAG, and conformal factuality work. Positioning must stay narrow around aligned evidence-orbit selective risk and cannot claim strong novelty until human-audited results and remaining baselines are complete. |
| Calibrated orbit risk model | `partial` | `results/v4_calibration_quality_20260529.json`<br>`results/v4_calibration_quality_20260529.md` | Calibration-quality artifact shows Brier wins 6/6 against rule/minimax references, but ECE wins 4/6. This supports empirical calibration-quality wording, not a formal risk guarantee. |
| Failure taxonomy and case studies | `pass` | `results/v4_failure_taxonomy_summary_20260529.json`<br>`paper/case_studies/v4_case_gallery_20260529.md`<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.svg` | Paper-facing diagnostics are complete but private-label, not human-adjudicated. |
| Risk-control claim | `fail` | `results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json` | Hotpot-only empirical transfer is positive; FEVER 0.20 target is negative, so no general/formal claim. |
| Claim ledger and evidence package | `pass` | `CLAIMS_LEDGER.json`<br>`results/claims_verification.json`<br>`results/v4_evidence_package_manifest_20260529.json` | Manifest artifacts: 206; missing: 0. |
| Independent external review | `blocked` | `results/external_review_packet_status_20260529.json`<br>`results/external_review_packet_20260529.md` | External review packet is ready, but no independent review response is present; place the response at `results\external_review_response_20260529.md`. |

## Claim Policy

This matrix tracks readiness against the NeurIPS main-track evidence plan. A pass means the current artifact supports that checklist item at the stated scope; partial means useful evidence exists but is too narrow or mixed; fail means current evidence contradicts the strong version of the requirement; blocked means the item cannot be completed without human labels, storage repair/approval, or an external review.
