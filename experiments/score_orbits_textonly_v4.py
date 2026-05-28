#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag.feature_firewall import assert_no_forbidden_features


def score_orbits_textonly_v4(
    raw_input: Path,
    private_input: Path,
    scored_output: Path,
    report_output: Path | None = None,
) -> dict:
    raw_rows = _read_jsonl(raw_input)
    private_rows = _read_jsonl(private_input)
    private_by_id = {row["orbit_id"]: row for row in private_rows}
    if len(private_by_id) != len(private_rows):
        raise ValueError("private eval file contains duplicate orbit_id values")

    scored_output.parent.mkdir(parents=True, exist_ok=True)
    method_meta = {
        "scorer": "textonly_lexical_v4",
        "uses_private_fields": False,
        "feature_sources": ["query", "candidate_answer", "visible_evidence_text", "retrieval_score"],
    }
    feature_summaries = []
    with scored_output.open("w", encoding="utf-8") as dst:
        for row in raw_rows:
            assert_no_forbidden_features(row)
            orbit_id = row["orbit_id"]
            if orbit_id not in private_by_id:
                raise ValueError(f"missing private eval row for orbit_id={orbit_id}")
            private = private_by_id[orbit_id]
            scored = _score_one(row, private, method_meta)
            feature_summaries.append(scored["metadata"]["textonly_v4"])
            dst.write(json.dumps(scored, ensure_ascii=False) + "\n")

    report = {
        "raw_input": str(raw_input),
        "private_input": str(private_input),
        "scored_output": str(scored_output),
        "orbits": len(raw_rows),
        "source_item_groups": len({row["source_item_group_id"] for row in raw_rows}),
        "scorer": method_meta,
        "feature_summary": _summarize_features(feature_summaries),
    }
    if report_output:
        report_output.parent.mkdir(parents=True, exist_ok=True)
        report_output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def _score_one(raw: dict, private: dict, method_meta: dict) -> dict:
    clean = _score_set(
        query=raw["query"],
        answer=raw["candidate_answer"],
        evidence=raw.get("clean_evidence") or [],
        label=bool(private["label_answerable"]),
        split=str(private.get("construction_type") or "unknown"),
    )
    perturbations = []
    set_scores = [clean["metadata"]["set_sufficiency"]]
    for item in raw.get("perturbations") or []:
        scored = _score_set(
            query=item.get("query") or raw["query"],
            answer=item.get("candidate_answer") or raw["candidate_answer"],
            evidence=item.get("evidence") or [],
            label=True,
            split=str(private.get("construction_type") or "unknown"),
        )
        perturbations.append(scored)
        set_scores.append(scored["metadata"]["set_sufficiency"])

    return {
        "orbit_id": raw["orbit_id"],
        "source_item_group_id": raw["source_item_group_id"],
        "dataset": raw["dataset"],
        "split": str(private.get("construction_type") or "unknown"),
        "clean": clean,
        "perturbations": perturbations,
        "metadata": {
            "textonly_v4": {
                "clean_sufficiency": clean["metadata"]["set_sufficiency"],
                "mean_sufficiency": sum(set_scores) / len(set_scores),
                "worst_sufficiency": min(set_scores),
                "sufficiency_variance": _variance(set_scores),
                "verifier_entropy": _entropy(set_scores),
                "method": method_meta,
            }
        },
    }


def _score_set(
    query: str,
    answer: str,
    evidence: list[dict[str, Any]],
    label: bool,
    split: str,
) -> dict:
    docs = []
    supports = []
    conflicts = []
    missing_values = []
    for doc in evidence:
        retrieval_score = _clip01(float(doc.get("retrieval_score") or 0.0))
        support, conflict, missing = _doc_scores(
            query,
            answer,
            doc.get("text") or "",
            retrieval_score,
        )
        supports.append(support)
        conflicts.append(conflict)
        missing_values.append(missing)
        docs.append(
            {
                "doc_id": str(doc.get("doc_id") or ""),
                "title": str(doc.get("title") or ""),
                "text": str(doc.get("text") or ""),
                "rank": int(doc.get("rank") or 0),
                "corm_score": float(doc.get("retrieval_score") or 0.0),
                "support": support,
                "conflict": conflict,
                "missing": missing,
                "textonly_model": "lexical_v4",
                "textonly_unit": "doc",
            }
        )

    max_support = max(supports) if supports else 0.0
    mean_support = sum(supports) / len(supports) if supports else 0.0
    max_conflict = max(conflicts) if conflicts else 0.0
    mean_missing = sum(missing_values) / len(missing_values) if missing_values else 1.0
    set_sufficiency = _clip01(0.60 * max_support + 0.20 * mean_support - 0.10 * max_conflict - 0.10 * mean_missing)
    return {
        "query": query,
        "answer": answer,
        "label_answerable": label,
        "split": split,
        "metadata": {
            "set_sufficiency": set_sufficiency,
            "set_textonly_support": max_support,
            "set_textonly_conflict": max_conflict,
            "set_textonly_missing": mean_missing,
            "nli_unit": "lexical_doc",
        },
        "docs": docs,
    }


def _doc_scores(query: str, answer: str, text: str, retrieval_score: float) -> tuple[float, float, float]:
    query_terms = _content_terms(query)
    answer_terms = _content_terms(answer)
    text_terms = _content_terms(text)
    if not text_terms:
        return 0.0, 0.0, 1.0

    query_overlap = _jaccard(query_terms, text_terms)
    answer_overlap = _jaccard(answer_terms, text_terms)
    answer_coverage = _coverage(answer_terms, text_terms)
    negation = _negation_pressure(text)
    support = _clip01(
        0.40 * query_overlap
        + 0.25 * answer_coverage
        + 0.10 * answer_overlap
        + 0.25 * retrieval_score
    )
    conflict = _clip01(negation * (0.5 + 0.5 * max(query_overlap, answer_overlap)))
    missing = _clip01(1.0 - max(support, 0.35 * query_overlap))
    return support, conflict, missing


def _content_terms(text: str) -> set[str]:
    tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
    return {tok for tok in tokens if tok not in _STOPWORDS and len(tok) > 1}


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _coverage(needles: set[str], haystack: set[str]) -> float:
    if not needles:
        return 0.0
    return len(needles & haystack) / len(needles)


def _negation_pressure(text: str) -> float:
    terms = _content_terms(text)
    if not terms:
        return 0.0
    hits = len(terms & {"not", "never", "false", "refute", "refutes", "refuted", "deny", "denies"})
    return _clip01(hits / 3.0)


def _entropy(values: list[float]) -> float:
    if not values:
        return 0.0
    buckets = Counter(round(_clip01(value), 1) for value in values)
    total = sum(buckets.values())
    entropy = 0.0
    for count in buckets.values():
        prob = count / total
        entropy -= prob * math.log(prob + 1e-12)
    return float(entropy)


def _variance(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values) / len(values)


def _summarize_features(rows: list[dict]) -> dict:
    if not rows:
        return {}
    fields = ["clean_sufficiency", "mean_sufficiency", "worst_sufficiency", "sufficiency_variance", "verifier_entropy"]
    summary = {}
    for field in fields:
        values = [float(row[field]) for row in rows]
        summary[field] = {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }
    return summary


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no} is not valid JSON") from exc
    return rows


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
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()
    report = score_orbits_textonly_v4(
        raw_input=args.raw,
        private_input=args.private,
        scored_output=args.output,
        report_output=args.report_output,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
