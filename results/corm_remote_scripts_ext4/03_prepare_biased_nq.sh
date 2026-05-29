#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/00_env.sh"

echo "Generate or stage perturbations, then materialize biased_nq_test.jsonl."

cd /home/syk/csrm_corm_reconstruction/workspace/external_repos/CoRM-RAG && OPENAI_API_KEY=$OPENAI_API_KEY OPENAI_BASE_URL=$OPENAI_BASE_URL $CORM_RECON_PYTHON src/gen_perturbations_api.py --output /home/syk/csrm_corm_reconstruction/data/perturbations.jsonl --data nq_val

cd /home/syk/csrm_corm_reconstruction/workspace && $CORM_RECON_PYTHON experiments/build_corm_biased_nq_test.py --perturbations /home/syk/csrm_corm_reconstruction/data/perturbations.jsonl --output /home/syk/csrm_corm_reconstruction/data/biased_nq_test.jsonl --manifest /home/syk/csrm_corm_reconstruction/outputs/biased_nq_manifest.json
