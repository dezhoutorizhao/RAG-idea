#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Callable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import (
    QueryOrbit,
    area_under_risk_coverage,
    corm_max_score,
    corm_mean_score,
    csrm_score,
    naive_orbit_sufficiency,
    risk_coverage_curve,
    roc_auc,
    selective_risk_at_coverage,
    single_set_sufficiency,
)
from experiments.evaluate_orbits import load_orbits


Scorer = Callable[[QueryOrbit], float]


METHODS: dict[str, Scorer] = {
    "corm_max_clean": lambda orbit: corm_max_score(orbit.clean),
    "corm_mean_clean": lambda orbit: corm_mean_score(orbit.clean),
    "single_set_sure_style": lambda orbit: single_set_sufficiency(orbit.clean),
    "naive_orbit_average": naive_orbit_sufficiency,
    "csrm": csrm_score,
}


def compare_methods(
    input_path: Path,
    target: str,
    baselines: Sequence[str],
    bootstrap_samples: int,
    bootstrap_seed: int,
) -> dict:
    orbits = [orbit for orbit in load_orbits(input_path) if orbit.clean.label_answerable is not None]
    if not orbits:
        raise ValueError("no labeled orbits found")
    labels = [orbit.label_answerable for orbit in orbits]
    target_scores = _scores(orbits, target)

    comparisons = {}
    for baseline in baselines:
        baseline_scores = _scores(orbits, baseline)
        comparisons[baseline] = _comparison(
            target_scores,
            baseline_scores,
            labels,
            bootstrap_samples=bootstrap_samples,
            bootstrap_seed=bootstrap_seed,
        )
    return {
        "input": str(input_path),
        "target": target,
        "baselines": list(baselines),
        "n": len(orbits),
        "positive": int(sum(labels)),
        "negative": int(len(labels) - sum(labels)),
        "comparisons": comparisons,
    }


def _scores(orbits: Sequence[QueryOrbit], method: str) -> list[float]:
    if method not in METHODS:
        raise ValueError(f"unknown method: {method}")
    scorer = METHODS[method]
    return [scorer(orbit) for orbit in orbits]


def _comparison(
    target_scores: Sequence[float],
    baseline_scores: Sequence[float],
    labels: Sequence[bool],
    bootstrap_samples: int,
    bootstrap_seed: int,
) -> dict:
    point = _delta_metrics(target_scores, baseline_scores, labels)
    boot = _bootstrap_deltas(
        target_scores,
        baseline_scores,
        labels,
        samples=bootstrap_samples,
        seed=bootstrap_seed,
    )
    return {
        "point": point,
        "bootstrap_ci": {
            key: _percentile_ci([item[key] for item in boot if item[key] is not None])
            for key in [
                "auroc_improvement",
                "risk_at_30_reduction",
                "risk_at_50_reduction",
                "aurc_reduction",
            ]
        },
        "bootstrap_samples": bootstrap_samples,
        "bootstrap_seed": bootstrap_seed,
    }


def _delta_metrics(
    target_scores: Sequence[float],
    baseline_scores: Sequence[float],
    labels: Sequence[bool],
) -> dict:
    target = _method_metrics(target_scores, labels)
    baseline = _method_metrics(baseline_scores, labels)
    return {
        "target": target,
        "baseline": baseline,
        "auroc_improvement": _safe_delta(target["auroc"], baseline["auroc"]),
        "risk_at_30_reduction": baseline["risk_at_30"] - target["risk_at_30"],
        "risk_at_50_reduction": baseline["risk_at_50"] - target["risk_at_50"],
        "aurc_reduction": baseline["aurc"] - target["aurc"],
    }


def _method_metrics(scores: Sequence[float], labels: Sequence[bool]) -> dict:
    return {
        "auroc": _safe_roc_auc(scores, labels),
        "risk_at_30": selective_risk_at_coverage(scores, labels, 0.30)["risk"],
        "risk_at_50": selective_risk_at_coverage(scores, labels, 0.50)["risk"],
        "aurc": area_under_risk_coverage(risk_coverage_curve(scores, labels)),
    }


def _bootstrap_deltas(
    target_scores: Sequence[float],
    baseline_scores: Sequence[float],
    labels: Sequence[bool],
    samples: int,
    seed: int,
) -> list[dict]:
    rng = random.Random(seed)
    n = len(labels)
    output = []
    for _ in range(samples):
        idx = [rng.randrange(n) for _ in range(n)]
        output.append(
            _delta_metrics(
                [target_scores[i] for i in idx],
                [baseline_scores[i] for i in idx],
                [labels[i] for i in idx],
            )
        )
    return output


def _safe_roc_auc(scores: Sequence[float], labels: Sequence[bool]) -> float | None:
    try:
        return roc_auc(scores, labels)
    except ValueError:
        return None


def _safe_delta(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    return left - right


def _percentile_ci(values: Sequence[float]) -> dict | None:
    if not values:
        return None
    ordered = sorted(values)
    return {
        "p2_5": ordered[int(0.025 * (len(ordered) - 1))],
        "median": ordered[int(0.500 * (len(ordered) - 1))],
        "p97_5": ordered[int(0.975 * (len(ordered) - 1))],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target", default="csrm")
    parser.add_argument(
        "--baselines",
        nargs="+",
        default=["corm_max_clean", "single_set_sure_style", "naive_orbit_average"],
    )
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--bootstrap-seed", type=int, default=71)
    args = parser.parse_args()

    result = compare_methods(
        input_path=args.input,
        target=args.target,
        baselines=args.baselines,
        bootstrap_samples=args.bootstrap_samples,
        bootstrap_seed=args.bootstrap_seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
