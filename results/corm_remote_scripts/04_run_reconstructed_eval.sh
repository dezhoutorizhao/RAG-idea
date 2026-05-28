#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/00_env.sh"

echo "Run reconstructed CoRM evaluation from the upstream src directory."

cd /mnt/ntfs-disk/csrm_corm_reconstruction/workspace/external_repos/CoRM-RAG/src && PATH=/dev/shm/csrm_corm_runtime/py_runtime/bin:$PATH HF_ENDPOINT=${HF_ENDPOINT:-https://hf-mirror.com} HF_HOME=/dev/shm/csrm_corm_runtime/hf_cache HF_HUB_CACHE=/dev/shm/csrm_corm_runtime/hf_cache/hub HF_DATASETS_CACHE=/dev/shm/csrm_corm_runtime/hf_cache/datasets HF_HUB_ETAG_TIMEOUT=${HF_HUB_ETAG_TIMEOUT:-60} HF_HUB_DOWNLOAD_TIMEOUT=${HF_HUB_DOWNLOAD_TIMEOUT:-180} DATA_SRC=/mnt/ntfs-disk/csrm_corm_reconstruction/data EVAL_STAGE_DIR=/mnt/ntfs-disk/csrm_corm_reconstruction/stage/eval_data SKIP_FAISS_COPY=${SKIP_FAISS_COPY:-1} CRITIC_PATH=/mnt/ntfs-disk/csrm_corm_reconstruction/workspace/checkpoints/hf/critic-v12-mixed/checkpoint-latest/state.pt OUTPUT_DIR=/mnt/ntfs-disk/csrm_corm_reconstruction/outputs/corm_reconstructed_eval GENERATOR_MODEL=${GENERATOR_MODEL:-Qwen/Qwen2.5-7B-Instruct} bash run_eval.sh
