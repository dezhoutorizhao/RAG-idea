#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

import numpy as np
from datasets import load_dataset

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
EXPERIMENTS = ROOT / "experiments"
for path in [ROOT, SRC, EXPERIMENTS]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from build_hotpot_orbits import (  # noqa: E402
    _answer_preserving_query,
    _contains_answer,
    _dedupe_docs,
    _make_set,
    _support_key,
    _tfidf_scores,
)
from csrm_rag.orbit_v4 import write_v4_jsonl  # noqa: E402


def build_hotpot_orbits_v4_semantic_swap(
    raw_output: Path,
    private_output: Path,
    *,
    max_examples: int,
    split: str,
    seed: int,
    max_docs: int = 6,
) -> dict:
    dataset = load_dataset("hotpot_qa", "distractor", split=split)
    rng = np.random.default_rng(seed)
    legacy_rows: list[dict] = []
    skipped = 0

    for idx in rng.permutation(len(dataset)):
        if len(legacy_rows) // 2 >= max_examples:
            break
        records = _build_semantic_swap_records(
            dataset[int(idx)],
            local_idx=len(legacy_rows) // 2,
            max_docs=max_docs,
        )
        if records:
            legacy_rows.extend(records)
        else:
            skipped += 1

    count = write_v4_jsonl(
        legacy_rows,
        raw_path=raw_output,
        private_path=private_output,
        dataset="hotpot_qa/distractor",
        perturbation_limit=1,
    )
    return {
        "dataset": "hotpot_qa/distractor",
        "raw_output": str(raw_output),
        "private_output": str(private_output),
        "orbits": count,
        "source_examples": count // 2,
        "split": split,
        "seed": seed,
        "max_examples": max_examples,
        "max_docs": max_docs,
        "skipped_items": skipped,
        "construction": "stable_plus_answer_preserving_semantic_swap",
    }


def _build_semantic_swap_records(item: dict, *, local_idx: int, max_docs: int) -> list[dict]:
    question = str(item["question"])
    answer = str(item["answer"])
    paragraphs = _paragraphs(item, question, answer)
    support_docs = [doc for doc in paragraphs if doc["is_support"]]
    distractor_docs = [doc for doc in paragraphs if not doc["is_support"]]
    if len(support_docs) < 2 or not distractor_docs:
        return []

    shared_docs = _shared_docs(support_docs, distractor_docs, max_docs)
    if len(shared_docs) != max_docs or not any(doc["has_answer"] for doc in shared_docs):
        return []
    swap_entity = _swap_entity(answer, shared_docs, distractor_docs)
    if not swap_entity:
        return []
    swapped_docs = _swap_answer_in_docs(shared_docs, answer, swap_entity)
    if not swapped_docs or [doc["title"] for doc in swapped_docs] != [doc["title"] for doc in shared_docs]:
        return []

    support_key = _support_key(support_docs)
    base_id = f"hotpot_semanticswap:{item['id'] or local_idx}"
    return [
        {
            "orbit_id": f"{base_id}:stable",
            "source": "hotpot_qa/distractor",
            "clean": _make_set(
                query=question,
                answer=answer,
                docs=shared_docs,
                label=True,
                split="hotpot_semanticswap_stable",
                support_key=support_key,
                perturbation_type="clean",
            ),
            "perturbations": [
                _make_set(
                    query=_answer_preserving_query(question, 0),
                    answer=answer,
                    docs=shared_docs,
                    label=True,
                    split="hotpot_semanticswap_stable",
                    support_key=support_key,
                    perturbation_type="answer_preserving_stable",
                )
            ],
        },
        {
            "orbit_id": f"{base_id}:semantic_swap",
            "source": "hotpot_qa/distractor",
            "clean": _make_set(
                query=question,
                answer=answer,
                docs=shared_docs,
                label=True,
                split="hotpot_semanticswap_fragile",
                support_key=support_key,
                perturbation_type="clean",
            ),
            "perturbations": [
                _make_set(
                    query=_semantic_swap_query(question),
                    answer=answer,
                    docs=swapped_docs,
                    label=False,
                    split="hotpot_semanticswap_fragile",
                    support_key=f"{support_key}:answer_swapped_to={swap_entity}",
                    perturbation_type="support_preserving_answer_entity_swap",
                )
            ],
        },
    ]


def _paragraphs(item: dict, question: str, answer: str) -> list[dict]:
    context_titles = item["context"]["title"]
    context_sentences = item["context"]["sentences"]
    supporting_titles = set(item["supporting_facts"]["title"])
    paragraphs = []
    for title, sentences in zip(context_titles, context_sentences):
        text = " ".join(sentences)
        paragraphs.append(
            {
                "title": title,
                "text": text,
                "is_support": title in supporting_titles,
                "has_answer": _contains_answer(text, answer),
            }
        )
    relevance_scores = _tfidf_scores(question, [doc["title"] + " " + doc["text"] for doc in paragraphs])
    for doc, score in zip(paragraphs, relevance_scores):
        doc["retrieval_score"] = score
    return paragraphs


def _shared_docs(support_docs: list[dict], distractor_docs: list[dict], max_docs: int) -> list[dict]:
    hard_distractors = sorted(
        distractor_docs,
        key=lambda doc: (-float(doc.get("retrieval_score") or 0.0), str(doc["title"])),
    )
    return _dedupe_docs([*support_docs, *hard_distractors])[:max_docs]


def _swap_entity(answer: str, shared_docs: list[dict], distractor_docs: list[dict]) -> str | None:
    answer_norm = _norm(answer)
    candidates = []
    for doc in [*distractor_docs, *shared_docs]:
        title = str(doc.get("title") or "").strip()
        if title and _norm(title) != answer_norm and title not in candidates:
            candidates.append(title)
    if candidates:
        return sorted(candidates, key=lambda item: (abs(len(item) - len(answer)), item))[0]
    return None


def _swap_answer_in_docs(docs: list[dict], answer: str, replacement: str) -> list[dict]:
    swapped = []
    changed = False
    pattern = re.compile(re.escape(answer), flags=re.IGNORECASE)
    for doc in docs:
        new_doc = copy.deepcopy(doc)
        new_text, count = pattern.subn(replacement, str(new_doc.get("text") or ""), count=2)
        if count:
            changed = True
            new_doc["text"] = new_text
            new_doc["has_answer"] = _contains_answer(new_text, answer)
        swapped.append(new_doc)
    return swapped if changed else []


def _semantic_swap_query(question: str) -> str:
    return f"{question} Verify the original answer using only the provided evidence."


def _norm(text: str) -> str:
    return re.sub(r"\W+", " ", text.lower()).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--private-output", type=Path, required=True)
    parser.add_argument("--max-examples", type=int, default=100)
    parser.add_argument("--split", default="validation")
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--max-docs", type=int, default=6)
    args = parser.parse_args()
    summary = build_hotpot_orbits_v4_semantic_swap(
        raw_output=args.raw_output,
        private_output=args.private_output,
        max_examples=args.max_examples,
        split=args.split,
        seed=args.seed,
        max_docs=args.max_docs,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
