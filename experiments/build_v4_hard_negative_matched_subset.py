#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag.feature_firewall import assert_no_forbidden_features


def build_v4_hard_negative_matched_subset(
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_prefix: Path,
    *,
    prefer_same_group: bool = True,
) -> dict[str, Any]:
    raw_rows = _read_jsonl(raw_path)
    private_rows = _read_jsonl(private_path)
    scored_rows = _read_jsonl(scored_path)
    if not (len(raw_rows) == len(private_rows) == len(scored_rows)):
        raise ValueError("raw, private, and scored files must contain the same number of rows")
    for index, (raw, private, scored) in enumerate(zip(raw_rows, private_rows, scored_rows)):
        assert_no_forbidden_features(raw)
        if raw["orbit_id"] != private["orbit_id"] or raw["orbit_id"] != scored["orbit_id"]:
            raise ValueError(f"row {index} has misaligned orbit_id values")

    labels = [bool(row["label_answerable"]) for row in private_rows]
    positives = [index for index, label in enumerate(labels) if label]
    negatives = [index for index, label in enumerate(labels) if not label]
    if not positives or not negatives:
        raise ValueError("hard-negative matching requires both positive and negative rows")

    feature_rows = [_hard_features(row) for row in raw_rows]
    vectors = _normalized_vectors(feature_rows)
    pairs = _greedy_pairs(raw_rows, positives, negatives, vectors, prefer_same_group=prefer_same_group)
    selected = sorted({index for pair in pairs for index in pair})

    raw_output = _append_suffix(output_prefix, ".raw.jsonl")
    private_output = _append_suffix(output_prefix, ".private_eval.jsonl")
    scored_output = _append_suffix(output_prefix, ".textonly_scored.jsonl")
    report_output = _append_suffix(output_prefix, ".hard_match_report.json")
    _write_jsonl(raw_output, [raw_rows[index] for index in selected])
    _write_jsonl(private_output, [private_rows[index] for index in selected])
    _write_jsonl(scored_output, [scored_rows[index] for index in selected])

    report = {
        "inputs": {
            "raw": str(raw_path),
            "private": str(private_path),
            "scored": str(scored_path),
        },
        "outputs": {
            "raw": str(raw_output),
            "private": str(private_output),
            "scored": str(scored_output),
            "report": str(report_output),
        },
        "prefer_same_group": prefer_same_group,
        "input_n": len(raw_rows),
        "input_positive": len(positives),
        "input_negative": len(negatives),
        "matched_n": len(selected),
        "matched_positive": len(pairs),
        "matched_negative": len(pairs),
        "negative_construction_counts": _construction_counts(private_rows, [neg for _, neg in pairs]),
        "feature_names": sorted(feature_rows[0]),
        "pairs": [
            {
                "positive_orbit_id": raw_rows[pos]["orbit_id"],
                "negative_orbit_id": raw_rows[neg]["orbit_id"],
                "negative_construction_type": private_rows[neg].get("construction_type"),
                "same_group": raw_rows[pos]["source_item_group_id"] == raw_rows[neg]["source_item_group_id"],
                "distance": _distance(vectors[pos], vectors[neg]),
            }
            for pos, neg in pairs
        ],
        "feature_balance": _feature_balance(feature_rows, labels, selected),
    }
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def _greedy_pairs(
    raw_rows: list[dict[str, Any]],
    positives: Sequence[int],
    negatives: Sequence[int],
    vectors: Sequence[Sequence[float]],
    *,
    prefer_same_group: bool,
) -> list[tuple[int, int]]:
    available = set(negatives)
    pairs = []
    for pos in positives:
        candidates = list(available)
        if prefer_same_group:
            same_group = [
                neg
                for neg in candidates
                if raw_rows[neg]["source_item_group_id"] == raw_rows[pos]["source_item_group_id"]
            ]
            if same_group:
                candidates = same_group
        if not candidates:
            break
        neg = min(candidates, key=lambda item: (_distance(vectors[pos], vectors[item]), raw_rows[item]["orbit_id"]))
        available.remove(neg)
        pairs.append((pos, neg))
    return pairs


