#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Callable, Dict, List, Sequence

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from csrm_rag import (
    QueryOrbit,
    area_under_risk_coverage,
    calibration_error,
    corm_max_score,
    corm_mean_score,
    csrm_components,
    csrm_score,
    naive_orbit_sufficiency,
    risk_coverage_curve,
    roc_auc,
    selective_risk_at_coverage,
    single_set_sufficiency,
)
from experiments.evaluate_orbits import load_orbits


def group_split(
    orbits: Sequence[QueryOrbit],
    train_frac: float,
    cal_frac: float,
    seed: int,
) -> dict:
    if train_frac <= 0.0 or cal_frac <= 0.0 or train_frac + cal_frac >= 1.0:
        raise ValueError("train_frac and cal_frac must be positive and leave test mass")

    groups: Dict[str, List[QueryOrbit]] = {}
    for orbit in orbits:
        groups.setdefault(_group_id(orbit.orbit_id), []).append(orbit)

    rng = random.Random(seed)
    group_ids = list(groups)
    rng.shuffle(group_ids)
    n_train = max(1, int(round(train_frac * len(group_ids))))
    n_cal = max(1, int(round(cal_frac * len(group_ids))))
    train_ids = set(group_ids[:n_train])
    cal_ids = set(group_ids[n_train : n_train + n_cal])
    test_ids = set(group_ids[n_train + n_cal :])
    if not test_ids:
        raise ValueError("test split is empty")

    return {
        "train": [orbit for gid in train_ids for orbit in groups[gid]],
        "calibration": [orbit for gid in cal_ids for orbit in groups[gid]],
        "test": [orbit for gid in test_ids for orbit in groups[gid]],
        "groups": {
            "train": sorted(train_ids),
            "calibration": sorted(cal_ids),
            "test": sorted(test_ids),
        },
    }


def train_and_evaluate(
    orbits: Sequence[QueryOrbit],
    train_frac: float,
    cal_frac: float,
    seed: int,
    risk_target: float,
) -> dict:
    split = group_split(orbits, train_frac, cal_frac, seed)
    train = split["train"]
    cal = split["calibration"]
    test = split["test"]

    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, class_weight="balanced", random_state=seed),
    )
    model.fit(_feature_matrix(train), _labels(train))

    methods: Dict[str, Callable[[Sequence[QueryOrbit]], List[float]]] = {
        "corm_max_clean": lambda xs: [corm_max_score(x.clean) for x in xs],
        "corm_mean_clean": lambda xs: [corm_mean_score(x.clean) for x in xs],
        "single_set_sure_style": lambda xs: [single_set_sufficiency(x.clean) for x in xs],
        "naive_orbit_average": lambda xs: [naive_orbit_sufficiency(x) for x in xs],
        "csrm_fixed_weights": lambda xs: [csrm_score(x) for x in xs],
        "csrm_logreg_calibrated": lambda xs: model.predict_proba(_feature_matrix(xs))[:, 1].tolist(),
    }

    output = {
        "split_sizes": {
            "train": len(train),
            "calibration": len(cal),
            "test": len(test),
            "train_groups": len(split["groups"]["train"]),
            "calibration_groups": len(split["groups"]["calibration"]),
            "test_groups": len(split["groups"]["test"]),
        },
        "risk_target": risk_target,
        "feature_names": _feature_names(),
        "methods": {},
    }
    for name, scorer in methods.items():
        cal_scores = scorer(cal)
        test_scores = scorer(test)
        threshold = _threshold_for_risk(cal_scores, _labels(cal), risk_target)
        output["methods"][name] = {
            "calibration": _score_summary(cal_scores, _labels(cal), threshold),
            "test": _score_summary(test_scores, _labels(test), threshold),
        }
    return output


def _feature_matrix(orbits: Sequence[QueryOrbit]) -> np.ndarray:
    rows = []
    for orbit in orbits:
        comp = csrm_components(orbit)
        rows.append(
            [
                corm_max_score(orbit.clean),
                corm_mean_score(orbit.clean),
                single_set_sufficiency(orbit.clean),
                naive_orbit_sufficiency(orbit),
                comp.clean_sufficiency,
                comp.mean_sufficiency,
                comp.worst_sufficiency,
                comp.stability,
                comp.conflict_monotonicity,
                comp.answer_consistency,
                comp.overlap,
            ]
        )
    return np.asarray(rows, dtype=float)


def _feature_names() -> List[str]:
    return [
        "corm_max_clean",
        "corm_mean_clean",
        "single_set_sufficiency",
        "naive_orbit_sufficiency",
        "clean_sufficiency",
        "mean_sufficiency",
        "worst_sufficiency",
        "stability",
        "conflict_monotonicity",
        "answer_consistency",
        "overlap",
    ]


def _labels(orbits: Sequence[QueryOrbit]) -> List[bool]:
    return [orbit.label_answerable for orbit in orbits]


def _score_summary(scores: Sequence[float], labels: Sequence[bool], threshold: float) -> dict:
    accepted = [score >= threshold for score in scores]
    accepted_count = sum(accepted)
    accepted_correct = [
        label for label, is_accepted in zip(labels, accepted) if is_accepted
    ]
    if accepted_count:
        selective_accuracy = sum(accepted_correct) / accepted_count
        selective_risk = 1.0 - selective_accuracy
    else:
        selective_accuracy = 0.0
        selective_risk = 0.0

    return {
        "n": len(labels),
        "positive": int(sum(labels)),
        "negative": int(len(labels) - sum(labels)),
        "auroc": _safe_roc_auc(scores, labels),
        "aurc": area_under_risk_coverage(risk_coverage_curve(scores, labels)),
        "calibration": calibration_error(scores, labels),
        "risk_at_30_coverage": selective_risk_at_coverage(scores, labels, 0.30),
        "risk_at_50_coverage": selective_risk_at_coverage(scores, labels, 0.50),
        "risk_at_70_coverage": selective_risk_at_coverage(scores, labels, 0.70),
        "calibrated_threshold": threshold,
        "calibrated_coverage": accepted_count / len(labels),
        "calibrated_risk": selective_risk,
        "calibrated_accuracy": selective_accuracy,
    }


def _threshold_for_risk(
    scores: Sequence[float],
    labels: Sequence[bool],
    risk_target: float,
) -> float:
    pairs = sorted(zip(scores, labels), key=lambda item: item[0], reverse=True)
    best_threshold = 1.0
    best_coverage = -1.0
    positives = 0
    for idx, (score, label) in enumerate(pairs, start=1):
        positives += int(label)
        risk = 1.0 - positives / idx
        coverage = idx / len(pairs)
        if risk <= risk_target and coverage > best_coverage:
            best_threshold = float(score)
            best_coverage = coverage
    return best_threshold


def _safe_roc_auc(scores: Sequence[float], labels: Sequence[bool]) -> float | None:
    try:
        return roc_auc(scores, labels)
    except ValueError:
        return None


def _group_id(orbit_id: str) -> str:
    parts = orbit_id.split(":")
    if len(parts) >= 2:
        return ":".join(parts[:2])
    return orbit_id


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--train-frac", type=float, default=0.60)
    parser.add_argument("--cal-frac", type=float, default=0.20)
    parser.add_argument("--seed", type=int, default=31)
    parser.add_argument("--risk-target", type=float, default=0.20)
    args = parser.parse_args()

    result = train_and_evaluate(
        load_orbits(args.input),
        train_frac=args.train_frac,
        cal_frac=args.cal_frac,
        seed=args.seed,
        risk_target=args.risk_target,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
