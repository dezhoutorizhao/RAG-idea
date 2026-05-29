#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import corm_max_score, csrm_score, naive_orbit_sufficiency, single_set_sufficiency
from csrm_rag.end2end import evaluate_selective_policy, generate_answer
from experiments.evaluate_orbits import load_orbits


GENERATORS = ["copy_candidate", "lexical_guarded"]
RETRIEVERS = ["bm25_orbit_pool", "dense_hash_orbit_pool"]
NON_CSRM_METHODS = [
    "retriever_confidence",
    "corm_max_clean",
    "single_set_sure_style",
    "naive_orbit_average",
    "generator_confidence",
]


@dataclass(frozen=True)
class DatasetConfig:
    name: str
    raw: Path
    private: Path
    scored: Path


DEFAULT_DATASETS = [
    DatasetConfig(
        "fever_v4_n100_structbalanced",
        Path("results/fever_orbits_v4_n100.constant.structbalanced.raw.jsonl"),
        Path("results/fever_orbits_v4_n100.constant.structbalanced.private_eval.jsonl"),
        Path("results/fever_orbits_v4_n100.constant.structbalanced.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        "hotpot_v4_hardneg_n100",
        Path("results/hotpot_orbits_v4_hardneg_n100.constant.raw.jsonl"),
        Path("results/hotpot_orbits_v4_hardneg_n100.private_eval.jsonl"),
        Path("results/hotpot_orbits_v4_hardneg_n100.constant.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        "hotpot_v4_n100_hardmatched",
        Path("results/hotpot_orbits_v4_n100.constant.hardmatched.raw.jsonl"),
        Path("results/hotpot_orbits_v4_n100.constant.hardmatched.private_eval.jsonl"),
        Path("results/hotpot_orbits_v4_n100.constant.hardmatched.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        "hotpot_v4_n100_structbalanced",
        Path("results/hotpot_orbits_v4_n100.constant.structbalanced.raw.jsonl"),
        Path("results/hotpot_orbits_v4_n100.constant.structbalanced.private_eval.jsonl"),
        Path("results/hotpot_orbits_v4_n100.constant.structbalanced.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        "hotpot_v4_semanticswap_n100",
        Path("results/hotpot_orbits_v4_semanticswap_n100.constant.raw.jsonl"),
        Path("results/hotpot_orbits_v4_semanticswap_n100.private_eval.jsonl"),
        Path("results/hotpot_orbits_v4_semanticswap_n100.constant.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        "hotpot_v4_supportpreserve_n100",
        Path("results/hotpot_orbits_v4_supportpreserve_n100.constant.raw.jsonl"),
        Path("results/hotpot_orbits_v4_supportpreserve_n100.private_eval.jsonl"),
        Path("results/hotpot_orbits_v4_supportpreserve_n100.constant.textonly_scored.jsonl"),
    ),
]


def run_end2end_retriever_generator_matrix_v4(
    datasets: Sequence[DatasetConfig],
    *,
    retrievers: Sequence[str] = RETRIEVERS,
    generators: Sequence[str] = GENERATORS,
    top_k: int = 6,
) -> dict[str, Any]:
    rows = [
        _dataset_row(dataset, retriever, generator, top_k=top_k)
        for dataset in datasets
        for retriever in retrievers
        for generator in generators
    ]
    aggregate = _aggregate(rows)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "datasets": [dataset.name for dataset in datasets],
        "dataset_count": len(datasets),
        "retrievers": list(retrievers),
        "generators": list(generators),
        "top_k": top_k,
        "row_count": len(rows),
        "rows": rows,
        "aggregate": aggregate,
        "protocol_complete": bool(datasets)
        and len(set(retrievers)) >= 2
        and len(set(generators)) >= 2
        and all(row["n"] > 0 for row in rows),
        "claim_policy": (
            "This matrix expands the end-to-end proxy to two retrieval policies and two generators "
            "over the materialized v4 orbit corpus. It is still a local-corpus proxy, not a full "
            "Wikipedia retrieval-generation reproduction."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    lines = [
        "# V4 End-to-End Retriever-Generator Matrix",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Datasets: `{summary['dataset_count']}`",
        f"Retrievers: `{summary['retrievers']}`",
        f"Generators: `{summary['generators']}`",
        f"Rows: `{summary['row_count']}`",
        f"Protocol complete: `{summary['protocol_complete']}`",
        "",
        "## Aggregate",
        "",
        f"- CSRM Risk@30 wins/ties/losses: `{aggregate['risk30_wins']}` / `{aggregate['risk30_ties']}` / `{aggregate['risk30_losses']}`.",
        f"- CSRM Risk@50 wins/ties/losses: `{aggregate['risk50_wins']}` / `{aggregate['risk50_ties']}` / `{aggregate['risk50_losses']}`.",
        f"- CSRM AURC wins/ties/losses: `{aggregate['aurc_wins']}` / `{aggregate['aurc_ties']}` / `{aggregate['aurc_losses']}`.",
        f"- Mean Risk@30 reduction: `{_fmt(aggregate['mean_risk30_reduction'])}`.",
        f"- Mean Risk@50 reduction: `{_fmt(aggregate['mean_risk50_reduction'])}`.",
        f"- Mean AURC reduction: `{_fmt(aggregate['mean_aurc_reduction'])}`.",
        "",
        "## Rows",
        "",
        "| Dataset | Retriever | Generator | Accuracy | CSRM Risk@30 | Best Risk@30 | Delta | CSRM Risk@50 | Best Risk@50 | Delta | CSRM AURC | Best AURC | Delta | Verdict |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary["rows"]:
        lines.append(
            f"| {row['dataset']} | {row['retriever']} | {row['generator']} | {_fmt(row['answer_accuracy'])} | "
            f"{_fmt(row['csrm']['risk30'])} | {_fmt(row['best_non_csrm']['risk30'])} | {_fmt(row['deltas']['risk30_reduction'])} | "
            f"{_fmt(row['csrm']['risk50'])} | {_fmt(row['best_non_csrm']['risk50'])} | {_fmt(row['deltas']['risk50_reduction'])} | "
            f"{_fmt(row['csrm']['aurc'])} | {_fmt(row['best_non_csrm']['aurc'])} | {_fmt(row['deltas']['aurc_reduction'])} | {row['verdict']} |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _dataset_row(dataset: DatasetConfig, retriever: str, generator: str, *, top_k: int) -> dict[str, Any]:
    scored = score_end2end_selector_methods(dataset, retriever, generator, top_k=top_k)
    method_metrics = {
        name: evaluate_selective_policy(scores, scored["correct"])
        for name, scores in sorted(scored["methods"].items())
    }
    csrm = _method_metrics(method_metrics["csrm"])
    best = _best_non_csrm(method_metrics)
    deltas = {
        "risk30_reduction": best["risk30"] - csrm["risk30"],
        "risk50_reduction": best["risk50"] - csrm["risk50"],
        "aurc_reduction": best["aurc"] - csrm["aurc"],
        "coverage_at_risk20_gain": csrm["coverage_at_risk20"] - best["coverage_at_risk20"],
    }
    return {
        "dataset": dataset.name,
        "retriever": retriever,
        "generator": generator,
        "n": scored["n"],
        "answer_accuracy": scored["answer_accuracy"],
        "selector_methods": sorted(scored["methods"]),
        "csrm": csrm,
        "best_non_csrm": best,
        "deltas": deltas,
        "verdict": _row_verdict(deltas),
        "outputs_sample": scored["outputs_sample"],
    }


def score_end2end_selector_methods(
    dataset: DatasetConfig,
    retriever: str,
    generator: str,
    *,
    top_k: int,
) -> dict[str, Any]:
    raw_rows = _read_jsonl(dataset.raw)
    private_by_id = {row["orbit_id"]: row for row in _read_jsonl(dataset.private)}
    scored_orbits = {orbit.orbit_id: orbit for orbit in load_orbits(dataset.scored)}
    if not raw_rows:
        raise ValueError(f"{dataset.raw} contains no rows")

    transformed_rows = [_with_retrieved_docs(row, retriever, top_k=top_k) for row in raw_rows]
    correct = []
    gen_conf = []
    retriever_conf = []
    outputs = []
    for row in transformed_rows:
        private = private_by_id.get(row["orbit_id"])
        if private is None:
            raise ValueError(f"missing private row for orbit_id={row['orbit_id']}")
        generated = generate_answer(row, private, generator)
        correct.append(generated.correct)
        gen_conf.append(generated.confidence)
        retriever_conf.append(_clean_retrieval_max(row))
        outputs.append(
            {
                "orbit_id": row["orbit_id"],
                "answer": generated.answer,
                "confidence": generated.confidence,
                "correct": generated.correct,
            }
        )

    methods = _selector_scores(transformed_rows, scored_orbits)
    methods["generator_confidence"] = gen_conf
    methods["retriever_confidence"] = retriever_conf
    return {
        "dataset": dataset.name,
        "retriever": retriever,
        "generator": generator,
        "n": len(raw_rows),
        "correct": correct,
        "answer_accuracy": sum(correct) / len(correct),
        "methods": methods,
        "outputs_sample": outputs[:5],
    }


def _selector_scores(raw_rows: list[dict[str, Any]], scored_orbits: dict[str, Any]) -> dict[str, list[float]]:
    methods = {
        "corm_max_clean": [],
        "single_set_sure_style": [],
        "naive_orbit_average": [],
        "csrm": [],
    }
    for row in raw_rows:
        orbit = scored_orbits.get(row["orbit_id"])
        if orbit is None:
            raise ValueError(f"missing scored row for orbit_id={row['orbit_id']}")
        methods["corm_max_clean"].append(corm_max_score(orbit.clean))
        methods["single_set_sure_style"].append(single_set_sufficiency(orbit.clean))
        methods["naive_orbit_average"].append(naive_orbit_sufficiency(orbit))
        methods["csrm"].append(csrm_score(orbit))
    return methods


def _with_retrieved_docs(row: dict[str, Any], retriever: str, *, top_k: int) -> dict[str, Any]:
    pool = _document_pool(row)
    if retriever == "bm25_orbit_pool":
        ranked = _rank_bm25_like(str(row.get("query") or ""), pool)
    elif retriever == "dense_hash_orbit_pool":
        ranked = _rank_dense_hash_like(str(row.get("query") or ""), pool)
    else:
        raise ValueError(f"unknown retriever {retriever!r}")
    clone = dict(row)
    clone["clean_evidence"] = ranked[:top_k]
    clone["perturbations"] = []
    return clone


def _document_pool(row: dict[str, Any]) -> list[dict[str, Any]]:
    seen = set()
    docs = []
    for doc in row.get("clean_evidence") or []:
        _append_doc(docs, seen, doc)
    for perturbation in row.get("perturbations") or []:
        for doc in perturbation.get("evidence") or []:
            _append_doc(docs, seen, doc)
    return docs


def _append_doc(docs: list[dict[str, Any]], seen: set[str], doc: dict[str, Any]) -> None:
    key = str(doc.get("doc_id") or doc.get("title") or doc.get("text") or len(docs))
    if key in seen:
        return
    clone = dict(doc)
    clone["doc_id"] = key
    seen.add(key)
    docs.append(clone)


def _rank_bm25_like(query: str, docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    query_terms = _terms(query)
    doc_terms = [_terms(_doc_text(doc)) for doc in docs]
    df = {term: sum(1 for terms in doc_terms if term in terms) for term in query_terms}
    n_docs = max(1, len(docs))
    scored = []
    for index, (doc, terms) in enumerate(zip(docs, doc_terms)):
        score = 0.0
        for term in query_terms:
            tf = terms.count(term)
            if tf == 0:
                continue
            idf = math.log((n_docs + 1) / (1 + df.get(term, 0))) + 1.0
            score += idf * tf / (tf + 1.2)
        scored.append((_decorate_doc(doc, score), score, index))
    return [doc for doc, _, _ in sorted(scored, key=lambda item: (-item[1], item[2]))]


def _rank_dense_hash_like(query: str, docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    query_vec = _hashed_char_vector(query)
    scored = []
    for index, doc in enumerate(docs):
        score = _cosine(query_vec, _hashed_char_vector(_doc_text(doc)))
        scored.append((_decorate_doc(doc, score), score, index))
    return [doc for doc, _, _ in sorted(scored, key=lambda item: (-item[1], item[2]))]


def _decorate_doc(doc: dict[str, Any], score: float) -> dict[str, Any]:
    clone = dict(doc)
    clone["retrieval_score"] = max(0.0, min(1.0, float(score)))
    return clone


def _doc_text(doc: dict[str, Any]) -> str:
    return f"{doc.get('title') or ''} {doc.get('text') or ''}"


def _terms(text: str) -> list[str]:
    return [term for term in re.findall(r"[A-Za-z0-9]+", text.lower()) if len(term) > 1 and term not in _STOPWORDS]


def _hashed_char_vector(text: str, dims: int = 64) -> list[float]:
    normalized = re.sub(r"\s+", " ", text.lower())
    vec = [0.0] * dims
    if len(normalized) < 3:
        return vec
    for index in range(len(normalized) - 2):
        tri = normalized[index : index + 3]
        digest = hashlib.blake2b(tri.encode("utf-8"), digest_size=8).digest()
        bucket = int.from_bytes(digest, "big") % dims
        vec[bucket] += 1.0
    return vec


def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def _clean_retrieval_max(row: dict[str, Any]) -> float:
    scores = [float(doc.get("retrieval_score") or 0.0) for doc in row.get("clean_evidence") or []]
    return max(scores) if scores else 0.0


def _method_metrics(metrics: dict[str, Any]) -> dict[str, float]:
    return {
        "risk30": float(metrics["accepted_error_at_30"]["risk"]),
        "risk50": float(metrics["accepted_error_at_50"]["risk"]),
        "risk70": float(metrics["accepted_error_at_70"]["risk"]),
        "coverage_at_risk20": float(metrics["coverage_at_risk_20"]["coverage"]),
        "aurc": float(metrics["aurc"]),
    }


def _best_non_csrm(methods: dict[str, Any]) -> dict[str, Any]:
    candidates = []
    for name in NON_CSRM_METHODS:
        if name not in methods:
            continue
        metrics = _method_metrics(methods[name])
        candidates.append({"method": name, **metrics})
    if not candidates:
        raise ValueError("no non-CSRM methods found")
    return min(candidates, key=lambda item: (item["risk30"], item["risk50"], item["aurc"]))


def _aggregate(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "risk30_wins": _count(rows, "risk30_reduction", positive=True),
        "risk30_ties": _count(rows, "risk30_reduction", zero=True),
        "risk30_losses": _count(rows, "risk30_reduction", negative=True),
        "risk50_wins": _count(rows, "risk50_reduction", positive=True),
        "risk50_ties": _count(rows, "risk50_reduction", zero=True),
        "risk50_losses": _count(rows, "risk50_reduction", negative=True),
        "aurc_wins": _count(rows, "aurc_reduction", positive=True),
        "aurc_ties": _count(rows, "aurc_reduction", zero=True),
        "aurc_losses": _count(rows, "aurc_reduction", negative=True),
        "mean_risk30_reduction": _mean(row["deltas"]["risk30_reduction"] for row in rows),
        "mean_risk50_reduction": _mean(row["deltas"]["risk50_reduction"] for row in rows),
        "mean_aurc_reduction": _mean(row["deltas"]["aurc_reduction"] for row in rows),
        "all_win": all(row["verdict"] == "win" for row in rows),
        "has_losses": any(row["verdict"] == "loss_or_mixed" for row in rows),
    }


def _row_verdict(deltas: dict[str, float]) -> str:
    if deltas["risk30_reduction"] > 1e-12 and deltas["risk50_reduction"] >= -1e-12:
        return "win"
    if abs(deltas["risk30_reduction"]) <= 1e-12 and deltas["risk50_reduction"] > 1e-12:
        return "mixed_positive"
    return "loss_or_mixed"


def _count(rows: Sequence[dict[str, Any]], key: str, *, positive=False, zero=False, negative=False) -> int:
    count = 0
    for row in rows:
        value = row["deltas"][key]
        count += int(positive and value > 1e-12)
        count += int(zero and abs(value) <= 1e-12)
        count += int(negative and value < -1e-12)
    return count


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values)


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.4f}"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no} is not valid JSON") from exc
    return rows


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=6)
    args = parser.parse_args()

    summary = run_end2end_retriever_generator_matrix_v4(DEFAULT_DATASETS, top_k=args.top_k)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


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


if __name__ == "__main__":
    main()
