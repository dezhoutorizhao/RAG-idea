#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_INPUTS = [
    Path("results/fever_orbits_v4_n100.constant.structbalanced.anti_shortcut.json"),
    Path("results/hotpot_orbits_v4_hardneg_n100.constant.anti_shortcut.json"),
    Path("results/hotpot_orbits_v4_n100.constant.hardmatched.anti_shortcut.json"),
    Path("results/hotpot_orbits_v4_n100.constant.structbalanced.anti_shortcut.json"),
    Path("results/hotpot_orbits_v4_semanticswap_n100.constant.anti_shortcut.json"),
    Path("results/hotpot_orbits_v4_supportpreserve_n100.constant.anti_shortcut.json"),
]


def summarize_v4_anti_shortcut(inputs: Sequence[Path]) -> dict[str, Any]:
    rows = [_row(path) for path in inputs]
    if not rows:
        raise ValueError("at least one anti-shortcut artifact is required")
    max_structural = max(row["max_single_feature_auroc"] for row in rows)
    random_medians = [row["random_label_auroc_median"] for row in rows]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [str(path) for path in inputs],
        "dataset_count": len(rows),
        "rows": rows,
        "aggregate": {
            "all_raw_firewall_passed": all(row["raw_firewall_passed"] for row in rows),
            "all_structural_only_passed_0_55": all(row["structural_only_passed_0_55"] for row in rows),
            "max_single_feature_auroc_max": max_structural,
            "all_group_split_no_overlap": all(row["group_split_no_overlap"] for row in rows),
            "random_label_median_min": min(random_medians),
            "random_label_median_max": max(random_medians),
            "random_label_median_all_near_half": all(
                0.45 <= value <= 0.55 for value in random_medians
            ),
            "private_metadata_upper_bound_all_high": all(
                row["private_metadata_oriented_auroc"] is not None
                and row["private_metadata_oriented_auroc"] >= 0.95
                for row in rows
            ),
            "pass_core_anti_shortcut_suite": (
                all(row["raw_firewall_passed"] for row in rows)
                and all(row["structural_only_passed_0_55"] for row in rows)
                and all(row["group_split_no_overlap"] for row in rows)
                and all(0.45 <= value <= 0.55 for value in random_medians)
            ),
        },
        "claim_implication": (
            "The primary v4 anti-shortcut suite passes the core non-oracle checks: raw feature "
            "firewall, structural-only <= 0.55, source-item group split without overlap, and "
            "random-label sanity near 0.5. Private construction metadata remains a high-leakage "
            "upper bound, so these fields must stay evaluator-only. This supports leakage-control "
            "claims but does not replace human audit or end-to-end RAG evidence."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    lines = [
        "# V4 Anti-Shortcut Summary",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Datasets: `{summary['dataset_count']}`",
        "",
        "## Aggregate",
        "",
        f"- Raw firewall all passed: `{aggregate['all_raw_firewall_passed']}`.",
        f"- Structural-only all passed <= 0.55: `{aggregate['all_structural_only_passed_0_55']}`; max AUROC: `{aggregate['max_single_feature_auroc_max']:.4f}`.",
        f"- Group split no-overlap all passed: `{aggregate['all_group_split_no_overlap']}`.",
        f"- Random-label median AUROC range: `{aggregate['random_label_median_min']:.4f}` to `{aggregate['random_label_median_max']:.4f}`.",
        f"- Private metadata upper bound all high: `{aggregate['private_metadata_upper_bound_all_high']}`.",
        f"- Core anti-shortcut suite passed: `{aggregate['pass_core_anti_shortcut_suite']}`.",
        "",
        "## Per Dataset",
        "",
        "| Dataset | n | max structural AUROC | structural pass | random median | group no-overlap | private metadata AUROC |",
        "|---|---:|---:|---|---:|---|---:|",
    ]
    for row in summary["rows"]:
        private_auc = row["private_metadata_oriented_auroc"]
        private_text = "n/a" if private_auc is None else f"{private_auc:.4f}"
        lines.append(
            f"| {row['dataset']} | {row['n']} | {row['max_single_feature_auroc']:.4f} | "
            f"`{row['structural_only_passed_0_55']}` | {row['random_label_auroc_median']:.4f} | "
            f"`{row['group_split_no_overlap']}` | {private_text} |"
        )
    lines.extend(["", "## Claim Implication", "", summary["claim_implication"], ""])
    return "\n".join(lines)


def _row(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    structural = payload["structural_only_probe"]
    random_auc = payload["random_label_sanity"]["auroc"]
    group_split = payload["group_split_probe"]
    private = payload["private_metadata_leakage_upper_bound"]
    return {
        "artifact": str(path),
        "dataset": _dataset_name(path),
        "n": payload["n"],
        "positive": payload["positive"],
        "negative": payload["negative"],
        "raw_firewall_passed": bool(payload["raw_firewall_passed"]),
        "max_single_feature_auroc": float(structural["max_single_feature_auroc"]),
        "structural_only_passed_0_55": bool(structural["passed_0_55_threshold"]),
        "random_label_auroc_median": float(random_auc["median"]),
        "random_label_auroc_p2_5": float(random_auc["p2_5"]),
        "random_label_auroc_p97_5": float(random_auc["p97_5"]),
        "group_count": int(group_split["n_groups"]),
        "group_split_no_overlap": bool(group_split["passed_no_group_overlap"]),
        "private_metadata_oriented_auroc": private.get("construction_type_oriented_auroc"),
    }


def _dataset_name(path: Path) -> str:
    name = path.name
    suffix = ".anti_shortcut.json"
    if name.endswith(suffix):
        name = name[: -len(suffix)]
    return name.replace(".constant.", "_").replace(".constant", "")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, nargs="+", default=DEFAULT_INPUTS)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_v4_anti_shortcut(args.inputs)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
