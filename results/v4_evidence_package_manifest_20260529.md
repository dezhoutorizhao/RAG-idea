# V4 Evidence Package Manifest

Generated: `2026-05-29T01:26:02.965139+00:00`

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
- Allowed/disallowed claim counts: `10` / `6`.

## Artifacts

| Path | Exists | Bytes | SHA256 |
|---|---:|---:|---|
| `results\current_evidence_reproduction_20260529.json` | `True` | `4337` | `9d86d8822542553f7f735fd6eca414bce9aabc002164f74350979e2984b41403` |
| `results\current_evidence_reproduction_20260529.md` | `True` | `3346` | `c707bc5f275ac158a7aef3c6ea83022cf333dd9920a9c6fcbf317072f6f6c0ec` |
| `results\evidence_closure_status_v4.json` | `True` | `21777` | `9dd50b5927055cae0002fbb442d5d600af03360a1f7ec8910cb826b75a45d435` |
| `results\evidence_closure_status_v4.md` | `True` | `11347` | `32f932f05c229eb51a466f954ec03fa5f4d7afa46922e354bf47f84106113599` |
| `results\human_audit_v4_status_20260529.json` | `True` | `5073` | `9c730826406716ab8f3fb7c417bca1626f06e418628e8971765d64cf4d73c9d1` |
| `results\human_audit_v4_eval_status_20260529.json` | `True` | `2528` | `3703442aa638c9b6ea69f245604e62a170ab871173452907e26d4857f9a8f3ba` |
| `results\fever_nearmiss_corm_v3_cp_transfer_sweep_summary_20260529.json` | `True` | `8163` | `d61a5108973fdb5b90ca0f9234cb499498c9c8293d8e9fc2f0d8065ab9b2cf5b` |
| `results\end2end_selective_rag_proxy_summary_20260529.json` | `True` | `13211` | `757cd314dddd60dd700b3567d9f9aca9bef9bf053be140e78c6a55216e36b87f` |
| `results\v4_strong_baseline_summary_20260529.json` | `True` | `43608` | `43ca117569b1f43e33e8f951b664f6ccab1c6b8e4b32cb0444bc82b775a35f7e` |
| `results\v4_anti_shortcut_summary_20260529.json` | `True` | `5006` | `33fcc576548d040c0f5fb10867b23a58a3f80908580a702310e942ef28c4747b` |
| `results\v4_failure_taxonomy_summary_20260529.json` | `True` | `46069` | `e7d42ab88372aa1051e939b83de271839e456d2a9eeac606f474aebcec82eaed` |
| `results\v4_case_gallery_summary_20260529.json` | `True` | `1882` | `243322aa972a7b1a2a1c9256c0038d8912d117f9cca6d3600c7147cd929ed427` |
| `results\clean_sufficiency_misleading_v4_20260529.json` | `True` | `2465` | `0485e3c18ac71760c6b2540774ecdf8defad1ba401ddc16159094fb66c4e1715` |
| `paper\case_studies\v4_case_gallery_20260529.jsonl` | `True` | `191730` | `f03232de577d772efa6cb88bb54c7c9e8b3d48881493364f7ac052c74dbe4a59` |
| `paper\case_studies\v4_case_gallery_20260529.md` | `True` | `27403` | `b7808eb9e81bf4f4d06f1073ef1436553ba0e022a248ade4065c189b3bd5701d` |
| `paper\figures\clean_sufficiency_misleading_v4_20260529.csv` | `True` | `3097` | `ded3232932e843f23579e5f85768c2fe16a3e90f18f920532564c3def0c2ab5e` |
| `paper\figures\clean_sufficiency_misleading_v4_20260529.svg` | `True` | `6083` | `a354e94977a8ffcf4d32cc4e560521006ab552b043189b98ea2dfd5103bd73f3` |
| `paper\figures\clean_sufficiency_misleading_v4_20260529.md` | `True` | `914` | `f9d497fe94af97a55893fe2391a434995db7a9dccd90250319d8d6f4091e9875` |
| `experiments\reproduce_current_evidence_v4.py` | `True` | `14213` | `21c4a041e1872fa303888942a2e2fa7d4dae58184f36c68307f5a4b57f69745d` |
| `experiments\summarize_evidence_closure.py` | `True` | `47133` | `f74872c0c4a10702bc4a984810f9e220286693bcbfc84933c88d82fe355b59e8` |
| `experiments\summarize_v4_failure_taxonomy.py` | `True` | `11135` | `f5eb0a9e034ef89964e4b51c7069b149bd36156705da4bda2f14f8f1948e3af1` |
| `experiments\summarize_v4_anti_shortcut.py` | `True` | `7039` | `2a57b2459f92de27e292070bcebb69870349dfc8370c08960cba54ca7b0c88f1` |
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
