#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any, Callable, Sequence

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from csrm_rag import (
    corm_max_score,
    corm_mean_score,
    csrm_score,
    naive_orbit_sufficiency,
    single_set_sufficiency,
)
from experiments.evaluate_orbits import load_orbits
from experiments.train_calibrated_csrm import (
    _feature_matrix,
    _labels,
    group_split,
)


DEFAULT_METHODS = [
    "corm_max_clean",
    "single_set_sure_style",
    "naive_orbit_average",
    "csrm_fixed_weights",
    "csrm_logreg_calibrated",
]


def run_risk_control_seeds(
    input_path: Path,
    seeds: Sequence[int],
    *,
    train_frac: float,
    cal_frac: float,
    risk_target: float,
    alpha: float,
    min_accepts: int,
    methods: Sequence[str] = DEFAULT_METHODS,
) -> dict[str, Any]:
    if not seeds:
        raise ValueError("at least one seed is required")
    if not 0.0 < risk_target < 1.0:
        raise ValueError("risk_target must be in (0, 1)")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0, 1)")
    if min_accepts < 1:
        raise ValueError("min_accepts must be positive")

    orbits = load_orbits(input_path)
    per_seed = []
    for seed in seeds:
        split = group_split(orbits, train_frac=train_frac, cal_frac=cal_frac, seed=seed)
        train = split["train"]
        calibration = split["calibration"]
        test = split["test"]

        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=2000, class_weight="balanced", random_state=seed),
        )
        model.fit(_feature_matrix(train), _labels(train))

        scorer_map = _scorers(model)
        seed_item: dict[str, Any] = {
            "seed": seed,
            "split_sizes": {
                "train": len(train),
                "calibration": len(calibration),
                "test": len(test),
                "train_groups": len(split["groups"]["train"]),
                "calibration_groups": len(split["groups"]["calibration"]),
                "test_groups": len(split["groups"]["test"]),
            },
            "methods": {},
        }
        for method in methods:
            scorer = scorer_map[method]
            cal_scores = scorer(calibration)
            cal_labels = _labels(calibration)
            test_scores = scorer(test)
            test_labels = _labels(test)
            selection = select_threshold_with_cp_bound(
                cal_scores,
                cal_labels,
                risk_target=risk_target,
                alpha=alpha,
                min_accepts=min_accepts,
            )
            seed_item["methods"][method] = {
                "calibration_selection": selection,
                "test": evaluate_threshold(
                    test_scores,
                    test_labels,
                    selection["threshold"],
                    risk_target=risk_target,
                ),
            }
        per_seed.append(seed_item)

    return {
        "input": str(input_path),
        "n_seeds": len(seeds),
        "seeds": list(seeds),
        "train_frac": train_frac,
        "cal_frac": cal_frac,
        "risk_target": risk_target,
        "alpha": alpha,
        "confidence": 1.0 - alpha,
        "min_accepts": min_accepts,
        "methods": list(methods),
        "per_seed": per_seed,
        "aggregate": _aggregate(per_seed, methods, risk_target),
        "interpretation": (
            "Thresholds are selected by a one-sided Clopper-Pearson upper bound "
            "on calibration-set selective risk. Test-set target hits are empirical "
            "transfer checks, not a distribution-free guarantee under dataset shift."
        ),
    }


def select_threshold_with_cp_bound(
    scores: Sequence[float],
    labels: Sequence[bool],
    *,
    risk_target: float,
    alpha: float,
    min_accepts: int,
) -> dict[str, Any]:
    if len(scores) != len(labels):
        raise ValueError("scores and labels must have the same length")
    if not scores:
        raise ValueError("cannot select a threshold on empty scores")

    pairs = sorted(zip(scores, labels), key=lambda item: item[0], reverse=True)
    best: dict[str, Any] | None = None
    accepted = 0
    errors = 0
    idx = 0
    while idx < len(pairs):
        threshold = pairs[idx][0]
        while idx < len(pairs) and pairs[idx][0] == threshold:
            accepted += 1
            errors += int(not pairs[idx][1])
            idx += 1
        empirical_risk = errors / accepted
        upper_bound = clopper_pearson_upper_bound(errors, accepted, alpha)
        if accepted >= min_accepts and upper_bound <= risk_target:
            best = _selection_summary(
                threshold=float(threshold),
                accepted=accepted,
                total=len(pairs),
                errors=errors,
                empirical_risk=empirical_risk,
                cp_upper_bound=upper_bound,
                risk_target=risk_target,
            )

    if best is not None:
        return best

    return {
        "threshold": None,
        "accepted": 0,
        "total": len(pairs),
        "coverage": 0.0,
        "errors": 0,
        "empirical_risk": None,
        "cp_upper_bound": None,
        "risk_target": risk_target,
        "cp_feasible": False,
    }


def evaluate_threshold(
    scores: Sequence[float],
    labels: Sequence[bool],
    threshold: float | None,
    *,
    risk_target: float,
) -> dict[str, Any]:
    if len(scores) != len(labels):
        raise ValueError("scores and labels must have the same length")
    if threshold is None:
        return {
            "threshold": None,
            "accepted": 0,
            "total": len(labels),
            "coverage": 0.0,
            "errors": 0,
            "empirical_risk": None,
            "accuracy": None,
            "target_met": False,
        }

    accepted_labels = [label for score, label in zip(scores, labels) if score >= threshold]
    accepted = len(accepted_labels)
    errors = sum(not label for label in accepted_labels)
    empirical_risk = errors / accepted if accepted else None
    accuracy = 1.0 - empirical_risk if empirical_risk is not None else None
    return {
        "threshold": float(threshold),
        "accepted": accepted,
        "total": len(labels),
        "coverage": accepted / len(labels) if labels else 0.0,
        "errors": errors,
        "empirical_risk": empirical_risk,
        "accuracy": accuracy,
        "target_met": bool(accepted and empirical_risk is not None and empirical_risk <= risk_target),
    }


