# External Review Packet

Generated: `2026-05-29T07:16:39.947119+00:00`

Packet ready: `True`
External review completed: `False`
Status: `packet_ready`
Blocker: `pending_external_review`

## Required Review Questions

1. Are every allowed claim and every disallowed claim in CLAIMS_LEDGER.json consistent with the current evidence package?
2. Does the negative evidence on FEVER risk transfer and strong baselines require weakening the main method claim further?
3. Are the text-only verifier and LLM judge artifacts sufficient as prepared execution paths, or is API-backed scoring required before paper writing?
4. Does the pending 300-item human audit block all human-audited validity language?
5. Does the remote storage evidence justify keeping full CoRM-RAG reproduction as unsupported until the NTFS/fuseblk write failure is repaired?
6. What exact additional experiments or labels are mandatory before a NeurIPS main-track submission claim can be made?

## Current Claim Boundary

- Verified claims: `{'passed_claims': 28, 'failed_claims': 0, 'total_claims': 28}`.
- Readiness status counts: `{'blocked': 3, 'fail': 1, 'partial': 5, 'pass': 5}`.
- Evidence manifest artifacts: `195`.
- Evidence manifest missing artifacts: `0`.

## Hard Blockers

| Requirement | Status | Boundary / next action |
|---|---|---|
| Human-audited orbit labels | `blocked` | Assignment batches ready: True; batch collection complete: False; pending labels: 1300; cannot claim human-audited results. |
| Full CoRM-RAG reproduction | `blocked` | Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts. Latest storage probe shows 322.1 GiB available and target_write_probe_passed=False; 6 target-dir file probes failed while writable fallback dirs are ['/home/syk', '/tmp', '/dev/shm']. |
| Independent external review | `blocked` | External review packet is ready, but no independent review response is present; place the response at `results\external_review_response_20260529.md`. |

## Negative Or Partial Evidence

| Requirement | Status | Boundary / next action |
|---|---|---|
| Text-only semantic verifier | `partial` | NLI cross-scorer evidence is directionally positive against required weak baselines, but LLM-NLI correlation and human-label text-only evaluation are not ready. |
| Strong baselines and equal-budget controls | `partial` | Baseline package exists, but CSRM-Rule has losses/ties against strongest learned/context baselines; coverage/budget matrices still mark faithful CoRM as partial, clean-only controls as lower-budget, and LLM judge scores as missing. The LLM judge request pack is ready, but no API-backed score artifact exists. Template multi-sample self-consistency, risk-control abstention baselines, shared calibration-threshold selection, and claim-safe target selection are auditable, but test risk/coverage remains mixed rather than all-win. |
| End-to-end selective RAG | `partial` | Proxy evidence now covers two local retrievers and two generators, but remains mixed and is not a full CoRM-RAG Wikipedia retrieval-generation reproduction. The risk-coverage and target-risk coverage artifacts summarize lower accepted-error risk at fixed coverage and higher coverage at fixed target risk, but do not remove the full-reproduction boundary. |
| Novelty and positioning | `partial` | Latest novelty audit recommends proceed-with-caution: closest risks are CoRM-RAG, SURE-RAG, Sufficient Context, CF-RAG, and conformal factuality work. Positioning must stay narrow around aligned evidence-orbit selective risk and cannot claim strong novelty until human-audited results and remaining baselines are complete. |
| Calibrated orbit risk model | `partial` | Calibration-quality artifact shows Brier wins 6/6 against rule/minimax references, but ECE wins 4/6. This supports empirical calibration-quality wording, not a formal risk guarantee. |
| Risk-control claim | `fail` | Hotpot-only empirical transfer is positive; FEVER 0.20 target is negative, so no general/formal claim. |

## Source Artifacts

| Artifact | Exists | Size | SHA256 |
|---|---|---:|---|
| `RAG-idea改进.md` | `True` | 49684 | `abea2cc9e252308bd254f974d86cbd89910eecfeab3ee4a55ab14fc5dee71242` |
| `CLAIMS_LEDGER.json` | `True` | 53391 | `f433d29dc1ca4d67e4097403e7e84c6adc8ec7de7c9785d1e3111a15d699d244` |
| `results\claims_verification.json` | `True` | 62860 | `b3051aff04cf1c2efe13719f0587dca08c1af41ba043266c8fdd1b7c3cde1a6e` |
| `results\evidence_closure_status_v4.json` | `True` | 49292 | `ba66df42e4a834cf157141544dd6ed368e1e0c96fc28676117f4e7f8619fa9d8` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14724 | `356b83fdf7788026e656c5aadf2869a591c4e4a76c280a359efaa92c3de50ed5` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 45821 | `943e49f5125e13c0044c90b046282af67a15e3aef09ef8bcd4852dcc48d80128` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `76be310d5c5b1dcd8bbc0a2c31ae5fa08f9464e7bda18f609823a5f222410e31` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `86787322c75d378e3cccc19fc50e66a01a1387161b85eae9a7bcceb6c9227861` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `943737359379597ae4902dc277175acb5ecbe60e47f7d9803d75dd00b05edda7` |
| `results\v4_claim_safe_target_selection_20260529.json` | `True` | 7318 | `15ad1e6d6f44ab1b2386f0a3a416b8bc6272a025e22336f25a910ab2d0c9f210` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `cc71e77e68ec4587677322d54c0e597e9433b2bcfe79b2ea84e6663a6a210e69` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `3ab28764ba6fcd657742f424910463dee7ea50ddb6db4dabc0d32d7aaacdb051` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `b730b9453c617716f14c5695f3c035cd7f2150b872a4da130ea82d49beaccb80` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `6c814291fc768e7e7e9d3bb9bc9bab24adf66bd7c6729dcd0c4c0d3e5118a869` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `b6a60af674fa53f79a555c510aa3d9441ada5ffe5beff41c969232920a3b12d0` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `3a699ff3ddd57013f00fcc4579d768ecd4a8a2d4fde537a33b3a3121319ce0eb` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `0c12cbd3bf28ee85de366d1a6cbe936dc06e1061e3ca88c1efcc6e2462b6e474` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `0e1caba861b87a13065e49a805fa5b2093ec335b546df797eb3da85ec3afd4ca` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17555 | `f321ed206415bc21c2a871130e568a9ec5f1432a87ccd1045d7adfb27a183f05` |
| `results\human_audit_v4_batch_collection_20260529.json` | `True` | 4742 | `3f1344cc5a48af8b06c7400272b6f9e05fe5aaae0a292b63e188a59c0cb2a88a` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
