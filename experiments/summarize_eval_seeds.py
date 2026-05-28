#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Sequence


DEFAULT_METHODS = [
    "corm_max_clean",
    "single_set_sure_style",
    "naive_orbit_average",
    "csrm",
    "csrm_no_answer_consistency",
]


def summarize_eval_seeds(inputs: Sequence[Path], methods: Sequence[str]) -> dict:
    if not inputs:
        raise ValueError("at least one eval file is required")

    per_seed = []
    values: dict[str, list[dict]] = {method: [] for method in methods}
    for path in inputs:
        payload = json.loads(path.read_text(encoding="utf-8"))
        seed_item = {"file": str(path), "methods": {}}
        for method in methods:
            summary = payload["summary"][method]
            item = {
                "auroc": summary["auroc"],
                "aurc": summary["aurc"],
                "risk_at_30": summary["risk_at_30_coverage"]["risk"],
                "risk_at_50": summary["risk_at_50_coverage"]["risk"],
                "accuracy_at_0_5": summary["accuracy_at_0_5"],
            }
            seed_item["methods"][method] = item
            values[method].append(item)
        per_seed.append(seed_item)

    aggregate = {}
    for method, rows in values.items():
        aggregate[method] = {}
        for metric in ["auroc", "aurc", "risk_at_30", "risk_at_50", "accuracy_at_0_5"]:
            nums = [row[metric] for row in rows]
            aggregate[method][metric] = {
                "mean": statistics.fmean(nums),
                "stdev": statistics.stdev(nums) if len(nums) > 1 else 0.0,
                "min": min(nums),
                "max": max(nums),
            }

    return {
        "n_seeds": len(inputs),
        "methods": list(methods),
        "per_seed": per_seed,
        "aggregate": aggregate,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--methods", nargs="+", default=DEFAULT_METHODS)
    args = parser.parse_args()

    summary = summarize_eval_seeds(args.input, args.methods)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
