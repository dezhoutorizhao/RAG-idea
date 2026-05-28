from experiments.check_corm_reproduction_readiness import check_corm_reproduction_readiness


def test_corm_reproduction_readiness_reports_missing_inputs(tmp_path):
    repo = tmp_path / "CoRM-RAG"
    (repo / "src").mkdir(parents=True)
    (repo / "README.md").write_text("repo", encoding="utf-8")
    (repo / "src" / "run_eval.sh").write_text("run", encoding="utf-8")
    (repo / "src" / "run_evaluation.py").write_text("eval", encoding="utf-8")
    (repo / "src" / "train_critic.py").write_text("train", encoding="utf-8")
    data = tmp_path / "data"
    data.mkdir()
    checkpoint = tmp_path / "state.pt"

    report = check_corm_reproduction_readiness(
        repo,
        data,
        checkpoint,
        require_cuda=False,
    )

    assert report["ready"] is False
    assert report["missing_required_artifacts"] >= 4
    assert any("wiki.faiss" in blocker for blocker in report["blockers"])
    assert any("checkpoint" in blocker for blocker in report["blockers"])
    assert report["cuda"]["satisfied"] is True
    assert "Push-Location external_repos/CoRM-RAG/src" in report["reproduction_command"]
    assert "bash run_eval.sh" in report["reproduction_command"]


def test_corm_reproduction_readiness_can_pass_with_mocked_minimum(tmp_path, monkeypatch):
    repo = tmp_path / "CoRM-RAG"
    (repo / "src").mkdir(parents=True)
    for relative_path in [
        "README.md",
        "src/run_eval.sh",
        "src/run_evaluation.py",
        "src/train_critic.py",
    ]:
        path = repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x", encoding="utf-8")

    data = tmp_path / "data"
    data.mkdir()
    for name in ["wiki.faiss", "wiki_passages.jsonl", "biased_nq_test.jsonl"]:
        (data / name).write_text("x", encoding="utf-8")
    checkpoint = tmp_path / "state.pt"
    checkpoint.write_text("x", encoding="utf-8")

    def fake_find_spec(_name):
        return object()

    monkeypatch.setattr(
        "experiments.check_corm_reproduction_readiness.importlib.util.find_spec",
        fake_find_spec,
    )

    report = check_corm_reproduction_readiness(
        repo,
        data,
        checkpoint,
        require_cuda=False,
    )

    assert report["ready"] is True
    assert report["blockers"] == []
    assert report["missing_required_artifacts"] == 0
