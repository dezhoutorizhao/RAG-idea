from pathlib import Path

from experiments.plan_corm_reconstruction import plan_corm_reconstruction


def test_run_eval_uses_configurable_large_stage_dir(tmp_path):
    script = Path("external_repos/CoRM-RAG/src/run_eval.sh").read_text(encoding="utf-8")
    assert 'DATA_DIR="${EVAL_STAGE_DIR:-/tmp/eval_data}"' in script
    assert 'SKIP_FAISS_COPY:-0' in script
    assert "EVAL_MAX_EXAMPLES" in script
    run_evaluation = Path("external_repos/CoRM-RAG/src/run_evaluation.py").read_text(encoding="utf-8")
    assert "--max_examples" in run_evaluation
    assert "Limiting {ds_name} to {n} examples for smoke run" in run_evaluation

    workspace = tmp_path / "workspace"
    data = workspace / "external_repos" / "CoRM-RAG" / "data"
    checkpoint = workspace / "checkpoints" / "hf" / "critic-v12-mixed" / "checkpoint-latest" / "state.pt"
    for path in [
        workspace / "external_repos" / "CoRM-RAG",
        workspace / "experiments",
        checkpoint.parent,
        data,
    ]:
        path.mkdir(parents=True, exist_ok=True)
    checkpoint.write_text("ckpt", encoding="utf-8")
    (workspace / "experiments" / "build_corm_faiss_index.py").write_text("x", encoding="utf-8")
    (workspace / "experiments" / "build_corm_biased_nq_test.py").write_text("x", encoding="utf-8")
    (workspace / "experiments" / "build_corm_template_perturbations.py").write_text("x", encoding="utf-8")
    (workspace / "experiments" / "encode_corm_wikipedia_streaming.py").write_text("x", encoding="utf-8")

    plan = plan_corm_reconstruction(
        workspace=workspace,
        data_src=data,
        checkpoint=checkpoint,
        remote_root="/mnt/ntfs-disk/test",
    )
    run_step = next(step for step in plan["remote_steps"] if step["name"] == "run_reconstructed_eval")
    assert "PATH=/dev/shm/csrm_corm_runtime/py_runtime/bin:$PATH" in run_step["command"]
    assert "EVAL_STAGE_DIR=/mnt/ntfs-disk/test/stage/eval_data" in run_step["command"]
    assert "SKIP_FAISS_COPY=${SKIP_FAISS_COPY:-1}" in run_step["command"]
    assert "GENERATOR_MODEL=${GENERATOR_MODEL:-Qwen/Qwen2.5-7B-Instruct}" in run_step["command"]
    smoke_step = next(step for step in plan["remote_steps"] if step["name"] == "run_template_biased_nq_smoke_eval")
    assert "EVAL_STAGE_DIR=/mnt/ntfs-disk/test/stage/eval_data_template_smoke" in smoke_step["command"]
    assert "EVAL_MAX_EXAMPLES=${EVAL_MAX_EXAMPLES:-20}" in smoke_step["command"]
    assert "GENERATOR_MODEL=${GENERATOR_MODEL:-Qwen/Qwen2.5-0.5B-Instruct}" in smoke_step["command"]
