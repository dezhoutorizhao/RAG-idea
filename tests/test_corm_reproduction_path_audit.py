import json
from pathlib import Path

from experiments.audit_corm_reproduction_path import audit_reproduction_path


def test_audit_detects_missing_faiss_writer(tmp_path):
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "run_evaluation.py").write_text(
        "\n".join(
            [
                "import faiss",
                "faiss.read_index('wiki.faiss')",
                "open('wiki_passages.jsonl')",
                "open('biased_nq_test.jsonl')",
                "from vllm import LLM",
            ]
        ),
        encoding="utf-8",
    )
    (repo / "src" / "encode_wikipedia.py").write_text(
        "open('wiki_passages.jsonl', 'w')\nnp.save('wiki_embeddings.npy', embeddings)",
        encoding="utf-8",
    )
    (repo / "src" / "run_eval.sh").write_text(
        "stage_file \"$DATA_SRC/wiki.faiss\" \"$DATA_DIR/wiki.faiss\"",
        encoding="utf-8",
    )

    report = audit_reproduction_path(repo)

    assert report["reconstructability_status"] == "blocked"
    assert report["repository_calls_faiss_write_index"] is False
    assert any("faiss.write_index" in item for item in report["blockers"])
    assert "supplemental_reconstruction" in report


def test_audit_detects_variable_based_passage_writer(tmp_path):
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "run_evaluation.py").write_text(
        "open('wiki_passages.jsonl')",
        encoding="utf-8",
    )
    (repo / "src" / "encode_wikipedia.py").write_text(
        "passages_path = os.path.join(output_dir, 'wiki_passages.jsonl')\n"
        "with open(passages_path, 'w') as f:\n"
        "    f.write('x')",
        encoding="utf-8",
    )

    report = audit_reproduction_path(repo)
    passage_report = next(item for item in report["required_runtime_artifacts"] if item["name"] == "wiki_passages.jsonl")

    assert passage_report["producer_detected"] is True


def test_audit_accepts_complete_minimal_path(tmp_path):
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "run_evaluation.py").write_text(
        "import faiss\nfaiss.read_index('wiki.faiss')\nopen('wiki_passages.jsonl')\nopen('biased_nq_test.jsonl')",
        encoding="utf-8",
    )
    (repo / "src" / "encode_wikipedia.py").write_text(
        "\n".join(
            [
                "open('wiki_passages.jsonl', 'w')",
                "faiss.write_index(index, 'wiki.faiss')",
                "open('biased_nq_test.jsonl', 'w')",
            ]
        ),
        encoding="utf-8",
    )
    (repo / "src" / "run_eval.sh").write_text("DATA_SRC=${DATA_SRC:-./data}", encoding="utf-8")

    report = audit_reproduction_path(repo)

    assert report["reconstructability_status"] == "scripted"
    assert report["blockers"] == []


def test_audit_output_is_json_serializable(tmp_path):
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "run_evaluation.py").write_text("", encoding="utf-8")

    json.dumps(audit_reproduction_path(repo))
