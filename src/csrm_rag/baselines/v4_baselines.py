from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from csrm_rag import (
    QueryOrbit,
    corm_max_score,
    corm_mean_score,
    csrm_components,
    csrm_score,
    naive_orbit_sufficiency,
    single_set_sufficiency,
)


BASELINE_METHODS = [
    "corm_max_clean",
    "corm_mean_clean",
    "faithful_sure_multi",
    "context_sufficiency_clean",
    "equal_budget_mean",
    "equal_budget_min",
    "equal_budget_q25",
    "retrieval_stability",
    "self_consistency_proxy",
    "equal_budget_ensemble_logistic",
    "calibrated_logistic_context",
    "calibrated_logistic_orbit",
    "csrm_rule",
]

ENSEMBLE_FEATURE_METHODS = [
    "corm_max_clean",
    "corm_mean_clean",
    "faithful_sure_multi",
    "context_sufficiency_clean",
    "equal_budget_mean",
    "equal_budget_min",
    "equal_budget_q25",
    "retrieval_stability",
    "self_consistency_proxy",
]


@dataclass(frozen=True)
class BaselineInputs:
    orbits: Sequence[QueryOrbit]
    labels: Sequence[bool]
    groups: Sequence[str] | None = None


def baseline_scores(inputs: BaselineInputs) -> dict[str, list[float]]:
    orbits = list(inputs.orbits)
    labels = list(inputs.labels)
    groups = list(inputs.groups) if inputs.groups is not None else None
    scores = {
        "corm_max_clean": [corm_max_score(orbit.clean) for orbit in orbits],
        "corm_mean_clean": [corm_mean_score(orbit.clean) for orbit in orbits],
        "faithful_sure_multi": [_faithful_sure_multi(orbit) for orbit in orbits],
        "context_sufficiency_clean": [single_set_sufficiency(orbit.clean) for orbit in orbits],
        "equal_budget_mean": [naive_orbit_sufficiency(orbit) for orbit in orbits],
        "equal_budget_min": [_equal_budget_min(orbit) for orbit in orbits],
        "equal_budget_q25": [_equal_budget_quantile(orbit, 0.25) for orbit in orbits],
        "retrieval_stability": [_retrieval_stability(orbit) for orbit in orbits],
        "self_consistency_proxy": [_answer_consistency(orbit) for orbit in orbits],
        "csrm_rule": [csrm_score(orbit) for orbit in orbits],
    }
    scores["calibrated_logistic_context"] = out_of_fold_logistic_scores(
        [_context_features(orbit) for orbit in orbits],
        labels,
        groups=groups,
    )
    scores["calibrated_logistic_orbit"] = out_of_fold_logistic_scores(
        [_orbit_features(orbit) for orbit in orbits],
        labels,
        groups=groups,
    )
    scores["equal_budget_ensemble_logistic"] = out_of_fold_logistic_scores(
        _score_feature_matrix(scores, ENSEMBLE_FEATURE_METHODS),
        labels,
        groups=groups,
    )
    return scores


def out_of_fold_logistic_scores(
    features: Sequence[Sequence[float]],
    labels: Sequence[bool],
    *,
    groups: Sequence[str] | None = None,
    n_splits: int = 5,
) -> list[float]:
    x = np.asarray(features, dtype=float)
    y = np.asarray(labels, dtype=bool)
    if x.shape[0] != y.shape[0]:
        raise ValueError("features and labels must have the same number of rows")
    if x.shape[0] < 4:
        return [float(y.mean())] * int(x.shape[0])
    if len(set(y.tolist())) < 2:
        return [float(y.mean())] * int(x.shape[0])

    splitter = _splitter(y, groups, n_splits)
    predictions = np.zeros(x.shape[0], dtype=float)
    for train_idx, test_idx in splitter:
        train_y = y[train_idx]
        if len(set(train_y.tolist())) < 2:
            predictions[test_idx] = float(train_y.mean()) if train_y.size else float(y.mean())
            continue
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, class_weight="balanced", random_state=0),
        )
        model.fit(x[train_idx], train_y)
        predictions[test_idx] = model.predict_proba(x[test_idx])[:, 1]
    return predictions.tolist()


