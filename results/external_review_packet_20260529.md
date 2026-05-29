# External Review Packet

Generated: `2026-05-29T07:59:36.854259+00:00`

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
- Evidence manifest artifacts: `206`.
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
| `results\evidence_closure_status_v4.json` | `True` | 49321 | `b29cf5b602967e6102a5b9bb79469ed86281f95efe8dcc9a91bb106cffd75a08` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14724 | `aa20f0a78e48afeec8272a1ed60855e37debe677c0bb45f6a2562b31012e9931` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 48647 | `32d25fecb4664cdad3bfe888613c624b5b342eb0158c575945950961db105d6c` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `eb02f6a44a06f8ee5fce038e86114cea88993a40f2d47d563ad7c2047bfda1c9` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `8bfa7df2296115705830da68a901a5c03c7b4e8d9b2e2dc83c7fc47e22da746e` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `203f4be3f66d15c20c7319e34ae3b3c79e542d674ac148dfc030cb1c783c1b50` |
| `results\v4_claim_safe_target_selection_20260529.json` | `True` | 7318 | `af7bf657b385010d05ad0e599636061afee10cd23518b445f7e92287720d166b` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `1a8fefdad52a410daec9e28a8c4daf73e37cc150095a89af5b7e358765d3143b` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `7e23443bffcd02558422d8f5d940f38bd0361310fba015a67f463b495d506864` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `0e71db8ede99789db4c2aec898f5503985a009a525726509e995eb4ab0745588` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `f5165537641047ef8467b75bd645d6468236dda82ea5f8ff6b90917c7d5e2cfc` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `8fcdcf1909285af18578e150b6a06f23d5ff228ad889ee89615c0b8b88ec2125` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `08950fa5030b065f1aef5e2c02a2486a93efe2fa13a0d29ad8ae6ff7861e6512` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `3246f13012a84b122534652634727bf6831df15d5157f57b1065d67a5a0d63d5` |
| `results\remote_home_storage_status_20260529.json` | `True` | 12190 | `d529ece561d4322c73df786bc23e482e2c3950d02db667ab05511ea57f645ffa` |
| `results\remote_ext4_prepare_dryrun_20260529.json` | `True` | 5843 | `71111d38d9457dc9a5ce5531cdd825948d7888d68e3e5cc63b0b246686f08601` |
| `results\remote_ext4_prepare_dryrun_20260529.md` | `True` | 1734 | `ca3bbbb1e00ba180ca6dec9f28e319e42d39e29ba55ff2e852a96467f6e62666` |
| `results\remote_storage_cleanup_plan_20260529.md` | `True` | 3669 | `a26c0c309ec8a84baa25d26cb02ec06b54d0abcd97743977b8dee3c1f30d5899` |
| `results\remote_cleanup_candidates_20260529.json` | `True` | 38761 | `e15260c3d8f95d2715972e6c927ca827f60a78e95cc767366a00e896637718aa` |
| `results\remote_cleanup_candidates_20260529.md` | `True` | 4266 | `e2ddd08c863e2770dc23875d6cceeda3c1cf74a244d5f04942d21a6d8f685535` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `10737066ba49482f90a94f04cb222b1a863bcbc79695ba8eb5b7f3d75f4cc892` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17555 | `e410c987428d2b6bba94e1fe474253d1f0de93380e892bb3805704d30d84e160` |
| `results\human_audit_v4_batch_collection_20260529.json` | `True` | 4742 | `751ab2644f1debb42bc9d2868f2723e576020e2bc27cafa6c389e60590709817` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
