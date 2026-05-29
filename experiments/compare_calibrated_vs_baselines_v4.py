#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import area_under_risk_coverage, risk_coverage_curve, roc_auc, selective_risk_at_coverage
from csrm_rag import corm_mean_score
from csrm_rag.baselines.v4_baselines import (
    ENSEMBLE_FEATURE_METHODS,
    _answer_consistency,
    _context_features,
    _equal_budget_min,
    _equal_budget_quantile,
    _faithful_sure_multi,
    _orbit_features,
    _retrieval_stability,
    _template_self_consistency,
)
from csrm_rag.calibration import OrbitRiskCalibrator, split_groups
from csrm_rag.calibration.orbit_risk_model import csrm_minimax_scores, csrm_rule_scores
from csrm_rag.feature_firewall import assert_no_forbidden_features
from experiments.evaluate_orbits import load_orbits


def compare_calibrated_vs_baselines_v4(
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_path: Path,
    *,
    seeds: Sequence[int],
    train_frac: float = 0.60,
    cal_frac: float = 0.20,
    bootstrap_samples: int = 500,
    bootstrap_seed: int = 101,
) -> dict[str, Any]:
    raw_rows = _read_jsonl(raw_path)
    private_rows = _read_jsonl(private_path)
    orbits = load_orbits(scored_path)
    if not (len(raw_rows) == len(private_rows) == len(orbits)):
        raise ValueError("raw, private, and scored files must have the same number of rows")
    for index, (raw, private, orbit) in enumerate(zip(raw_rows, private_rows, orbits)):
        assert_no_forbidden_features(raw)
        if raw["orbit_id"] != private["orbit_id"] or raw["orbit_id"] != orbit.orbit_id:
            raise ValueError(f"row {index} has misaligned orbit_id values")

    labels = [bool(row["label_answerable"]) for row in private_rows]
    groups = [str(row.get("source_item_group_id") or row["orbit_id"]) for row in raw_rows]
    per_seed = [
        _run_seed(
            orbits,
            labels,
            groups,
            seed=seed,
            train_frac=train_frac,
            cal_frac=cal_frac,
            bootstrap_samples=bootstrap_samples,
            bootstrap_seed=bootstrap_seed + seed,
        )
        for seed in seeds
    ]
    result = {
        "raw_input": str(raw_path),
        "private_input": str(private_path),
        "scored_input": str(scored_path),
        "n": len(orbits),
        "positive": int(sum(labels)),
        "negative": int(len(labels) - sum(labels)),
        "source_item_groups": len(set(groups)),
        "seeds": list(seeds),
        "train_frac": train_frac,
        "cal_frac": cal_frac,
        "bootstrap_samples": bootstrap_samples,
        "bootstrap_seed": bootstrap_seed,
        "per_seed": per_seed,
        "aggregate": _aggregate(per_seed),
        "interpretation": "Positive deltas mean the CSRM target outperforms the named non-CSRM baseline.",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


def _run_seed(
    orbits,
    labels,
    groups,
    *,
    seed: int,
    train_frac: float,
    cal_frac: float,
    bootstrap_samples: int,
    bootstrap_seed: int,
) -> dict[str, Any]:
    split = split_groups(groups, labels, train_frac=train_frac, cal_frac=cal_frac, seed=seed)
    train_orbits = [orbits[index] for index in split.train]
    cal_orbits = [orbits[index] for index in split.calibration]
    test_orbits = [orbits[index] for index in split.test]
    train_labels = [labels[index] for index in split.train]
    cal_labels = [labels[index] for index in split.calibration]
    test_labels = [labels[index] for index in split.test]
    test_groups = [groups[index] for index in split.test]

    calibrator = OrbitRiskCalibrator(random_state=seed).fit(
        train_orbits,
        train_labels,
        calibration_orbits=cal_orbits,
        calibration_labels=cal_labels,
    )
    targets = {
        "csrm_rule": csrm_rule_scores(test_orbits),
        "csrm_minimax": csrm_minimax_scores(test_orbits),
        "csrm_calibrated_logistic": calibrator.predict_logistic(test_orbits),
        "csrm_calibrated_isotonic": calibrator.predict_isotonic(test_orbits),
    }
    baselines = _baseline_scores(train_orbits, train_labels, test_orbits)
    target_metrics = {name: _metrics(scores, test_labels) for name, scores in targets.items()}
    baseline_metrics = {name: _metrics(scores, test_labels) for name, scores in baselines.items()}
    comparisons = {}
    for target_name, target_scores in targets.items():
        comparisons[target_name] = {}
        for baseline_name, baseline_scores in baselines.items():
            comparisons[target_name][baseline_name] = _comparison(
                target_scores,
                baseline_scores,
                test_labels,
                test_groups,
                bootstrap_samples=bootstrap_samples,
                bootstrap_seed=bootstrap_seed,
            )
    return {
        "seed": seed,
        "split_sizes": {
            "train": len(split.train),
            "calibration": len(split.calibration),
            "test": len(split.test),
            "train_groups": len(split.train_groups),
            "calibration_groups": len(split.calibration_groups),
            "test_groups": len(split.test_groups),
        },
        "target_metrics": target_metrics,
        "baseline_metrics": baseline_metrics,
        "comparisons": comparisons,
    }


def _baseline_scores(train_orbits, train_labels, test_orbits) -> dict[str, list[float]]:
    train_base = _nonlearned_baseline_scores(train_orbits)
    test_base = _nonlearned_baseline_scores(test_orbits)
    baselines = dict(test_base)
    baselines["equal_budget_ensemble_logistic"] = _fit_predict_logistic(
        _score_feature_matrix(train_base, ENSEMBLE_FEATURE_METHODS),
        train_labels,
        _score_feature_matrix(test_base, ENSEMBLE_FEATURE_METHODS),
    )
    baselines["calibrated_logistic_context"] = _fit_predict_logistic(
        [_context_features(orbit) for orbit in train_orbits],
        train_labels,
        [_context_features(orbit) for orbit in test_orbits],
    )
    baselines["calibrated_logistic_orbit"] = _fit_predict_logistic(
        [_orbit_features(orbit) for orbit in train_orbits],
        train_labels,
        [_orbit_features(orbit) for orbit in test_orbits],
    )
    return baselines


def _nonlearned_baseline_scores(orbits) -> dict[str, list[float]]:
    return {
        "corm_max_clean": [max([doc.corm_score for doc in orbit.clean.docs] or [0.0]) for orbit in orbits],
        "corm_mean_clean": [corm_mean_score(orbit.clean) for orbit in orbits],
        "faithful_sure_multi": [_faithful_sure_multi(orbit) for orbit in orbits],
        "context_sufficiency_clean": [
            _safe_context_sufficiency(orbit) for orbit in orbits
        ],
        "equal_budget_mean": [_equal_budget_mean(orbit) for orbit in orbits],
        "equal_budget_min": [_equal_budget_min(orbit) for orbit in orbits],
        "equal_budget_q25": [_equal_budget_quantile(orbit, 0.25) for orbit in orbits],
        "retrieval_stability": [_retrieval_stability(orbit) for orbit in orbits],
        "self_consistency_proxy": [_answer_consistency(orbit) for orbit in orbits],
        "template_self_consistency": [_template_self_consistency(orbit) for orbit in orbits],
    }


def _score_feature_matrix(scores: dict[str, Sequence[float]], methods: Sequence[str]) -> list[list[float]]:
    if not methods:
        return []
    row_count = len(scores[methods[0]])
    return [[float(scores[method][index]) for method in methods] for index in range(row_count)]


def _fit_predict_logistic(features_train, train_labels, features_test) -> list[float]:
    y = np.asarray(train_labels, dtype=bool)
    if not len(features_test):
        return []
    if len(set(y.tolist())) < 2:
        return [float(y.mean()) if y.size else 0.5] * len(features_test)
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, class_weight="balanced", random_state=0),
    )
    model.fit(np.asarray(features_train, dtype=float), y)
    return model.predict_proba(np.asarray(features_test, dtype=float))[:, 1].tolist()


