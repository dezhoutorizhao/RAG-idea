#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any, Iterable, Iterator

import numpy as np


def article_to_passages(title: str, text: str, *, words_per_passage: int = 200, min_words: int = 30) -> list[str]:
    words = text.split()
    passages = []
    for start in range(0, len(words), words_per_passage):
        chunk_words = words[start : start + words_per_passage]
        if len(chunk_words) < min_words:
            continue
        passages.append(f"{title}: {' '.join(chunk_words)}")
    return passages


def iter_wikipedia_passages(
    dataset: Iterable[dict[str, Any]],
    *,
    max_articles: int | None = None,
    max_passages: int | None = None,
    skip_passages: int = 0,
    words_per_passage: int = 200,
    min_words: int = 30,
) -> Iterator[tuple[int, str]]:
    seen = 0
    if skip_passages < 0:
        raise ValueError("skip_passages must be non-negative")
    for article_idx, article in enumerate(dataset):
        if max_articles is not None and article_idx >= max_articles:
            break
        title = str(article.get("title", ""))
        text = str(article.get("text", ""))
        for passage in article_to_passages(
            title,
            text,
            words_per_passage=words_per_passage,
            min_words=min_words,
        ):
            if max_passages is not None and seen >= max_passages:
                return
            if seen < skip_passages:
                seen += 1
                continue
            yield article_idx, passage
            seen += 1


def load_wikipedia_stream() -> Iterable[dict[str, Any]]:
    from datasets import load_dataset

    try:
        return load_dataset("wikimedia/wikipedia", "20231101.en", split="train", streaming=True)
    except Exception:
        return load_dataset("wikipedia", "20220301.en", split="train", streaming=True, trust_remote_code=True)


