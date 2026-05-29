# Current Evidence V4 Reproduction

Generated: `2026-05-29T01:25:57.428379+00:00`

Ready for NeurIPS main claim: `False`

## Commands

| Step | Ready | Outputs |
|---|---|---|
| summarize_human_audit_v4_status | `False` | `results\human_audit_v4_status_20260529.json`<br>`results\human_audit_v4_status_20260529.md` |
| run_human_audit_eval_v4 | `False` | `results\human_audit_v4_eval_status_20260529.json`<br>`results\human_audit_v4_eval_status_20260529.md` |
| summarize_fever_cp_transfer_sweep | `False` | `results\fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json`<br>`results\fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.md` |
| summarize_end2end_selective_rag_proxy | `False` | `results\end2end_selective_rag_proxy_summary_20260529.json`<br>`results\end2end_selective_rag_proxy_summary_20260529.md` |
| summarize_v4_strong_baselines | `False` | `results\v4_strong_baseline_summary_20260529.json`<br>`results\v4_strong_baseline_summary_20260529.md` |
| summarize_v4_failure_taxonomy | `True` | `results\v4_failure_taxonomy_summary_20260529.json`<br>`results\v4_failure_taxonomy_summary_20260529.md` |
| export_v4_case_gallery | `True` | `paper\case_studies\v4_case_gallery_20260529.jsonl`<br>`paper\case_studies\v4_case_gallery_20260529.md`<br>`results\v4_case_gallery_summary_20260529.json` |
| build_clean_sufficiency_misleading_figure | `True` | `paper\figures\clean_sufficiency_misleading_v4_20260529.csv`<br>`results\clean_sufficiency_misleading_v4_20260529.json`<br>`paper\figures\clean_sufficiency_misleading_v4_20260529.svg`<br>`paper\figures\clean_sufficiency_misleading_v4_20260529.md` |
| summarize_v4_anti_shortcut | `True` | `results\v4_anti_shortcut_summary_20260529.json`<br>`results\v4_anti_shortcut_summary_20260529.md` |
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
- End-to-end selective RAG evidence is currently proxy-only and mixed on some Hotpot v4 variants; it is not a full CoRM-RAG reproduction.
- V4 strong baselines are present, but CSRM-Rule loses or ties the strongest learned/context baselines; main claims must use calibrated/proxy wording with caveats.

## Claim Policy

This one-command reproduction rebuilds the current evidence gates and closure artifacts. It does not fabricate human labels, does not delete server data, and does not complete full CoRM-RAG reproduction.
