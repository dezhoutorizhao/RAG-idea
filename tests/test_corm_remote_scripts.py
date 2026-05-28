import json

from experiments.materialize_corm_remote_scripts import materialize_remote_scripts


def test_materialize_remote_scripts_creates_secret_free_runbook(tmp_path):
    plan = {
        "claim_policy": "reconstructed-pipeline evidence only",
        "missing_local_reconstruction_inputs": ["wiki_faiss"],
        "remote": {
            "host": "192.168.103.101",
            "user": "syk",
            "ssh_port": 22,
            "remote_root": "/mnt/ntfs-disk/test",
            "runtime_root": "/dev/shm/csrm_corm_runtime",
            "hf_home": "/dev/shm/csrm_corm_runtime/hf_cache",
            "hf_endpoint_default": "https://hf-mirror.com",
            "storage_policy": "Use /mnt/ntfs-disk for persistent data and /dev/shm for runtime.",
            "password_policy": "Do not write passwords into scripts or reports; use interactive SSH.",
        },
        "remote_steps": [
            {"name": "prepare_remote_dirs", "command": "mkdir -p /mnt/ntfs-disk/test/workspace"},
            {"name": "create_remote_venv", "command": "python3 -m venv /mnt/ntfs-disk/test/venv"},
            {"name": "install_runtime", "command": "/mnt/ntfs-disk/test/venv/bin/pip install numpy"},
            {"name": "build_passages_and_embeddings", "command": "echo build_passages"},
            {"name": "build_faiss_index", "command": "echo build_faiss"},
            {"name": "generate_or_stage_perturbations", "command": "echo use existing OPENAI_API_KEY from environment"},
            {"name": "materialize_biased_nq", "command": "echo biased"},
            {"name": "run_template_biased_nq_smoke_eval", "command": "echo template smoke EVAL_MAX_EXAMPLES"},
            {"name": "run_reconstructed_eval", "command": "cd /mnt/ntfs-disk/test/workspace/external_repos/CoRM-RAG/src && bash run_eval.sh"},
        ],
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    manifest = materialize_remote_scripts(plan_path, tmp_path / "scripts")

    assert manifest["status"] == "materialized"
    assert manifest["contains_secret_markers"] is False
    assert "04_run_reconstructed_eval.sh" in manifest["scripts"]
    assert "04_run_template_biased_nq_smoke_eval.sh" in manifest["scripts"]
    assert "05_watch_and_run_template_smoke_eval.sh" in manifest["scripts"]
    assert "03_prepare_biased_nq_template_smoke.sh" in manifest["scripts"]
    run_eval = (tmp_path / "scripts" / "04_run_reconstructed_eval.sh").read_text(encoding="utf-8")
    assert "CoRM-RAG/src" in run_eval
    assert "20030729" not in run_eval
    smoke_eval = (tmp_path / "scripts" / "04_run_template_biased_nq_smoke_eval.sh").read_text(encoding="utf-8")
    assert "template smoke EVAL_MAX_EXAMPLES" in smoke_eval
    watcher = (tmp_path / "scripts" / "05_watch_and_run_template_smoke_eval.sh").read_text(encoding="utf-8")
    assert "WATCH_TIMEOUT_SECONDS" in watcher
    assert "04_run_template_biased_nq_smoke_eval.sh" in watcher
    assert "wiki.faiss" in watcher
    env_script = (tmp_path / "scripts" / "00_env.sh").read_text(encoding="utf-8")
    assert 'CORM_RUNTIME_ROOT="${CORM_RUNTIME_ROOT:-/dev/shm/csrm_corm_runtime}"' in env_script
    assert 'HF_ENDPOINT="${HF_ENDPOINT:-https://hf-mirror.com}"' in env_script
    assert 'HF_HOME="${HF_HOME:-$CORM_RUNTIME_ROOT/hf_cache}"' in env_script
    assert 'HF_DATASETS_CACHE="${HF_DATASETS_CACHE:-$HF_HOME/datasets}"' in env_script
    assert 'PIP_CACHE_DIR="$CORM_RUNTIME_ROOT/pip_cache"' in env_script
    assert 'TMPDIR="$CORM_RUNTIME_ROOT/tmp"' in env_script
    assert 'CORM_RECON_ENV="$CORM_RUNTIME_ROOT/py_runtime"' in env_script
