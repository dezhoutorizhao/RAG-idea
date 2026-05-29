from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from csrm_rag import QueryOrbit, corm_max_score, corm_mean_score, csrm_components, csrm_score, naive_orbit_sufficiency, single_set_sufficiency


@dataclass(frozen=True)
class CalibrationSplit:
    train: list[int]
    calibration: list[int]
    test: list[int]
    train_groups: list[str]
    calibration_groups: list[str]
    test_groups: list[str]


class OrbitRiskCalibrator:
    def __init__(self, random_state: int = 0) -> None:
        self.random_state = random_state
        self.model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=2000, class_weight="balanced", random_state=random_state),
        )
        self.gbdt_model = GradientBoostingClassifier(
            n_estimators=64,
            learning_rate=0.05,
            max_depth=2,
            min_samples_leaf=5,
            random_state=random_state,
        )
        self.isotonic = IsotonicRegression(out_of_bounds="clip")
        self.prior_: float | None = None
        self.logistic_ready_ = False
        self.gbdt_ready_ = False
        self.isotonic_ready_ = False

    def fit(
        self,
        train_orbits: Sequence[QueryOrbit],
        train_labels: Sequence[bool],
        calibration_orbits: Sequence[QueryOrbit] | None = None,
        calibration_labels: Sequence[bool] | None = None,
    ) -> "OrbitRiskCalibrator":
        y_train = np.asarray(train_labels, dtype=bool)
        self.prior_ = float(y_train.mean()) if y_train.size else 0.5
        if y_train.size and len(set(y_train.tolist())) >= 2:
            features = _feature_matrix(train_orbits)
            self.model.fit(features, y_train)
            self.gbdt_model.fit(features, y_train)
            self.logistic_ready_ = True
            self.gbdt_ready_ = True
        if calibration_orbits is not None and calibration_labels is not None:
            y_cal = np.asarray(calibration_labels, dtype=bool)
            if y_cal.size and len(set(y_cal.tolist())) >= 2:
                self.isotonic.fit(self.predict_logistic(calibration_orbits), y_cal.astype(float))
                self.isotonic_ready_ = True
        return self

    def predict_logistic(self, orbits: Sequence[QueryOrbit]) -> list[float]:
        if not orbits:
            return []
        if not self.logistic_ready_:
            return [0.5 if self.prior_ is None else self.prior_] * len(orbits)
        return self.model.predict_proba(_feature_matrix(orbits))[:, 1].tolist()

    def predict_isotonic(self, orbits: Sequence[QueryOrbit]) -> list[float]:
        logistic_scores = self.predict_logistic(orbits)
        if not logistic_scores:
            return []
        if not self.isotonic_ready_:
            return logistic_scores
        return self.isotonic.predict(logistic_scores).tolist()

    def predict_gbdt(self, orbits: Sequence[QueryOrbit]) -> list[float]:
        if not orbits:
            return []
        if not self.gbdt_ready_:
            return [0.5 if self.prior_ is None else self.prior_] * len(orbits)
        return self.gbdt_model.predict_proba(_feature_matrix(orbits))[:, 1].tolist()

    def coefficients(self) -> dict[str, float]:
        if not self.logistic_ready_:
            return {}
        estimator = self.model.named_steps["logisticregression"]
        return {
            name: float(weight)
            for name, weight in zip(csrm_v4_feature_names(), estimator.coef_[0].tolist())
        }


def split_groups(
    groups: Sequence[str],
    labels: Sequence[bool],
    *,
    train_frac: float = 0.60,
    cal_frac: float = 0.20,
    seed: int = 0,
) -> CalibrationSplit:
    if train_frac <= 0.0 or cal_frac <= 0.0 or train_frac + cal_frac >= 1.0:
        raise ValueError("train_frac and cal_frac must be positive and leave test mass")
    if len(groups) != len(labels):
        raise ValueError("groups and labels must have the same length")

    group_to_indices: dict[str, list[int]] = {}
    for index, group in enumerate(groups):
        group_to_indices.setdefault(str(group), []).append(index)
    group_ids = list(group_to_indices)
    if len(group_ids) < 3:
        raise ValueError("at least three source groups are required for train/calibration/test")

    rng = random.Random(seed)
    best = None
    for attempt in range(128):
        shuffled = list(group_ids)
        rng.shuffle(shuffled)
        n_train = max(1, int(round(train_frac * len(shuffled))))
        n_cal = max(1, int(round(cal_frac * len(shuffled))))
        if n_train + n_cal >= len(shuffled):
            n_cal = max(1, len(shuffled) - n_train - 1)
        train_groups = sorted(shuffled[:n_train])
        cal_groups = sorted(shuffled[n_train : n_train + n_cal])
        test_groups = sorted(shuffled[n_train + n_cal :])
        candidate = _split_from_group_ids(group_to_indices, train_groups, cal_groups, test_groups)
        if _all_splits_have_both_labels(candidate, labels):
            return candidate
        if best is None or _split_score(candidate, labels) > _split_score(best, labels):
            best = candidate
        rng.seed(seed + attempt + 1)
    if best is None:
        raise ValueError("failed to construct calibration split")
    return best


