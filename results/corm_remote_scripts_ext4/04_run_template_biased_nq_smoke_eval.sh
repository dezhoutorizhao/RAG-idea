#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/00_env.sh"

echo "Run a small template Biased-NQ reconstructed-eval smoke from the upstream src directory."

SMOKE_DATA_SRC=/home/syk/csrm_corm_reconstruction/stage/template_smoke_data && mkdir -p "$SMOKE_DATA_SRC" && ln -sf /home/syk/csrm_corm_reconstruction/data/wiki.faiss "$SMOKE_DATA_SRC/wiki.faiss" && ln -sf /home/syk/csrm_corm_reconstruction/data/wiki_passages.jsonl "$SMOKE_DATA_SRC/wiki_passages.jsonl" && ln -sf /home/syk/csrm_corm_reconstruction/data/biased_nq_test.template_smoke.jsonl "$SMOKE_DATA_SRC/biased_nq_test.jsonl" && cd /home/syk/csrm_corm_reconstruction/workspace/external_repos/CoRM-RAG/src && PATH=/dev/shm/csrm_corm_runtime/py_runtime/bin:$PATH HF_ENDPOINT=${HF_ENDPOINT:-https://hf-mirror.com} HF_HOME=/dev/shm/csrm_corm_runtime/hf_cache HF_HUB_CACHE=/dev/shm/csrm_corm_runtime/hf_cache/hub HF_DATASETS_CACHE=/dev/shm/csrm_corm_runtime/hf_cache/datasets HF_HUB_ETAG_TIMEOUT=${HF_HUB_ETAG_TIMEOUT:-60} HF_HUB_DOWNLOAD_TIMEOUT=${HF_HUB_DOWNLOAD_TIMEOUT:-180} DATA_SRC="$SMOKE_DATA_SRC" EVAL_STAGE_DIR=/home/syk/csrm_corm_reconstruction/stage/eval_data_template_smoke SKIP_FAISS_COPY=${SKIP_FAISS_COPY:-1} EVAL_DATASETS=Biased_NQ EVAL_MAX_EXAMPLES=${EVAL_MAX_EXAMPLES:-20} EVAL_RERANK_DEPTH=${EVAL_RERANK_DEPTH:-10} EVAL_MAX_CONTEXT_DOCS=${EVAL_MAX_CONTEXT_DOCS:-2} CRITIC_PATH=/home/syk/csrm_corm_reconstruction/workspace/checkpoints/hf/critic-v12-mixed/checkpoint-latest/state.pt OUTPUT_DIR=/home/syk/csrm_corm_reconstruction/outputs/corm_reconstructed_eval_template_smoke GENERATOR_MODEL=${GENERATOR_MODEL:-Qwen/Qwen2.5-0.5B-Instruct} bash run_eval.sh
