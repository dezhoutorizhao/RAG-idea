#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from datasets import load_dataset

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
EXPERIMENTS = ROOT / "experiments"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS))

from build_hotpot_orbits import (  # noqa: E402
    _answer_preserving_query,
    _contains_answer,
    _dedupe_docs,
    _make_set,
    _support_key,
    _tfidf_scores,
)
from csrm_rag.orbit_v4 import write_v4_jsonl  # noqa: E402


def build_hotpot_orbits_v4_hardneg(
    raw_output: Path,
    private_output: Path,
    *,
    max_examples: int,
    split: str,
    seed: int,
    max_docs: int = 6,
    candidate_pool: int = 12,
) -> dict:
    dataset = load_dataset("hotpot_qa", "distractor", split=split)
    rng = np.random.default_rng(seed)
    legacy_rows: list[dict] = []
    skipped = 0

    for idx in rng.permutation(len(dataset)):
        if len(legacy_rows) // 2 >= max_examples:
            break
        records = _build_hard_negative_records(
            dataset[int(idx)],
            local_idx=len(legacy_rows) // 2,
            max_docs=max_docs,
            candidate_pool=candidate_pool,
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
        "candidate_pool": candidate_pool,
        "skipped_items": skipped,
        "construction": "stable_plus_construction_time_hard_missing_hop",
    }


