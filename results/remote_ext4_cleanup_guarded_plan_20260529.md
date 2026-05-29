# Guarded Remote Ext4 Cleanup Plan

Generated: `2026-05-29T08:04:31.634770+00:00`
Remote: `syk@192.168.103.101:22`
Target: `/home/syk`
Execute requested: `False`
Destructive operations executed: `False`
Can execute now: `False`

## Preflight

- Passed: `True`.
- Recommended reclaim lower bound: `182.8 GiB`.
- Required reclaim lower bound: `180.0 GiB`.
- Candidate audit read-only: `True`.
- Required scope present: `True`.

## Cleanup Scope

- truncate Docker json-file logs only
- delete immediate contents of /root/.cache
- delete immediate contents of /home/syk/.cache

## Explicit Non-Scope

- no docker system prune
- no Docker volume deletion
- no container/image deletion
- no /mnt/ntfs-disk deletion
- no other users' home directory deletion

## Execute Command

Run this only after explicit user approval:

```powershell
$env:CORM_REMOTE_PASSWORD='<set locally>'; python -m experiments.guarded_remote_ext4_cleanup --host 192.168.103.101 --user syk --port 22 --target /home/syk --min-free-gib 180 --execute --confirm-token APPROVE_EXT4_LOG_CACHE_CLEANUP_FOR_FULL_CORM_RAG_REPRO
```

Then run the independent post-cleanup probe:

```powershell
$env:CORM_REMOTE_PASSWORD='<set locally>'; python -m experiments.check_remote_storage_status --host 192.168.103.101 --user syk --port 22 --target /home/syk --output results/remote_storage_status_after_ext4_cleanup.json --min-free-gib 180
```

## Claim Policy

This guarded plan is not a cleanup result. It exists to prevent accidental remote deletion and to make the required approval token and cleanup scope auditable.
