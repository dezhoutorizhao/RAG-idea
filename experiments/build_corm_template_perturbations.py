#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Iterable


SLOT_PATTERNS = (
    (1, 2, 3, 1, 2),
    (2, 3, 1, 2, 3),
    (3, 1, 2, 3, 1),
)

DISTRACTOR_SENTENCES = (
    "The history of ceramic glazing includes several mineral-based firing techniques.",
    "Early postal routes often followed river valleys and established market roads.",
    "Several jazz arrangements use syncopation to shift emphasis away from the downbeat.",
    "Botanical classification changed substantially after molecular phylogenetics became common.",
    "Astronomers often calibrate instruments using standard candles and reference spectra.",
)


def build_template_perturbations(
    rows: Iterable[dict[str, Any]],
    *,
    output: Path,
    max_queries: int | None = None,
    seed: int = 42,
    manifest: Path | None = None,
) -> dict[str, Any]:
    normalized = []
    skipped = 0
    for idx, row in enumerate(rows):
        try:
            normalized.append(_normalize_query(row, idx))
        except ValueError:
            skipped += 1
    if max_queries is not None:
        normalized = normalized[:max_queries]
    if not normalized:
        raise ValueError("no NQ rows with answers were available")

    rng = random.Random(seed)
    wrong_pool = [row["correct_answer"] for row in normalized if _is_entity_like(row["correct_answer"])]
    output.parent.mkdir(parents=True, exist_ok=True)
    type_counts = {1: 0, 2: 0, 3: 0}
    with output.open("w", encoding="utf-8") as handle:
        for local_idx, row in enumerate(normalized):
            qid = int(row["query_idx"])
            pattern = SLOT_PATTERNS[qid % len(SLOT_PATTERNS)]
            wrongs = _sample_wrong_answers(wrong_pool, row["correct_answer"], rng)
            perturbations = []
            t1_seen = 0
            t2_seen = 0
            t3_seen = 0
            for slot_idx, ptype in enumerate(pattern):
                type_counts[ptype] += 1
                if ptype == 1:
                    wrong = wrongs[t1_seen % len(wrongs)]
                    t1_seen += 1
                    perturbed = _false_belief_question(row["question"], wrong)
                    perturbations.append(
                        {
                            "perturbation_type": 1,
                            "perturbation_text": perturbed,
                            "perturbed_query": perturbed,
                            "wrong_belief": wrong,
                            "generator": "template_fallback",
                        }
                    )
                elif ptype == 2:
                    variant = "A" if t2_seen % 2 == 0 else "B"
                    t2_seen += 1
                    perturbed = _confirmation_bias_question(row["question"], variant)
                    perturbations.append(
                        {
                            "perturbation_type": 2,
                            "perturbation_text": perturbed,
                            "perturbed_query": perturbed,
                            "t2_variant": variant,
                            "generator": "template_fallback",
                        }
                    )
                else:
                    sentence = DISTRACTOR_SENTENCES[(local_idx + t3_seen) % len(DISTRACTOR_SENTENCES)]
                    t3_seen += 1
                    perturbations.append(
                        {
                            "perturbation_type": 3,
                            "perturbation_text": sentence,
                            "perturbed_query": f"{row['question']} {sentence}",
                            "topic": "deterministic_unrelated_sentence",
                            "generator": "template_fallback",
                        }
                    )

            handle.write(
                json.dumps(
                    {
                        "query_idx": qid,
                        "question": row["question"],
                        "correct_answer": row["correct_answer"],
                        "all_answers": row["all_answers"],
                        "perturbations": perturbations,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )

    report = {
        "status": "built",
        "output": str(output),
        "rows": len(normalized),
        "skipped_rows": skipped,
        "perturbations": sum(type_counts.values()),
        "type_counts": {str(k): v for k, v in sorted(type_counts.items())},
        "max_queries": max_queries,
        "seed": seed,
        "claim_policy": (
            "Template fallback for reconstructed-pipeline smoke tests only. It is not "
            "the authors' OpenAI-generated perturbation set and must not be reported "
            "as original Biased-NQ evidence."
        ),
    }
    if manifest:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def load_nq_rows(split: str) -> list[dict[str, Any]]:
    from datasets import load_dataset

    nq = load_dataset("google-research-datasets/nq_open")
    return list(nq[split])


def _normalize_query(row: dict[str, Any], fallback_idx: int) -> dict[str, Any]:
    answers = row.get("answer") or row.get("all_answers") or []
    if not answers:
        raise ValueError(f"row {fallback_idx} has no answers")
    question = str(row.get("question", "")).strip()
    if not question:
        raise ValueError(f"row {fallback_idx} has no question")
    return {
        "query_idx": int(row.get("query_idx", fallback_idx)),
        "question": question,
        "correct_answer": str(row.get("correct_answer", answers[0])),
        "all_answers": [str(answer) for answer in answers],
    }


def _sample_wrong_answers(pool: list[str], correct: str, rng: random.Random) -> list[str]:
    candidates = [item for item in pool if item.lower() != correct.lower()]
    if len(candidates) >= 2:
        return rng.sample(candidates, 2)
    if len(candidates) == 1:
        return [candidates[0], "a different entity"]
    return ["a different entity", "another historical figure"]


def _false_belief_question(question: str, wrong: str) -> str:
    return f"Under the assumption that {wrong} is the relevant answer, {question.rstrip('?')}?"


def _confirmation_bias_question(question: str, variant: str) -> str:
    if variant == "A":
        return f"From a source that frames the topic with an outdated premise, {question.rstrip('?')}?"
    return f"When the background context gives a misleading cue, {question.rstrip('?')}?"


def _is_entity_like(text: str) -> bool:
    text = text.strip()
    if not (3 <= len(text) <= 60):
        return False
    if any(ch.isdigit() for ch in text):
        return False
    return len(text.split()) <= 6


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--split", choices=["validation", "train"], default="validation")
    parser.add_argument("--max-queries", type=int)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    result = build_template_perturbations(
        load_nq_rows(args.split),
        output=args.output,
        max_queries=args.max_queries,
        seed=args.seed,
        manifest=args.manifest,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
