#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/00_env.sh"

echo "Prepare remote directories and Python environment."

mkdir -p /home/syk/csrm_corm_reconstruction/workspace /home/syk/csrm_corm_reconstruction/data /home/syk/csrm_corm_reconstruction/outputs/corm_reconstructed_eval /home/syk/csrm_corm_reconstruction/outputs/corm_reconstructed_eval_template_smoke /home/syk/csrm_corm_reconstruction/stage/eval_data /home/syk/csrm_corm_reconstruction/stage/eval_data_template_smoke /home/syk/csrm_corm_reconstruction/stage/template_smoke_data /dev/shm/csrm_corm_runtime/hf_cache /dev/shm/csrm_corm_runtime/hf_cache/hub /dev/shm/csrm_corm_runtime/hf_cache/datasets /dev/shm/csrm_corm_runtime/pip_cache /dev/shm/csrm_corm_runtime/tmp /dev/shm/csrm_corm_runtime/xdg_cache /dev/shm/csrm_corm_runtime/vllm_cache /dev/shm/csrm_corm_runtime/mamba_root /dev/shm/csrm_corm_runtime/mamba_pkgs /dev/shm/csrm_corm_runtime/micromamba

if [ ! -x /dev/shm/csrm_corm_runtime/micromamba/bin/micromamba ]; then curl -L https://micro.mamba.pm/api/micromamba/linux-64/latest | tar --touch -xvj -C /dev/shm/csrm_corm_runtime/micromamba bin/micromamba; fi && (/dev/shm/csrm_corm_runtime/micromamba/bin/micromamba create -y -p /dev/shm/csrm_corm_runtime/py_runtime -c conda-forge python=3.10 pip || (rm -rf /dev/shm/csrm_corm_runtime/py_runtime && python3 -m venv --copies /dev/shm/csrm_corm_runtime/py_runtime))

$CORM_RECON_PIP install --upgrade pip setuptools wheel && if $CORM_RECON_PYTHON -c "import sys; raise SystemExit(0 if sys.version_info < (3, 9) else 1)"; then $CORM_RECON_PIP install numpy scipy scikit-learn datasets huggingface_hub transformers tokenizers==0.20.3 'torch>=2.1' faiss-cpu 'vllm==0.5.5'; else $CORM_RECON_PIP install numpy scipy scikit-learn datasets huggingface_hub transformers 'torch>=2.1' faiss-cpu 'vllm>=0.5'; fi && $CORM_RECON_PYTHON -c "import sysconfig; from pathlib import Path; p=Path(sysconfig.get_paths()['purelib'])/'pyairports'; p.mkdir(exist_ok=True); (p/'__init__.py').write_text('from .airports import AIRPORT_LIST\\n'); (p/'airports.py').write_text('AIRPORT_LIST = []\\n')"
