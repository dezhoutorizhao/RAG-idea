# Hidden Local Path Audit

Passed: `False`.
Scanned artifacts: `209`.
Findings: `5`.

Remote /mnt/ntfs-disk and /home/syk paths are documented operational paths, not hidden local dependencies.

## Findings

| Artifact | Pattern | Match |
|---|---|---|
| `experiments/audit_remote_cleanup_candidates.py` | `/home/(?!syk\b)[^/\s]+` | `/home/{shlex.quote(user)}` |
| `experiments/audit_remote_cleanup_candidates.py` | `/home/(?!syk\b)[^/\s]+` | `/home/{shlex.quote(user)}` |
| `experiments/audit_remote_cleanup_candidates.py` | `/home/(?!syk\b)[^/\s]+` | `/home/{shlex.quote(user)}` |
| `experiments/audit_remote_cleanup_candidates.py` | `/home/(?!syk\b)[^/\s]+` | `/home/{shlex.quote(user)}` |
| `experiments/audit_remote_cleanup_candidates.py` | `/home/(?!syk\b)[^/\s]+` | `/home/{shlex.quote(user)}` |
