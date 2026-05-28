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


def build_fever_orbits(
    output_path: Path,
    max_examples: int,
    split: str,
    seed: int,
) -> None:
    dataset = load_dataset("copenlu/fever_gold_evidence", split=split)
    examples = [
        item
        for item in dataset
        if item.get("label") in {"SUPPORTS", "REFUTES"} and _evidence_docs(item)
    ]
    rng = np.random.default_rng(seed)
    rng.shuffle(examples)

    selected = _balanced_examples(examples, max_examples)
    pools = _distractor_pools(examples)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        written = 0
        for idx, item in enumerate(selected):
            records = _build_records(item, pools, idx)
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                written += 1


def _balanced_examples(examples: List[dict], max_examples: int) -> List[dict]:
    by_label = {"SUPPORTS": [], "REFUTES": []}
    for item in examples:
        by_label[item["label"]].append(item)
    per_label = max_examples // 2
    selected = by_label["SUPPORTS"][:per_label] + by_label["REFUTES"][:per_label]
    remainder = max_examples - len(selected)
    if remainder > 0:
        selected.extend(by_label["SUPPORTS"][per_label : per_label + remainder])
    return selected


def _distractor_pools(examples: List[dict]) -> dict:
    pools = {"SUPPORTS": [], "REFUTES": [], "all": []}
    for item in examples:
        docs = _evidence_docs(item)
        if not docs:
            continue
        pools[item["label"]].extend(docs)
        pools["all"].extend(docs)
    return pools


