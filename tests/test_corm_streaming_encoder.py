import json

import numpy as np

from experiments.encode_corm_wikipedia_streaming import (
    article_to_passages,
    encode_passages_dummy,
    encode_wikipedia_streaming,
    iter_wikipedia_passages,
    load_jsonl_articles,
)


def test_article_to_passages_chunks_and_filters_short_tail():
    text = " ".join(f"w{i}" for i in range(95))

    passages = article_to_passages("Title", text, words_per_passage=40, min_words=30)

    assert len(passages) == 2
    assert passages[0].startswith("Title: w0 w1")
    assert "w39" in passages[0]
    assert "w79" in passages[1]


def test_iter_wikipedia_passages_honors_limits():
    dataset = [
        {"title": "A", "text": " ".join("a" for _ in range(80))},
        {"title": "B", "text": " ".join("b" for _ in range(80))},
    ]

    rows = list(
        iter_wikipedia_passages(
            dataset,
            max_articles=2,
            max_passages=3,
            words_per_passage=40,
            min_words=30,
        )
    )

    assert len(rows) == 3
    assert rows[0][0] == 0
    assert rows[-1][0] == 1


def test_iter_wikipedia_passages_can_skip_completed_prefix():
    dataset = [
        {"title": "A", "text": " ".join("a" for _ in range(80))},
        {"title": "B", "text": " ".join("b" for _ in range(80))},
    ]

    rows = list(
        iter_wikipedia_passages(
            dataset,
            max_passages=4,
            skip_passages=2,
            words_per_passage=40,
            min_words=30,
        )
    )

    assert len(rows) == 2
    assert rows[0][0] == 1


def test_load_jsonl_articles_accepts_staged_rows(tmp_path):
    path = tmp_path / "articles.jsonl"
    path.write_text(
        json.dumps({"title": "T", "text": "body"}) + "\n" + json.dumps({"text": "passage only"}) + "\n",
        encoding="utf-8",
    )

    rows = list(load_jsonl_articles(path))

    assert rows == [{"title": "T", "text": "body"}, {"title": "staged", "text": "passage only"}]


def test_dummy_encoder_is_deterministic_and_normalized():
    a = encode_passages_dummy(["same text"], dim=8)
    b = encode_passages_dummy(["same text"], dim=8)

    assert np.allclose(a, b)
    assert np.allclose(np.linalg.norm(a, axis=1), [1.0])


def test_streaming_encoder_resume_repairs_passage_tail_and_appends(tmp_path):
    text = " ".join(f"w{i}" for i in range(650))
    dataset = [{"title": "T", "text": text}]
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    np.save(output_dir / "embeddings_shard_000000.npy", np.ones((1, 16), dtype=np.float32))
    (output_dir / "wiki_passages.jsonl").write_text(
        json.dumps({"text": "kept"}) + "\n" + json.dumps({"text": "stale extra"}) + "\n",
        encoding="utf-8",
    )

    manifest = encode_wikipedia_streaming(
        output_dir=output_dir,
        dataset=dataset,
        backend="dummy",
        dummy_dim=16,
        passages_per_shard=1,
        max_passages=3,
        resume=True,
    )

    assert manifest["resume"] is True
    assert manifest["resume_existing_shards"] == 1
    assert manifest["resume_repaired_passages"] is True
    assert manifest["embedding_shard_count"] == 3
    assert (output_dir / "embeddings_shard_000001.npy").exists()
    assert (output_dir / "embeddings_shard_000002.npy").exists()
    assert not (output_dir / "wiki_passages.jsonl.resume_repair").exists()
    assert len((output_dir / "wiki_passages.jsonl").read_text(encoding="utf-8").splitlines()) == 3


def test_streaming_encoder_resume_drops_incomplete_last_shard(tmp_path):
    text = " ".join(f"w{i}" for i in range(650))
    dataset = [{"title": "T", "text": text}]
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    np.save(output_dir / "embeddings_shard_000000.npy", np.ones((1, 16), dtype=np.float32))
    partial = output_dir / "embeddings_shard_000001.npy"
    np.save(partial, np.ones((3, 16), dtype=np.float32))
    partial.write_bytes(partial.read_bytes()[:-8])
    (output_dir / "wiki_passages.jsonl").write_text(
        json.dumps({"text": "kept"}) + "\n" + json.dumps({"text": "unembedded tail"}) + "\n",
        encoding="utf-8",
    )

    manifest = encode_wikipedia_streaming(
        output_dir=output_dir,
        dataset=dataset,
        backend="dummy",
        dummy_dim=16,
        passages_per_shard=1,
        max_passages=2,
        resume=True,
    )

    assert manifest["resume_existing_shards"] == 1
    assert manifest["resume_dropped_incomplete_shards"]
    assert manifest["resume_repaired_passages"] is True
    assert (output_dir / "embeddings_shard_000001.npy").exists()
    assert len((output_dir / "wiki_passages.jsonl").read_text(encoding="utf-8").splitlines()) == 2
