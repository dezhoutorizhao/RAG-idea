#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

import torch
from transformers import AutoTokenizer


def score_orbits_corm(
    input_path: Path,
    output_path: Path,
    checkpoint_path: Path,
    corm_src: Path,
    backbone: str,
    batch_size: int,
    max_length: int,
    max_orbits: int | None,
    device: str | None,
) -> None:
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"CoRM checkpoint not found: {checkpoint_path}")
    if not corm_src.exists():
        raise FileNotFoundError(f"CoRM source directory not found: {corm_src}")

    sys.path.insert(0, str(corm_src))
    from train_critic import EvidenceCritic  # type: ignore

    device_obj = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    tokenizer = AutoTokenizer.from_pretrained(backbone)
    model = EvidenceCritic(backbone=backbone)
    state = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(state["model"])
    try:
        model.encoder.gradient_checkpointing_disable()
    except Exception:
        pass
    model.to(device_obj).float().eval()

    records = _load_records(input_path, max_orbits=max_orbits)
    pending = list(_iter_docs(records))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cache: dict[tuple[str, str], float] = {}
    for start in range(0, len(pending), batch_size):
        batch = pending[start : start + batch_size]
        uncached = [
            (query, doc)
            for query, doc in batch
            if (query, doc.get("text", "")) not in cache
        ]
        if uncached:
            queries = [query for query, _doc in uncached]
            texts = [doc.get("text", "") for _query, doc in uncached]
            scores = _score_batch(
                model=model,
                tokenizer=tokenizer,
                queries=queries,
                docs=texts,
                max_length=max_length,
                device=device_obj,
            )
            for (query, doc), score in zip(uncached, scores):
                cache[(query, doc.get("text", ""))] = score

        for query, doc in batch:
            old_score = doc.get("corm_score")
            if old_score is not None:
                doc.setdefault("metadata", {})["pre_corm_score"] = old_score
            doc["corm_score"] = cache[(query, doc.get("text", ""))]
            doc["corm_scorer"] = "released_corm_critic"
            doc["corm_backbone"] = backbone

    with output_path.open("w", encoding="utf-8") as dst:
        for record in records:
            dst.write(json.dumps(record, ensure_ascii=False) + "\n")


def _load_records(input_path: Path, max_orbits: int | None) -> List[dict]:
    records = []
    with input_path.open("r", encoding="utf-8") as src:
        for line in src:
            if max_orbits is not None and len(records) >= max_orbits:
                break
            if line.strip():
                records.append(json.loads(line))
    return records


def _iter_docs(records: Iterable[dict]) -> Iterable[Tuple[str, dict]]:
    for record in records:
        for evidence_set in [record["clean"], *record.get("perturbations", [])]:
            query = evidence_set.get("query", "")
            for doc in evidence_set.get("docs", []):
                yield query, doc


def _score_batch(
    model,
    tokenizer,
    queries: List[str],
    docs: List[str],
    max_length: int,
    device: torch.device,
) -> List[float]:
    encoded = tokenizer(
        queries,
        docs,
        max_length=max_length,
        truncation=True,
        padding=True,
        return_tensors="pt",
    )
    encoded = {key: value.to(device) for key, value in encoded.items()}
    with torch.inference_mode():
        scores = model.predict_robustness(
            encoded["input_ids"],
            encoded["attention_mask"],
        )
    return [float(score) for score in scores.detach().cpu()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("checkpoints/hf/critic-v12-mixed/checkpoint-latest/state.pt"),
    )
    parser.add_argument(
        "--corm-src",
        type=Path,
        default=Path("external_repos/CoRM-RAG/src"),
    )
    parser.add_argument("--backbone", default="microsoft/deberta-v3-large")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--max-orbits", type=int)
    parser.add_argument("--device")
    args = parser.parse_args()
    score_orbits_corm(
        input_path=args.input,
        output_path=args.output,
        checkpoint_path=args.checkpoint,
        corm_src=args.corm_src,
        backbone=args.backbone,
        batch_size=args.batch_size,
        max_length=args.max_length,
        max_orbits=args.max_orbits,
        device=args.device,
    )


if __name__ == "__main__":
    main()
