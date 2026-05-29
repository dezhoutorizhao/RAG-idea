#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/00_env.sh"

echo "Generate deterministic template perturbations and materialize a smoke Biased-NQ file."

cd /home/syk/csrm_corm_reconstruction/workspace && HF_ENDPOINT=${HF_ENDPOINT:-https://hf-mirror.com} HF_HOME=/dev/shm/csrm_corm_runtime/hf_cache HF_HUB_CACHE=/dev/shm/csrm_corm_runtime/hf_cache/hub HF_DATASETS_CACHE=/dev/shm/csrm_corm_runtime/hf_cache/datasets $CORM_RECON_PYTHON experiments/build_corm_template_perturbations.py --output /home/syk/csrm_corm_reconstruction/data/perturbations.template_smoke.jsonl --manifest /home/syk/csrm_corm_reconstruction/outputs/perturbations_template_smoke_manifest.json --max-queries 100

cd /home/syk/csrm_corm_reconstruction/workspace && $CORM_RECON_PYTHON experiments/build_corm_biased_nq_test.py --perturbations /home/syk/csrm_corm_reconstruction/data/perturbations.template_smoke.jsonl --output /home/syk/csrm_corm_reconstruction/data/biased_nq_test.template_smoke.jsonl --manifest /home/syk/csrm_corm_reconstruction/outputs/biased_nq_template_smoke_manifest.json
