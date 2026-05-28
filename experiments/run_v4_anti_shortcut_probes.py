#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
import statistics
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import csrm_score, roc_auc
from csrm_rag.feature_firewall import assert_no_forbidden_features
from experiments.evaluate_orbits import load_orbits


def run_v4_anti_shortcut_probes(
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_path: Path | None = None,
    random_trials: int = 200,
    seed: int = 91,
) -> dict:
    raw_rows = _read_jsonl(raw_path)
    private_rows = _read_jsonl(private_path)
    scored_orbits = load_orbits(scored_path)
    if not (len(raw_rows) == len(private_rows) == len(scored_orbits)):
        raise ValueError("raw, private, and scored files must contain the same number of orbits")

    for row in raw_rows:
        assert_no_forbidden_features(row)

    labels = [bool(row["label_answerable"]) for row in private_rows]
    group_ids = [str(row["source_item_group_id"]) for row in raw_rows]
    construction_types = [str(row.get("construction_type") or "unknown") for row in private_rows]
    csrm_scores = [csrm_score(orbit) for orbit in scored_orbits]

    report = {
        "inputs": {
            "raw": str(raw_path),
            "private": str(private_path),
            "scored": str(scored_path),
        },
        "n": len(labels),
        "positive": int(sum(labels)),
        "negative": int(len(labels) - sum(labels)),
        "raw_firewall_passed": True,
        "structural_only_probe": _structural_only_probe(raw_rows, labels),
        "random_label_sanity": _random_label_sanity(csrm_scores, labels, random_trials, seed),
        "group_split_probe": _group_split_probe(group_ids, labels, seed),
        "private_metadata_leakage_upper_bound": _private_metadata_probe(construction_types, labels),
        "interpretation": {
            "structural_only_pass_threshold": "max_single_feature_auroc <= 0.55 is preferred",
            "random_label_pass_threshold": "random_label_csrm_auroc_median near 0.5 is preferred",
            "private_metadata_note": "This is an upper bound from evaluator-only private fields; high values mean these fields must never reach scorers.",
        },
    }
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def _structural_only_probe(raw_rows: list[dict], labels: Sequence[bool]) -> dict:
    features = {
        "perturbation_count": [float(len(row.get("perturbations") or [])) for row in raw_rows],
        "clean_doc_count": [float(len(row.get("clean_evidence") or [])) for row in raw_rows],
        "total_doc_count": [_total_doc_count(row) for row in raw_rows],
        "mean_doc_chars": [_mean_doc_chars(row) for row in raw_rows],
        "total_doc_chars": [_total_doc_chars(row) for row in raw_rows],
        "mean_retrieval_score": [_mean(row.get("retrieval_scores") or [0.0]) for row in raw_rows],
        "max_retrieval_score": [max(row.get("retrieval_scores") or [0.0]) for row in raw_rows],
    }
    feature_results = {}
    for name, values in features.items():
        feature_results[name] = {
            "auroc": _safe_oriented_auc(values, labels),
            "unique_values": len(set(values)),
            "mean_positive": _mean([value for value, label in zip(values, labels) if label]),
            "mean_negative": _mean([value for value, label in zip(values, labels) if not label]),
        }
    aurocs = [item["auroc"] for item in feature_results.values() if item["auroc"] is not None]
    return {
        "features": feature_results,
        "max_single_feature_auroc": max(aurocs) if aurocs else None,
        "passed_0_55_threshold": max(aurocs) <= 0.55 if aurocs else None,
    }


def _random_label_sanity(scores: Sequence[float], labels: Sequence[bool], trials: int, seed: int) -> dict:
    rng = random.Random(seed)
    values = []
    labels_list = list(labels)
    for _ in range(trials):
        shuffled = labels_list[:]
        rng.shuffle(shuffled)
        auc = _safe_auc(scores, shuffled)
        if auc is not None:
            values.append(auc)
    if not values:
        return {"trials": trials, "valid_trials": 0, "auroc": None}
    ordered = sorted(values)
    return {
        "trials": trials,
        "valid_trials": len(values),
        "auroc": {
            "min": min(values),
            "median": statistics.median(values),
            "max": max(values),
            "p2_5": ordered[int(0.025 * (len(ordered) - 1))],
            "p97_5": ordered[int(0.975 * (len(ordered) - 1))],
        },
    }


def _group_split_probe(group_ids: Sequence[str], labels: Sequence[bool], seed: int) -> dict:
    folds: dict[int, list[int]] = {0: [], 1: [], 2: []}
    for index, group_id in enumerate(group_ids):
        fold = _stable_fold(group_id, seed, n_folds=3)
        folds[fold].append(index)

    fold_summary = {}
    for fold, indices in folds.items():
        fold_labels = [labels[index] for index in indices]
        fold_summary[str(fold)] = {
            "n": len(indices),
            "positive": int(sum(fold_labels)),
            "negative": int(len(fold_labels) - sum(fold_labels)),
            "groups": len({group_ids[index] for index in indices}),
        }

    overlaps = []
    for left in range(3):
        left_groups = {group_ids[index] for index in folds[left]}
        for right in range(left + 1, 3):
            right_groups = {group_ids[index] for index in folds[right]}
            overlaps.append(len(left_groups & right_groups))
    return {
        "n_groups": len(set(group_ids)),
        "folds": fold_summary,
        "max_group_overlap_between_folds": max(overlaps) if overlaps else 0,
        "passed_no_group_overlap": all(overlap == 0 for overlap in overlaps),
    }


def _private_metadata_probe(construction_types: Sequence[str], labels: Sequence[bool]) -> dict:
    values_by_type: dict[str, list[bool]] = {}
    for construction_type, label in zip(construction_types, labels):
        values_by_type.setdefault(construction_type, []).append(label)
    type_positive_rate = {
        key: sum(values) / len(values)
        for key, values in sorted(values_by_type.items())
        if values
    }
    scores = [type_positive_rate[item] for item in construction_types]
    return {
        "construction_type_positive_rate": type_positive_rate,
        "construction_type_oriented_auroc": _safe_oriented_auc(scores, labels),
    }


def _safe_oriented_auc(scores: Sequence[float], labels: Sequence[bool]) -> float | None:
    auc = _safe_auc(scores, labels)
    if auc is None:
        return None
    return max(auc, 1.0 - auc)


def _safe_auc(scores: Sequence[float], labels: Sequence[bool]) -> float | None:
    try:
        return roc_auc(scores, labels)
    except ValueError:
        return None


def _stable_fold(group_id: str, seed: int, n_folds: int) -> int:
    digest = hashlib.sha256(f"{seed}:{group_id}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % n_folds


def _total_doc_count(row: dict) -> float:
    return float(len(row.get("clean_evidence") or []) + sum(len(item.get("evidence") or []) for item in row.get("perturbations") or []))


def _mean_doc_chars(row: dict) -> float:
    texts = _all_texts(row)
    return _mean([len(text) for text in texts])


def _total_doc_chars(row: dict) -> float:
    return float(sum(len(text) for text in _all_texts(row)))


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--scored", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=91)
    args = parser.parse_args()
    report = run_v4_anti_shortcut_probes(
        raw_path=args.raw,
        private_path=args.private,
        scored_path=args.scored,
        output_path=args.output,
        random_trials=args.random_trials,
        seed=args.seed,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
