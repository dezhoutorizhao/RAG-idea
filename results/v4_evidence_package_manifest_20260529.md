# V4 Evidence Package Manifest

Generated: `2026-05-29T01:21:06.119321+00:00`

Package status: `complete_with_known_blockers`
Ready for NeurIPS main claim: `False`
Missing artifacts: `0`

## Gate Summary

- claim_verifier_passed: `True`
- full_corm_reconstruction_ready: `False`
- human_audit_v4_eval_ready: `False`
- human_audit_v4_evaluated_pack_count: `0`
- human_audit_v4_pending: `300`
- human_audit_v4_ready: `False`
- remote_storage_ready: `False`

## Claim Verification

- Passed: `28/28`.
- Failed: `0`.
- Allowed/disallowed claim counts: `9` / `6`.

## Artifacts

| Path | Exists | Bytes | SHA256 |
|---|---:|---:|---|
| `results\current_evidence_reproduction_20260529.json` | `True` | `4109` | `9cffdf383b0f07dcf4ddb761a8f7576b1a156b2582287d060a51ce220692ede7` |
| `results\current_evidence_reproduction_20260529.md` | `True` | `3204` | `3eebb529e45f9963d5526d4efea5797312fd356057ff651d5dd7c488e0563eaf` |
| `results\evidence_closure_status_v4.json` | `True` | `20656` | `19eee7de1b0db572adfd68f6f998fbb318a103f24d7227e31868ed62b59ce3eb` |
| `results\evidence_closure_status_v4.md` | `True` | `10439` | `44b7a343f9a830a28ae4868205205ef916477a5cb6c126c43c7ad27506b92aee` |
| `results\human_audit_v4_status_20260529.json` | `True` | `5073` | `9c730826406716ab8f3fb7c417bca1626f06e418628e8971765d64cf4d73c9d1` |
| `results\human_audit_v4_eval_status_20260529.json` | `True` | `2528` | `3703442aa638c9b6ea69f245604e62a170ab871173452907e26d4857f9a8f3ba` |
| `results\fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json` | `True` | `8163` | `ece8d611ab0a5e28680eb178d6e5426f444fe2ac520b2fbe5a6e25bd1c5c4d42` |
| `results\end2end_selective_rag_proxy_summary_20260529.json` | `True` | `13211` | `09fcc2daa87d707cf74785f1a24e50c2fceebab40ddd4857f0bc61215e601810` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | `43608` | `2017ede5855a1426d7b7dd6fa93bf2e4f31110616cee09d6e3aebf0baa827152` |
| `results\v4_failure_taxonomy_summary_20260529.json` | `True` | `46069` | `4ca6ace1818666a470af7e10bbd83e0e6a8f30f697829f45e617810213b587cb` |
| `results\v4_case_gallery_summary_20260529.json` | `True` | `1882` | `546d175e231bcceae11b1c11dcfafb527787afdda956d0a9074b55ecfe9eadc7` |
| `results\clean_sufficiency_misleading_v4_20260529.json` | `True` | `2465` | `06d85a00fcc5da698310d85ef5f270c46b235436fa3efb9b2d7f3298227a49ee` |
| `paper\case_studies\v4_case_gallery_20260529.jsonl` | `True` | `191730` | `f03232de577d772efa6cb88bb54c7c9e8b3d48881493364f7ac052c74dbe4a59` |
| `paper\case_studies\v4_case_gallery_20260529.md` | `True` | `27403` | `c2c4c7909e6185df0d701c9c1a31a30a0f18ce27b7c8102dacd19b0ce5d5b1c6` |
| `paper\figures\clean_sufficiency_misleading_v4_20260529.csv` | `True` | `3097` | `ded3232932e843f23579e5f85768c2fe16a3e90f18f920532564c3def0c2ab5e` |
| `paper\figures\clean_sufficiency_misleading_v4_20260529.svg` | `True` | `6083` | `a354e94977a8ffcf4d32cc4e560521006ab552b043189b98ea2dfd5103bd73f3` |
| `paper\figures\clean_sufficiency_misleading_v4_20260529.md` | `True` | `914` | `f3457c2c64e37b73a7a8e23045c6ed4eeab39b1b168c9516562a0a93907965a0` |
| `experiments\reproduce_current_evidence_v4.py` | `True` | `13343` | `fda86d1a8c1030b193e4d8dc612418e69a73e34c3aafa7e6b15e3f650c382779` |
| `experiments\summarize_evidence_closure.py` | `True` | `44282` | `e601fc5bf92d63f6962f4f4fbf600439bf0446dc9957c5f86aa3105c5c4b1379` |
| `experiments\summarize_v4_failure_taxonomy.py` | `True` | `11135` | `f5eb0a9e034ef89964e4b51c7069b149bd36156705da4bda2f14f8f1948e3af1` |
| `experiments\export_v4_case_gallery.py` | `True` | `7379` | `1751ee166e02c37ab4d185e0b38bbd04f9269ca162e251ae39e6e6aa49b1f5b7` |
| `experiments\build_clean_sufficiency_misleading_figure.py` | `True` | `13978` | `6d7c26b097a0f9e69a8dc87c3c38f7fa8d95255e5bbf9efbf39373a213f1f6c7` |

## Remaining Human-Audit Blockers

- Human audit v4 packs are prepared for Hotpot semantic-swap blind200 and FEVER structbalanced blind100, but adjudicated labels are pending for all 300 items.

## Remaining Non-Human Blockers

- Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts; an ext4 cleanup path exists but needs explicit approval before deleting logs/caches.
- FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.
- Independent external review has not been rerun after the latest storage-status update.
- End-to-end selective RAG evidence is currently proxy-only and mixed on some Hotpot v4 variants; it is not a full CoRM-RAG reproduction.
- V4 strong baselines are present, but CSRM-Rule loses or ties the strongest learned/context baselines; main claims must use calibrated/proxy wording with caveats.

## Claim Boundary

This manifest verifies that the current evidence package is present and hashable. It does not convert pending human audit, failed storage, proxy-only end-to-end results, or negative strong-baseline evidence into NeurIPS-ready main-claim support.