def _build_records(item: dict, pools: dict, local_idx: int) -> List[dict]:
    label = item["label"]
    opposite = "REFUTES" if label == "SUPPORTS" else "SUPPORTS"
    claim = item["claim"]
    answer = label
    # Keep the auditable support key within the fixed-size evidence set budget.
    # FEVER may list many gold sentences; this bridge treats the first few as
    # the required support subset and verifies that every listed id is present.
    gold_docs = _evidence_docs(item)[:3]
    if not gold_docs:
        return []

    distractors = _take_not_matching(pools["all"], gold_docs, 6)
    conflict_docs = _take_not_matching(pools[opposite], gold_docs, 6)
    if not distractors or not conflict_docs:
        return []

    all_candidates = _dedupe_docs([*gold_docs, *distractors, *conflict_docs])
    relevance_scores = _tfidf_scores(
        claim,
        [doc["title"] + " " + doc["text"] for doc in all_candidates],
    )
    for doc, score in zip(all_candidates, relevance_scores):
        doc["retrieval_score"] = score

    gold_docs = _refresh_scores(gold_docs, all_candidates)
    distractors = _refresh_scores(distractors, all_candidates)
    conflict_docs = _refresh_scores(conflict_docs, all_candidates)

    clean_docs = _dedupe_docs([*gold_docs, *sorted(distractors, key=lambda doc: doc["retrieval_score"], reverse=True)])[:6]
    stable_docs = [
        clean_docs,
        _dedupe_docs([*gold_docs[::-1], *distractors])[:6],
    ]
    # If a claim has only one gold evidence sentence, keeping gold_docs[0] would
    # make the "missing" perturbation fully answerable. Use distractors only in
    # that case so the structural label remains defensible.
    missing_docs = (
        _dedupe_docs([gold_docs[0], *distractors])[:6]
        if len(gold_docs) > 1
        else distractors[:6]
    )
    conflict_set = _dedupe_docs([*conflict_docs, *distractors])[:6]
    distractor_set = distractors[:6]
    near_miss_sets = [
        _dedupe_docs([*conflict_docs, *distractors])[:6],
        _dedupe_docs([*conflict_docs[::-1], *distractors])[:6],
        _dedupe_docs([*distractors[:2], *conflict_docs])[:6],
        _dedupe_docs([*conflict_docs, *distractors[::-1]])[:6],
    ]
    support_key = _support_key(gold_docs)
    gold_doc_ids = {doc["doc_id"] for doc in gold_docs}
    conflict_doc_ids = {doc["doc_id"] for doc in conflict_docs}
    base_id = f"fever:{item.get('id') or item.get('original_id') or local_idx}"

    return [
        {
            "orbit_id": f"{base_id}:stable",
            "source": "copenlu/fever_gold_evidence",
            "clean": _make_set(
                query=_claim_query(claim),
                answer=answer,
                docs=clean_docs,
                label=True,
                split="fever_stable_evidence",
                support_key=support_key,
                perturbation_type="clean",
                gold_doc_ids=gold_doc_ids,
                conflict_doc_ids=conflict_doc_ids,
            ),
            "perturbations": [
                _make_set(
                    query=_stable_query(claim, i),
                    answer=answer,
                    docs=docs,
                    label=True,
                    split="fever_stable_evidence",
                    support_key=support_key,
                    perturbation_type="answer_preserving",
                    gold_doc_ids=gold_doc_ids,
                    conflict_doc_ids=conflict_doc_ids,
                )
                for i, docs in enumerate(stable_docs)
            ],
        },
        {
            "orbit_id": f"{base_id}:missing",
            "source": "copenlu/fever_gold_evidence",
            "clean": _make_set(
                query=_claim_query(claim),
                answer=answer,
                docs=clean_docs,
                label=True,
                split="fever_missing_evidence",
                support_key=support_key,
                perturbation_type="clean",
                gold_doc_ids=gold_doc_ids,
                conflict_doc_ids=conflict_doc_ids,
            ),
            "perturbations": [
                _make_set(
                    query=_missing_query(claim),
                    answer=answer,
                    docs=missing_docs,
                    label=False,
                    split="fever_missing_evidence",
                    support_key=f"{support_key}:partial",
                    perturbation_type="missing_evidence",
                    gold_doc_ids=gold_doc_ids,
                    conflict_doc_ids=conflict_doc_ids,
                )
            ],
        },
        {
            "orbit_id": f"{base_id}:fragile_mixed",
            "source": "copenlu/fever_gold_evidence",
            "clean": _make_set(
                query=_claim_query(claim),
                answer=answer,
                docs=clean_docs,
                label=True,
                split="fever_fragile_mixed",
                support_key=support_key,
                perturbation_type="clean",
                gold_doc_ids=gold_doc_ids,
                conflict_doc_ids=conflict_doc_ids,
            ),
            "perturbations": [
                *[
                    _make_set(
                        query=_stable_query(claim, i),
                        answer=answer,
                        docs=docs,
                        label=True,
                        split="fever_fragile_mixed",
                        support_key=support_key,
                        perturbation_type="answer_preserving",
                        gold_doc_ids=gold_doc_ids,
                        conflict_doc_ids=conflict_doc_ids,
                    )
                    for i, docs in enumerate(stable_docs)
                ],
                _make_set(
                    query=_conflict_query(claim, opposite),
                    answer=answer,
                    docs=conflict_set,
                    label=False,
                    split="fever_fragile_mixed",
                    support_key=f"opposite:{opposite}",
                    perturbation_type="single_critical_conflict",
                    gold_doc_ids=gold_doc_ids,
                    conflict_doc_ids=conflict_doc_ids,
                ),
            ],
        },
        {
            "orbit_id": f"{base_id}:conflict",
            "source": "copenlu/fever_gold_evidence",
            "clean": _make_set(
                query=_claim_query(claim),
                answer=answer,
                docs=clean_docs,
                label=True,
                split="fever_conflicting_evidence",
                support_key=support_key,
                perturbation_type="clean",
                gold_doc_ids=gold_doc_ids,
                conflict_doc_ids=conflict_doc_ids,
            ),
            "perturbations": [
                _make_set(
                    query=_conflict_query(claim, opposite),
                    answer=answer,
                    docs=conflict_set,
                    label=False,
                    split="fever_conflicting_evidence",
                    support_key=f"opposite:{opposite}",
                    perturbation_type="opposite_label_evidence",
                    gold_doc_ids=gold_doc_ids,
                    conflict_doc_ids=conflict_doc_ids,
                )
            ],
        },
        {
            "orbit_id": f"{base_id}:near_miss_dilution",
            "source": "copenlu/fever_gold_evidence",
            "clean": _make_set(
                query=_claim_query(claim),
                answer=answer,
                docs=clean_docs,
                label=True,
                split="fever_near_miss_dilution",
                support_key=support_key,
                perturbation_type="clean",
                gold_doc_ids=gold_doc_ids,
                conflict_doc_ids=conflict_doc_ids,
            ),
            "perturbations": [
                _make_set(
                    query=_near_miss_query(claim, i),
                    answer=answer,
                    docs=docs,
                    label=False,
                    split="fever_near_miss_dilution",
                    support_key=f"near_miss:{opposite}:{i}",
                    perturbation_type="near_miss_high_sufficiency",
                    gold_doc_ids=gold_doc_ids,
                    conflict_doc_ids=conflict_doc_ids,
                    high_plausibility=True,
                )
                for i, docs in enumerate(near_miss_sets)
            ],
        },
        {
            "orbit_id": f"{base_id}:distractor",
            "source": "copenlu/fever_gold_evidence",
            "clean": _make_set(
                query=_claim_query(claim),
                answer=answer,
                docs=clean_docs,
                label=True,
                split="fever_distractor_only",
                support_key=support_key,
                perturbation_type="clean",
                gold_doc_ids=gold_doc_ids,
                conflict_doc_ids=conflict_doc_ids,
            ),
            "perturbations": [
                _make_set(
                    query=_distractor_query(claim),
                    answer=answer,
                    docs=distractor_set,
                    label=False,
                    split="fever_distractor_only",
                    support_key="distractor_only",
                    perturbation_type="distractor_only",
                    gold_doc_ids=gold_doc_ids,
                    conflict_doc_ids=conflict_doc_ids,
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
    gold_doc_ids: set[str],
    conflict_doc_ids: set[str],
    high_plausibility: bool = False,
) -> dict:
    return {
        "query": query,
        "answer": answer,
        "label_answerable": label,
        "split": split,
        "metadata": {
            "support_key": support_key,
            "perturbation_type": perturbation_type,
            "label_source": "fever_gold_evidence_heuristic",
        },
        "docs": [
            _make_doc(
                doc,
                rank,
                gold_doc_ids=gold_doc_ids,
                conflict_doc_ids=conflict_doc_ids,
                high_plausibility=high_plausibility,
            )
            for rank, doc in enumerate(docs)
        ],
    }


def _make_doc(
    doc: dict,
    rank: int,
    *,
    gold_doc_ids: set[str],
    conflict_doc_ids: set[str],
    high_plausibility: bool = False,
) -> dict:
    is_gold = doc["doc_id"] in gold_doc_ids
    is_conflict = doc["doc_id"] in conflict_doc_ids
    is_near_miss = high_plausibility and not is_gold
    return {
        "doc_id": doc["doc_id"],
        "title": doc["title"],
        "text": doc["text"],
        "rank": rank,
        "corm_score": doc["retrieval_score"],
        "support": 0.9 if is_gold else (0.95 if is_near_miss else (0.2 if is_conflict else 0.15)),
        "conflict": 0.8 if is_conflict else 0.0,
        "missing": 0.05 if is_gold or is_near_miss else (0.4 if is_conflict else 0.75),
    }


def _evidence_docs(item: dict) -> List[dict]:
    docs = []
    for idx, evidence in enumerate(item.get("evidence") or []):
        if len(evidence) < 3:
            continue
        title, sentence_id, text = evidence[0], evidence[1], evidence[2]
        if not text:
            continue
        docs.append(
            {
                "doc_id": f"{title}:{sentence_id}",
                "title": _clean_title(str(title)),
                "text": str(text),
                "label": item.get("label"),
                "retrieval_score": 0.0,
            }
        )
    return _dedupe_docs(docs)


def _take_not_matching(pool: List[dict], gold_docs: List[dict], count: int) -> List[dict]:
    blocked = {doc["doc_id"] for doc in gold_docs}
    output = []
    for doc in pool:
        if doc["doc_id"] in blocked:
            continue
        output.append(dict(doc))
        if len(output) >= count:
            break
    return output


def _refresh_scores(docs: List[dict], scored_docs: List[dict]) -> List[dict]:
    by_id = {doc["doc_id"]: doc for doc in scored_docs}
    return [dict(by_id[doc["doc_id"]]) for doc in docs if doc["doc_id"] in by_id]


def _tfidf_scores(query: str, docs: List[str]) -> List[float]:
    matrix = TfidfVectorizer(stop_words="english", max_features=5000).fit_transform([query, *docs])
    query_vec = matrix[0]
    doc_matrix = matrix[1:]
    raw = (doc_matrix @ query_vec.T).toarray().ravel()
    if raw.max() <= raw.min():
        return [0.5 for _ in raw]
    scaled = (raw - raw.min()) / (raw.max() - raw.min())
    return [float(score) for score in scaled]


def _support_key(docs: Iterable[dict]) -> str:
    return "|".join(sorted(doc["doc_id"] for doc in docs))


def _dedupe_docs(docs: Iterable[dict]) -> List[dict]:
    seen = set()
    output = []
    for doc in docs:
        if doc["doc_id"] in seen:
            continue
        seen.add(doc["doc_id"])
        output.append(dict(doc))
    return output


def _clean_title(title: str) -> str:
    title = title.replace("-LRB-", "(").replace("-RRB-", ")")
    title = title.replace("_", " ")
    return re.sub(r"\s+", " ", title).strip()


def _claim_query(claim: str) -> str:
    return f"Determine whether this claim is supported or refuted: {claim}"


def _stable_query(claim: str, index: int) -> str:
    if index == 0:
        return f"Using only the evidence, fact-check this claim: {claim}"
    return f"Verify the claim and preserve the factual label: {claim}"


def _missing_query(claim: str) -> str:
    return f"Fact-check the claim with incomplete evidence if possible: {claim}"


def _conflict_query(claim: str, opposite: str) -> str:
    return f"Assuming the evidence may indicate {opposite}, fact-check this claim: {claim}"


def _distractor_query(claim: str) -> str:
    return f"Fact-check the claim using only background evidence if direct evidence is absent: {claim}"


def _near_miss_query(claim: str, index: int) -> str:
    return f"Fact-check this claim with highly plausible but potentially mismatched evidence set {index}: {claim}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results/fever_orbits.jsonl"))
    parser.add_argument("--max-examples", type=int, default=200)
    parser.add_argument("--split", default="validation")
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()
    build_fever_orbits(args.output, args.max_examples, args.split, args.seed)


if __name__ == "__main__":
    main()