def _safe_context_sufficiency(orbit) -> float:
    from csrm_rag import single_set_sufficiency

    return single_set_sufficiency(orbit.clean)


def _equal_budget_mean(orbit) -> float:
    from csrm_rag import naive_orbit_sufficiency

    return naive_orbit_sufficiency(orbit)


def _comparison(
    target_scores,
    baseline_scores,
    labels,
    groups,
    *,
    bootstrap_samples: int,
    bootstrap_seed: int,
) -> dict[str, Any]:
    point = _delta(target_scores, baseline_scores, labels)
    boot = _cluster_bootstrap_deltas(
        target_scores,
        baseline_scores,
        labels,
        groups,
        samples=bootstrap_samples,
        seed=bootstrap_seed,
    )
    return {
        "point": point,
        "cluster_bootstrap_ci": {
            key: _percentile_ci([row[key] for row in boot if row[key] is not None])
            for key in ["auroc_improvement", "risk_at_30_reduction", "risk_at_50_reduction", "aurc_reduction"]
        },
        "bootstrap_samples": bootstrap_samples,
        "bootstrap_seed": bootstrap_seed,
    }


def _cluster_bootstrap_deltas(target_scores, baseline_scores, labels, groups, *, samples: int, seed: int):
    rng = random.Random(seed)
    group_to_indices: dict[str, list[int]] = {}
    for index, group in enumerate(groups):
        group_to_indices.setdefault(str(group), []).append(index)
    group_ids = sorted(group_to_indices)
    output = []
    for _ in range(samples):
        sampled_groups = [rng.choice(group_ids) for _ in group_ids]
        indices = [index for group in sampled_groups for index in group_to_indices[group]]
        output.append(
            _delta(
                [target_scores[index] for index in indices],
                [baseline_scores[index] for index in indices],
                [labels[index] for index in indices],
            )
        )
    return output


