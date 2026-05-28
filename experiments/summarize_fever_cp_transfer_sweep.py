#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_INPUTS = [
    Path("results/fever_nearmiss_corm_v3_risk_control_cp_multiseed.json"),
    Path("results/fever_nearmiss_corm_v3_risk_control_cp_target025.json"),
    Path("results/fever_nearmiss_corm_v3_risk_control_cp_target030.json"),
    Path("results/fever_nearmiss_corm_v3_risk_control_cp_target035.json"),
]

PRIMARY_METHODS = ["csrm_logreg_calibrated", "csrm_fixed_weights"]


def summarize_fever_cp_transfer_sweep(
    inputs: Sequence[Path],
    *,
    primary_method: str = "csrm_logreg_calibrated",
) -> dict[str, Any]:
    runs = [_load_json(path) for path in inputs]
    if not runs:
        raise ValueError("at least one CP run is required")
    runs = sorted(runs, key=lambda item: float(item["risk_target"]))

    methods = [method for method in PRIMARY_METHODS if method in runs[0]["aggregate"]]
    if primary_method not in methods:
        methods.insert(0, primary_method)

    target_rows = [_target_row(run, methods) for run in runs]
    primary_rows = [row["methods"][primary_method] for row in target_rows]
    exact_020 = next((row for row in primary_rows if abs(row["risk_target"] - 0.20) < 1e-9), None)
    first_supported = next(
        (row for row in primary_rows if row["empirical_transfer_supported"]),
        None,
    )

    baseline_run = runs[0]
    failures_at_020 = _seed_rows(
        baseline_run,
        primary_method,
        risk_target=0.20,
        only_failures=True,
    )

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [str(path) for path in inputs],
        "dataset": "FEVER v3 near-miss CoRM 1200",
        "primary_method": primary_method,
        "methods": methods,
        "risk_targets": [float(run["risk_target"]) for run in runs],
        "target_rows": target_rows,
        "primary_method_target_020": exact_020,
        "primary_method_first_supported_target": first_supported,
        "primary_method_failures_at_020": failures_at_020,
        "claim_implication": _claim_implication(exact_020, first_supported),
        "negative_evidence_for_main_risk_claim": bool(
            exact_020 and not exact_020["empirical_transfer_supported"]
        ),
        "formal_risk_guarantee_supported": False,
        "interpretation": (
            "This diagnostic sweeps the empirical risk target while keeping the same "
            "FEVER near-miss input, split seeds, train/calibration fractions, alpha, and "
            "minimum-acceptance rule. It is an empirical transfer stress test, not a "
            "distribution-free guarantee."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# FEVER CP Transfer Sweep",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Dataset: `{summary['dataset']}`",
        f"Primary method: `{summary['primary_method']}`",
        "",
        "## Target Sweep",
        "",
        "| Risk target | Method | Target met | Misses | Test risk mean | Test risk max | Test coverage mean | Transfer supported |",
        "|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for target in summary["target_rows"]:
        for method, row in target["methods"].items():
            lines.append(
                "| "
                f"{_fmt(row['risk_target'])} | {method} | {row['target_met_count']}/"
                f"{row['seed_count']} | {row['target_miss_count']} | "
                f"{_fmt(row['test_empirical_risk_mean'])} | "
                f"{_fmt(row['test_empirical_risk_max'])} | "
                f"{_fmt(row['test_coverage_mean'])} | "
                f"`{row['empirical_transfer_supported']}` |"
            )

    first_supported = summary["primary_method_first_supported_target"]
    lines.extend(["", "## Boundary", ""])
    if first_supported:
        lines.append(
            "The primary method first passes all observed seeds at risk target "
            f"`{_fmt(first_supported['risk_target'])}` with max test empirical risk "
            f"`{_fmt(first_supported['test_empirical_risk_max'])}`."
        )
    else:
        lines.append("The primary method does not pass all observed risk targets.")

    lines.extend(
        [
            "",
            "Failures at risk target `0.2000`:",
            "",
            "| Seed | Accepted | Coverage | Errors | Empirical risk | Risk excess |",
            "|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in summary["primary_method_failures_at_020"]:
        lines.append(
            f"| {row['seed']} | {row['accepted']} | {_fmt(row['coverage'])} | "
            f"{row['errors']} | {_fmt(row['empirical_risk'])} | "
            f"{_fmt(row['risk_excess'])} |"
        )

    lines.extend(
        [
            "",
            "## Claim Implication",
            "",
            summary["claim_implication"],
            "",
            summary["interpretation"],
            "",
        ]
    )
    return "\n".join(lines)


def _target_row(run: dict[str, Any], methods: Sequence[str]) -> dict[str, Any]:
    return {
        "risk_target": float(run["risk_target"]),
        "input": run["input"],
        "seeds": run["seeds"],
        "methods": {method: _method_row(run, method) for method in methods},
    }


def _method_row(run: dict[str, Any], method: str) -> dict[str, Any]:
    aggregate = run["aggregate"][method]
    risk_summary = aggregate["test_empirical_risk"]
    coverage_summary = aggregate["test_coverage"]
    return {
        "risk_target": float(run["risk_target"]),
        "method": method,
        "seed_count": int(run["n_seeds"]),
        "target_met_count": int(aggregate["target_met_count"]),
        "target_miss_count": int(aggregate["target_miss_count"]),
        "cp_feasible_count": int(aggregate["cp_feasible_count"]),
        "nonzero_coverage_count": int(aggregate["nonzero_coverage_count"]),
        "test_empirical_risk_mean": risk_summary["mean"],
        "test_empirical_risk_max": risk_summary["max"],
        "test_coverage_mean": coverage_summary["mean"],
        "empirical_transfer_supported": bool(aggregate["empirical_transfer_supported"]),
        "formal_risk_guarantee_supported": bool(aggregate["formal_risk_guarantee_supported"]),
    }


def _seed_rows(
    run: dict[str, Any],
    method: str,
    *,
    risk_target: float,
    only_failures: bool,
) -> list[dict[str, Any]]:
    rows = []
    for seed_item in run["per_seed"]:
        test = seed_item["methods"][method]["test"]
        empirical_risk = test["empirical_risk"]
        target_met = bool(test["target_met"])
        if only_failures and target_met:
            continue
        rows.append(
            {
                "seed": seed_item["seed"],
                "accepted": test["accepted"],
                "coverage": test["coverage"],
                "errors": test["errors"],
                "empirical_risk": empirical_risk,
                "target_met": target_met,
                "risk_excess": None if empirical_risk is None else empirical_risk - risk_target,
            }
        )
    return rows


def _claim_implication(exact_020: dict[str, Any] | None, first_supported: dict[str, Any] | None) -> str:
    if exact_020 and exact_020["empirical_transfer_supported"]:
        return "FEVER near-miss supports the 0.20 empirical risk-transfer claim in this sweep."
    if first_supported:
        return (
            "FEVER near-miss is negative evidence for the 0.20 empirical risk-transfer claim: "
            f"the primary method misses at 0.20 and only passes all observed seeds after relaxing "
            f"the target to {_fmt(first_supported['risk_target'])}. This should be reported as a "
            "boundary condition, not as a NeurIPS-level main risk-control result."
        )
    return (
        "FEVER near-miss is negative evidence for the empirical risk-transfer claim across all "
        "observed targets in this sweep."
    )


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.4f}"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, nargs="+", default=DEFAULT_INPUTS)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--primary-method", default="csrm_logreg_calibrated")
    args = parser.parse_args()

    summary = summarize_fever_cp_transfer_sweep(
        args.inputs,
        primary_method=args.primary_method,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
