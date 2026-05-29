# External Review Packet

Generated: `2026-05-29T08:13:58.670595+00:00`

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
- Evidence manifest artifacts: `212`.
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
| `results\evidence_closure_status_v4.json` | `True` | 49321 | `5a04378622b54ed30a921e496447b99ac4d50a84d0192c69ba2475f415c44da4` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14724 | `f2dc2a2d441aa3f0df8f4bb5706d73ab3a8869477afae6bce0c8cfe9bf16ccb0` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 49949 | `c491ddd2937988e54d38c48e08401df0a4ad32f5cdbbb206d55ca1b32ecb8869` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `1c6dc87d42584bab28414eefdc2da598b66382ee4ba3b661badfe81a2846f98e` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `217978c56afc0895b914bd2ebeb85371c6e92dd1ead1b2c4f679a2c1e62bf656` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `3de0e7914e1555519764f139ee596cf023e8412a71754bea65c8bf7d932b9804` |
| `results\v4_claim_safe_target_selection_20260529.json` | `True` | 7318 | `0bd93a0aaee29975c1c8551e8fcde5dadcd2cf91cbfdbea762ede6b9c8b161bb` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `7f16f0ffc8e205907445f41f31dd61091c89f282fe5bc4708dc9f72d5a026ab8` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `78ad226d9fce92617e33cef92ce8b889715dc1377243555a09117cbf89618be3` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `1a9653a91c3256df8b9c6b20b592da0e4d056517ff96c53c0c8b4d2d05c02b10` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `8c13c7d5b739e99c10a77fbac9476cc1bc87fcbd0c045498870494c536b9a8ff` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `7d3da263d8f72e96fd1d730af80d9f3d15291cbd82197b000ce170757f2de384` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `ca430d7dd95deb0b33d77b21b1e43146286a9600b5dbcadeb889964152134dc6` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `3246f13012a84b122534652634727bf6831df15d5157f57b1065d67a5a0d63d5` |
| `results\remote_home_storage_status_20260529.json` | `True` | 12190 | `d529ece561d4322c73df786bc23e482e2c3950d02db667ab05511ea57f645ffa` |
| `results\remote_ext4_prepare_dryrun_20260529.json` | `True` | 5843 | `71111d38d9457dc9a5ce5531cdd825948d7888d68e3e5cc63b0b246686f08601` |
| `results\remote_ext4_prepare_dryrun_20260529.md` | `True` | 1734 | `ca3bbbb1e00ba180ca6dec9f28e319e42d39e29ba55ff2e852a96467f6e62666` |
| `results\remote_storage_cleanup_plan_20260529.md` | `True` | 3669 | `a26c0c309ec8a84baa25d26cb02ec06b54d0abcd97743977b8dee3c1f30d5899` |
| `results\remote_cleanup_candidates_20260529.json` | `True` | 38761 | `e15260c3d8f95d2715972e6c927ca827f60a78e95cc767366a00e896637718aa` |
| `results\remote_cleanup_candidates_20260529.md` | `True` | 4266 | `e2ddd08c863e2770dc23875d6cceeda3c1cf74a244d5f04942d21a6d8f685535` |
| `results\remote_ext4_cleanup_guarded_plan_20260529.json` | `True` | 1955 | `b44decb70c0ded5c908cad493c50823aeef621ed596426df4a3e57f79da2e011` |
| `results\remote_ext4_cleanup_guarded_plan_20260529.md` | `True` | 1621 | `1248591274c56256e722a5ae061feafcc1130c9a225402ac249ea65f08d5f8bd` |
| `results\corm_reconstruction_plan_ext4_20260529.json` | `True` | 15313 | `a46b280db45636f2a1d7c30cf4e1c9433e14ad3581cc7df4cb681a4fba6dd4e9` |
| `results\corm_remote_scripts_ext4_manifest.json` | `True` | 1217 | `3162cdc7ce709777e29e6ea3003c061309ed743ec151db846b090f69996d0bfe` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `500d4f5b1a24cbefa063fb63120bff6cf5942cc7b772a3a67e4d74ebff9e3135` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17555 | `c77b6169b1f3961a8ed6e2ee2290ce8c42a22258e8021ca132d63fc8d433b97c` |
| `results\human_audit_v4_batch_collection_20260529.json` | `True` | 4742 | `f21036742afd064e922627ddada747bab9f0480606de7a23e4f832a707bfddf2` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