def _delta(target_scores, baseline_scores, labels) -> dict[str, float | None]:
    target = _metrics(target_scores, labels)
    baseline = _metrics(baseline_scores, labels)
    return {
        "target": target,
        "baseline": baseline,
        "auroc_improvement": _maybe_delta(target["auroc"], baseline["auroc"]),
        "risk_at_30_reduction": baseline["risk_at_30"] - target["risk_at_30"],
        "risk_at_50_reduction": baseline["risk_at_50"] - target["risk_at_50"],
        "aurc_reduction": baseline["aurc"] - target["aurc"],
    }


def _metrics(scores, labels) -> dict[str, float | None]:
    return {
        "auroc": _safe_auc(scores, labels),
        "risk_at_30": selective_risk_at_coverage(scores, labels, 0.30)["risk"],
        "risk_at_50": selective_risk_at_coverage(scores, labels, 0.50)["risk"],
        "aurc": area_under_risk_coverage(risk_coverage_curve(scores, labels)),
    }


def _safe_auc(scores, labels) -> float | None:
    try:
        return roc_auc(scores, labels)
    except ValueError:
        return None


def _maybe_delta(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    return left - right


def _percentile_ci(values: Sequence[float]) -> dict[str, float] | None:
    if not values:
        return None
    ordered = sorted(values)
    return {
        "p2_5": ordered[int(0.025 * (len(ordered) - 1))],
        "median": ordered[int(0.500 * (len(ordered) - 1))],
        "p97_5": ordered[int(0.975 * (len(ordered) - 1))],
    }


def _aggregate(per_seed: Sequence[dict[str, Any]]) -> dict[str, Any]:
    target_names = sorted(per_seed[0]["comparisons"])
    baseline_names = sorted(next(iter(per_seed[0]["comparisons"].values())))
    output = {}
    for target in target_names:
        output[target] = {}
        for baseline in baseline_names:
            rows = [seed_item["comparisons"][target][baseline]["point"] for seed_item in per_seed]
            output[target][baseline] = {
                key: _numeric_summary([row[key] for row in rows if row[key] is not None])
                for key in ["auroc_improvement", "risk_at_30_reduction", "risk_at_50_reduction", "aurc_reduction"]
            }
            ci_rows = [seed_item["comparisons"][target][baseline]["cluster_bootstrap_ci"] for seed_item in per_seed]
            output[target][baseline]["seed_ci_lower_bounds"] = {
                key: [ci[key]["p2_5"] for ci in ci_rows if ci[key] is not None]
                for key in ["auroc_improvement", "risk_at_30_reduction", "risk_at_50_reduction", "aurc_reduction"]
            }
    return output


def _numeric_summary(values: Sequence[float]) -> dict[str, float | None]:
    if not values:
        return {"mean": None, "min": None, "max": None}
    return {"mean": float(np.mean(values)), "min": min(values), "max": max(values)}


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--scored", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[17, 31, 47])
    parser.add_argument("--train-frac", type=float, default=0.60)
    parser.add_argument("--cal-frac", type=float, default=0.20)
    parser.add_argument("--bootstrap-samples", type=int, default=500)
    parser.add_argument("--bootstrap-seed", type=int, default=101)
    args = parser.parse_args()

    result = compare_calibrated_vs_baselines_v4(
        args.raw,
        args.private,
        args.scored,
        args.output,
        seeds=args.seeds,
        train_frac=args.train_frac,
        cal_frac=args.cal_frac,
        bootstrap_samples=args.bootstrap_samples,
        bootstrap_seed=args.bootstrap_seed,
    )
    compact = {
        "output": str(args.output),
        "n": result["n"],
        "seeds": result["seeds"],
        "aggregate_keys": sorted(result["aggregate"]),
    }
    print(json.dumps(compact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
