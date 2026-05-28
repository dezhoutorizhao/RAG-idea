#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from experiments.build_v4_score_controlled_variant import build_v4_score_controlled_variant
from experiments.build_v4_structural_balanced_subset import build_v4_structural_balanced_subset
from experiments.compare_methods import compare_methods
from experiments.evaluate_orbits import evaluate, load_orbits
from experiments.run_v4_anti_shortcut_probes import run_v4_anti_shortcut_probes
from experiments.score_orbits_textonly_v4 import score_orbits_textonly_v4


def run_v4_structural_balance_diagnostic(
    raw_path: Path,
    private_path: Path,
    output_prefix: Path,
    constant_score: float = 0.5,
    max_combinations: int = 250_000,
    search_seed: int = 97,
    bootstrap_samples: int = 200,
    bootstrap_seed: int = 13,
    compare_bootstrap_seed: int = 71,
    random_trials: int = 200,
) -> dict:
    constant_raw = _append_suffix(output_prefix, ".constant.raw.jsonl")
    constant_score_report = _append_suffix(output_prefix, ".constant.score_control_report.json")
    scored = _append_suffix(output_prefix, ".constant.textonly_scored.jsonl")
    scored_report = _append_suffix(output_prefix, ".constant.textonly_report.json")
    balanced_prefix = _append_suffix(output_prefix, ".constant.structbalanced")
    anti_shortcut_output = _append_suffix(output_prefix, ".constant.structbalanced.anti_shortcut.json")
    eval_output = _append_suffix(output_prefix, ".constant.structbalanced.textonly_eval.json")
    compare_output = _append_suffix(output_prefix, ".constant.structbalanced.textonly_compare.json")
    summary_output = _append_suffix(output_prefix, ".constant.structbalanced.summary.json")

    score_control_report = build_v4_score_controlled_variant(
        raw_input=raw_path,
        raw_output=constant_raw,
        report_output=constant_score_report,
        mode="constant",
        constant_score=constant_score,
    )
    scoring_report = score_orbits_textonly_v4(
        raw_input=constant_raw,
        private_input=private_path,
        scored_output=scored,
        report_output=scored_report,
    )
    balance_report = build_v4_structural_balanced_subset(
        raw_path=constant_raw,
        private_path=private_path,
        scored_path=scored,
        output_prefix=balanced_prefix,
        max_combinations=max_combinations,
        seed=search_seed,
    )
    anti_shortcut = run_v4_anti_shortcut_probes(
        raw_path=Path(balance_report["outputs"]["raw"]),
        private_path=Path(balance_report["outputs"]["private"]),
        scored_path=Path(balance_report["outputs"]["scored"]),
        output_path=anti_shortcut_output,
        random_trials=random_trials,
        seed=search_seed,
    )
    eval_report = evaluate(
        load_orbits(Path(balance_report["outputs"]["scored"])),
        bootstrap_samples=bootstrap_samples,
        bootstrap_seed=bootstrap_seed,
    )
    eval_output.parent.mkdir(parents=True, exist_ok=True)
    eval_output.write_text(json.dumps(eval_report, indent=2, sort_keys=True), encoding="utf-8")
    compare_report = compare_methods(
        input_path=Path(balance_report["outputs"]["scored"]),
        target="csrm",
        baselines=["corm_max_clean", "single_set_sure_style", "naive_orbit_average"],
        bootstrap_samples=bootstrap_samples,
        bootstrap_seed=compare_bootstrap_seed,
    )
    compare_output.parent.mkdir(parents=True, exist_ok=True)
    compare_output.write_text(json.dumps(compare_report, indent=2, sort_keys=True), encoding="utf-8")

    summary = {
        "inputs": {
            "raw": str(raw_path),
            "private": str(private_path),
        },
        "outputs": {
            "constant_raw": str(constant_raw),
            "constant_score_report": str(constant_score_report),
            "constant_scored": str(scored),
            "constant_scored_report": str(scored_report),
            "balanced_raw": balance_report["outputs"]["raw"],
            "balanced_private": balance_report["outputs"]["private"],
            "balanced_scored": balance_report["outputs"]["scored"],
            "balance_report": balance_report["outputs"]["report"],
            "anti_shortcut": str(anti_shortcut_output),
            "eval": str(eval_output),
            "compare": str(compare_output),
            "summary": str(summary_output),
        },
        "score_control": {
            "mode": "constant",
            "constant_score": constant_score,
            "score_summary_before": score_control_report["score_summary_before"],
            "score_summary_after": score_control_report["score_summary_after"],
        },
        "scoring": {
            "orbits": scoring_report["orbits"],
            "source_item_groups": scoring_report["source_item_groups"],
            "scorer": scoring_report["scorer"],
        },
        "balance": {
            "selected_n": balance_report["selected_n"],
            "selected_positive": balance_report["selected_positive"],
            "selected_negative": balance_report["selected_negative"],
            "search": balance_report["search"],
        },
        "anti_shortcut": {
            "structural_max_auc": anti_shortcut["structural_only_probe"]["max_single_feature_auroc"],
            "structural_passed_0_55": anti_shortcut["structural_only_probe"]["passed_0_55_threshold"],
            "random_label_median_auc": anti_shortcut["random_label_sanity"]["auroc"]["median"],
        },
        "csrm": _method_summary(eval_report, "csrm"),
        "compare_vs_naive": compare_report["comparisons"]["naive_orbit_average"]["point"],
        "limitations": [
            "Constant-score diagnostics remove retrieval-score shortcuts and are not real retrieval evidence.",
            "Structural-balanced subset selection is diagnostic; main evidence still requires larger construction-time hard negatives and human-audited labels.",
        ],
    }
    summary_output.parent.mkdir(parents=True, exist_ok=True)
    summary_output.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def _method_summary(eval_report: dict, method: str) -> dict:
    item = eval_report["summary"][method]
    return {
        "n": item["n"],
        "positive": item["positive"],
        "negative": item["negative"],
        "auroc": item["auroc"],
        "risk_at_30": item["risk_at_30_coverage"]["risk"],
        "risk_at_50": item["risk_at_50_coverage"]["risk"],
        "aurc": item["aurc"],
    }


def _append_suffix(path: Path, suffix: str) -> Path:
    return path.with_name(path.name + suffix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--constant-score", type=float, default=0.5)
    parser.add_argument("--max-combinations", type=int, default=250_000)
    parser.add_argument("--search-seed", type=int, default=97)
    parser.add_argument("--bootstrap-samples", type=int, default=200)
    parser.add_argument("--bootstrap-seed", type=int, default=13)
    parser.add_argument("--compare-bootstrap-seed", type=int, default=71)
    parser.add_argument("--random-trials", type=int, default=200)
    args = parser.parse_args()
    summary = run_v4_structural_balance_diagnostic(
        raw_path=args.raw,
        private_path=args.private,
        output_prefix=args.output_prefix,
        constant_score=args.constant_score,
        max_combinations=args.max_combinations,
        search_seed=args.search_seed,
        bootstrap_samples=args.bootstrap_samples,
        bootstrap_seed=args.bootstrap_seed,
        compare_bootstrap_seed=args.compare_bootstrap_seed,
        random_trials=args.random_trials,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
