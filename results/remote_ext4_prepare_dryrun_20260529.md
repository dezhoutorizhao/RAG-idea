# Remote Ext4 Preparation Dry Run

Date: 2026-05-29

This dry run validates the exact commands that would prepare writable ext4 space for full CoRM-RAG reproduction. No destructive operation was executed.

## Mode

```text
mode = dry_run
destructive_operations_executed = false
target = /home/syk
minimum_free_required = 180 GiB
```

## Current Space

```text
target filesystem = ext4
current free on / = about 13 GiB
```

Observed cleanup candidates:

```text
Docker JSON logs = 143790630971 bytes, about 133.94 GiB
/root/.cache = 31G
/home/syk/.cache = 19G
/home/syk/miniconda3/pkgs = 5.0G
```

## Planned Commands

```text
find /var/lib/docker/containers -name '*-json.log' -type f -exec sh -c 'for path do : > "$path"; done' sh {} +
test -d /root/.cache && find /root/.cache -mindepth 1 -maxdepth 1 -exec rm -rf -- {} + || true
test -d /home/syk/.cache && find /home/syk/.cache -mindepth 1 -maxdepth 1 -exec rm -rf -- {} + || true
```

These commands intentionally avoid:

```text
docker system prune --volumes
deleting containers
deleting Docker volumes
deleting /mnt/ntfs-disk contents
deleting other users' home directories
```

## Required Follow-Up After Explicit Cleanup Approval

After running execute mode, the storage target must pass:

```text
python experiments/check_remote_storage_status.py \
  --host 192.168.103.101 \
  --user syk \
  --port 22 \
  --target /home/syk \
  --min-free-gib 180 \
  --output results/remote_storage_status_after_ext4_cleanup.json
```

Full CoRM-RAG reproduction must not be resumed until that post-cleanup probe reports:

```text
ready_for_full_reproduction_storage = true
target_min_free_met = true
target_write_probe_passed = true
```
