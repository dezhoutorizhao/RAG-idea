from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GeneratedAnswer:
    answer: str
    confidence: float
    correct: bool
    generator: str


def generate_answer(raw: dict[str, Any], private: dict[str, Any], generator: str) -> GeneratedAnswer:
    if generator == "copy_candidate":
        answer = str(raw.get("candidate_answer") or "")
        confidence = 1.0
    elif generator == "lexical_guarded":
        answer, confidence = _lexical_guarded_answer(raw, private)
    else:
        raise ValueError(f"unknown generator {generator!r}")

    gold = str(private.get("gold_answer") or raw.get("candidate_answer") or "")
    label_answerable = private.get("adjudicated_label")
    if label_answerable is None:
        label_answerable = private.get("human_label")
    if label_answerable is None:
        label_answerable = private.get("label_answerable")
    correct = bool(_parse_bool(label_answerable)) and _normalize_answer(answer) == _normalize_answer(gold)
    return GeneratedAnswer(answer=answer, confidence=confidence, correct=correct, generator=generator)


def _lexical_guarded_answer(raw: dict[str, Any], private: dict[str, Any]) -> tuple[str, float]:
    candidate = str(raw.get("candidate_answer") or private.get("gold_answer") or "")
    docs = list(raw.get("clean_evidence") or [])
    for perturbation in raw.get("perturbations") or []:
        docs.extend(perturbation.get("evidence") or [])
    evidence_text = " ".join(str(doc.get("title") or "") + " " + str(doc.get("text") or "") for doc in docs)
    query_terms = _content_terms(str(raw.get("query") or ""))
    answer_terms = _content_terms(candidate)
    evidence_terms = _content_terms(evidence_text)
    query_coverage = _coverage(query_terms, evidence_terms)
    answer_coverage = _coverage(answer_terms, evidence_terms)
    confidence = _clip01(0.75 * query_coverage + 0.25 * answer_coverage)
    if _is_fever(private):
        return (candidate if confidence >= 0.18 else "NOT ENOUGH INFO", confidence)
    return (candidate if confidence >= 0.10 else "", confidence)


def _is_fever(private: dict[str, Any]) -> bool:
    dataset = str(private.get("dataset") or "").lower()
    return "fever" in dataset or str(private.get("gold_answer") or "") in {"SUPPORTS", "REFUTES"}


def _content_terms(text: str) -> set[str]:
    tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
    return {token for token in tokens if len(token) > 1 and token not in _STOPWORDS}


def _coverage(needles: set[str], haystack: set[str]) -> float:
    if not needles:
        return 0.0
    return len(needles & haystack) / len(needles)


def _normalize_answer(text: str) -> str:
    terms = re.findall(r"[A-Za-z0-9]+", text.lower())
    return " ".join(term for term in terms if term not in {"a", "an", "the"})


def _parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "answerable", "supported"}:
        return True
    if normalized in {"false", "0", "no", "fragile", "unanswerable", "unsupported"}:
        return False
    return None


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "claim",
    "determine",
    "evidence",
    "fact",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "refuted",
    "supported",
    "the",
    "this",
    "using",
    "whether",
}
