# External Review Packet

Generated: `2026-05-29T07:43:14.517920+00:00`

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
- Evidence manifest artifacts: `202`.
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
| `results\evidence_closure_status_v4.json` | `True` | 49323 | `2f8a357c37c2b4909c9a7ac68e3a30b8f22df54c2e6e3b3ac8394246080ab9a2` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14724 | `988dfdb71be41f5ea3b4fab4e26c760f7a4edf1de589591dbe07be8a4642f892` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 47787 | `5ed9ce83eaa9b4a02355fca2396ade2938f8cd1bd785d185480570b307b09119` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `196baf9b7e2824b0f1676e576932b262f65548feace02a23ffd6c74724d0c1e1` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `6de6021e690c41665e5cf4339ddacc679476d45e4c17c73f2010ca3f90c97fb5` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `3dc5a4589bbb682361069e1bfdc862e44459728efc52762bcbe47e9c5a2f4566` |
| `results\v4_claim_safe_target_selection_20260529.json` | `True` | 7318 | `afd172b24b22d1889d795134e31306f2995472fdbbb80bf71d8ab3fc68f70b07` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `f26618a7f5116c47862357175b1c474dc6af9aae377a744d3eba9396be86b2cb` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `975b9eb071c1ab3d21a8ddb14fa344067f08a235eafc8dcbc156fc515f23133b` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `77597a14dd04f281ea261c719bd77c5963ad6e492a6f5f491ff1900fd546656a` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `fa29a33dee1f2db125c4530b23da7a0d15f5dc7528cc7322e440b0fc06eeb798` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `cd618a088897733e4ac4de4a65cb002b2fde14435e5d1b8eb3ef1db7bea15fac` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `ddb70a449364b4a11faf7f1e79b7c04986545e866e5f865f51ef217073777296` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `3246f13012a84b122534652634727bf6831df15d5157f57b1065d67a5a0d63d5` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `e1b52d506528a96275c61da1480bd579555450d8c9b92b625f3051589ccab86c` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17555 | `c9528065ede0b0db36523f8dccd45b915206fb3331abaf9f297f6c6785106b93` |
| `results\human_audit_v4_batch_collection_20260529.json` | `True` | 4742 | `5753c328352d7e5e64e6ec37078feb055bcaa6d2d151dcc6ff9b3b287ab66bb4` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