def load_jsonl_articles(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if "title" in row and "text" in row:
                yield {"title": row["title"], "text": row["text"]}
            elif "text" in row:
                yield {"title": row.get("title", "staged"), "text": row["text"]}
            else:
                raise ValueError(f"JSONL row must contain text: {row}")


def mean_pooling(model_output: Any, attention_mask: Any) -> Any:
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return token_embeddings.mul(input_mask_expanded).sum(1) / input_mask_expanded.sum(1).clamp(min=1e-9)


def encode_passages(
    passages: list[str],
    *,
    tokenizer: Any,
    model: Any,
    device: str,
    batch_size: int,
    max_length: int,
) -> np.ndarray:
    import torch

    batches = []
    with torch.no_grad():
        for start in range(0, len(passages), batch_size):
            batch = passages[start : start + batch_size]
            enc = tokenizer(
                batch,
                max_length=max_length,
                truncation=True,
                padding=True,
                return_tensors="pt",
            ).to(device)
            outputs = model(**enc)
            emb = mean_pooling(outputs, enc["attention_mask"])
            emb = torch.nn.functional.normalize(emb, p=2, dim=1)
            batches.append(emb.cpu().numpy().astype(np.float32, copy=False))
    return np.concatenate(batches, axis=0) if batches else np.empty((0, 0), dtype=np.float32)


def encode_passages_dummy(passages: list[str], *, dim: int = 16) -> np.ndarray:
    rows = []
    for passage in passages:
        digest = hashlib.sha256(passage.encode("utf-8")).digest()
        raw = np.frombuffer((digest * ((dim // len(digest)) + 1))[:dim], dtype=np.uint8).astype(np.float32)
        raw = raw - raw.mean()
        norm = np.linalg.norm(raw)
        rows.append(raw / max(norm, 1e-12))
    return np.asarray(rows, dtype=np.float32)


def _save_npy_chunked(path: Path, array: np.ndarray, *, row_chunk_size: int = 8192) -> None:
    array = np.ascontiguousarray(array)
    header = {
        "descr": np.lib.format.dtype_to_descr(array.dtype),
        "fortran_order": False,
        "shape": array.shape,
    }
    with path.open("wb") as handle:
        np.lib.format.write_array_header_1_0(handle, header)
        if array.ndim == 0:
            handle.write(array.tobytes(order="C"))
            return
        rows = int(array.shape[0])
        for start in range(0, rows, row_chunk_size):
            chunk = np.ascontiguousarray(array[start : start + row_chunk_size])
            handle.write(chunk.tobytes(order="C"))


def _embedding_shard_index(path: Path) -> int:
    match = re.fullmatch(r"embeddings_shard_(\d{6})\.npy", path.name)
    if not match:
        raise ValueError(f"unexpected embedding shard name: {path.name}")
    return int(match.group(1))


def _load_completed_shard(shard: Path) -> tuple[Path, int]:
    array = np.load(shard, mmap_mode="r")
    if array.ndim != 2:
        raise ValueError(f"embedding shard must be rank-2: {shard}")
    rows = int(array.shape[0])
    if rows < 1:
        raise ValueError(f"embedding shard must not be empty: {shard}")
    expected_size = int(getattr(array, "offset", 0)) + int(array.nbytes)
    actual_size = shard.stat().st_size
    if actual_size < expected_size:
        raise ValueError(
            f"incomplete embedding shard: {shard} has {actual_size} bytes, expected at least {expected_size}"
        )
    return shard, rows


def _completed_embedding_shards(
    output_dir: Path,
    *,
    drop_incomplete_last: bool = False,
) -> tuple[list[tuple[Path, int]], list[str]]:
    shards = sorted(output_dir.glob("embeddings_shard_*.npy"), key=_embedding_shard_index)
    completed = []
    dropped = []
    for expected_idx, shard in enumerate(shards):
        actual_idx = _embedding_shard_index(shard)
        if actual_idx != expected_idx:
            raise ValueError(f"non-consecutive embedding shards: expected {expected_idx:06d}, found {shard.name}")
        try:
            completed.append(_load_completed_shard(shard))
        except (OSError, ValueError) as exc:
            if not drop_incomplete_last:
                raise
            for suffix_shard in shards[expected_idx:]:
                suffix_idx = _embedding_shard_index(suffix_shard)
                if suffix_idx != expected_idx + len(dropped):
                    raise ValueError(
                        f"non-consecutive embedding shards after incomplete suffix: "
                        f"expected {expected_idx + len(dropped):06d}, found {suffix_shard.name}"
                    )
                dropped.append(f"{suffix_shard.name}: dropped incomplete or placeholder suffix")
                try:
                    suffix_shard.open("wb").close()
                except OSError:
                    suffix_shard.unlink()
            break
    return completed, dropped


def _count_jsonl_lines(path: Path) -> int:
    with path.open("rb") as handle:
        return sum(1 for _ in handle)


def _write_passage_shard(path: Path, passages: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for passage in passages:
            handle.write(json.dumps({"text": passage}, ensure_ascii=False) + "\n")


def _truncate_jsonl_to_lines(path: Path, keep_lines: int) -> None:
    if keep_lines < 0:
        raise ValueError("keep_lines must be non-negative")
    with path.open("rb+") as handle:
        truncate_at = 0
        for _ in range(keep_lines):
            line = handle.readline()
            if not line:
                raise ValueError(f"cannot truncate {path}: fewer than {keep_lines} lines")
            truncate_at = handle.tell()
        handle.truncate(truncate_at)


def encode_wikipedia_streaming(
    *,
    output_dir: Path,
    model_name: str = "facebook/contriever-msmarco",
    device: str = "cuda:0",
    encode_batch_size: int = 256,
    passages_per_shard: int = 50_000,
    max_length: int = 256,
    max_articles: int | None = None,
    max_passages: int | None = None,
    dataset: Iterable[dict[str, Any]] | None = None,
    input_jsonl: Path | None = None,
    backend: str = "hf",
    dummy_dim: int = 16,
    resume: bool = False,
    passage_output: str = "monolithic",
) -> dict[str, Any]:
    if encode_batch_size < 1:
        raise ValueError("encode_batch_size must be positive")
    if passages_per_shard < 1:
        raise ValueError("passages_per_shard must be positive")

    if backend not in {"hf", "dummy"}:
        raise ValueError("backend must be 'hf' or 'dummy'")
    if passage_output not in {"monolithic", "sharded", "both"}:
        raise ValueError("passage_output must be 'monolithic', 'sharded', or 'both'")

    output_dir.mkdir(parents=True, exist_ok=True)
    passages_path = output_dir / "wiki_passages.jsonl"
    passage_shard_dir = output_dir / "wiki_passage_shards"
    manifest_path = output_dir / "wiki_streaming_manifest.json"

    resume_existing_shards = 0
    resume_completed_passages = 0
    resume_passage_lines_before_repair = None
    resume_repaired_passages = False
    resume_dropped_incomplete_shards: list[str] = []
    if resume:
        existing_shards, resume_dropped_incomplete_shards = _completed_embedding_shards(
            output_dir,
            drop_incomplete_last=True,
        )
        resume_existing_shards = len(existing_shards)
        resume_completed_passages = sum(rows for _, rows in existing_shards)
        if passage_output in {"monolithic", "both"} and resume_completed_passages and not passages_path.exists():
            raise ValueError("cannot resume: wiki_passages.jsonl is missing")
        if passage_output in {"monolithic", "both"} and passages_path.exists():
            resume_passage_lines_before_repair = _count_jsonl_lines(passages_path)
            if resume_passage_lines_before_repair < resume_completed_passages:
                raise ValueError(
                    "cannot resume: wiki_passages.jsonl has fewer rows than completed embedding shards "
                    f"({resume_passage_lines_before_repair} < {resume_completed_passages})"
                )
            if resume_passage_lines_before_repair > resume_completed_passages:
                repair_path = output_dir / "wiki_passages.jsonl.resume_repair"
                if repair_path.exists():
                    repair_path.unlink()
                _truncate_jsonl_to_lines(passages_path, resume_completed_passages)
                resume_repaired_passages = True
    else:
        for stale in output_dir.glob("embeddings_shard_*.npy"):
            stale.unlink()
        if passages_path.exists():
            passages_path.unlink()
        if passage_shard_dir.exists():
            for stale in passage_shard_dir.glob("wiki_passages_shard_*.jsonl"):
                stale.unlink()

    if dataset is None:
        dataset = load_jsonl_articles(input_jsonl) if input_jsonl else load_wikipedia_stream()
    tokenizer = model = None
    if backend == "hf":
        from transformers import AutoModel, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name).to(device).eval()

    shard_paths: list[str] = [str(path) for path, _ in existing_shards] if resume else []
    buffer: list[str] = []
    total_passages = resume_completed_passages
    articles_seen = 0
    shard_idx = resume_existing_shards
    t0 = time.time()

    def flush() -> None:
        nonlocal buffer, shard_idx, total_passages
        if not buffer:
            return
        shard_passages = buffer
        if backend == "dummy":
            embeddings = encode_passages_dummy(shard_passages, dim=dummy_dim)
        else:
            embeddings = encode_passages(
                shard_passages,
                tokenizer=tokenizer,
                model=model,
                device=device,
                batch_size=encode_batch_size,
                max_length=max_length,
            )
        shard_path = output_dir / f"embeddings_shard_{shard_idx:06d}.npy"
        _save_npy_chunked(shard_path, embeddings.astype(np.float32, copy=False))
        if passage_output in {"sharded", "both"}:
            passage_shard_path = passage_shard_dir / f"wiki_passages_shard_{shard_idx:06d}.jsonl"
            _write_passage_shard(passage_shard_path, shard_passages)
        shard_paths.append(str(shard_path))
        total_passages += len(shard_passages)
        shard_idx += 1
        buffer = []

    passage_mode = "a" if resume else "w"
    passages_file = passages_path.open(passage_mode, encoding="utf-8") if passage_output in {"monolithic", "both"} else None
    try:
        for article_idx, passage in iter_wikipedia_passages(
            dataset,
            max_articles=max_articles,
            max_passages=max_passages,
            skip_passages=resume_completed_passages,
        ):
            articles_seen = max(articles_seen, article_idx + 1)
            if passages_file is not None:
                passages_file.write(json.dumps({"text": passage}, ensure_ascii=False) + "\n")
            buffer.append(passage)
            if len(buffer) >= passages_per_shard:
                flush()
        flush()
    finally:
        if passages_file is not None:
            passages_file.close()

    if model is not None:
        import torch

        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    manifest = {
        "status": "built",
        "output_dir": str(output_dir),
        "passages_path": str(passages_path) if passage_output in {"monolithic", "both"} else None,
        "passage_output": passage_output,
        "passage_shard_dir": str(passage_shard_dir) if passage_output in {"sharded", "both"} else None,
        "embedding_shards": shard_paths,
        "embedding_shard_count": len(shard_paths),
        "passages": total_passages,
        "articles_seen": articles_seen,
        "model_name": model_name,
        "backend": backend,
        "input_jsonl": str(input_jsonl) if input_jsonl else None,
        "device": device,
        "encode_batch_size": encode_batch_size,
        "passages_per_shard": passages_per_shard,
        "max_articles": max_articles,
        "max_passages": max_passages,
        "dummy_dim": dummy_dim if backend == "dummy" else None,
        "resume": resume,
        "resume_existing_shards": resume_existing_shards,
        "resume_completed_passages": resume_completed_passages,
        "resume_existing_shard_rows": [rows for _, rows in existing_shards] if resume else [],
        "resume_passage_lines_before_repair": resume_passage_lines_before_repair,
        "resume_repaired_passages": resume_repaired_passages,
        "resume_dropped_incomplete_shards": resume_dropped_incomplete_shards,
        "elapsed_seconds": round(time.time() - t0, 3),
        "note": (
            "Supplemental streaming encoder for CoRM-RAG reconstruction. It writes "
            "wiki_passages.jsonl and embeddings_shard_*.npy without holding the full "
            "Wikipedia passage list or full embedding matrix in memory."
        ),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model-name", default="facebook/contriever-msmarco")
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--encode-batch-size", type=int, default=256)
    parser.add_argument("--passages-per-shard", type=int, default=50_000)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--max-articles", type=int)
    parser.add_argument("--max-passages", type=int)
    parser.add_argument("--input-jsonl", type=Path)
    parser.add_argument("--backend", choices=["hf", "dummy"], default="hf")
    parser.add_argument("--dummy-dim", type=int, default=16)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--passage-output", choices=["monolithic", "sharded", "both"], default="monolithic")
    args = parser.parse_args()

    manifest = encode_wikipedia_streaming(
        output_dir=args.output_dir,
        model_name=args.model_name,
        device=args.device,
        encode_batch_size=args.encode_batch_size,
        passages_per_shard=args.passages_per_shard,
        max_length=args.max_length,
        max_articles=args.max_articles,
        max_passages=args.max_passages,
        input_jsonl=args.input_jsonl,
        backend=args.backend,
        dummy_dim=args.dummy_dim,
        resume=args.resume,
        passage_output=args.passage_output,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
