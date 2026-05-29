# External Review Packet

Generated: `2026-05-29T08:23:28.846627+00:00`

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
- Evidence manifest artifacts: `226`.
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
| `results\evidence_closure_status_v4.json` | `True` | 49321 | `5957c7b55d76c0fe5b0cbf692a93a0325604bdbd3d3a3e3cd2e3832ebb628b18` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14724 | `89ae6c58628690bfae7ae56d4bd4fac074d2a4a4b93893aa5254a26c6a8009ca` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 53008 | `c5d93e5942b4da4ffb7fad719fb340b83af3d7d487d48ff40df912a6277fe4ca` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `1fed0d7926b109f5ad4a3ac9cc0984ed5da7b840c8b06ae10a3bd7d4d90164e2` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `58867ac43d2cc715538fc1ab346ba3898a98962480b748d999144c28e1887fac` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `2dad023896781667c5d026a87c5802b27c5bccf3e494ece87b5584cdbc223984` |
| `results\v4_claim_safe_target_selection_20260529.json` | `True` | 7318 | `607ab3740eade0ae032ade43f15605a91089e6a74480e01babdd3b5a96dab7e6` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `33ce6c6f36ca02a3bc22b69ae570f8d05067ec55582d185bfd654555ad47bc4f` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `79ad6fea2d399ec5c90d8ddcbd1339b995dc48176542aa7a8cf8b532d445bb02` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `405a7236cdec41e104df573d5ca4c4ffa03b1eb5bc2a6f68a9db49b60195d7ec` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `c728447467dc12c35f77d2892d89b226571875b1236ce99a8339737e8223d2de` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `ec0584901366957c0c7b99328374b82245d3a2ae9c835083d9090257cf760f36` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `8e075ad2b515884692c7d020f6b102d838613991bcef784093588ff19d745abb` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `3246f13012a84b122534652634727bf6831df15d5157f57b1065d67a5a0d63d5` |
| `results\remote_home_storage_status_20260529.json` | `True` | 12190 | `d529ece561d4322c73df786bc23e482e2c3950d02db667ab05511ea57f645ffa` |
| `results\remote_ext4_prepare_dryrun_20260529.json` | `True` | 5843 | `71111d38d9457dc9a5ce5531cdd825948d7888d68e3e5cc63b0b246686f08601` |
| `results\remote_ext4_prepare_dryrun_20260529.md` | `True` | 1734 | `ca3bbbb1e00ba180ca6dec9f28e319e42d39e29ba55ff2e852a96467f6e62666` |
| `results\remote_storage_cleanup_plan_20260529.md` | `True` | 3669 | `a26c0c309ec8a84baa25d26cb02ec06b54d0abcd97743977b8dee3c1f30d5899` |
| `results\remote_cleanup_candidates_20260529.json` | `True` | 38761 | `e15260c3d8f95d2715972e6c927ca827f60a78e95cc767366a00e896637718aa` |
| `results\remote_cleanup_candidates_20260529.md` | `True` | 4266 | `e2ddd08c863e2770dc23875d6cceeda3c1cf74a244d5f04942d21a6d8f685535` |
| `results\remote_ext4_cleanup_guarded_plan_20260529.json` | `True` | 1955 | `b44decb70c0ded5c908cad493c50823aeef621ed596426df4a3e57f79da2e011` |
| `results\remote_ext4_cleanup_guarded_plan_20260529.md` | `True` | 1621 | `1248591274c56256e722a5ae061feafcc1130c9a225402ac249ea65f08d5f8bd` |
| `results\remote_home_storage_status_latest.json` | `True` | 12190 | `7318441dc62207444b4e66b99f07730f7150855d99ee7cbeef3444832efc1c75` |
| `results\remote_ntfs_storage_status_latest.json` | `True` | 14189 | `5c70d0708c43e9f9dc3095bf012577cb15049b1974b5eddba632d60e103790ab` |
| `results\remote_full_corm_launch_gate_20260529.json` | `True` | 2847 | `1db494f68e4b6f92604d6d64357326a01426bcbc4e79c699e83a34b8ac7888d6` |
| `results\remote_full_corm_launch_gate_20260529.md` | `True` | 1348 | `6c8d6421703286d4c9eddbb9b7ea571e216e15f071a9de582d8ee3a40c783873` |
| `results\corm_reconstruction_plan_ext4_20260529.json` | `True` | 15313 | `a46b280db45636f2a1d7c30cf4e1c9433e14ad3581cc7df4cb681a4fba6dd4e9` |
| `results\corm_remote_scripts_ext4_manifest.json` | `True` | 1217 | `3162cdc7ce709777e29e6ea3003c061309ed743ec151db846b090f69996d0bfe` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `e4846cc7f7b327de36a5a73027d9d038c01ec085117788999360ffa3000fcd88` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17555 | `db6fb92a41ef1facae7013116e0595f9f10fe1484b0e7d9157bd5d066ca24111` |
| `results\human_audit_v4_batch_collection_20260529.json` | `True` | 4742 | `ebc112507783ea30dffeec93e08d37ec7538f170df1dc0565f4d793fbd6dc03f` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
