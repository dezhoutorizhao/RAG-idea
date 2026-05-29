# External Review Packet

Generated: `2026-05-29T07:05:32.344823+00:00`

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
| Human-audited orbit labels | `blocked` | Assignment batches ready: True; batch collection complete: None; pending labels: 1300; cannot claim human-audited results. |
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
| `results\evidence_closure_status_v4.json` | `True` | 47504 | `bfda775700571e2bcd3d748b0b49a517f94b0ab15ad019eb089e0110076f9301` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 14534 | `f87a66a46765c7610aa7634781bd79b5db542a08fa2ec2d6c3c2906658dc0d19` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 44286 | `5f72e603c525a0ba7bb5817cff0f664356f9659dd92c50f955ed508a9557ae01` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4153 | `2fca0442f6c55a7e7d302b906b7944283f083b04a886d6b6b1fdebdf197e28ff` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `aa8c5a8a9fc1795df6d0fb01a71484a9f55697c8db25b5dd541fec02ed221a5b` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `cdd48bf8e53d181dc0bdbc98dcd5f7664dc88f8f835d9de77b5f9f0aca163ac3` |
| `results\risk_control_abstention_baselines_20260529.json` | `True` | 11626 | `19a4a839a367f8e22ae06352c517c9b17e334ee7fbb3ede70b2f4873747c4a28` |
| `results\theory_formalization_status_20260529.json` | `True` | 1761 | `46fe26d2ca8e875b5b10806b14f34b604be81304570845e7d347487e296dc0c6` |
| `results\novelty_audit_20260529.json` | `True` | 5760 | `e3856ff5e4417365c2fd0ac18e1870214100472dc58d087109a390e8eb7e6580` |
| `paper\sections\formalization.tex` | `True` | 2869 | `4a9985e6c1156ba7209df22ee2527d76300e696b3bc0ce6560773d07e6018df2` |
| `paper\sections\theory.tex` | `True` | 3841 | `5c04e9b9ae97e0b9ccbce85ef0734c5887044a9a808975a452d8dcd80f89925d` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `beaefb4d3c8933c385383211eff9ad850d610b40154360533125e9d1b4846fb5` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `224b93d35b35ba0996849e2b17a8a2cf3f14fd82c5dfcd9b35a3823960ce7624` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `c9e3a7c925bb672e563d32520c86e496edfaa47630ed965119f5c0772800e455` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `0c12cbd3bf28ee85de366d1a6cbe936dc06e1061e3ca88c1efcc6e2462b6e474` |
| `results\human_audit_v4_paper_pack_status_20260529.json` | `True` | 4984 | `488b131a18440478e16444f604252d26234ff24c999ab293ca223430072f1d70` |
| `results\human_audit_v4_assignment_batches_20260529.json` | `True` | 17555 | `b24b80871c7682b705f5fcfd1f8b9cacaa1d2d298b4f50a3d54326db3d5344f4` |
| `results\human_audit_v4_batch_collection_20260529.json` | `True` | 4742 | `1c4b3972ad936dd715e56545e735cbdf9299a487617aec104e0ee030d2458577` |
| `results\human_audit_v4_status_20260529.json` | `True` | 13342 | `6c1147bdc32e6fbb51c99364a38eec82eae403cf4bc97ed219ed64e8f753232b` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
