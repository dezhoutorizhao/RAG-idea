# External Review Packet

Generated: `2026-05-29T07:34:39.522621+00:00`

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
- Evidence manifest artifacts: `198`.
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
| `results\evidence_closure_status_v4.json` | `True` | 49321 | `818a74768d3d08ca40b895f5b4249b10885c088d7ebcf553efa50a47fde4f44c` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14724 | `f7604c0291e0e0cd63aab51ceed6a8474f5fa0f8e650d64abcdadd78be485380` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 46932 | `94a9ffef7fccf350cff1738eb112247caaef19437aea633fa3f4841f2c6e93d1` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `97fc9076407d526c4cb2142b7cc65fd9b7fb01e499b6c9420ecbc1200933685f` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `032c3acd4b1263de801dca3707e5f0f66ab37420466cc5a097af0fd8f45335f7` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `789b0173a5ce7b45870a256635f3948d034de19ce311eee51d0c4ca4365694ff` |
| `results\v4_claim_safe_target_selection_20260529.json` | `True` | 7318 | `ab13cebf95ccaa89eb13c851a1a93eea71079b2598762ebe676366ceeec6bd55` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `fcd5e91966036b8a69907ab299a9ec314ec35660044c39ca32d700025ce12d83` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `b16517cde51d67010447b968412295c33d82269f2558f710a86414835dc785c3` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `669ba6501eb43678b337c2820c3aee95bda93ac5e971721d3197cb19c2fb3553` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `0396840d6280d83c83a6729a4a0202cc546762555def7eb194005129e232de58` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `295ec13471ef1b709b3589d87ef5434991c4ed3c47a0f272e9798a57f7e0f51a` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `2f5b737c2109f8f430c6d808242e13321642ef0a9cc7ca5df41f7c974d178051` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `3246f13012a84b122534652634727bf6831df15d5157f57b1065d67a5a0d63d5` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `d219b41ba960531b404eb0de97de8870d259fc55643b7ed5987341958868d492` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17555 | `a9979fe24ec49c915028edddb0546a207a1ef677358d5b9ed9690df23355724a` |
| `results\human_audit_v4_batch_collection_20260529.json` | `True` | 4742 | `9c2b8cd0fc57e30ed7e731e4d7a0171ea7411ae5793c7733196fd5ff49715f84` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
