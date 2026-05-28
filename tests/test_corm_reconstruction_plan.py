from experiments.plan_corm_reconstruction import plan_corm_reconstruction


def test_reconstruction_plan_reports_missing_inputs_and_commands(tmp_path):
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

    report = plan_corm_reconstruction(
        workspace=workspace,
        data_src=data,
        checkpoint=checkpoint,
        remote_root="/mnt/ntfs-disk/test",
    )

    assert report["status"] == "planned_not_executed"
    assert report["supplemental_tools_ready"] is True
    assert "wiki_faiss" in report["missing_local_reconstruction_inputs"]
    assert any(step["name"] == "build_faiss_index" for step in report["remote_steps"])
    assert any("encode_corm_wikipedia_streaming.py" in step["command"] for step in report["remote_steps"])
    assert report["remote"]["hf_home"] == "/dev/shm/csrm_corm_runtime/hf_cache"
    assert report["remote"]["hf_endpoint_default"] == "https://hf-mirror.com"
    assert any("HF_ENDPOINT=${HF_ENDPOINT:-https://hf-mirror.com}" in step["command"] for step in report["remote_steps"])
    assert any("HF_DATASETS_CACHE=/dev/shm/csrm_corm_runtime/hf_cache/datasets" in step["command"] for step in report["remote_steps"])
    assert any(step["name"] == "generate_template_perturbations_smoke" for step in report["remote_steps"])
    assert any(step["name"] == "materialize_template_biased_nq_smoke" for step in report["remote_steps"])
    assert any(step["name"] == "run_template_biased_nq_smoke_eval" for step in report["remote_steps"])
    smoke_step = next(step for step in report["remote_steps"] if step["name"] == "run_template_biased_nq_smoke_eval")
    assert "biased_nq_test.template_smoke.jsonl" in smoke_step["command"]
    assert "EVAL_DATASETS=Biased_NQ" in smoke_step["command"]
    assert "EVAL_MAX_EXAMPLES=${EVAL_MAX_EXAMPLES:-20}" in smoke_step["command"]
    assert any("cd /mnt/ntfs-disk/test/workspace/external_repos/CoRM-RAG/src" in step["command"] for step in report["remote_steps"])
    assert "reconstructed-pipeline evidence" in report["claim_policy"]
