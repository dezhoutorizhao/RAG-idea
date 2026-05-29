# NeurIPS Readiness Matrix

Generated: `2026-05-29T03:24:09.554759+00:00`

Ready for NeurIPS main-track claim: `False`

## Status Counts

- pass: `4`
- partial: `2`
- fail: `1`
- blocked: `3`

## Checklist

| Requirement | Status | Evidence | Boundary / next action |
|---|---|---|---|
| Leakage-free v4 pipeline | `pass` | `results/v4_anti_shortcut_summary_20260529.json`<br>`results/evidence_closure_status_v4.json` | Core anti-shortcut suite passes; private construction metadata remains evaluator-only. |
| Human-audited orbit labels | `blocked` | `results/human_audit_v4_status_20260529.json`<br>`results/human_audit_v4_disagreement_taxonomy_20260529.json`<br>`results/human_audit_v4_mismatch_20260529.json`<br>`results/human_audit_v4_eval_status_20260529.json` | Pending labels: 300; cannot claim human-audited results. |
| Strong baselines and equal-budget controls | `partial` | `results/v4_strong_baseline_summary_20260529.json`<br>`results/v4_baseline_coverage_matrix_20260529.json`<br>`results/v4_baseline_budget_parity_20260529.json`<br>`results/v4_shared_threshold_selection_20260529.json`<br>`results/v4_split_threshold_protocol_20260529.json` | Baseline package exists, but CSRM-Rule has losses/ties against strongest learned/context baselines; coverage/budget matrices still mark faithful CoRM as partial, clean-only controls as lower-budget, and LLM judge as missing. Template multi-sample self-consistency and shared calibration-threshold selection are now auditable, but test risk/coverage remains mixed rather than all-win. |
| End-to-end selective RAG | `partial` | `results/end2end_selective_rag_proxy_summary_20260529.json`<br>`results/end2end_retriever_generator_matrix_20260529.json` | Proxy evidence now covers two local retrievers and two generators, but remains mixed and is not a full CoRM-RAG Wikipedia retrieval-generation reproduction. |
| Full CoRM-RAG reproduction | `blocked` | `results/corm_reproduction_preflight.json`<br>`results/corm_full_wikipedia_job_status.json`<br>`results/remote_storage_status_20260529.json` | Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts. |
| Mechanism ablations | `pass` | `results/mechanism_ablation_summary_20260529.json` | Alignment evidence is strong; no-worst-sufficiency is weak/redundant in current bridge artifacts. |
| Failure taxonomy and case studies | `pass` | `results/v4_failure_taxonomy_summary_20260529.json`<br>`paper/case_studies/v4_case_gallery_20260529.md`<br>`paper/figures/clean_sufficiency_misleading_v4_20260529.svg` | Paper-facing diagnostics are complete but private-label, not human-adjudicated. |
| Risk-control claim | `fail` | `results/fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json` | Hotpot-only empirical transfer is positive; FEVER 0.20 target is negative, so no general/formal claim. |
| Claim ledger and evidence package | `pass` | `CLAIMS_LEDGER.json`<br>`results/claims_verification.json`<br>`results/v4_evidence_package_manifest_20260529.json` | Manifest artifacts: 104; missing: 0. |
| Independent external review | `blocked` |  | Not rerun after latest evidence package; requires explicit external/subagent review or another approved review path. |

## Claim Policy

This matrix tracks readiness against the NeurIPS main-track evidence plan. A pass means the current artifact supports that checklist item at the stated scope; partial means useful evidence exists but is too narrow or mixed; fail means current evidence contradicts the strong version of the requirement; blocked means the item cannot be completed without human labels, storage repair/approval, or an external review.
