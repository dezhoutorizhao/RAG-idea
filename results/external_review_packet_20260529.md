# External Review Packet

Generated: `2026-05-29T07:21:53.961369+00:00`

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
| `results\evidence_closure_status_v4.json` | `True` | 49321 | `f02355d7890f8c15bd6d0f4cbba303c6c71b083cee7976cd94649712e8d442be` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14724 | `da668978478bb5b356de0b70b0feeceb15a8f304b17fe086e46ae53097c6e974` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 46932 | `8009a5c54c145c7b6422379903a8a3b638e7519ea35bb7afeddfc030433ecff5` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `eaf10aa4d96b394067e768b77de5eb0cb0dcca4b87f2ddfc181921a5c34dfaad` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `6f5083c7448256a271102f28b9be06a785acbc5bfce6524a2065dcdff06cebe3` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `826ba96d991d599fd8914cb1edce58c0139c3ca10d42d4b9b1804716adbd5ac0` |
| `results\v4_claim_safe_target_selection_20260529.json` | `True` | 7318 | `70e69c8789c14aded2c9b7d98e29361b97756fcf9b05e678dadba3fce03c543f` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `de71544a8d610d635b1595d8cd6b2613f1afb4c8dd058c136df6833a0652f008` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `56eb46f749b095bccf5161ffed864e5989f3954783b5a82de77e858b425079db` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `5263d922fe972412d98f73422e8cf474b9e54689dde54f66f2464c63927b3dcd` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `32fec538f3dac85137ec8d687bbb1f3074a6d11b455101d791abef9f977727ed` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `a498ae507f31e6c595742fc878600bcff801918250c29bc1a6bc224709070a76` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `135129397af70e1975ee496ab4bca7f23501eefd39d3e1962815b18a83c14095` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `3246f13012a84b122534652634727bf6831df15d5157f57b1065d67a5a0d63d5` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `7f666eb93642b0ea0f6fcd45508a5d72eb0f7d2aebeddd5fe25612d6f2df4d87` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17555 | `f51619874299d12f9105d4f110929378202b216b679c6d19774591edb4accc34` |
| `results\human_audit_v4_batch_collection_20260529.json` | `True` | 4742 | `7ed501876195db394bcc06ee8abbe3d3b3136d4da9436d8d5192fdd9646b911a` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
