# CoRM Reconstructed Remote Runbook

Status: `planned_not_executed`

Remote target: `syk@192.168.103.101:22`

Remote root: `/home/syk/csrm_corm_reconstruction`

Storage policy: Use the repaired ext4 home filesystem for persistent workspace/data and /dev/shm/csrm_corm_runtime for the transient Python runtime and HuggingFace cache. Do not use /mnt/ntfs-disk for full reproduction until an independent write probe passes.

Runtime root: `/dev/shm/csrm_corm_runtime`

HuggingFace cache: `/dev/shm/csrm_corm_runtime/hf_cache`

Default HuggingFace endpoint: `https://hf-mirror.com`

Password/API policy: Do not write passwords into scripts or reports; use interactive SSH, SSH keys, or caller-provided secret handling.

Run order:

1. `bash 01_prepare_env.sh`
2. `bash 02_build_wikipedia_and_faiss.sh`
3. `bash 03_prepare_biased_nq.sh`
4. Optional fallback only: `bash 03_prepare_biased_nq_template_smoke.sh`
5. Optional smoke only: `bash 04_run_template_biased_nq_smoke_eval.sh`
6. `bash 04_run_reconstructed_eval.sh`
7. Optional watcher: `bash 05_watch_and_run_template_smoke_eval.sh`

Current missing local reconstruction inputs:

- `wiki_passages`
- `wiki_embeddings`
- `wiki_faiss`
- `perturbations`
- `biased_nq_test`

Claim policy:

A run using these steps is reconstructed-pipeline evidence, not exact CoRM-RAG original reproduction, unless original artifacts or equivalence checks are supplied. The ext4 relocation is a launch plan only; it is not evidence that full CoRM-RAG reproduction has run.
