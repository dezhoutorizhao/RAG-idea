#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/00_env.sh"

echo "Build Wikipedia passages, embeddings, and supplemental FAISS index."

cd /mnt/ntfs-disk/csrm_corm_reconstruction/workspace && HF_ENDPOINT=${HF_ENDPOINT:-https://hf-mirror.com} HF_HOME=/dev/shm/csrm_corm_runtime/hf_cache HF_HUB_CACHE=/dev/shm/csrm_corm_runtime/hf_cache/hub HF_DATASETS_CACHE=/dev/shm/csrm_corm_runtime/hf_cache/datasets HF_HUB_ETAG_TIMEOUT=${HF_HUB_ETAG_TIMEOUT:-60} HF_HUB_DOWNLOAD_TIMEOUT=${HF_HUB_DOWNLOAD_TIMEOUT:-180} $CORM_RECON_PYTHON experiments/encode_corm_wikipedia_streaming.py --output-dir /mnt/ntfs-disk/csrm_corm_reconstruction/data --device cuda:0 --encode-batch-size 256 --passages-per-shard 250000 --resume

cd /mnt/ntfs-disk/csrm_corm_reconstruction/workspace && $CORM_RECON_PYTHON experiments/build_corm_faiss_index.py --embeddings /mnt/ntfs-disk/csrm_corm_reconstruction/data --output /mnt/ntfs-disk/csrm_corm_reconstruction/data/wiki.faiss --manifest /mnt/ntfs-disk/csrm_corm_reconstruction/outputs/wiki_faiss_manifest.json