def _hard_features(row: dict[str, Any]) -> dict[str, float]:
    evidence_texts = _all_texts(row)
    clean_texts = [str(doc.get("text") or "") for doc in row.get("clean_evidence") or []]
    perturbation_texts = [
        str(doc.get("text") or "")
        for item in row.get("perturbations") or []
        for doc in item.get("evidence") or []
    ]
    answer_terms = _terms(str(row.get("candidate_answer") or ""))
    query_terms = _terms(str(row.get("query") or ""))
    all_terms = _terms(" ".join(evidence_texts))
    clean_terms = _terms(" ".join(clean_texts))
    perturbation_terms = _terms(" ".join(perturbation_texts))
    retrieval_scores = [float(value) for value in row.get("retrieval_scores") or [0.0]]
    return {
        "answer_all_coverage": _coverage(answer_terms, all_terms),
        "answer_clean_coverage": _coverage(answer_terms, clean_terms),
        "answer_perturbation_coverage": _coverage(answer_terms, perturbation_terms),
        "answer_all_count": float(_term_count(answer_terms, evidence_texts)),
        "query_all_jaccard": _jaccard(query_terms, all_terms),
        "query_clean_jaccard": _jaccard(query_terms, clean_terms),
        "query_perturbation_jaccard": _jaccard(query_terms, perturbation_terms),
        "clean_perturbation_jaccard": _jaccard(clean_terms, perturbation_terms),
        "perturbation_count": float(len(row.get("perturbations") or [])),
        "clean_doc_count": float(len(row.get("clean_evidence") or [])),
        "total_doc_count": float(len(clean_texts) + len(perturbation_texts)),
        "mean_doc_chars": _mean([len(text) for text in evidence_texts]),
        "total_doc_chars": float(sum(len(text) for text in evidence_texts)),
        "mean_retrieval_score": _mean(retrieval_scores),
        "max_retrieval_score": max(retrieval_scores),
    }


def _feature_balance(
    feature_rows: Sequence[dict[str, float]],
    labels: Sequence[bool],
    selected: Sequence[int],
) -> dict[str, Any]:
    selected_labels = [labels[index] for index in selected]
    selected_features = [feature_rows[index] for index in selected]
    output = {}
    for name in sorted(selected_features[0]):
        pos_values = [row[name] for row, label in zip(selected_features, selected_labels) if label]
        neg_values = [row[name] for row, label in zip(selected_features, selected_labels) if not label]
        output[name] = {
            "positive_mean": _mean(pos_values),
            "negative_mean": _mean(neg_values),
            "absolute_mean_gap": abs(_mean(pos_values) - _mean(neg_values)),
        }
    return output


def _construction_counts(private_rows: Sequence[dict[str, Any]], indices: Sequence[int]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for index in indices:
        key = str(private_rows[index].get("construction_type") or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def _normalized_vectors(features: Sequence[dict[str, float]]) -> list[list[float]]:
    names = sorted(features[0])
    columns = {name: [row[name] for row in features] for name in names}
    means = {name: _mean(values) for name, values in columns.items()}
    scales = {}
    for name, values in columns.items():
        mean = means[name]
        variance = _mean([(value - mean) ** 2 for value in values])
        scales[name] = math.sqrt(variance) or 1.0
    return [[(row[name] - means[name]) / scales[name] for name in names] for row in features]


def _distance(left: Sequence[float], right: Sequence[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def _all_texts(row: dict[str, Any]) -> list[str]:
    texts = [str(doc.get("text") or "") for doc in row.get("clean_evidence") or []]
    for item in row.get("perturbations") or []:
        texts.extend(str(doc.get("text") or "") for doc in item.get("evidence") or [])
    return texts


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


def _term_count(terms: set[str], texts: Sequence[str]) -> int:
    if not terms:
        return 0
    count = 0
    for text in texts:
        tokens = re.findall(r"[A-Za-z0-9]+", str(text).lower())
        count += sum(1 for token in tokens if token in terms)
    return count


def _mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return float(sum(values) / len(values))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
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


def _write_jsonl(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _append_suffix(path: Path, suffix: str) -> Path:
    return path.with_name(path.name + suffix)


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
    parser.add_argument("--scored", type=Path, required=True)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--no-prefer-same-group", action="store_true")
    args = parser.parse_args()
    report = build_v4_hard_negative_matched_subset(
        args.raw,
        args.private,
        args.scored,
        args.output_prefix,
        prefer_same_group=not args.no_prefer_same_group,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
