# Current Evidence V4 Reproduction

Generated: `2026-05-28T18:53:01.149343+00:00`

Ready for NeurIPS main claim: `False`

## Commands

| Step | Ready | Outputs |
|---|---|---|
| summarize_human_audit_v4_status | `False` | `results\human_audit_v4_status_20260529.json`<br>`results\human_audit_v4_status_20260529.md` |
| run_human_audit_eval_v4 | `False` | `results\human_audit_v4_eval_status_20260529.json`<br>`results\human_audit_v4_eval_status_20260529.md` |
| summarize_evidence_closure | `False` | `results\evidence_closure_status_v4.json`<br>`results\evidence_closure_status_v4.md` |

## Gate Summary

- Human audit v4 ready: `False`.
- Human audit v4 eval ready: `False`.
- Human audit v4 pending labels: `300`.
- Human audit v4 evaluated packs: `0`.
- Full CoRM reconstruction ready: `False`.
- Remote storage ready: `False`.
- Claim verifier passed: `True`.

## Blockers

Human audit:
- Human audit v4 packs are prepared for Hotpot semantic-swap blind200 and FEVER structbalanced blind100, but adjudicated labels are pending for all 300 items.

Non-human:
- Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts; an ext4 cleanup path exists but needs explicit approval before deleting logs/caches.
- FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.
- Independent external review has not been rerun after the latest storage-status update.

## Claim Policy

This one-command reproduction rebuilds the current evidence gates and closure artifacts. It does not fabricate human labels, does not delete server data, and does not complete full CoRM-RAG reproduction.