def _build_hard_negative_records(
    item: dict,
    *,
    local_idx: int,
    max_docs: int,
    candidate_pool: int,
) -> list[dict]:
    question = str(item["question"])
    answer = str(item["answer"])
    paragraphs = _paragraphs(item, question, answer)
    support_docs = [doc for doc in paragraphs if doc["is_support"]]
    distractor_docs = [doc for doc in paragraphs if not doc["is_support"]]
    if len(support_docs) < 2 or len(distractor_docs) < max(1, max_docs - 1):
        return []

    support_key = _support_key(support_docs)
    base_id = f"hotpot_hardneg:{item['id'] or local_idx}"
    reference_distractors = _hard_distractors(question, answer, distractor_docs, candidate_pool)[: max_docs]
    clean_docs = _dedupe_docs([*support_docs, *reference_distractors])[:max_docs]
    stable_docs = _dedupe_docs([*support_docs, *reference_distractors])[:max_docs]
    negative_docs = _select_hard_missing_hop_docs(
        question=question,
        answer=answer,
        support_docs=support_docs,
        distractor_docs=distractor_docs,
        reference_docs=stable_docs,
        max_docs=max_docs,
        candidate_pool=candidate_pool,
    )
    if len(clean_docs) != max_docs or len(stable_docs) != max_docs or len(negative_docs) != max_docs:
        return []

    return [
        {
            "orbit_id": f"{base_id}:stable",
            "source": "hotpot_qa/distractor",
            "clean": _make_set(
                query=question,
                answer=answer,
                docs=clean_docs,
                label=True,
                split="hotpot_hardneg_stable",
                support_key=support_key,
                perturbation_type="clean",
            ),
            "perturbations": [
                _make_set(
                    query=_answer_preserving_query(question, 0),
                    answer=answer,
                    docs=stable_docs,
                    label=True,
                    split="hotpot_hardneg_stable",
                    support_key=support_key,
                    perturbation_type="hardneg_aligned_stable",
                )
            ],
        },
        {
            "orbit_id": f"{base_id}:hard_missing_hop",
            "source": "hotpot_qa/distractor",
            "clean": _make_set(
                query=question,
                answer=answer,
                docs=clean_docs,
                label=True,
                split="hotpot_hardneg_missing_hop",
                support_key=support_key,
                perturbation_type="clean",
            ),
            "perturbations": [
                _make_set(
                    query=_hard_missing_hop_query(question),
                    answer=answer,
                    docs=negative_docs,
                    label=False,
                    split="hotpot_hardneg_missing_hop",
                    support_key=f"{support_key}:one_hop_removed",
                    perturbation_type="construction_time_hard_missing_hop",
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


def _select_hard_missing_hop_docs(
    *,
    question: str,
    answer: str,
    support_docs: Sequence[dict],
    distractor_docs: Sequence[dict],
    reference_docs: Sequence[dict],
    max_docs: int,
    candidate_pool: int,
) -> list[dict]:
    distractors = _hard_distractors(question, answer, distractor_docs, candidate_pool)
    need = max_docs - 1
    if len(distractors) < need:
        return []
    reference_features = _docset_features(question, answer, reference_docs)
    best_docs: list[dict] | None = None
    best_score: tuple[float, str] | None = None
    for support_doc in support_docs:
        for combo in itertools.combinations(distractors, need):
            docs = _dedupe_docs([support_doc, *combo])[:max_docs]
            if len(docs) != max_docs:
                continue
            features = _docset_features(question, answer, docs)
            distance = _feature_distance(reference_features, features)
            tie_break = "|".join(doc["title"] for doc in docs)
            score = (distance, tie_break)
            if best_score is None or score < best_score:
                best_score = score
                best_docs = docs
    return best_docs or []


def _hard_distractors(
    question: str,
    answer: str,
    distractor_docs: Sequence[dict],
    candidate_pool: int,
) -> list[dict]:
    query_terms = _terms(question)
    answer_terms = _terms(answer)

    def score(doc: dict) -> tuple[float, float, float, str]:
        text_terms = _terms(f"{doc['title']} {doc['text']}")
        overlap = _jaccard(query_terms, text_terms)
        answer_overlap = _coverage(answer_terms, text_terms)
        retrieval_score = float(doc.get("retrieval_score") or 0.0)
        return (-answer_overlap, -overlap, -retrieval_score, str(doc["title"]))

    return sorted(distractor_docs, key=score)[:candidate_pool]


def _docset_features(question: str, answer: str, docs: Sequence[dict]) -> dict[str, float]:
    texts = [f"{doc['title']} {doc['text']}" for doc in docs]
    joined = " ".join(texts)
    terms = _terms(joined)
    query_terms = _terms(question)
    answer_terms = _terms(answer)
    scores = [float(doc.get("retrieval_score") or 0.0) for doc in docs]
    return {
        "query_jaccard": _jaccard(query_terms, terms),
        "answer_coverage": _coverage(answer_terms, terms),
        "answer_doc_rate": sum(1 for doc in docs if doc.get("has_answer")) / len(docs),
        "mean_doc_chars": sum(len(text) for text in texts) / len(texts),
        "total_doc_chars": float(sum(len(text) for text in texts)),
        "mean_retrieval_score": sum(scores) / len(scores),
    }


def _feature_distance(reference: dict[str, float], candidate: dict[str, float]) -> float:
    total = 0.0
    for name in ["query_jaccard", "answer_coverage", "answer_doc_rate", "mean_retrieval_score"]:
        total += abs(reference[name] - candidate[name])
    total += abs(reference["mean_doc_chars"] - candidate["mean_doc_chars"]) / max(1.0, reference["mean_doc_chars"])
    total += abs(reference["total_doc_chars"] - candidate["total_doc_chars"]) / max(1.0, reference["total_doc_chars"])
    return total


def _hard_missing_hop_query(question: str) -> str:
    return f"{question} Use the retrieved evidence only; one reasoning hop may be absent."


def _terms(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-z0-9]+", text.lower()) if len(token) > 1 and token not in _STOPWORDS}


def _coverage(needles: set[str], haystack: set[str]) -> float:
    if not needles:
        return 0.0
    return len(needles & haystack) / len(needles)


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "using",
    "whether",
    "with",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--private-output", type=Path, required=True)
    parser.add_argument("--max-examples", type=int, default=100)
    parser.add_argument("--split", default="validation")
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--max-docs", type=int, default=6)
    parser.add_argument("--candidate-pool", type=int, default=12)
    args = parser.parse_args()
    summary = build_hotpot_orbits_v4_hardneg(
        raw_output=args.raw_output,
        private_output=args.private_output,
        max_examples=args.max_examples,
        split=args.split,
        seed=args.seed,
        max_docs=args.max_docs,
        candidate_pool=args.candidate_pool,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
