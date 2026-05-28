#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Iterable

import numpy as np


def build_faiss_index(
    embeddings_path: Path,
    output: Path,
    *,
    index_type: str = "ivf",
    nlist: int = 4096,
    batch_size: int = 100_000,
    normalize: bool = True,
    manifest: Path | None = None,
    faiss_module: Any | None = None,
) -> dict[str, Any]:
    if index_type not in {"flat", "ivf"}:
        raise ValueError("index_type must be 'flat' or 'ivf'")
    files = find_embedding_files(embeddings_path)
    if not files:
        raise FileNotFoundError(f"no embedding .npy files found under {embeddings_path}")

    arrays = [_load_array(path) for path in files]
    dim = int(arrays[0].shape[1])
    total = int(sum(array.shape[0] for array in arrays))
    if total <= 0:
        raise ValueError("embedding arrays are empty")
    if any(array.shape[1] != dim for array in arrays):
        raise ValueError("all embedding arrays must have the same second dimension")

    faiss = faiss_module or _import_faiss()
    if index_type == "flat":
        index = faiss.IndexFlatIP(dim)
        effective_nlist = None
    else:
        effective_nlist = max(1, min(int(nlist), total))
        if total < int(nlist):
            effective_nlist = max(1, int(math.sqrt(total)))
        quantizer = faiss.IndexFlatIP(dim)
        index = faiss.IndexIVFFlat(quantizer, dim, effective_nlist, faiss.METRIC_INNER_PRODUCT)
        train_sample = _training_sample(arrays, max_train=max(effective_nlist * 40, 1024))
        if normalize:
            _normalize_in_place(train_sample)
        index.train(train_sample)

    for batch in _iter_batches(arrays, batch_size=batch_size, normalize=normalize):
        index.add(batch)

    output.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(output))
    report = {
        "input": str(embeddings_path),
        "embedding_files": [str(path) for path in files],
        "output": str(output),
        "index_type": index_type,
        "metric": "inner_product",
        "normalized": normalize,
        "vectors": total,
        "dim": dim,
        "nlist": effective_nlist,
        "ntotal": int(index.ntotal),
        "status": "built",
        "note": (
            "Supplemental reconstruction helper for CoRM-RAG. This creates a FAISS "
            "index compatible with run_evaluation.py inputs, but it is not the "
            "authors' original released wiki.faiss artifact."
        ),
    }
    if manifest:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def build_sharded_faiss_indexes(
    embeddings_path: Path,
    output_dir: Path,
    *,
    index_type: str = "flat",
    nlist: int = 4096,
    batch_size: int = 100_000,
    normalize: bool = True,
    manifest: Path | None = None,
    faiss_module: Any | None = None,
) -> dict[str, Any]:
    if index_type not in {"flat", "ivf"}:
        raise ValueError("index_type must be 'flat' or 'ivf'")
    files = find_embedding_files(embeddings_path)
    if not files:
        raise FileNotFoundError(f"no embedding .npy files found under {embeddings_path}")

    faiss = faiss_module or _import_faiss()
    output_dir.mkdir(parents=True, exist_ok=True)
    shards = []
    offset = 0
    dim = None
    for shard_idx, embedding_file in enumerate(files):
        array = _load_array(embedding_file)
        if dim is None:
            dim = int(array.shape[1])
        if int(array.shape[1]) != dim:
            raise ValueError("all embedding arrays must have the same second dimension")
        index = _make_index(
            faiss,
            [array],
            dim=dim,
            index_type=index_type,
            nlist=nlist,
            normalize=normalize,
        )
        for batch in _iter_batches([array], batch_size=batch_size, normalize=normalize):
            index.add(batch)
        index_path = output_dir / f"wiki_faiss_shard_{shard_idx:06d}.faiss"
        faiss.write_index(index, str(index_path))
        rows = int(array.shape[0])
        shards.append(
            {
                "index": shard_idx,
                "embedding_file": str(embedding_file),
                "faiss_file": str(index_path),
                "offset": offset,
                "vectors": rows,
            }
        )
        offset += rows

    report = {
        "input": str(embeddings_path),
        "output_dir": str(output_dir),
        "index_type": index_type,
        "metric": "inner_product",
        "normalized": normalize,
        "vectors": offset,
        "dim": dim,
        "shard_count": len(shards),
        "shards": shards,
        "status": "built",
        "note": (
            "Supplemental sharded FAISS reconstruction. It avoids one giant wiki.faiss "
            "file and requires a sharded-aware evaluation loader."
        ),
    }
    if manifest:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def _make_index(
    faiss: Any,
    arrays: list[np.ndarray],
    *,
    dim: int,
    index_type: str,
    nlist: int,
    normalize: bool,
) -> Any:
    if index_type == "flat":
        return faiss.IndexFlatIP(dim)
    total = int(sum(array.shape[0] for array in arrays))
    effective_nlist = max(1, min(int(nlist), total))
    if total < int(nlist):
        effective_nlist = max(1, int(math.sqrt(total)))
    quantizer = faiss.IndexFlatIP(dim)
    index = faiss.IndexIVFFlat(quantizer, dim, effective_nlist, faiss.METRIC_INNER_PRODUCT)
    train_sample = _training_sample(arrays, max_train=max(effective_nlist * 40, 1024))
    if normalize:
        _normalize_in_place(train_sample)
    index.train(train_sample)
    return index


