# Evidence Closure Status

Generated: `2026-05-28T18:13:28.583452+00:00`

Verdict: non-human bridge evidence is substantially closed, but full CoRM reconstruction and general formal risk control remain unsupported. Human audit v3 is explicitly excluded from this closure by user request.

## HotpotQA Bridge

| Method | AUROC | Risk@30 | AURC |
|---|---:|---:|---:|
| csrm | 0.9976 | 0.1669 | 0.4049 |
| naive_orbit_average | 0.8321 | 0.5119 | 0.5829 |
| corm_max_clean | 0.5000 | 0.7497 | 0.7444 |
| single_set_sure_style | 0.5000 | 0.7497 | 0.7375 |
| csrm_shuffled_perturbations | 0.0001 | 1.0000 | 0.9633 |

## FEVER v3 Near-Miss Bridge

| Method | AUROC | Risk@30 | AURC |
|---|---:|---:|---:|
| csrm | 1.0000 | 0.4444 | 0.5301 |
| naive_orbit_average | 0.7764 | 0.6407 | 0.7719 |
| corm_max_clean | 0.5000 | 0.8333 | 0.8306 |
| single_set_sure_style | 0.5000 | 0.8333 | 0.8264 |
| csrm_shuffled_perturbations | 0.0327 | 1.0000 | 0.9778 |

## NLI Cross-Scorer Probe

| Method | AUROC | Risk@30 | AURC |
|---|---:|---:|---:|
| csrm | 0.7353 | 0.6267 | 0.6676 |
| naive_orbit_average | 0.4880 | 0.8600 | 0.7959 |
| corm_max_clean | 0.5244 | 0.7800 | 0.7838 |
| single_set_sure_style | 0.4818 | 0.8700 | 0.8202 |
| csrm_shuffled_perturbations | 0.3281 | 0.9367 | 0.8921 |

## Risk Control

- Hotpot CP empirical transfer: `True`; formal guarantee: `False`; target misses: `0`.
- FEVER CP empirical transfer: `False`; formal guarantee: `False`; target misses: `2`.

## CoRM Reconstruction

- Preflight ready: `False`.
- Missing required artifacts: `5`.
- Remote status: `failed_storage_io_after_fresh_250k_recovery`.
- Complete embedding shards: `52`; latest: `embeddings_shard_000051.npy`.
- FAISS exists: `False`.
- Terminal failure: The 250k-shard resume wrote embeddings_shard_000051.npy completely, then failed while writing/flushing wiki_passages.jsonl with OSError [Errno 5] Input/output error on the NTFS/fuseblk mount.

Latest storage probe:
- Target: `/mnt/ntfs-disk` (fuseblk, capacity `84%`).
- Reported available: `322.1444` GiB; minimum met: `True`.
- Write probe passed: `False`; storage-ready: `False`.
- Write probe error: `mktemp: 无法通过模板 “/mnt/ntfs-disk/csrm_write_probe.XXXXXX” 创建目录: 设备上没有空间`.
- GPU query: `0, NVIDIA GeForce RTX 4090, 24564, 24076; 1, NVIDIA GeForce RTX 4090, 24564, 24097`.

## Latest V4 Hotpot Diagnostic

Semantic-swap n100:
- Construction audit passed: `True`; failed groups: `0`.
- Perturbation doc overlap: `1.0000`; text changed rate: `1.0000`; answer-mention reduced rate: `1.0000`.
- Structural-only max AUROC: `0.5009`.
- CSRM-Rule AUROC/Risk@30/AURC: `0.9031` / `0.1500` / `0.2280`.
- Strongest non-CSRM: `calibrated_logistic_orbit` with AUROC `0.9649`.
- CSRM-Calibrated-Logistic AUROC mean: `0.9658`; vs calibrated logistic orbit AUROC delta mean: `0.0000`.
- Human-audited labels complete: `False` (labeled `0`, pending `200`).

## Claim Boundary

Allowed claims:
- CSRM has strong bridge evidence on HotpotQA-derived orbits with released CoRM critic scores.
- CSRM has secondary bridge evidence on FEVER v3 near-miss orbits.
- Orbit alignment is necessary under the implemented shuffled-perturbation ablation.
- The directional CSRM ranking survives an automated NLI cross-scorer sensitivity probe.
- Hotpot-only empirical risk-target transfer is supported under the conservative CP pressure test.
- Hotpot semantic-swap v4 is a leakage-controlled diagnostic where self-consistency and retrieval-stability shortcuts fail.

Disallowed claims:
- Full original CoRM-RAG retrieval-generation reproduction is complete.
- A general formal risk-control guarantee is established.
- The results are human-audited.
- The method solves robust RAG generally across tasks.
- CSRM significantly beats the strongest learned orbit baseline on Hotpot semantic-swap v4.

Remaining non-human blockers:
- Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts.
- FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.
- Independent external review has not been rerun after the latest storage-status update.

Remaining human-audit blockers:
- Hotpot semantic-swap blind200 pack is prepared, but adjudicated labels are pending.

## Verification

Claim verifier: `28/28` passed, `0` failed.
