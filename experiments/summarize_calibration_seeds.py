#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any, Sequence

from experiments.evaluate_orbits import load_orbits
from experiments.train_calibrated_csrm import train_and_evaluate


DEFAULT_METHODS = [
    "corm_max_clean",
    "single_set_sure_style",
    "naive_orbit_average",
    "csrm_fixed_weights",
    "csrm_logreg_calibrated",
]
SUMMARY_METRICS = [
    "auroc",
    "aurc",
    "calibrated_coverage",
    "calibrated_risk",
    "calibrated_accuracy",
]


def run_calibration_seeds(
    input_path: Path,
    seeds: Sequence[int],
    *,
    train_frac: float,
    cal_frac: float,
    risk_target: float,
    methods: Sequence[str] = DEFAULT_METHODS,
) -> dict[str, Any]:
    if not seeds:
        raise ValueError("at least one calibration seed is required")

    orbits = load_orbits(input_path)
    per_seed = []
    for seed in seeds:
        result = train_and_evaluate(
            orbits,
            train_frac=train_frac,
            cal_frac=cal_frac,
            seed=seed,
            risk_target=risk_target,
        )
        seed_item = {
            "seed": seed,
            "split_sizes": result["split_sizes"],
            "methods": {},
        }
        for method in methods:
            test = result["methods"][method]["test"]
            seed_item["methods"][method] = _select_metrics(test, risk_target)
        per_seed.append(seed_item)

    return {
        "input": str(input_path),
        "n_seeds": len(seeds),
        "seeds": list(seeds),
        "train_frac": train_frac,
        "cal_frac": cal_frac,
        "risk_target": risk_target,
        "methods": list(methods),
        "per_seed": per_seed,
        "aggregate": _aggregate(per_seed, methods, risk_target),
    }


def summarize_calibration_files(
    inputs: Sequence[Path],
    *,
    risk_target: float | None = None,
    methods: Sequence[str] = DEFAULT_METHODS,
) -> dict[str, Any]:
    if not inputs:
        raise ValueError("at least one calibration result file is required")

    per_seed = []
    inferred_target = risk_target
    for index, path in enumerate(inputs):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if inferred_target is None:
            inferred_target = float(payload["risk_target"])
        seed_item = {
            "seed": payload.get("seed", index),
            "file": str(path),
            "split_sizes": payload.get("split_sizes", {}),
            "methods": {},
        }
        for method in methods:
            test = payload["methods"][method]["test"]
            seed_item["methods"][method] = _select_metrics(test, float(inferred_target))
        per_seed.append(seed_item)

    target = 0.0 if inferred_target is None else float(inferred_target)
    return {
        "inputs": [str(path) for path in inputs],
        "n_seeds": len(inputs),
        "risk_target": target,
        "methods": list(methods),
        "per_seed": per_seed,
        "aggregate": _aggregate(per_seed, methods, target),
    }


def _select_metrics(test: dict[str, Any], risk_target: float) -> dict[str, Any]:
    calibrated_risk = float(test["calibrated_risk"])
    return {
        "auroc": test["auroc"],
        "aurc": test["aurc"],
        "risk_at_30": test["risk_at_30_coverage"]["risk"],
        "calibrated_threshold": test["calibrated_threshold"],
        "calibrated_coverage": test["calibrated_coverage"],
        "calibrated_risk": calibrated_risk,
        "calibrated_accuracy": test["calibrated_accuracy"],
        "risk_excess_over_target": calibrated_risk - risk_target,
        "target_met": calibrated_risk <= risk_target,
    }


def _aggregate(
    per_seed: Sequence[dict[str, Any]],
    methods: Sequence[str],
    risk_target: float,
) -> dict[str, Any]:
    aggregate = {}
    for method in methods:
        rows = [item["methods"][method] for item in per_seed]
        metric_summary = {}
        for metric in SUMMARY_METRICS + ["risk_at_30", "risk_excess_over_target"]:
            nums = [row[metric] for row in rows if row[metric] is not None]
            metric_summary[metric] = _numeric_summary(nums)
        target_met = [bool(row["target_met"]) for row in rows]
        nonzero_coverage = [float(row["calibrated_coverage"]) > 0.0 for row in rows]
        aggregate[method] = {
            **metric_summary,
            "target_met_count": sum(target_met),
            "target_met_rate": sum(target_met) / len(target_met),
            "target_miss_count": len(target_met) - sum(target_met),
            "zero_coverage_count": len(nonzero_coverage) - sum(nonzero_coverage),
            "formal_risk_guarantee_supported": all(target_met) and all(nonzero_coverage),
            "risk_target": risk_target,
        }
    return aggregate


def _numeric_summary(nums: Sequence[float]) -> dict[str, float | None]:
    if not nums:
        return {"mean": None, "stdev": None, "min": None, "max": None}
    return {
        "mean": statistics.fmean(nums),
        "stdev": statistics.stdev(nums) if len(nums) > 1 else 0.0,
        "min": min(nums),
        "max": max(nums),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="Orbit JSONL file to evaluate across seeds.")
    parser.add_argument("--from-files", type=Path, nargs="+", help="Existing calibration JSON files.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[17, 31, 47])
    parser.add_argument("--train-frac", type=float, default=0.60)
    parser.add_argument("--cal-frac", type=float, default=0.20)
    parser.add_argument("--risk-target", type=float, default=0.20)
    parser.add_argument("--methods", nargs="+", default=DEFAULT_METHODS)
    args = parser.parse_args()

    if bool(args.input) == bool(args.from_files):
        raise SystemExit("provide exactly one of --input or --from-files")

    if args.input:
        result = run_calibration_seeds(
            args.input,
            args.seeds,
            train_frac=args.train_frac,
            cal_frac=args.cal_frac,
            risk_target=args.risk_target,
            methods=args.methods,
        )
    else:
        result = summarize_calibration_files(
            args.from_files,
            risk_target=args.risk_target,
            methods=args.methods,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
