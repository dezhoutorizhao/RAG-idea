#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Tuple

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def score_orbits_nli(
    input_path: Path,
    output_path: Path,
    model_name: str,
    batch_size: int,
    max_length: int,
    max_orbits: int | None,
    device: str | None,
    unit: str,
) -> None:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    device_obj = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    model.to(device_obj)
    model.eval()
    label_indices = _label_indices(model.config.id2label)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open("r", encoding="utf-8") as src, output_path.open("w", encoding="utf-8") as dst:
        pending: List[Tuple[dict, dict, dict | None]] = []
        records = []
        for line_no, line in enumerate(src, start=1):
            if max_orbits is not None and len(records) >= max_orbits:
                break
            if not line.strip():
                continue
            record = json.loads(line)
            records.append(record)
            for evidence_set in [record["clean"], *record.get("perturbations", [])]:
                if unit == "set":
                    pending.append((record, evidence_set, None))
                else:
                    for doc in evidence_set.get("docs", []):
                        pending.append((record, evidence_set, doc))

        for start in range(0, len(pending), batch_size):
            batch = pending[start : start + batch_size]
            premises = [
                _premise(evidence_set, doc, unit)
                for _record, evidence_set, doc in batch
            ]
            hypotheses = [
                _hypothesis(evidence_set.get("query", ""), evidence_set.get("answer", ""))
                for _record, evidence_set, _doc in batch
            ]
            probs = _predict_nli(
                model,
                tokenizer,
                premises,
                hypotheses,
                label_indices,
                max_length,
                device_obj,
            )
            for (_record, evidence_set, doc), scores in zip(batch, probs):
                if unit == "set":
                    evidence_set.setdefault("metadata", {})["set_nli_support"] = scores["entailment"]
                    evidence_set.setdefault("metadata", {})["set_nli_conflict"] = scores["contradiction"]
                    evidence_set.setdefault("metadata", {})["set_nli_missing"] = max(
                        scores["neutral"], 1.0 - scores["entailment"]
                    )
                    evidence_set.setdefault("metadata", {})["nli_model"] = model_name
                    evidence_set.setdefault("metadata", {})["nli_unit"] = unit
                    for set_doc in evidence_set.get("docs", []):
                        set_doc["support"] = scores["entailment"]
                        set_doc["conflict"] = scores["contradiction"]
                        set_doc["missing"] = max(scores["neutral"], 1.0 - scores["entailment"])
                        set_doc["nli_model"] = model_name
                        set_doc["nli_unit"] = unit
                else:
                    assert doc is not None
                    doc["support"] = scores["entailment"]
                    doc["conflict"] = scores["contradiction"]
                    doc["missing"] = max(scores["neutral"], 1.0 - scores["entailment"])
                    doc["nli_model"] = model_name
                    doc["nli_unit"] = unit

        for record in records:
            dst.write(json.dumps(record, ensure_ascii=False) + "\n")


def _predict_nli(
    model,
    tokenizer,
    premises: List[str],
    hypotheses: List[str],
    label_indices: dict,
    max_length: int,
    device: torch.device,
) -> List[dict]:
    encoded = tokenizer(
        premises,
        hypotheses,
        truncation=True,
        padding=True,
        max_length=max_length,
        return_tensors="pt",
    )
    encoded = {key: value.to(device) for key, value in encoded.items()}
    with torch.inference_mode():
        logits = model(**encoded).logits
        prob = torch.softmax(logits, dim=-1).detach().cpu()
    output = []
    for row in prob:
        output.append(
            {
                "entailment": float(row[label_indices["entailment"]]),
                "contradiction": float(row[label_indices["contradiction"]]),
                "neutral": float(row[label_indices["neutral"]]),
            }
        )
    return output


def _label_indices(id2label: dict) -> dict:
    normalized = {idx: label.lower() for idx, label in id2label.items()}
    indices = {}
    for target in ["entailment", "contradiction", "neutral"]:
        for idx, label in normalized.items():
            if target in label:
                indices[target] = int(idx)
                break
    if set(indices) == {"entailment", "contradiction", "neutral"}:
        return indices

    # Common MNLI fallback order for many sequence-classification checkpoints.
    return {"contradiction": 0, "neutral": 1, "entailment": 2}


def _hypothesis(query: str, answer: str) -> str:
    return f"For the question '{query}', the answer is '{answer}'."


def _premise(evidence_set: dict, doc: dict | None, unit: str) -> str:
    if unit == "doc":
        assert doc is not None
        return doc.get("text", "")
    docs = evidence_set.get("docs", [])
    parts = []
    for item in docs:
        title = item.get("title") or item.get("doc_id") or ""
        text = item.get("text", "")
        parts.append(f"{title}: {text}")
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="cross-encoder/nli-deberta-v3-small")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=384)
    parser.add_argument("--max-orbits", type=int)
    parser.add_argument("--device")
    parser.add_argument("--unit", choices=["doc", "set"], default="doc")
    args = parser.parse_args()
    score_orbits_nli(
        input_path=args.input,
        output_path=args.output,
        model_name=args.model,
        batch_size=args.batch_size,
        max_length=args.max_length,
        max_orbits=args.max_orbits,
        device=args.device,
        unit=args.unit,
    )


if __name__ == "__main__":
    main()
