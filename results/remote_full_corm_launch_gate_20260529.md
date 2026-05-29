# Remote Full CoRM-RAG Launch Gate

Generated: `2026-05-29T08:23:29.376726+00:00`
Ready to launch Full CoRM-RAG: `False`

## Storage Gates

| Target | Ready | Free GiB | Min-free met | Write probe |
|---|---:|---:|---:|---:|
| `/home/syk` | `False` | `12.2` | `False` | `True` |
| `/mnt/ntfs-disk` | `False` | `322.1` | `True` | `False` |

## Script Gate

- Manifest ready: `True`.
- Remote root: `/home/syk/csrm_corm_reconstruction`.
- Script count: `9`.
- Contains secret markers: `False`.

## Cleanup Gate

- Cleanup preflight passed: `True`.
- Destructive operations executed: `False`.
- Recommended reclaim lower bound: `182.8 GiB`.

## Must Not Launch Reasons

- ext4_home_storage_not_ready: /home/syk is writable but does not meet the 180 GiB free-space gate
- guarded_ext4_cleanup_not_executed
- ntfs_target_not_usable_for_full_reproduction

## Next Safe Actions

- obtain explicit user approval before executing guarded ext4 cleanup
- after cleanup, rerun the /home/syk storage probe and require >=180 GiB plus write probe pass
- launch results/corm_remote_scripts_ext4/02_build_wikipedia_and_faiss.sh only after the post-cleanup gate passes

## Claim Policy

This artifact is a launch gate only. It records whether Full CoRM-RAG may be started; it is not evidence that Full CoRM-RAG has completed.