def find_embedding_files(path: Path) -> list[Path]:
    path = path.resolve()
    if path.is_file():
        return [path]
    if not path.exists():
        return []
    merged = path / "wiki_embeddings.npy"
    if merged.is_file():
        return [merged]
    return sorted(path.glob("embeddings_shard_*.npy"))


def _load_array(path: Path) -> np.ndarray:
    array = np.load(path, mmap_mode="r")
    if array.ndim != 2:
        raise ValueError(f"expected 2D embeddings in {path}, got shape {array.shape}")
    if array.dtype != np.float32:
        array = array.astype(np.float32)
    return array


def _training_sample(arrays: list[np.ndarray], *, max_train: int) -> np.ndarray:
    chunks = []
    remaining = max_train
    for array in arrays:
        if remaining <= 0:
            break
        take = min(int(array.shape[0]), remaining)
        chunks.append(np.array(array[:take], dtype=np.float32, copy=True))
        remaining -= take
    return np.concatenate(chunks, axis=0)


def _iter_batches(
    arrays: Iterable[np.ndarray],
    *,
    batch_size: int,
    normalize: bool,
) -> Iterable[np.ndarray]:
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    for array in arrays:
        for start in range(0, int(array.shape[0]), batch_size):
            batch = np.array(array[start : start + batch_size], dtype=np.float32, copy=True)
            if normalize:
                _normalize_in_place(batch)
            yield batch


def _normalize_in_place(array: np.ndarray) -> None:
    norms = np.linalg.norm(array, axis=1, keepdims=True)
    np.divide(array, np.maximum(norms, 1e-12), out=array)


def _import_faiss() -> Any:
    try:
        import faiss
    except ImportError as exc:  # pragma: no cover - depends on optional runtime
        raise SystemExit("faiss is required: install faiss-cpu or faiss-gpu") from exc
    return faiss


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--embeddings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--index-type", choices=["flat", "ivf"], default="ivf")
    parser.add_argument("--sharded", action="store_true")
    parser.add_argument("--nlist", type=int, default=4096)
    parser.add_argument("--batch-size", type=int, default=100_000)
    parser.add_argument("--no-normalize", action="store_true")
    args = parser.parse_args()

    if args.sharded:
        result = build_sharded_faiss_indexes(
            args.embeddings,
            args.output,
            index_type=args.index_type,
            nlist=args.nlist,
            batch_size=args.batch_size,
            normalize=not args.no_normalize,
            manifest=args.manifest,
        )
    else:
        result = build_faiss_index(
            args.embeddings,
            args.output,
            index_type=args.index_type,
            nlist=args.nlist,
            batch_size=args.batch_size,
            normalize=not args.no_normalize,
            manifest=args.manifest,
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
