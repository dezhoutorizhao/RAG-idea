# External Review Packet

Generated: `2026-05-29T06:56:05.483365+00:00`

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
- Evidence manifest artifacts: `189`.
- Evidence manifest missing artifacts: `0`.

## Hard Blockers

| Requirement | Status | Boundary / next action |
|---|---|---|
| Human-audited orbit labels | `blocked` | Assignment batches ready: True; pending labels: 1300; cannot claim human-audited results. |
| Full CoRM-RAG reproduction | `blocked` | Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts. Latest storage probe shows 322.1 GiB available and target_write_probe_passed=False; 6 target-dir file probes failed while writable fallback dirs are ['/home/syk', '/tmp', '/dev/shm']. |
| Independent external review | `blocked` | External review packet is ready, but no independent review response is present; place the response at `results\external_review_response_20260529.md`. |

## Negative Or Partial Evidence

| Requirement | Status | Boundary / next action |
|---|---|---|
| Text-only semantic verifier | `partial` | NLI cross-scorer evidence is directionally positive against required weak baselines, but LLM-NLI correlation and human-label text-only evaluation are not ready. |
| Strong baselines and equal-budget controls | `partial` | Baseline package exists, but CSRM-Rule has losses/ties against strongest learned/context baselines; coverage/budget matrices still mark faithful CoRM as partial, clean-only controls as lower-budget, and LLM judge scores as missing. The LLM judge request pack is ready, but no API-backed score artifact exists. Template multi-sample self-consistency, risk-control abstention baselines, and shared calibration-threshold selection are auditable, but test risk/coverage remains mixed rather than all-win. |
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
| `results\evidence_closure_status_v4.json` | `True` | 47504 | `d60b12afc0bb237d1d5d7c8f00105564bdba921be55b8b433992e8377ca3a55d` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14336 | `244fc070e5b8682a8ba91513efcc071a118545507496b72bc70a11a1d0a9f7cb` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 44286 | `cf3df814887626f89912d45ce0e8e3a33d5ae6dfd6c289e02b398c03ba3512d9` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `91fa742d4e70bc56d854cd251c17dc781edb8c979a003808fa20049cd15e53b7` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `7d4283e81b6c3588be5bc19f1c82d87e9b36f4a37c901c8525a37703d1b4c9fb` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `5883438ff89cdaa22df4842fc444ba6fa583a462adfbaebe8d2aaadb94b27848` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `6f96322eac30806282aef295b34dd4e37afa48edb711a8a70505c1f181d24253` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `d016fceda0bf353028940488d26420cd7b99dbeb62927933f180755411418728` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `d2f5e6176e3f29fc8f5a676ea63c2522a1678511351e77b000d339387e8fc044` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `c7238afe2893954f4ad2fa43993abb5cc8d5d1fc376f01c36668241a2ae2fa45` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `6c69af77451105a412edbd7fe3542d75ca0c4e0f895855a7cb8915943b7c0e3a` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `c956599e0191bed8f18213fb56276c08b4c1251f6c78b23770e00cf9602532c4` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `99f9144bc129a4635f4083a47e6f57129aec1eef4194e4ced49f864c36ef42c6` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `8228a9c175b5c77d9cbc40e658bff5c25e366f96f0a1a47218a18e3f0846affc` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17188 | `5f4b8563020da3c68f806614b63f046f3cd3554ed4c66b312095dc2388946718` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
