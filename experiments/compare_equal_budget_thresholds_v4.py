#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag.baselines.v4_baselines import (
    ENSEMBLE_FEATURE_METHODS,
    _context_features,
    _orbit_features,
)
from csrm_rag.calibration import OrbitRiskCalibrator, split_groups
from csrm_rag.calibration.orbit_risk_model import csrm_minimax_scores, csrm_rule_scores
from csrm_rag.feature_firewall import assert_no_forbidden_features
from experiments.compare_calibrated_vs_baselines_v4 import (
    _fit_predict_logistic,
    _metrics,
    _nonlearned_baseline_scores,
    _score_feature_matrix,
    _read_jsonl,
)
from experiments.evaluate_orbits import load_orbits


TARGET_METHODS = [
    "csrm_rule",
    "csrm_minimax",
    "csrm_calibrated_logistic",
    "csrm_calibrated_isotonic",
]


@dataclass(frozen=True)
class DatasetConfig:
    name: str
    raw: Path
    private: Path
    scored: Path


DEFAULT_DATASETS = [
    DatasetConfig(
        name="fever_v4_n100_structbalanced",
        raw=Path("results/fever_orbits_v4_n100.constant.structbalanced.raw.jsonl"),
        private=Path("results/fever_orbits_v4_n100.constant.structbalanced.private_eval.jsonl"),
        scored=Path("results/fever_orbits_v4_n100.constant.structbalanced.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        name="hotpot_v4_hardneg_n100",
        raw=Path("results/hotpot_orbits_v4_hardneg_n100.constant.raw.jsonl"),
        private=Path("results/hotpot_orbits_v4_hardneg_n100.private_eval.jsonl"),
        scored=Path("results/hotpot_orbits_v4_hardneg_n100.constant.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        name="hotpot_v4_n100_hardmatched",
        raw=Path("results/hotpot_orbits_v4_n100.constant.hardmatched.raw.jsonl"),
        private=Path("results/hotpot_orbits_v4_n100.constant.hardmatched.private_eval.jsonl"),
        scored=Path("results/hotpot_orbits_v4_n100.constant.hardmatched.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        name="hotpot_v4_n100_structbalanced",
        raw=Path("results/hotpot_orbits_v4_n100.constant.structbalanced.raw.jsonl"),
        private=Path("results/hotpot_orbits_v4_n100.constant.structbalanced.private_eval.jsonl"),
        scored=Path("results/hotpot_orbits_v4_n100.constant.structbalanced.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        name="hotpot_v4_semanticswap_n100",
        raw=Path("results/hotpot_orbits_v4_semanticswap_n100.constant.raw.jsonl"),
        private=Path("results/hotpot_orbits_v4_semanticswap_n100.private_eval.jsonl"),
        scored=Path("results/hotpot_orbits_v4_semanticswap_n100.constant.textonly_scored.jsonl"),
    ),
    DatasetConfig(
        name="hotpot_v4_supportpreserve_n100",
        raw=Path("results/hotpot_orbits_v4_supportpreserve_n100.constant.raw.jsonl"),
        private=Path("results/hotpot_orbits_v4_supportpreserve_n100.private_eval.jsonl"),
        scored=Path("results/hotpot_orbits_v4_supportpreserve_n100.constant.textonly_scored.jsonl"),
    ),
]


def compare_equal_budget_thresholds_v4(
    datasets: Sequence[DatasetConfig],
    *,
    seeds: Sequence[int],
    risk_targets: Sequence[float],
    train_frac: float = 0.60,
    cal_frac: float = 0.20,
) -> dict[str, Any]:
    dataset_rows = [
        _run_dataset(
            dataset,
            seeds=seeds,
            risk_targets=risk_targets,
            train_frac=train_frac,
            cal_frac=cal_frac,
        )
        for dataset in datasets
    ]
    flat_rows = [
        threshold_row
        for dataset in dataset_rows
        for seed_row in dataset["per_seed"]
        for threshold_row in seed_row["threshold_rows"]
    ]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": {
            "same_source_item_group_split": True,
            "threshold_selected_on": "calibration split",
            "threshold_applied_to": "held-out test split",
            "selection_rule": "maximize calibration coverage subject to empirical calibration risk <= target",
            "score_direction": "higher score means more answerable / safer to accept",
        },
        "seeds": list(seeds),
        "risk_targets": [float(item) for item in risk_targets],
        "train_frac": train_frac,
        "cal_frac": cal_frac,
        "dataset_count": len(dataset_rows),
        "datasets": dataset_rows,
        "aggregate": _aggregate_threshold_rows(flat_rows, risk_targets),
        "shared_threshold_protocol_complete": bool(dataset_rows)
        and all(dataset["protocol_complete"] for dataset in dataset_rows),
        "claim_policy": (
            "This artifact closes the protocol-fairness requirement that all methods use the same "
            "source-group split and select thresholds only on the calibration split. Test risk can "
            "still miss the calibration target, so this is not a formal risk-control guarantee."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# V4 Shared Calibration-Threshold Selection",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Datasets: `{summary['dataset_count']}`",
        f"Seeds: `{summary['seeds']}`",
        f"Risk targets: `{summary['risk_targets']}`",
        f"Protocol complete: `{summary['shared_threshold_protocol_complete']}`",
        "",
        "## Protocol",
        "",
    ]
    for key, value in summary["protocol"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Target Coverage vs Strongest Baseline",
            "",
            "| Risk target | Target | Wins | Ties | Losses | Mean coverage delta | Mean test risk | Missed target rows |",
            "|---:|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for item in summary["aggregate"]["target_vs_strongest_baseline"]:
        lines.append(
            f"| {item['risk_target']:.2f} | {item['target']} | {item['wins']} | {item['ties']} | "
            f"{item['losses']} | {_fmt(item['mean_coverage_delta'])} | {_fmt(item['mean_test_risk'])} | "
            f"{item['missed_target_rows']} |"
        )
    lines.extend(
        [
            "",
            "## Method Summary",
            "",
            "| Risk target | Method | Mean cal coverage | Mean test coverage | Mean test risk | Test target pass rate | No-accept rows |",
            "|---:|---|---:|---:|---:|---:|---:|",
        ]
    )
    for item in summary["aggregate"]["method_summary"]:
        lines.append(
            f"| {item['risk_target']:.2f} | {item['method']} | {_fmt(item['mean_cal_coverage'])} | "
            f"{_fmt(item['mean_test_coverage'])} | {_fmt(item['mean_test_risk'])} | "
            f"{_fmt(item['test_target_pass_rate'])} | {item['no_accept_rows']} |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _run_dataset(
    dataset: DatasetConfig,
    *,
    seeds: Sequence[int],
    risk_targets: Sequence[float],
    train_frac: float,
    cal_frac: float,
) -> dict[str, Any]:
    raw_rows = _read_jsonl(dataset.raw)
    private_rows = _read_jsonl(dataset.private)
    orbits = load_orbits(dataset.scored)
    if not (len(raw_rows) == len(private_rows) == len(orbits)):
        raise ValueError(f"{dataset.name}: raw, private, and scored files must align")
    for index, (raw, private, orbit) in enumerate(zip(raw_rows, private_rows, orbits)):
        assert_no_forbidden_features(raw)
        if raw["orbit_id"] != private["orbit_id"] or raw["orbit_id"] != orbit.orbit_id:
            raise ValueError(f"{dataset.name}: row {index} has misaligned orbit_id values")

    labels = [bool(row["label_answerable"]) for row in private_rows]
    groups = [str(row.get("source_item_group_id") or row["orbit_id"]) for row in raw_rows]
    per_seed = [
        _run_seed(
            dataset.name,
            orbits,
            labels,
            groups,
            seed=seed,
            risk_targets=risk_targets,
            train_frac=train_frac,
            cal_frac=cal_frac,
        )
        for seed in seeds
    ]
    return {
        "dataset": dataset.name,
        "raw_input": str(dataset.raw),
        "private_input": str(dataset.private),
        "scored_input": str(dataset.scored),
        "n": len(orbits),
        "positive": int(sum(labels)),
        "negative": int(len(labels) - sum(labels)),
        "source_item_groups": len(set(groups)),
        "per_seed": per_seed,
        "protocol_complete": all(seed_row["protocol_complete"] for seed_row in per_seed),
    }


def _run_seed(
    dataset_name: str,
    orbits,
    labels: Sequence[bool],
    groups: Sequence[str],
    *,
    seed: int,
    risk_targets: Sequence[float],
    train_frac: float,
    cal_frac: float,
) -> dict[str, Any]:
    split = split_groups(groups, labels, train_frac=train_frac, cal_frac=cal_frac, seed=seed)
    train_orbits = [orbits[index] for index in split.train]
    cal_orbits = [orbits[index] for index in split.calibration]
    test_orbits = [orbits[index] for index in split.test]
    train_labels = [labels[index] for index in split.train]
    cal_labels = [labels[index] for index in split.calibration]
    test_labels = [labels[index] for index in split.test]
    scores = _method_scores(
        train_orbits,
        train_labels,
        cal_orbits,
        cal_labels,
        test_orbits,
        seed=seed,
    )
    threshold_rows = []
    for risk_target in risk_targets:
        for method, method_scores in sorted(scores.items()):
            threshold = _threshold_for_risk(method_scores["calibration"], cal_labels, risk_target)
            threshold_rows.append(
                {
                    "dataset": dataset_name,
                    "seed": seed,
                    "risk_target": float(risk_target),
                    "method": method,
                    "family": "target" if method in TARGET_METHODS else "baseline",
                    "threshold": threshold,
                    "calibration": _threshold_summary(method_scores["calibration"], cal_labels, threshold, risk_target),
                    "test": _threshold_summary(method_scores["test"], test_labels, threshold, risk_target),
                    "test_ranking_metrics": _metrics(method_scores["test"], test_labels),
                }
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
        "method_count": len(scores),
        "threshold_rows": threshold_rows,
        "protocol_complete": bool(scores) and all(row["calibration"]["selected_on_calibration"] for row in threshold_rows),
    }


def _method_scores(
    train_orbits,
    train_labels,
    cal_orbits,
    cal_labels,
    test_orbits,
    *,
    seed: int,
) -> dict[str, dict[str, list[float]]]:
    return _fit_calibrated_targets(
        train_orbits,
        train_labels,
        cal_orbits,
        cal_labels,
        test_orbits,
        seed=seed,
    ) | _fit_baselines(
        train_orbits,
        train_labels,
        cal_orbits,
        test_orbits,
    )


def _fit_calibrated_targets(
    train_orbits,
    train_labels,
    cal_orbits,
    cal_labels,
    test_orbits,
    *,
    seed: int,
) -> dict[str, dict[str, list[float]]]:
    calibrator = OrbitRiskCalibrator(random_state=seed).fit(
        train_orbits,
        train_labels,
        calibration_orbits=cal_orbits,
        calibration_labels=cal_labels,
    )
    return {
        "csrm_rule": {
            "calibration": csrm_rule_scores(cal_orbits),
            "test": csrm_rule_scores(test_orbits),
        },
        "csrm_minimax": {
            "calibration": csrm_minimax_scores(cal_orbits),
            "test": csrm_minimax_scores(test_orbits),
        },
        "csrm_calibrated_logistic": {
            "calibration": calibrator.predict_logistic(cal_orbits),
            "test": calibrator.predict_logistic(test_orbits),
        },
        "csrm_calibrated_isotonic": {
            "calibration": calibrator.predict_isotonic(cal_orbits),
            "test": calibrator.predict_isotonic(test_orbits),
        },
    }


def _fit_baselines(train_orbits, train_labels, cal_orbits, test_orbits) -> dict[str, dict[str, list[float]]]:
    train_base = _nonlearned_baseline_scores(train_orbits)
    cal_base = _nonlearned_baseline_scores(cal_orbits)
    test_base = _nonlearned_baseline_scores(test_orbits)
    output = {
        method: {"calibration": cal_scores, "test": test_base[method]}
        for method, cal_scores in cal_base.items()
    }
    output["equal_budget_ensemble_logistic"] = {
        "calibration": _fit_predict_logistic(
            _score_feature_matrix(train_base, ENSEMBLE_FEATURE_METHODS),
            train_labels,
            _score_feature_matrix(cal_base, ENSEMBLE_FEATURE_METHODS),
        ),
        "test": _fit_predict_logistic(
            _score_feature_matrix(train_base, ENSEMBLE_FEATURE_METHODS),
            train_labels,
            _score_feature_matrix(test_base, ENSEMBLE_FEATURE_METHODS),
        ),
    }
    output["calibrated_logistic_context"] = {
        "calibration": _fit_predict_logistic(
            [_context_features(orbit) for orbit in train_orbits],
            train_labels,
            [_context_features(orbit) for orbit in cal_orbits],
        ),
        "test": _fit_predict_logistic(
            [_context_features(orbit) for orbit in train_orbits],
            train_labels,
            [_context_features(orbit) for orbit in test_orbits],
        ),
    }
    output["calibrated_logistic_orbit"] = {
        "calibration": _fit_predict_logistic(
            [_orbit_features(orbit) for orbit in train_orbits],
            train_labels,
            [_orbit_features(orbit) for orbit in cal_orbits],
        ),
        "test": _fit_predict_logistic(
            [_orbit_features(orbit) for orbit in train_orbits],
            train_labels,
            [_orbit_features(orbit) for orbit in test_orbits],
        ),
    }
    return output


def _threshold_for_risk(scores: Sequence[float], labels: Sequence[bool], risk_target: float) -> float:
    if len(scores) != len(labels):
        raise ValueError("scores and labels must have the same length")
    if not scores:
        return 1.0
    thresholds = sorted({float(score) for score in scores}, reverse=True)
    best_threshold = max(scores) + 1e-9
    best_coverage = -1.0
    for threshold in thresholds:
        accepted = [float(score) >= threshold for score in scores]
        accepted_count = sum(accepted)
        if accepted_count == 0:
            continue
        error_count = sum(1 for keep, label in zip(accepted, labels) if keep and not label)
        risk = error_count / accepted_count
        coverage = accepted_count / len(scores)
        if risk <= risk_target and coverage > best_coverage:
            best_threshold = float(threshold)
            best_coverage = coverage
    return float(best_threshold)


def _threshold_summary(
    scores: Sequence[float],
    labels: Sequence[bool],
    threshold: float,
    risk_target: float,
) -> dict[str, Any]:
    accepted = [score >= threshold for score in scores]
    accepted_count = sum(accepted)
    error_count = sum(1 for keep, label in zip(accepted, labels) if keep and not label)
    risk = None if accepted_count == 0 else error_count / accepted_count
    return {
        "selected_on_calibration": True,
        "threshold": float(threshold),
        "accepted_count": int(accepted_count),
        "total_count": len(labels),
        "coverage": accepted_count / len(labels) if labels else 0.0,
        "error_count": int(error_count),
        "risk": risk,
        "risk_target": float(risk_target),
        "target_met": bool(risk is not None and risk <= risk_target),
        "no_accept": accepted_count == 0,
    }


def _aggregate_threshold_rows(rows: list[dict[str, Any]], risk_targets: Sequence[float]) -> dict[str, Any]:
    methods = sorted({row["method"] for row in rows})
    method_summary = [
        _method_summary(rows, method, float(risk_target))
        for risk_target in risk_targets
        for method in methods
    ]
    return {
        "method_summary": method_summary,
        "target_vs_strongest_baseline": [
            _target_vs_strongest_baseline(rows, target, float(risk_target))
            for risk_target in risk_targets
            for target in TARGET_METHODS
        ],
    }


def _method_summary(rows: list[dict[str, Any]], method: str, risk_target: float) -> dict[str, Any]:
    subset = [row for row in rows if row["method"] == method and row["risk_target"] == risk_target]
    test_risks = [row["test"]["risk"] for row in subset if row["test"]["risk"] is not None]
    return {
        "risk_target": risk_target,
        "method": method,
        "family": "target" if method in TARGET_METHODS else "baseline",
        "row_count": len(subset),
        "mean_cal_coverage": _mean(row["calibration"]["coverage"] for row in subset),
        "mean_test_coverage": _mean(row["test"]["coverage"] for row in subset),
        "mean_test_risk": _mean(test_risks),
        "test_target_pass_rate": _mean(1.0 if row["test"]["target_met"] else 0.0 for row in subset),
        "no_accept_rows": sum(1 for row in subset if row["test"]["no_accept"]),
    }


def _target_vs_strongest_baseline(rows: list[dict[str, Any]], target: str, risk_target: float) -> dict[str, Any]:
    grouped: dict[tuple[str, int, float], dict[str, dict[str, Any]]] = {}
    for row in rows:
        if row["risk_target"] != risk_target:
            continue
        group_key = (str(row["dataset"]), int(row["seed"]), float(row["risk_target"]))
        grouped.setdefault(group_key, {})[row["method"]] = row
    deltas = []
    risks = []
    missed = 0
    for group in grouped.values():
        target_row = group.get(target)
        if not target_row:
            continue
        baseline_rows = [row for method, row in group.items() if method not in TARGET_METHODS]
        strongest_baseline = max(
            (_valid_coverage(row) for row in baseline_rows),
            default=0.0,
        )
        target_coverage = _valid_coverage(target_row)
        deltas.append(target_coverage - strongest_baseline)
        if target_row["test"]["risk"] is not None:
            risks.append(target_row["test"]["risk"])
        if not target_row["test"]["target_met"]:
            missed += 1
    return {
        "risk_target": risk_target,
        "target": target,
        "row_count": len(deltas),
        "wins": sum(1 for value in deltas if value > 1e-12),
        "ties": sum(1 for value in deltas if abs(value) <= 1e-12),
        "losses": sum(1 for value in deltas if value < -1e-12),
        "mean_coverage_delta": _mean(deltas),
        "mean_test_risk": _mean(risks),
        "missed_target_rows": missed,
    }


def _valid_coverage(row: dict[str, Any]) -> float:
    return float(row["test"]["coverage"]) if row["test"]["target_met"] else 0.0


def _mean(values) -> float | None:
    values = [float(value) for value in values if value is not None]
    if not values:
        return None
    return float(np.mean(values))


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.4f}"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[17, 31, 47])
    parser.add_argument("--risk-targets", type=float, nargs="+", default=[0.20, 0.30])
    parser.add_argument("--train-frac", type=float, default=0.60)
    parser.add_argument("--cal-frac", type=float, default=0.20)
    args = parser.parse_args()

    summary = compare_equal_budget_thresholds_v4(
        DEFAULT_DATASETS,
        seeds=args.seeds,
        risk_targets=args.risk_targets,
        train_frac=args.train_frac,
        cal_frac=args.cal_frac,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
