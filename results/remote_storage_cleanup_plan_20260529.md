# Remote Storage Cleanup Plan

Date: 2026-05-29

Latest dry-run snapshot: `2026-05-29T07:49:14Z`

This report identifies the current storage blocker for full CoRM-RAG reproduction and the smallest observed cleanup path that can plausibly provide at least 180 GiB of writable ext4 space.

## Current Blocker

`/mnt/ntfs-disk` is not usable for full reproduction right now.

- Filesystem: `fuseblk`
- Reported available space: about `322.1 GiB`
- Write probe: failed
- Failure mode: creating a file or directory returns `No space left on device`
- Scope: failures occur at the mount root and inside existing directories including `/mnt/ntfs-disk/syk`, `/mnt/ntfs-disk/csrm_corm_reconstruction`, `/mnt/ntfs-disk/cseu_idea3_external`, and `/mnt/ntfs-disk/tmp`

Interpretation: this is not a normal permission or inode exhaustion case. The NTFS/fuseblk write path is returning ENOSPC despite enough reported bytes and inodes, so the mount must not be treated as reproduction-ready.

## Writable Fallbacks

The following paths can create temporary directories:

- `/home/syk`
- `/tmp`
- `/dev/shm`

They are not currently sufficient for full reproduction because the ext4 root filesystem has only about `12.2 GiB` free, and `/dev/shm` is not persistent.

## Space Candidates

Observed root filesystem usage:

| Path | Usage |
|---|---:|
| `/home` | `1.4T` |
| `/var` | `261G` |
| `/root` | `69G` |
| `/usr` | `25G` |
| `/tmp` | `2.4G` |

Relevant cleanup candidates:

| Candidate | Size | Operation | Risk |
|---|---:|---|---|
| Docker JSON logs | `134.1 GiB` | truncate `/var/lib/docker/containers/*/*-json.log` | medium |
| `/root/.cache` | `31 GiB` | remove root cache contents | medium |
| `/home/syk/.cache` | `19 GiB` | remove user cache contents | low-to-medium |
| `/home/syk/miniconda3/pkgs` | `5 GiB` | conda package-cache cleanup | low |

Projected free space:

| Cleanup set | Projected free |
|---|---:|
| current root free only | `12.2 GiB` |
| Docker logs only | `146.3 GiB` |
| Docker logs + `/root/.cache` | `177.3 GiB` |
| Docker logs + `/root/.cache` + `/home/syk/.cache` | `196.3 GiB` |
| plus conda package cache | `201.3 GiB` |

The minimum practical cleanup set that appears to satisfy the 180 GiB requirement is:

```text
1. truncate Docker JSON logs
2. remove /root/.cache contents
3. remove /home/syk/.cache contents
```

## Not Recommended Without Coordination

- Do not run `ntfsfix`, unmount, or remount `/mnt/ntfs-disk` without coordinating with active users. The volume is mounted read-write and NTFS tools refused safe inspection while mounted.
- Do not run `docker system prune --volumes` blindly. Docker reports reclaimable data, but pruning volumes/containers can delete active service state.
- Do not delete other users' `/home` directories or `/mnt/ntfs-disk` project directories without ownership confirmation.

## Recommended Next Action

Get explicit permission to perform the minimum practical cleanup set above. After cleanup, re-run a create-write-fsync-read-delete probe on the intended ext4 target directory. Start full CoRM-RAG reproduction only after the target has at least 180 GiB free and the write probe passes.