def _splitter(y: np.ndarray, groups: Sequence[str] | None, n_splits: int):
    if groups is not None and len(set(groups)) >= 2:
        group_count = len(set(groups))
        splits = max(2, min(n_splits, group_count))
        return GroupKFold(n_splits=splits).split(np.zeros_like(y), y, np.asarray(groups))
    positive = int(y.sum())
    negative = int((~y).sum())
    splits = max(2, min(n_splits, positive, negative))
    return StratifiedKFold(n_splits=splits, shuffle=True, random_state=0).split(np.zeros_like(y), y)


def _score_feature_matrix(scores: dict[str, Sequence[float]], methods: Sequence[str]) -> list[list[float]]:
    if not methods:
        return []
    row_count = len(scores[methods[0]])
    return [[float(scores[method][index]) for method in methods] for index in range(row_count)]


def _faithful_sure_multi(orbit: QueryOrbit) -> float:
    set_scores = _set_scores(orbit)
    mean_score = float(np.mean(set_scores))
    worst_score = float(min(set_scores))
    max_conflict = max(_max_doc_attr(orbit, "conflict"), 0.0)
    mean_missing = _mean_doc_attr(orbit, "missing")
    return _clip01(0.35 * mean_score + 0.35 * worst_score + 0.15 * (1.0 - max_conflict) + 0.15 * (1.0 - mean_missing))


def _equal_budget_min(orbit: QueryOrbit) -> float:
    return float(min(_set_scores(orbit)))


def _equal_budget_quantile(orbit: QueryOrbit, quantile: float) -> float:
    return float(np.quantile(_set_scores(orbit), quantile))


def _retrieval_stability(orbit: QueryOrbit) -> float:
    set_scores = [corm_mean_score(item) for item in orbit.all_sets]
    if not set_scores:
        return 0.0
    overlap = csrm_components(orbit).overlap
    score_std = float(np.std(set_scores))
    return _clip01(0.50 * float(np.mean(set_scores)) + 0.30 * overlap + 0.20 * (1.0 - score_std))


def _answer_consistency(orbit: QueryOrbit) -> float:
    return csrm_components(orbit).answer_consistency


def _context_features(orbit: QueryOrbit) -> list[float]:
    clean = orbit.clean
    supports = [doc.support for doc in clean.docs] or [0.0]
    conflicts = [doc.conflict for doc in clean.docs] or [0.0]
    missing = [doc.missing for doc in clean.docs] or [1.0]
    corm = [doc.corm_score for doc in clean.docs] or [0.0]
    return [
        single_set_sufficiency(clean),
        max(supports),
        float(np.mean(supports)),
        max(conflicts),
        float(np.mean(missing)),
        max(corm),
        float(np.mean(corm)),
        float(len(clean.docs)),
    ]


def _orbit_features(orbit: QueryOrbit) -> list[float]:
    components = csrm_components(orbit)
    set_scores = _set_scores(orbit)
    return [
        components.clean_sufficiency,
        components.mean_sufficiency,
        components.worst_sufficiency,
        components.stability,
        components.conflict_monotonicity,
        components.answer_consistency,
        components.overlap,
        max(_max_conflict(item) for item in orbit.all_sets),
        _mean_doc_attr(orbit, "missing"),
        float(np.std(set_scores)),
        float(len(orbit.perturbations)),
    ]


def _set_scores(orbit: QueryOrbit) -> list[float]:
    return [single_set_sufficiency(item) for item in orbit.all_sets]


def _max_doc_attr(orbit: QueryOrbit, attr: str) -> float:
    values = [getattr(doc, attr) for item in orbit.all_sets for doc in item.docs]
    return float(max(values)) if values else 0.0


def _mean_doc_attr(orbit: QueryOrbit, attr: str) -> float:
    values = [getattr(doc, attr) for item in orbit.all_sets for doc in item.docs]
    return float(np.mean(values)) if values else 0.0


def _max_conflict(evidence_set) -> float:
    values = [doc.conflict for doc in evidence_set.docs]
    return float(max(values)) if values else 0.0


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
