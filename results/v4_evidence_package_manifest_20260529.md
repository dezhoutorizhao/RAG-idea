# V4 Evidence Package Manifest

Generated: `2026-05-29T01:13:35.814053+00:00`

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
- Allowed/disallowed claim counts: `8` / `6`.

## Artifacts

| Path | Exists | Bytes | SHA256 |
|---|---:|---:|---|
| `results\current_evidence_reproduction_20260529.json` | `True` | `3699` | `869a00121bbc5d73954e0014da2d7e1b30178ae8b6ceab4d12ae3b616a706e5a` |
| `results\current_evidence_reproduction_20260529.md` | `True` | `2899` | `63f8031d689905cb5f9ce518957bb204ae03a2b6a849e8964e7b89e8930e8e45` |
| `results\evidence_closure_status_v4.json` | `True` | `19454` | `7abeaf3eb2409ae9e56791e81e8647207f5a2e9fd8a5fd4c5e1da7c5c7177d3f` |
| `results\evidence_closure_status_v4.md` | `True` | `9668` | `b30af6a9bd61f915d872bd7c74fc5e95e78cf296203f28805deea37213a97e1a` |
| `results\human_audit_v4_status_20260529.json` | `True` | `5073` | `9c730826406716ab8f3fb7c417bca1626f06e418628e8971765d64cf4d73c9d1` |
| `results\human_audit_v4_eval_status_20260529.json` | `True` | `2528` | `3703442aa638c9b6ea69f245604e62a170ab871173452907e26d4857f9a8f3ba` |
| `results\fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json` | `True` | `8163` | `e4a4918da2be8442f6d8acdeea2c7c1e8cc40ddc3000ef8ac8b5a11eb4ec3e6b` |
| `results\end2end_selective_rag_proxy_summary_20260529.json` | `True` | `13211` | `f91909eacd99f969289fa81b40e1fe2a625809d5bdbcf295599edddbe86b793c` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | `43608` | `895529f53a14b666ab45238a29878302eac7bcf973d141004fca69b7a561176a` |
| `results\v4_failure_taxonomy_summary_20260529.json` | `True` | `46069` | `9e6893d1eac31e45fc06bad34c135fcf13164e415f7f9ddd24bfa9ff162b3af6` |
| `results\v4_case_gallery_summary_20260529.json` | `True` | `1882` | `4e14b4e16abdfa8ed8a17ce2a83f52e953039359febd56944e9a077426ccf377` |
| `paper\case_studies\v4_case_gallery_20260529.jsonl` | `True` | `191730` | `f03232de577d772efa6cb88bb54c7c9e8b3d48881493364f7ac052c74dbe4a59` |
| `paper\case_studies\v4_case_gallery_20260529.md` | `True` | `27403` | `e280c965878982dce6f0711f316f3d2b4e951f19faae1b3fb34c66852bb15052` |
| `experiments\reproduce_current_evidence_v4.py` | `True` | `12132` | `ef81b9cb100e1a55b8e68dbd82f2fb185b02294ae32166c7878fbb6ae92c555c` |
| `experiments\summarize_evidence_closure.py` | `True` | `41338` | `acc564f275db9b51041d18a76795492ac01e093cc45a43b39a96aeb3d2d012e3` |
| `experiments\summarize_v4_failure_taxonomy.py` | `True` | `11135` | `f5eb0a9e034ef89964e4b51c7069b149bd36156705da4bda2f14f8f1948e3af1` |
| `experiments\export_v4_case_gallery.py` | `True` | `7379` | `1751ee166e02c37ab4d185e0b38bbd04f9269ca162e251ae39e6e6aa49b1f5b7` |

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
