from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

import numpy as np


@dataclass(frozen=True)
class RiskCoveragePoint:
    threshold: float
    coverage: float
    risk: float
    accuracy: float


def calibration_error(
    confidences: Sequence[float],
    correct: Sequence[bool],
    n_bins: int = 10,
) -> dict:
    conf = np.asarray(confidences, dtype=float)
    y = np.asarray(correct, dtype=bool)
    if conf.shape[0] != y.shape[0]:
        raise ValueError("confidences and correct must have the same length")
    if conf.size == 0:
        raise ValueError("cannot compute calibration on an empty input")

    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    mce = 0.0
    for left, right in zip(bins[:-1], bins[1:]):
        if right == 1.0:
            mask = (conf >= left) & (conf <= right)
        else:
            mask = (conf >= left) & (conf < right)
        if not mask.any():
            continue
        acc = y[mask].mean()
        avg_conf = conf[mask].mean()
        gap = abs(float(acc) - float(avg_conf))
        ece += float(mask.mean()) * gap
        mce = max(mce, gap)
    return {"ece": ece, "mce": mce}


def risk_coverage_curve(
    confidences: Sequence[float],
    correct: Sequence[bool],
    thresholds: Iterable[float] | None = None,
) -> List[RiskCoveragePoint]:
    conf = np.asarray(confidences, dtype=float)
    y = np.asarray(correct, dtype=bool)
    if conf.shape[0] != y.shape[0]:
        raise ValueError("confidences and correct must have the same length")
    if conf.size == 0:
        raise ValueError("cannot compute risk coverage on an empty input")

    if thresholds is None:
        thresholds = np.linspace(0.0, 1.0, 101)

    points = []
    for threshold in thresholds:
        accepted = conf >= threshold
        coverage = float(accepted.mean())
        if accepted.any():
            accuracy = float(y[accepted].mean())
            risk = 1.0 - accuracy
        else:
            accuracy = 0.0
            risk = 0.0
        points.append(
            RiskCoveragePoint(
                threshold=float(threshold),
                coverage=coverage,
                risk=risk,
                accuracy=accuracy,
            )
        )
    return points


def area_under_risk_coverage(points: Sequence[RiskCoveragePoint]) -> float:
    if not points:
        raise ValueError("cannot compute AURC on an empty curve")

    ordered = sorted(points, key=lambda item: item.coverage)
    area = 0.0
    prev_coverage = 0.0
    prev_risk = ordered[0].risk
    for point in ordered:
        coverage = point.coverage
        if coverage < prev_coverage:
            raise ValueError("coverage must be nondecreasing after sorting")
        area += (coverage - prev_coverage) * ((prev_risk + point.risk) / 2.0)
        prev_coverage = coverage
        prev_risk = point.risk
    if prev_coverage < 1.0:
        area += (1.0 - prev_coverage) * prev_risk
    return float(area)


def selective_risk_at_coverage(
    confidences: Sequence[float],
    correct: Sequence[bool],
    target_coverage: float,
) -> dict:
    if not 0.0 < target_coverage <= 1.0:
        raise ValueError("target_coverage must be in (0, 1]")

    conf = np.asarray(confidences, dtype=float)
    y = np.asarray(correct, dtype=bool)
    if conf.shape[0] != y.shape[0]:
        raise ValueError("confidences and correct must have the same length")
    if conf.size == 0:
        raise ValueError("cannot compute selective risk on an empty input")

    order = np.argsort(-conf)
    n_accept = max(1, int(np.ceil(target_coverage * conf.size)))
    accepted_idx = order[:n_accept]
    accuracy = float(y[accepted_idx].mean())
    threshold = float(conf[accepted_idx[-1]])
    return {
        "coverage": n_accept / conf.size,
        "risk": 1.0 - accuracy,
        "accuracy": accuracy,
        "threshold": threshold,
        "accepted": n_accept,
    }


def roc_auc(scores: Sequence[float], labels: Sequence[bool]) -> float:
    score_arr = np.asarray(scores, dtype=float)
    label_arr = np.asarray(labels, dtype=bool)
    if score_arr.shape[0] != label_arr.shape[0]:
        raise ValueError("scores and labels must have the same length")
    n_pos = int(label_arr.sum())
    n_neg = int((~label_arr).sum())
    if n_pos == 0 or n_neg == 0:
        raise ValueError("roc_auc requires at least one positive and one negative")

    order = np.argsort(score_arr)
    sorted_scores = score_arr[order]
    ranks = np.empty_like(sorted_scores, dtype=float)
    start = 0
    while start < sorted_scores.size:
        end = start + 1
        while end < sorted_scores.size and sorted_scores[end] == sorted_scores[start]:
            end += 1
        avg_rank = (start + 1 + end) / 2.0
        ranks[start:end] = avg_rank
        start = end

    original_ranks = np.empty_like(ranks)
    original_ranks[order] = ranks
    pos_rank_sum = float(original_ranks[label_arr].sum())
    return (pos_rank_sum - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def average_precision(scores: Sequence[float], labels: Sequence[bool]) -> float:
    score_arr = np.asarray(scores, dtype=float)
    label_arr = np.asarray(labels, dtype=bool)
    if score_arr.shape[0] != label_arr.shape[0]:
        raise ValueError("scores and labels must have the same length")
    n_pos = int(label_arr.sum())
    if n_pos == 0:
        raise ValueError("average_precision requires at least one positive")

    order = np.argsort(-score_arr)
    sorted_labels = label_arr[order]
    precisions = []
    true_positives = 0
    for rank, is_positive in enumerate(sorted_labels, start=1):
        if is_positive:
            true_positives += 1
            precisions.append(true_positives / rank)
    return float(np.mean(precisions))
