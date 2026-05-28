#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag.feature_firewall import assert_no_forbidden_features
from experiments.run_v4_anti_shortcut_probes import _structural_only_probe


def build_v4_structural_balanced_subset(
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_prefix: Path,
    max_combinations: int = 250_000,
    seed: int = 97,
) -> dict:
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
    if not positives or len(negatives) < len(positives):
        raise ValueError("balanced subset requires at least as many negatives as positives")

    best = _select_negatives(
        raw_rows=raw_rows,
        labels=labels,
        positives=positives,
        negatives=negatives,
        max_combinations=max_combinations,
        seed=seed,
    )
    selected = sorted([*positives, *best["negative_indices"]])

    raw_output = _append_suffix(output_prefix, ".raw.jsonl")
    private_output = _append_suffix(output_prefix, ".private_eval.jsonl")
    scored_output = _append_suffix(output_prefix, ".textonly_scored.jsonl")
    report_output = _append_suffix(output_prefix, ".balance_report.json")
    _write_jsonl(raw_output, [raw_rows[index] for index in selected])
    _write_jsonl(private_output, [private_rows[index] for index in selected])
    _write_jsonl(scored_output, [scored_rows[index] for index in selected])

    selected_labels = [labels[index] for index in selected]
    selected_raw = [raw_rows[index] for index in selected]
    structural_probe = _structural_only_probe(selected_raw, selected_labels)
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
        "input_n": len(raw_rows),
        "input_positive": len(positives),
        "input_negative": len(negatives),
        "selected_n": len(selected),
        "selected_positive": len(positives),
        "selected_negative": len(best["negative_indices"]),
        "selected_negative_orbit_ids": [raw_rows[index]["orbit_id"] for index in best["negative_indices"]],
        "search": {
            "objective": "minimize structural-only max single-feature AUROC, then mean feature gap",
            "candidate_combinations_evaluated": best["evaluated"],
            "candidate_combinations_total": best["total_combinations"],
            "max_combinations": max_combinations,
            "seed": seed,
            "exhaustive": best["evaluated"] == best["total_combinations"],
        },
        "feature_balance": _feature_balance(selected_raw, selected_labels),
        "structural_only_probe": structural_probe,
    }
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def _select_negatives(
    raw_rows: list[dict],
    labels: Sequence[bool],
    positives: Sequence[int],
    negatives: Sequence[int],
    max_combinations: int,
    seed: int,
) -> dict:
    choose = len(positives)
    total = math.comb(len(negatives), choose)
    combos: Sequence[tuple[int, ...]]
    if total <= max_combinations:
        combos = itertools.combinations(negatives, choose)
    else:
        rng = random.Random(seed)
        seen = set()

        def sampled() -> Sequence[tuple[int, ...]]:
            output = []
            while len(output) < max_combinations:
                combo = tuple(sorted(rng.sample(list(negatives), choose)))
                if combo in seen:
                    continue
                seen.add(combo)
                output.append(combo)
            return output

        combos = sampled()

    best_key = None
    best_combo = None
    evaluated = 0
    for combo in combos:
        selected = [*positives, *combo]
        selected_rows = [raw_rows[index] for index in selected]
        selected_labels = [labels[index] for index in selected]
        probe = _structural_only_probe(selected_rows, selected_labels)
        max_auc = float(probe["max_single_feature_auroc"] or 1.0)
        gap = _mean_feature_gap(selected_rows, selected_labels)
        key = (max_auc, gap, tuple(raw_rows[index]["orbit_id"] for index in combo))
        evaluated += 1
        if best_key is None or key < best_key:
            best_key = key
            best_combo = combo
    if best_combo is None:
        raise ValueError("no negative combination evaluated")
    return {
        "negative_indices": list(best_combo),
        "evaluated": evaluated,
        "total_combinations": total,
        "objective": best_key,
    }


def _feature_balance(raw_rows: Sequence[dict], labels: Sequence[bool]) -> dict:
    features = [_structural_features(row) for row in raw_rows]
    output = {}
    for name in sorted(features[0]):
        pos_values = [row[name] for row, label in zip(features, labels) if label]
        neg_values = [row[name] for row, label in zip(features, labels) if not label]
        output[name] = {
            "positive_mean": _mean(pos_values),
            "negative_mean": _mean(neg_values),
            "absolute_mean_gap": abs(_mean(pos_values) - _mean(neg_values)),
        }
    return output


def _mean_feature_gap(raw_rows: Sequence[dict], labels: Sequence[bool]) -> float:
    balance = _feature_balance(raw_rows, labels)
    return _mean([item["absolute_mean_gap"] for item in balance.values()])


def _structural_features(row: dict) -> dict[str, float]:
    retrieval_scores = [float(value) for value in row.get("retrieval_scores") or [0.0]]
    texts = _all_texts(row)
    return {
        "perturbation_count": float(len(row.get("perturbations") or [])),
        "clean_doc_count": float(len(row.get("clean_evidence") or [])),
        "total_doc_count": float(len(row.get("clean_evidence") or []) + sum(len(item.get("evidence") or []) for item in row.get("perturbations") or [])),
        "mean_doc_chars": _mean([len(text) for text in texts]),
        "total_doc_chars": float(sum(len(text) for text in texts)),
        "mean_retrieval_score": _mean(retrieval_scores),
        "max_retrieval_score": max(retrieval_scores),
    }


def _all_texts(row: dict) -> list[str]:
    texts = [str(doc.get("text") or "") for doc in row.get("clean_evidence") or []]
    for item in row.get("perturbations") or []:
        texts.extend(str(doc.get("text") or "") for doc in item.get("evidence") or [])
    return texts


def _mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return float(sum(values) / len(values))


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


def _write_jsonl(path: Path, rows: Sequence[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _append_suffix(path: Path, suffix: str) -> Path:
    return path.with_name(path.name + suffix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--scored", type=Path, required=True)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--max-combinations", type=int, default=250_000)
    parser.add_argument("--seed", type=int, default=97)
    args = parser.parse_args()
    report = build_v4_structural_balanced_subset(
        raw_path=args.raw,
        private_path=args.private,
        scored_path=args.scored,
        output_prefix=args.output_prefix,
        max_combinations=args.max_combinations,
        seed=args.seed,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