def clopper_pearson_upper_bound(errors: int, n: int, alpha: float) -> float:
    if n < 0 or errors < 0 or errors > n:
        raise ValueError("expected 0 <= errors <= n")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0, 1)")
    if n == 0 or errors == n:
        return 1.0
    if errors == 0:
        return 1.0 - alpha ** (1.0 / n)

    lo = errors / n
    hi = 1.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        cdf = _binomial_cdf(errors, n, mid)
        if cdf > alpha:
            lo = mid
        else:
            hi = mid
    return hi


def _binomial_cdf(k: int, n: int, p: float) -> float:
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 1.0 if k >= n else 0.0
    log_p = math.log(p)
    log_q = math.log1p(-p)
    terms = [
        math.lgamma(n + 1)
        - math.lgamma(i + 1)
        - math.lgamma(n - i + 1)
        + i * log_p
        + (n - i) * log_q
        for i in range(k + 1)
    ]
    max_log = max(terms)
    return math.exp(max_log) * sum(math.exp(term - max_log) for term in terms)


def _scorers(model: Any) -> dict[str, Callable[[Sequence[Any]], list[float]]]:
    return {
        "corm_max_clean": lambda xs: [corm_max_score(x.clean) for x in xs],
        "corm_mean_clean": lambda xs: [corm_mean_score(x.clean) for x in xs],
        "single_set_sure_style": lambda xs: [single_set_sufficiency(x.clean) for x in xs],
        "naive_orbit_average": lambda xs: [naive_orbit_sufficiency(x) for x in xs],
        "csrm_fixed_weights": lambda xs: [csrm_score(x) for x in xs],
        "csrm_logreg_calibrated": lambda xs: model.predict_proba(_feature_matrix(xs))[:, 1].tolist(),
    }


def _selection_summary(
    *,
    threshold: float,
    accepted: int,
    total: int,
    errors: int,
    empirical_risk: float,
    cp_upper_bound: float,
    risk_target: float,
) -> dict[str, Any]:
    return {
        "threshold": threshold,
        "accepted": accepted,
        "total": total,
        "coverage": accepted / total,
        "errors": errors,
        "empirical_risk": empirical_risk,
        "cp_upper_bound": cp_upper_bound,
        "risk_target": risk_target,
        "cp_feasible": True,
    }


def _aggregate(
    per_seed: Sequence[dict[str, Any]],
    methods: Sequence[str],
    risk_target: float,
) -> dict[str, Any]:
    aggregate = {}
    for method in methods:
        rows = [item["methods"][method] for item in per_seed]
        target_met = [bool(row["test"]["target_met"]) for row in rows]
        nonzero_coverage = [row["test"]["coverage"] > 0.0 for row in rows]
        cp_feasible = [bool(row["calibration_selection"]["cp_feasible"]) for row in rows]
        aggregate[method] = {
            "calibration_coverage": _numeric_summary(
                [row["calibration_selection"]["coverage"] for row in rows]
            ),
            "calibration_cp_upper_bound": _numeric_summary(
                [
                    row["calibration_selection"]["cp_upper_bound"]
                    for row in rows
                    if row["calibration_selection"]["cp_upper_bound"] is not None
                ]
            ),
            "test_coverage": _numeric_summary([row["test"]["coverage"] for row in rows]),
            "test_empirical_risk": _numeric_summary(
                [
                    row["test"]["empirical_risk"]
                    for row in rows
                    if row["test"]["empirical_risk"] is not None
                ]
            ),
            "cp_feasible_count": sum(cp_feasible),
            "nonzero_coverage_count": sum(nonzero_coverage),
            "target_met_count": sum(target_met),
            "target_met_rate": sum(target_met) / len(target_met),
            "target_miss_count": len(target_met) - sum(target_met),
            "empirical_transfer_supported": all(target_met) and all(nonzero_coverage),
            "formal_risk_guarantee_supported": False,
            "risk_target": risk_target,
        }
    return aggregate


def _numeric_summary(nums: Sequence[float]) -> dict[str, float | None]:
    clean = [float(num) for num in nums if num is not None and np.isfinite(num)]
    if not clean:
        return {"mean": None, "stdev": None, "min": None, "max": None}
    return {
        "mean": statistics.fmean(clean),
        "stdev": statistics.stdev(clean) if len(clean) > 1 else 0.0,
        "min": min(clean),
        "max": max(clean),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[17, 31, 47])
    parser.add_argument("--train-frac", type=float, default=0.60)
    parser.add_argument("--cal-frac", type=float, default=0.20)
    parser.add_argument("--risk-target", type=float, default=0.20)
    parser.add_argument("--alpha", type=float, default=0.10)
    parser.add_argument("--min-accepts", type=int, default=5)
    parser.add_argument("--methods", nargs="+", default=DEFAULT_METHODS)
    args = parser.parse_args()

    result = run_risk_control_seeds(
        args.input,
        args.seeds,
        train_frac=args.train_frac,
        cal_frac=args.cal_frac,
        risk_target=args.risk_target,
        alpha=args.alpha,
        min_accepts=args.min_accepts,
        methods=args.methods,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
