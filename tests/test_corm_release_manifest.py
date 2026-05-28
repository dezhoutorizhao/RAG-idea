from experiments.check_corm_release_manifest import analyze_release_manifest


def test_release_manifest_detects_checkpoint_only_release():
    report = analyze_release_manifest(
        hf_files=[
            ".gitattributes",
            "README.md",
            "critic-v12-mixed/checkpoint-latest/state.pt",
        ],
        github_files=["README.md", "src/run_eval.sh"],
    )

    assert report["checkpoint_available"] is True
    assert report["missing_public_data_count"] == 3
    assert report["release_status"] == "checkpoint_only_or_data_missing"


def test_release_manifest_accepts_data_from_either_source():
    report = analyze_release_manifest(
        hf_files=["critic-v12-mixed/checkpoint-latest/state.pt", "data/wiki.faiss"],
        github_files=["data/wiki_passages.jsonl", "data/biased_nq_test.jsonl"],
    )

    assert report["missing_public_data_artifacts"] == []
    assert report["release_status"] == "checkpoint_plus_data"
