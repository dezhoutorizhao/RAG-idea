# External Review Packet

Generated: `2026-05-29T07:52:23.076821+00:00`

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
| `results\evidence_closure_status_v4.json` | `True` | 49321 | `ae4b2dee398b47e0659d0ac351eead0026256fe8c2da31376a8a536d06f23dc3` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14724 | `7a5eab3c4b0023a3cff9e923e58f442dcdf831347621cc9676fff93944081d7e` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 47785 | `5d7111e13c28b6bd0e5b52e0e51d2ca49879c228a2f4eb6ae2487eac1ca0403f` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `635d4006e51f9d337b39445ef08d245bf143a47348718ae6874843b57729f745` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `fc21c48e17872fa7a79b46e94e0e9d7d7c831d0114485289eb4a41b8bcf60ca1` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `efdc82ec6d8da85dd9ed3fc1fa18f574a9cd893786800f7695cc2a326293c629` |
| `results\v4_claim_safe_target_selection_20260529.json` | `True` | 7318 | `7c828c77d345e7a8f61e5b82082a9ac15bfe2971628a25dcc5e84d89f666d16e` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `108f2625b9851c54a33ecee602ad38fa6df89f88c2f56e1919fb19b924c8767b` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `c941c428358570e0a96cccf1411e0f5eeb35012d91c2b3bd9472a338384e7841` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `e7af4d4605c99def0bbe3586cd4d682897942619eab978f2089a916c7a70d844` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `d09bf3fbc06b0c67202074cf18f5fb24fe69049ffb955571f15746e126ea5eca` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `6d288e6e97e84c20799a0caf0c65d886ea34a6d8223902781bd34ffa22581a49` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `c11ea3d86999b55187e042c5589d025b494a26681f91671c05f1ce43034bc662` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `3246f13012a84b122534652634727bf6831df15d5157f57b1065d67a5a0d63d5` |
| `results\remote_home_storage_status_20260529.json` | `True` | 12190 | `d529ece561d4322c73df786bc23e482e2c3950d02db667ab05511ea57f645ffa` |
| `results\remote_ext4_prepare_dryrun_20260529.json` | `True` | 5843 | `71111d38d9457dc9a5ce5531cdd825948d7888d68e3e5cc63b0b246686f08601` |
| `results\remote_ext4_prepare_dryrun_20260529.md` | `True` | 1734 | `ca3bbbb1e00ba180ca6dec9f28e319e42d39e29ba55ff2e852a96467f6e62666` |
| `results\remote_storage_cleanup_plan_20260529.md` | `True` | 3157 | `34ed3083f59843c94f40ae3abda0f1e892e14e8186556c713fd5edb7c33d5399` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `a178f167f64dd190f598e7f8b3d82dd69a3ddf33f0492f70f636355e5aa79803` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17555 | `6e73084ecd03781fc4c6edb801c25f523f92cdaa96a414a4bebf8b951fa8f7d5` |
| `results\human_audit_v4_batch_collection_20260529.json` | `True` | 4742 | `5fcc4d03f8a16cb288fb6cb119e14f72428731c355d349694fdefca1a24a9edb` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