def csrm_v4_feature_names() -> list[str]:
    return [
        "corm_max_clean",
        "corm_mean_clean",
        "context_sufficiency_clean",
        "naive_orbit_average",
        "clean_sufficiency",
        "mean_sufficiency",
        "min_sufficiency",
        "sufficiency_variance",
        "max_conflict",
        "mean_missing",
        "answer_consistency",
        "support_signature_consistency",
        "retrieval_overlap",
        "verifier_entropy",
        "clean_to_worst_gap",
        "orbit_answer_flip_rate",
        "perturbation_count",
    ]


def csrm_v4_features(orbit: QueryOrbit) -> list[float]:
    comp = csrm_components(orbit)
    set_scores = [single_set_sufficiency(item) for item in orbit.all_sets]
    clean = set_scores[0] if set_scores else 0.0
    worst = min(set_scores) if set_scores else 0.0
    return [
        corm_max_score(orbit.clean),
        corm_mean_score(orbit.clean),
        single_set_sufficiency(orbit.clean),
        naive_orbit_sufficiency(orbit),
        comp.clean_sufficiency,
        comp.mean_sufficiency,
        comp.worst_sufficiency,
        float(np.var(set_scores)) if set_scores else 0.0,
        _max_doc_attr(orbit, "conflict"),
        _mean_doc_attr(orbit, "missing"),
        comp.answer_consistency,
        comp.answer_consistency,
        comp.overlap,
        _entropy(set_scores),
        max(0.0, clean - worst),
        1.0 - comp.answer_consistency,
        float(len(orbit.perturbations)),
    ]


def csrm_minimax_score(orbit: QueryOrbit) -> float:
    comp = csrm_components(orbit)
    max_conflict = _max_doc_attr(orbit, "conflict")
    mean_missing = _mean_doc_attr(orbit, "missing")
    return _clip01(
        0.45 * comp.worst_sufficiency
        + 0.20 * comp.answer_consistency
        + 0.15 * comp.overlap
        + 0.10 * (1.0 - max_conflict)
        + 0.10 * (1.0 - mean_missing)
    )


def csrm_rule_scores(orbits: Sequence[QueryOrbit]) -> list[float]:
    return [csrm_score(orbit) for orbit in orbits]


def csrm_minimax_scores(orbits: Sequence[QueryOrbit]) -> list[float]:
    return [csrm_minimax_score(orbit) for orbit in orbits]


def _feature_matrix(orbits: Sequence[QueryOrbit]) -> np.ndarray:
    return np.asarray([csrm_v4_features(orbit) for orbit in orbits], dtype=float)


def _split_from_group_ids(
    group_to_indices: dict[str, list[int]],
    train_groups: Sequence[str],
    cal_groups: Sequence[str],
    test_groups: Sequence[str],
) -> CalibrationSplit:
    return CalibrationSplit(
        train=[idx for group in train_groups for idx in group_to_indices[group]],
        calibration=[idx for group in cal_groups for idx in group_to_indices[group]],
        test=[idx for group in test_groups for idx in group_to_indices[group]],
        train_groups=list(train_groups),
        calibration_groups=list(cal_groups),
        test_groups=list(test_groups),
    )


def _all_splits_have_both_labels(split: CalibrationSplit, labels: Sequence[bool]) -> bool:
    return all(_has_both([labels[index] for index in indices]) for indices in [split.train, split.calibration, split.test])


def _has_both(values: Sequence[bool]) -> bool:
    return bool(values) and len(set(bool(value) for value in values)) == 2


def _split_score(split: CalibrationSplit, labels: Sequence[bool]) -> int:
    score = 0
    for indices in [split.train, split.calibration, split.test]:
        score += int(_has_both([labels[index] for index in indices]))
    return score


def _max_doc_attr(orbit: QueryOrbit, attr: str) -> float:
    values = [float(getattr(doc, attr)) for item in orbit.all_sets for doc in item.docs]
    return max(values) if values else 0.0


def _mean_doc_attr(orbit: QueryOrbit, attr: str) -> float:
    values = [float(getattr(doc, attr)) for item in orbit.all_sets for doc in item.docs]
    return float(np.mean(values)) if values else 0.0


def _entropy(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    clipped = np.clip(np.asarray(values, dtype=float), 1e-8, 1.0 - 1e-8)
    return float(-np.mean(clipped * np.log(clipped) + (1.0 - clipped) * np.log(1.0 - clipped)))


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
