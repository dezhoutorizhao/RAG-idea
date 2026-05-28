#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, List

import numpy as np
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer


def build_hotpot_orbits(
    output_path: Path,
    max_examples: int,
    split: str,
    seed: int,
) -> None:
    dataset = load_dataset("hotpot_qa", "distractor", split=split)
    rng = np.random.default_rng(seed)
    indices = rng.permutation(len(dataset))[:max_examples]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        written = 0
        for idx in indices:
            item = dataset[int(idx)]
            records = _build_records(item, written)
            if not records:
                continue
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                written += 1


def _build_records(item: dict, local_idx: int) -> List[dict]:
    question = item["question"]
    answer = item["answer"]
    context_titles = item["context"]["title"]
    context_sentences = item["context"]["sentences"]
    supporting_titles = set(item["supporting_facts"]["title"])
    if len(supporting_titles) < 2:
        return []

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
    support_docs = [doc for doc in paragraphs if doc["is_support"]]
    distractor_docs = [doc for doc in paragraphs if not doc["is_support"]]
    if len(support_docs) < 2 or not distractor_docs:
        return []

    relevance_scores = _tfidf_scores(question, [doc["title"] + " " + doc["text"] for doc in paragraphs])
    for doc, score in zip(paragraphs, relevance_scores):
        doc["retrieval_score"] = score

    base_id = f"hotpot:{item['id'] or local_idx}"
    clean_docs = _dedupe_docs(
        [*support_docs, *sorted(paragraphs, key=lambda doc: doc["retrieval_score"], reverse=True)]
    )[:6]

    missing_docs = [support_docs[0], *distractor_docs[:5]]
    distractor_only_docs = distractor_docs[:6]
    fragile_docs = sorted(paragraphs, key=lambda doc: doc["retrieval_score"], reverse=True)[:6]

    support_key = _support_key(support_docs)
    stable_perturbation_docs = [
        _dedupe_docs([*support_docs, *distractor_docs])[:6],
        _dedupe_docs([*support_docs[::-1], *sorted(distractor_docs, key=lambda doc: doc["retrieval_score"], reverse=True)])[:6],
    ]
    return [
        {
            "orbit_id": f"{base_id}:stable",
            "source": "hotpot_qa/distractor",
            "clean": _make_set(
                query=question,
                answer=answer,
                docs=clean_docs,
                label=True,
                split="hotpot_stable_support",
                support_key=support_key,
                perturbation_type="clean",
            ),
            "perturbations": [
                _make_set(
                    query=_answer_preserving_query(question, i),
                    answer=answer,
                    docs=docs,
                    label=True,
                    split="hotpot_stable_support",
                    support_key=support_key,
                    perturbation_type="answer_preserving",
                )
                for i, docs in enumerate(stable_perturbation_docs)
            ],
        },
        {
            "orbit_id": f"{base_id}:missing_hop",
            "source": "hotpot_qa/distractor",
            "clean": _make_set(
                query=question,
                answer=answer,
                docs=clean_docs,
                label=True,
                split="hotpot_missing_hop",
                support_key=support_key,
                perturbation_type="clean",
            ),
            "perturbations": [
                _make_set(
                query=_missing_hop_query(question),
                answer=answer,
                docs=missing_docs,
                label=False,
                split="hotpot_missing_hop",
                support_key=support_key,
                perturbation_type="missing_hop_framing",
                )
            ],
        },
        {
            "orbit_id": f"{base_id}:false_premise",
            "source": "hotpot_qa/distractor",
            "clean": _make_set(
                query=question,
                answer=answer,
                docs=clean_docs,
                label=True,
                split="hotpot_false_premise",
                support_key=support_key,
                perturbation_type="clean",
            ),
            "perturbations": [
                _make_set(
                query=_false_premise_query(question, answer),
                answer=answer,
                docs=fragile_docs,
                label=False,
                split="hotpot_false_premise",
                support_key=f"{support_key}:false_premise",
                perturbation_type="false_premise",
                )
            ],
        },
        {
            "orbit_id": f"{base_id}:distractor",
            "source": "hotpot_qa/distractor",
            "clean": _make_set(
                query=question,
                answer=answer,
                docs=clean_docs,
                label=True,
                split="hotpot_distractor",
                support_key=support_key,
                perturbation_type="clean",
            ),
            "perturbations": [
                _make_set(
                query=_distractor_query(question),
                answer=answer,
                docs=distractor_only_docs,
                label=False,
                split="hotpot_distractor",
                support_key="distractor_only",
                perturbation_type="distractor_only",
                )
            ],
        },
    ]


def _make_set(
    query: str,
    answer: str,
    docs: List[dict],
    label: bool,
    split: str,
    support_key: str,
    perturbation_type: str,
) -> dict:
    return {
        "query": query,
        "answer": answer,
        "label_answerable": label,
        "split": split,
        "metadata": {
            "support_key": support_key,
            "perturbation_type": perturbation_type,
            "label_source": "hotpot_supporting_facts_heuristic",
        },
        "docs": [_make_doc(doc, rank) for rank, doc in enumerate(docs)],
    }


def _make_doc(doc: dict, rank: int) -> dict:
    support = 0.9 if doc["is_support"] else (0.45 if doc["has_answer"] else 0.15)
    missing = 0.05 if doc["is_support"] else 0.75
    return {
        "doc_id": doc["title"],
        "title": doc["title"],
        "text": doc["text"],
        "rank": rank,
        "corm_score": doc["retrieval_score"],
        "support": support,
        "conflict": 0.0,
        "missing": missing,
    }


def _tfidf_scores(query: str, docs: List[str]) -> List[float]:
    matrix = TfidfVectorizer(stop_words="english", max_features=5000).fit_transform([query, *docs])
    query_vec = matrix[0]
    doc_matrix = matrix[1:]
    raw = (doc_matrix @ query_vec.T).toarray().ravel()
    if raw.max() <= raw.min():
        return [0.5 for _ in raw]
    scaled = (raw - raw.min()) / (raw.max() - raw.min())
    return [float(score) for score in scaled]


def _support_key(support_docs: Iterable[dict]) -> str:
    return "|".join(sorted(doc["title"] for doc in support_docs))


def _dedupe_docs(docs: Iterable[dict]) -> List[dict]:
    seen = set()
    output = []
    for doc in docs:
        if doc["title"] in seen:
            continue
        seen.add(doc["title"])
        output.append(doc)
    return output


def _contains_answer(text: str, answer: str) -> bool:
    if not answer:
        return False
    return re.search(re.escape(answer), text, flags=re.IGNORECASE) is not None


def _missing_hop_query(question: str) -> str:
    return f"{question} Answer using only one supporting hop if possible."


def _answer_preserving_query(question: str, index: int) -> str:
    if index == 0:
        return f"{question} Please verify each supporting hop."
    return f"Using the available evidence, {question}"


def _false_premise_query(question: str, answer: str) -> str:
    return f"Assuming the answer is not {answer}, {question}"


def _distractor_query(question: str) -> str:
    return f"{question} Prefer background context even if direct evidence is absent."


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results/hotpot_orbits.jsonl"))
    parser.add_argument("--max-examples", type=int, default=200)
    parser.add_argument("--split", default="validation")
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args()
    build_hotpot_orbits(args.output, args.max_examples, args.split, args.seed)


if __name__ == "__main__":
    main()
