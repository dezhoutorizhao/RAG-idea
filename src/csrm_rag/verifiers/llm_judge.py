from __future__ import annotations

import json
from typing import Any

from csrm_rag.feature_firewall import assert_no_forbidden_features


SYSTEM_PROMPT = (
    "You are an independent RAG evidence judge. Use only the visible query, candidate answer, "
    "and retrieved evidence text. Do not assume hidden labels or dataset construction metadata."
)


def build_llm_judge_request(
    raw_row: dict[str, Any],
    *,
    model: str,
    max_docs_per_set: int = 6,
    temperature: float = 0.0,
) -> dict[str, Any]:
    assert_no_forbidden_features(raw_row)
    orbit_id = str(raw_row["orbit_id"])
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _user_prompt(raw_row, max_docs_per_set=max_docs_per_set)},
    ]
    return {
        "custom_id": orbit_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": model,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
            "messages": messages,
        },
    }


def parse_llm_judge_response(content: str) -> dict[str, Any]:
    payload = json.loads(content)
    score = float(payload["answerable_score"])
    if not 0.0 <= score <= 1.0:
        raise ValueError("answerable_score must be in [0, 1]")
    label = str(payload.get("label") or "").strip().lower()
    if label not in {"answerable", "fragile", "unanswerable", "ambiguous"}:
        raise ValueError("label must be one of answerable, fragile, unanswerable, ambiguous")
    return {
        "answerable_score": score,
        "label": label,
        "rationale": str(payload.get("rationale") or ""),
    }


def _user_prompt(raw_row: dict[str, Any], *, max_docs_per_set: int) -> str:
    payload = {
        "task": (
            "Judge whether the candidate answer is supported robustly by the visible evidence. "
            "Return JSON with keys answerable_score, label, and rationale. answerable_score is the "
            "probability that the answer should be accepted in selective RAG."
        ),
        "label_options": ["answerable", "fragile", "unanswerable", "ambiguous"],
        "query": raw_row.get("query"),
        "candidate_answer": raw_row.get("candidate_answer"),
        "clean_evidence": _docs(raw_row.get("clean_evidence") or [], max_docs_per_set=max_docs_per_set),
        "counterfactual_sets": [
            {
                "query": item.get("query"),
                "candidate_answer": item.get("candidate_answer"),
                "evidence": _docs(item.get("evidence") or [], max_docs_per_set=max_docs_per_set),
            }
            for item in raw_row.get("perturbations") or []
        ],
        "output_schema": {
            "answerable_score": "float in [0, 1]",
            "label": "answerable | fragile | unanswerable | ambiguous",
            "rationale": "short explanation grounded in visible evidence",
        },
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _docs(docs: list[dict[str, Any]], *, max_docs_per_set: int) -> list[dict[str, Any]]:
    output = []
    for doc in docs[:max_docs_per_set]:
        output.append(
            {
                "doc_id": doc.get("doc_id"),
                "title": doc.get("title"),
                "text": doc.get("text"),
                "rank": doc.get("rank"),
            }
        )
    return output
