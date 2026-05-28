import json
from pathlib import Path

import numpy as np

from experiments.build_corm_biased_nq_test import build_biased_nq_test
from experiments.build_corm_faiss_index import build_faiss_index, find_embedding_files


class _FakeFaiss:
    METRIC_INNER_PRODUCT = 0

    class IndexFlatIP:
        def __init__(self, dim):
            self.dim = dim
            self.ntotal = 0

        def add(self, batch):
            self.ntotal += len(batch)

    class IndexIVFFlat:
        def __init__(self, quantizer, dim, nlist, metric):
            self.quantizer = quantizer
            self.dim = dim
            self.nlist = nlist
            self.metric = metric
            self.ntotal = 0
            self.trained = False

        def train(self, batch):
            self.trained = True

        def add(self, batch):
            self.ntotal += len(batch)

    @staticmethod
    def write_index(index, path):
        Path(path).write_text(f"fake index {index.ntotal}", encoding="utf-8")


def test_find_embedding_files_prefers_merged_file(tmp_path):
    np.save(tmp_path / "wiki_embeddings.npy", np.zeros((2, 3), dtype=np.float32))
    np.save(tmp_path / "embeddings_shard_0.npy", np.zeros((1, 3), dtype=np.float32))

    files = find_embedding_files(tmp_path)

    assert files == [(tmp_path / "wiki_embeddings.npy").resolve()]


def test_build_faiss_index_with_fake_faiss(tmp_path):
    embeddings = tmp_path / "wiki_embeddings.npy"
    np.save(embeddings, np.asarray([[3.0, 4.0], [1.0, 0.0]], dtype=np.float32))
    output = tmp_path / "wiki.faiss"
    manifest = tmp_path / "manifest.json"

    report = build_faiss_index(
        embeddings,
        output,
        index_type="flat",
        batch_size=1,
        manifest=manifest,
        faiss_module=_FakeFaiss,
    )

    assert output.exists()
    assert report["vectors"] == 2
    assert report["dim"] == 2
    assert json.loads(manifest.read_text(encoding="utf-8"))["status"] == "built"


def test_build_biased_nq_test_materializes_expected_schema(tmp_path):
    source = tmp_path / "perturbations.jsonl"
    source.write_text(
        json.dumps(
            {
                "query_idx": 7,
                "question": "Who wrote Hamlet?",
                "correct_answer": "William Shakespeare",
                "all_answers": ["William Shakespeare", "Shakespeare"],
                "perturbations": [
                    {"perturbation_type": 1, "perturbed_query": "Who wrote Hamlet under the false premise?"},
                    {"perturbation_type": 2, "perturbed_query": "Who wrote Hamlet if the timeline is confused?"},
                    {"perturbation_type": 3, "perturbed_query": "Who wrote Hamlet? The Eiffel Tower is in Paris."},
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "biased_nq_test.jsonl"

    report = build_biased_nq_test(source, output)

    row = json.loads(output.read_text(encoding="utf-8"))
    assert report["rows"] == 1
    assert row["query_idx"] == 7
    assert row["all_answers"][0] == "William Shakespeare"
    assert {p["perturbation_type"] for p in row["perturbations"]} == {1, 2, 3}


def test_build_biased_nq_test_rejects_missing_type(tmp_path):
    source = tmp_path / "perturbations.jsonl"
    source.write_text(
        json.dumps(
            {
                "query_idx": 1,
                "question": "Q?",
                "all_answers": ["A"],
                "perturbations": [{"perturbation_type": 1, "perturbed_query": "Q with bias?"}],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    try:
        build_biased_nq_test(source, tmp_path / "out.jsonl")
    except ValueError as exc:
        assert "missing required perturbation types" in str(exc)
    else:
        raise AssertionError("expected ValueError")
