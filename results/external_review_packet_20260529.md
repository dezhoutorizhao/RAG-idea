# External Review Packet

Generated: `2026-05-29T05:37:10.587548+00:00`

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
- Evidence manifest artifacts: `141`.
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
| `results\evidence_closure_status_v4.json` | `True` | 35843 | `b806073fa7086f84fcad87bac5c436104911e9f254af76119513c1d4ced2efe7` |
| `results\neurips_readiness_matrix_20260529.json` | `True` | 11968 | `c6e791a7bc12846e46647be023301f9b829a7657c255216a9f3a41b0e0c448ac` |
| `results\v4_evidence_package_manifest_20260529.json` | `True` | 33108 | `a0f18c3bd47f3798e3a7d42f3011ff158b77599a1e93639326c743ea686f7224` |
| `results\text_only_verifier_status_20260529.json` | `True` | 4152 | `00703658895912ea0f19733d5495b17cc480ea0b096adbd09f8dc399e1e3ef33` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | 62689 | `4debcac5620bdea32e272134bf8304dafc556a098a9db5b4090cb12cc4e4947a` |
| `results\v4_calibration_quality_20260529.json` | `True` | 25694 | `218ce3b3712b79e5cf608ad0251d841ffe1afaa43ad7d5070533ae5f1be7d3c9` |
| `results\end2end_retriever_generator_matrix_20260529.json` | `True` | 52753 | `962355c722e2fac072f0c0a00bf9c324e6c88530e658be08fd92032518773fb6` |
| `results\end2end_risk_coverage_curves_20260529.json` | `True` | 130245 | `6daf70d1926e1d9e4f88270ace5cb47920497964f911c0019b44a04affc7f0d4` |
| `results\end2end_target_risk_coverage_20260529.json` | `True` | 30644 | `d0891e4a7f3710cde789688611c3759e7cbc399167a2513d0dfe2a0bf7d3f29e` |
| `results\remote_storage_status_20260529.json` | `True` | 14189 | `99f9144bc129a4635f4083a47e6f57129aec1eef4194e4ced49f864c36ef42c6` |
| `results\human_audit_v4_status_20260529.json` | `True` | 9104 | `9382df70b54b3413e6dd64c70b17e5900aa48ca69bcc83c212fdba19fb7ac003` |

## Reviewer Output Contract

Place the independent review response at `results\external_review_response_20260529.md`. The response should state whether the current claim ledger is acceptable, list any unsupported claims, identify missing experiments, and give a final accept/reject recommendation for NeurIPS main-track readiness under the current evidence boundaries.

## Claim Policy

This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.
