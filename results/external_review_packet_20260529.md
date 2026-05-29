# External Review Packet

Generated: `2026-05-29T06:02:39.591861+00:00`

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
- Readiness status counts: `{'blocked': 3, 'fail': 1, 'partial': 4, 'pass': 4}`.
- Evidence manifest artifacts: `144`.
- Evidence manifest missing artifacts: `0`.

## Hard Blockers

| Requirement | Status | Boundary / next action |
|---|---|---|
| Human-audited orbit labels | `blocked` | Pending labels: 300; cannot claim human-audited results. |
| Full CoRM-RAG reproduction | `blocked` | Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts. Latest storage probe shows 322.1 GiB available and target_write_probe_passed=False; 6 target-dir file probes failed while writable fallback dirs are ['/home/syk', '/tmp', '/dev/shm']. |
| Independent external review | `blocked` | External review packet is ready, but no independent review response is present; place the response at `results\external_review_response_20260529.md`. |

## Negative Or Partial Evidence

| Requirement | Status | Boundary / next action |
|---|---|---|
| Text-only semantic verifier | `partial` | NLI cross-scorer evidence is directionally positive against required weak baselines, but LLM-NLI correlation and human-label text-only evaluation are not ready. |
| Strong baselines and equal-budget controls | `partial` | Baseline package exists, but CSRM-Rule has losses/ties against strongest learned/context baselines; coverage/budget matrices still mark faithful CoRM as partial, clean-only controls as lower-budget, and LLM judge scores as missing. The LLM judge request pack is ready, but no API-backed score artifact exists. Template multi-sample self-consistency and shared calibration-threshold selection are auditable, but test risk/coverage remains mixed rather than all-win. |
| End-to-end selective RAG | `partial` | Proxy evidence now covers two local retrievers and two generators, but remains mixed and is not a full CoRM-RAG Wikipedia retrieval-generation reproduction. The risk-coverage and target-risk coverage artifacts summarize lower accepted-error risk at fixed coverage and higher coverage at fixed target risk, but do not remove the full-reproduction boundary. |
| Calibrated orbit risk model | `partial` | Calibration-quality artifact shows Brier wins 6/6 against rule/minimax references, but ECE wins 4/6. This supports empirical calibration-quality wording, not a formal risk guarantee. |
| Risk-control claim | `fail` | Hotpot-only empirical transfer is positive; FEVER 0.20 target is negative, so no general/formal claim. |

## Source Artifacts

| Artifact | Exists | Size | SHA256 |
|---|---|---:|---|
| `RAG-idea改进.md` | `True` | 49684 | `abea2cc9e252308bd254f974d86cbd89910eecfeab3ee4a55ab14fc5dee71242` |
| `CLAIMS_LEDGER.json` | `True` | 53391 | `f433d29dc1ca4d67e4097403e7e84c6adc8ec7de7c9785d1e3111a15d699d244` |
| `results\claims_verification.json` | `True` | 62860 | `b3051aff04cf1c2efe13719f0587dca08c1af41ba043266c8fdd1b7c3cde1a6e` |
| `results\evidence_closure_status_v4.json` | `True` | 36022 | `ba75955c63774286d0b21b86975ab1d0fe419718fafb3df1fe5d23abc75ce4a5` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 11968 | `eaf5532a68fe92103ea8f176b82cecfbfaffc7b977f255d713d930b304d21140` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 33840 | `e8995bb68e08bcec8cdb9337ef58603617cd160f146202598315e90bc5579cca` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4152 | `2797f56788e9eb7bc9bc1a7654d22e772b943f5791440221dbd763fceaaa7b50` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 73809 | `0a6340030864c014149d77110e01116eb2e2ba8f0efe67eee0be92b04495acbf` |
| `results\v4_calibration_quality_20260529.json` | `True` | 28533 | `c294f596311f7278c3719a3de0880bf9bd5198ceb4c5c71a0603d1ac01234794` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `112f80a56317e800dfccdb141f91fda1bc6296ac6b744cec1a5582183a71991d` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `debf5cd39a03c5847960b4487bad9243bfab05b82e7efa4dbad9a4d3d6d97c32` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `e0a6cd484a25db8d2318c148abc419df240de40f572813046ce5591ee8e7ba61` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `99f9144bc129a4635f4083a47e6f57129aec1eef4194e4ced49f864c36ef42c6` |
| `results\human_audit_v4_status_20260529.json` | `True` | 9104 | `9382df70b54b3413e6dd64c70b17e5900aa48ca69bcc83c212fdba19fb7ac003` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
