#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import area_under_risk_coverage, calibration_error, risk_coverage_curve, roc_auc, selective_risk_at_coverage
from csrm_rag.calibration import OrbitRiskCalibrator, csrm_v4_feature_names, split_groups
from csrm_rag.calibration.orbit_risk_model import csrm_minimax_scores, csrm_rule_scores
from csrm_rag.feature_firewall import assert_no_forbidden_features
from experiments.evaluate_orbits import load_orbits


def train_csrm_calibrated_v4(
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_path: Path,
    *,
    seeds: Sequence[int],
    train_frac: float = 0.60,
    cal_frac: float = 0.20,
    risk_target: float = 0.20,
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
        _run_seed(orbits, labels, groups, seed, train_frac, cal_frac, risk_target)
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
        "risk_target": risk_target,
        "feature_names": csrm_v4_feature_names(),
        "per_seed": per_seed,
        "aggregate": _aggregate(per_seed, risk_target),
        "claim_guardrails": [
            "Thresholds are selected on calibration split only.",
            "Splits are by source_item_group_id.",
            "This is an empirical calibrated selective-risk estimator, not a formal guarantee.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


def _run_seed(orbits, labels, groups, seed, train_frac, cal_frac, risk_target) -> dict[str, Any]:
    split = split_groups(groups, labels, train_frac=train_frac, cal_frac=cal_frac, seed=seed)
    train_orbits = [orbits[index] for index in split.train]
    cal_orbits = [orbits[index] for index in split.calibration]
    test_orbits = [orbits[index] for index in split.test]
    train_labels = [labels[index] for index in split.train]
    cal_labels = [labels[index] for index in split.calibration]
    test_labels = [labels[index] for index in split.test]

    calibrator = OrbitRiskCalibrator(random_state=seed).fit(
        train_orbits,
        train_labels,
        calibration_orbits=cal_orbits,
        calibration_labels=cal_labels,
    )
    methods = {
        "csrm_rule": (csrm_rule_scores(cal_orbits), csrm_rule_scores(test_orbits)),
        "csrm_minimax": (csrm_minimax_scores(cal_orbits), csrm_minimax_scores(test_orbits)),
        "csrm_calibrated_logistic": (
            calibrator.predict_logistic(cal_orbits),
            calibrator.predict_logistic(test_orbits),
        ),
        "csrm_calibrated_isotonic": (
            calibrator.predict_isotonic(cal_orbits),
            calibrator.predict_isotonic(test_orbits),
        ),
    }
    method_results = {}
    for name, (cal_scores, test_scores) in methods.items():
        threshold = _threshold_for_risk(cal_scores, cal_labels, risk_target)
        method_results[name] = {
            "calibration": _score_summary(cal_scores, cal_labels, threshold),
            "test": _score_summary(test_scores, test_labels, threshold),
        }
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
        "methods": method_results,
        "logistic_coefficients": calibrator.coefficients(),
    }


def _score_summary(scores: Sequence[float], labels: Sequence[bool], threshold: float) -> dict[str, Any]:
    accepted = [score >= threshold for score in scores]
    accepted_count = sum(accepted)
    accepted_labels = [label for label, flag in zip(labels, accepted) if flag]
    accepted_accuracy = sum(accepted_labels) / accepted_count if accepted_count else 0.0
    brier = float(np.mean([(float(score) - float(label)) ** 2 for score, label in zip(scores, labels)]))
    return {
        "n": len(labels),
        "positive": int(sum(labels)),
        "negative": int(len(labels) - sum(labels)),
        "auroc": _safe_auc(scores, labels),
        "aurc": area_under_risk_coverage(risk_coverage_curve(scores, labels)),
        "brier": brier,
        "calibration": calibration_error(scores, labels),
        "risk_at_30": selective_risk_at_coverage(scores, labels, 0.30)["risk"],
        "risk_at_50": selective_risk_at_coverage(scores, labels, 0.50)["risk"],
        "risk_at_70": selective_risk_at_coverage(scores, labels, 0.70)["risk"],
        "selected_threshold": threshold,
        "selected_coverage": accepted_count / len(labels),
        "selected_risk": 1.0 - accepted_accuracy if accepted_count else 0.0,
        "selected_accuracy": accepted_accuracy,
    }


def _threshold_for_risk(scores: Sequence[float], labels: Sequence[bool], risk_target: float) -> float:
    unique_scores = sorted({float(score) for score in scores}, reverse=True)
    best_threshold = 1.0 + max(float(score) for score in scores)
    best_coverage = -1.0
    for threshold in unique_scores:
        accepted = [float(score) >= threshold for score in scores]
        accepted_count = sum(accepted)
        if not accepted_count:
            continue
        accepted_labels = [label for label, flag in zip(labels, accepted) if flag]
        risk = 1.0 - (sum(accepted_labels) / accepted_count)
        coverage = accepted_count / len(labels)
        if risk <= risk_target and coverage > best_coverage:
            best_threshold = threshold
            best_coverage = coverage
    return best_threshold


def _aggregate(per_seed: Sequence[dict[str, Any]], risk_target: float) -> dict[str, Any]:
    methods = sorted(per_seed[0]["methods"])
    aggregate = {}
    for method in methods:
        rows = [item["methods"][method]["test"] for item in per_seed]
        aggregate[method] = {
            metric: _numeric_summary([row[metric] for row in rows if row[metric] is not None])
            for metric in [
                "auroc",
                "aurc",
                "brier",
                "risk_at_30",
                "risk_at_50",
                "selected_coverage",
                "selected_risk",
            ]
        }
        target_met = [row["selected_risk"] <= risk_target for row in rows]
        nonzero = [row["selected_coverage"] > 0.0 for row in rows]
        aggregate[method]["target_met_count"] = sum(target_met)
        aggregate[method]["target_met_rate"] = sum(target_met) / len(target_met)
        aggregate[method]["zero_coverage_count"] = len(nonzero) - sum(nonzero)
    return aggregate


def _numeric_summary(values: Sequence[float]) -> dict[str, float | None]:
    if not values:
        return {"mean": None, "min": None, "max": None}
    return {"mean": float(np.mean(values)), "min": min(values), "max": max(values)}


def _safe_auc(scores: Sequence[float], labels: Sequence[bool]) -> float | None:
    try:
        return roc_auc(scores, labels)
    except ValueError:
        return None


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
    parser.add_argument("--risk-target", type=float, default=0.20)
    args = parser.parse_args()

    result = train_csrm_calibrated_v4(
        args.raw,
        args.private,
        args.scored,
        args.output,
        seeds=args.seeds,
        train_frac=args.train_frac,
        cal_frac=args.cal_frac,
        risk_target=args.risk_target,
    )
    compact = {
        "output": str(args.output),
        "n": result["n"],
        "seeds": result["seeds"],
        "aggregate": result["aggregate"],
    }
    print(json.dumps(compact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
