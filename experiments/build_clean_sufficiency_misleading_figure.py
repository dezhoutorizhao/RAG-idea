#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_INPUTS = [
    Path("results/fever_orbits_v4_n100.constant.structbalanced.textonly_scored.jsonl"),
    Path("results/hotpot_orbits_v4_hardneg_n100.constant.textonly_scored.jsonl"),
    Path("results/hotpot_orbits_v4_n100.constant.hardmatched.textonly_scored.jsonl"),
    Path("results/hotpot_orbits_v4_n100.constant.structbalanced.textonly_scored.jsonl"),
    Path("results/hotpot_orbits_v4_semanticswap_n100.constant.textonly_scored.jsonl"),
    Path("results/hotpot_orbits_v4_supportpreserve_n100.constant.textonly_scored.jsonl"),
]

FEATURES = ["clean_sufficiency", "worst_sufficiency", "mean_sufficiency"]


def build_clean_sufficiency_misleading_figure(
    inputs: Sequence[Path],
    output_csv: Path,
    output_json: Path,
    output_svg: Path,
    output_md: Path,
    *,
    bins: int = 10,
) -> dict[str, Any]:
    rows = _load_rows(inputs)
    binned = _bin_rows(rows, bins)
    summary = _summary(rows, binned, inputs, output_csv, output_json, output_svg, output_md)
    _write_csv(output_csv, binned)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    output_svg.parent.mkdir(parents=True, exist_ok=True)
    output_svg.write_text(_render_svg(binned), encoding="utf-8")
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(_render_markdown(summary), encoding="utf-8")
    return summary


def _load_rows(inputs: Sequence[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in inputs:
        dataset = _dataset_name(path)
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                raw = json.loads(line)
                features = raw.get("metadata", {}).get("textonly_v4", {})
                label = raw.get("clean", {}).get("label_answerable")
                if label is None:
                    raise ValueError(f"{path}:{line_no} missing clean.label_answerable")
                rows.append(
                    {
                        "dataset": dataset,
                        "orbit_id": raw.get("orbit_id"),
                        "construction_type": raw.get("split") or raw.get("clean", {}).get("split"),
                        "label_answerable": bool(label),
                        "failure": not bool(label),
                        "features": {
                            feature: float(features[feature])
                            for feature in FEATURES
                            if feature in features
                        },
                    }
                )
    if not rows:
        raise ValueError("no scored rows found")
    return rows


def _bin_rows(rows: Sequence[dict[str, Any]], bins: int) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for feature in FEATURES:
        values = [row["features"][feature] for row in rows if feature in row["features"]]
        if not values:
            continue
        minimum = min(values)
        maximum = max(values)
        width = (maximum - minimum) / bins if maximum > minimum else 1.0 / bins
        for index in range(bins):
            lower = minimum + index * width
            upper = minimum + (index + 1) * width
            selected = [
                row
                for row in rows
                if feature in row["features"]
                and lower <= row["features"][feature] <= upper
                and (index == bins - 1 or row["features"][feature] < upper)
            ]
            failures = sum(1 for row in selected if row["failure"])
            output.append(
                {
                    "feature": feature,
                    "bin_index": index,
                    "bin_lower": lower,
                    "bin_upper": upper,
                    "bin_midpoint": (lower + upper) / 2,
                    "n": len(selected),
                    "failures": failures,
                    "failure_rate": failures / len(selected) if selected else None,
                }
            )
    return output


def _summary(
    rows: Sequence[dict[str, Any]],
    binned: Sequence[dict[str, Any]],
    inputs: Sequence[Path],
    output_csv: Path,
    output_json: Path,
    output_svg: Path,
    output_md: Path,
) -> dict[str, Any]:
    high_feature_stats = {}
    for feature in FEATURES:
        values = sorted(row["features"][feature] for row in rows if feature in row["features"])
        if not values:
            high_feature_stats[feature] = {
                "threshold": None,
                "threshold_policy": "feature_top_quartile",
                "n": 0,
                "failures": 0,
                "failure_rate": None,
            }
            continue
        high_threshold = values[int(0.75 * (len(values) - 1))]
        selected = [row for row in rows if row["features"].get(feature, -1.0) >= high_threshold]
        failures = sum(1 for row in selected if row["failure"])
        high_feature_stats[feature] = {
            "threshold": high_threshold,
            "threshold_policy": "feature_top_quartile",
            "n": len(selected),
            "failures": failures,
            "failure_rate": failures / len(selected) if selected else None,
        }
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [str(path) for path in inputs],
        "dataset_count": len(inputs),
        "row_count": len(rows),
        "failure_count": sum(1 for row in rows if row["failure"]),
        "failure_rate": sum(1 for row in rows if row["failure"]) / len(rows),
        "dataset_counts": dict(sorted(Counter(row["dataset"] for row in rows).items())),
        "construction_type_counts": dict(sorted(Counter(str(row["construction_type"]) for row in rows).items())),
        "high_sufficiency_failure": high_feature_stats,
        "nonempty_bin_count": sum(1 for row in binned if row["n"] > 0),
        "outputs": {
            "csv": str(output_csv),
            "json": str(output_json),
            "svg": str(output_svg),
            "markdown": str(output_md),
        },
        "claim_boundary": (
            "Private-label diagnostic figure: failure rates come from v4 heuristic/private labels, "
            "not human-adjudicated labels."
        ),
    }


def _write_csv(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "feature",
                "bin_index",
                "bin_lower",
                "bin_upper",
                "bin_midpoint",
                "n",
                "failures",
                "failure_rate",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def _render_svg(rows: Sequence[dict[str, Any]]) -> str:
    width = 760
    height = 460
    margin_left = 70
    margin_right = 30
    margin_top = 40
    margin_bottom = 70
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    colors = {
        "clean_sufficiency": "#3366cc",
        "worst_sufficiency": "#cc6633",
        "mean_sufficiency": "#228855",
    }
    x_min = min(row["bin_lower"] for row in rows if row["n"] > 0)
    x_max = max(row["bin_upper"] for row in rows if row["n"] > 0)
    if x_max <= x_min:
        x_max = x_min + 1.0

    def x(value: float) -> float:
        return margin_left + ((value - x_min) / (x_max - x_min)) * plot_width

    def y(value: float) -> float:
        return margin_top + (1.0 - value) * plot_height

    lines = [
        f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">",
        "<rect width=\"100%\" height=\"100%\" fill=\"white\"/>",
        "<text x=\"70\" y=\"24\" font-family=\"Arial\" font-size=\"18\" font-weight=\"700\">Clean sufficiency can be misleading</text>",
        f"<line x1=\"{margin_left}\" y1=\"{margin_top + plot_height}\" x2=\"{margin_left + plot_width}\" y2=\"{margin_top + plot_height}\" stroke=\"#222\"/>",
        f"<line x1=\"{margin_left}\" y1=\"{margin_top}\" x2=\"{margin_left}\" y2=\"{margin_top + plot_height}\" stroke=\"#222\"/>",
    ]
    for tick in range(0, 6):
        value = x_min + (x_max - x_min) * tick / 5
        y_value = tick / 5
        lines.extend(
            [
                f"<line x1=\"{x(value):.1f}\" y1=\"{margin_top + plot_height}\" x2=\"{x(value):.1f}\" y2=\"{margin_top + plot_height + 5}\" stroke=\"#222\"/>",
                f"<text x=\"{x(value):.1f}\" y=\"{margin_top + plot_height + 22}\" text-anchor=\"middle\" font-family=\"Arial\" font-size=\"11\">{value:.2f}</text>",
                f"<line x1=\"{margin_left - 5}\" y1=\"{y(y_value):.1f}\" x2=\"{margin_left}\" y2=\"{y(y_value):.1f}\" stroke=\"#222\"/>",
                f"<text x=\"{margin_left - 10}\" y=\"{y(y_value) + 4:.1f}\" text-anchor=\"end\" font-family=\"Arial\" font-size=\"11\">{y_value:.1f}</text>",
            ]
        )
        if tick not in {0, 5}:
            lines.append(
                f"<line x1=\"{margin_left}\" y1=\"{y(y_value):.1f}\" x2=\"{margin_left + plot_width}\" y2=\"{y(y_value):.1f}\" stroke=\"#eee\"/>"
            )

    for feature in FEATURES:
        points = [
            (row["bin_midpoint"], row["failure_rate"], row["n"])
            for row in rows
            if row["feature"] == feature and row["failure_rate"] is not None
        ]
        if not points:
            continue
        polyline = " ".join(f"{x(px):.1f},{y(py):.1f}" for px, py, _ in points)
        lines.append(
            f"<polyline points=\"{polyline}\" fill=\"none\" stroke=\"{colors[feature]}\" stroke-width=\"2.5\"/>"
        )
        for px, py, n in points:
            radius = 3.0 + min(5.0, n ** 0.5 / 4.0)
            lines.append(
                f"<circle cx=\"{x(px):.1f}\" cy=\"{y(py):.1f}\" r=\"{radius:.1f}\" fill=\"{colors[feature]}\" fill-opacity=\"0.78\"/>"
            )

    legend_x = 500
    legend_y = 52
    for index, feature in enumerate(FEATURES):
        y_pos = legend_y + index * 22
        lines.extend(
            [
                f"<line x1=\"{legend_x}\" y1=\"{y_pos}\" x2=\"{legend_x + 28}\" y2=\"{y_pos}\" stroke=\"{colors[feature]}\" stroke-width=\"3\"/>",
                f"<text x=\"{legend_x + 36}\" y=\"{y_pos + 4}\" font-family=\"Arial\" font-size=\"12\">{feature}</text>",
            ]
        )

    lines.extend(
        [
            f"<text x=\"{margin_left + plot_width / 2:.1f}\" y=\"{height - 22}\" text-anchor=\"middle\" font-family=\"Arial\" font-size=\"13\">Sufficiency proxy bin</text>",
            f"<text x=\"18\" y=\"{margin_top + plot_height / 2:.1f}\" transform=\"rotate(-90 18,{margin_top + plot_height / 2:.1f})\" text-anchor=\"middle\" font-family=\"Arial\" font-size=\"13\">Private-label failure rate</text>",
            "<text x=\"70\" y=\"446\" font-family=\"Arial\" font-size=\"11\" fill=\"#555\">Diagnostic only: labels are heuristic/private v4 labels, not human audit.</text>",
            "</svg>",
        ]
    )
    return "\n".join(lines)


def _render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Clean Sufficiency Misleading Diagnostic",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Rows: `{summary['row_count']}` across `{summary['dataset_count']}` scored v4 inputs.",
        f"Overall private-label failure rate: `{summary['failure_rate']:.4f}`.",
        "",
        "## High-Sufficiency Failure Rates",
        "",
        "| Feature | Threshold policy | Threshold | n | failures | failure rate |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for feature, item in summary["high_sufficiency_failure"].items():
        rate = "n/a" if item["failure_rate"] is None else f"{item['failure_rate']:.4f}"
        threshold = "n/a" if item["threshold"] is None else f"{item['threshold']:.4f}"
        lines.append(
            f"| {feature} | {item['threshold_policy']} | {threshold} | {item['n']} | {item['failures']} | {rate} |"
        )
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- CSV: `{summary['outputs']['csv']}`",
            f"- SVG: `{summary['outputs']['svg']}`",
            f"- JSON: `{summary['outputs']['json']}`",
            "",
            "## Claim Boundary",
            "",
            summary["claim_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def _dataset_name(path: Path) -> str:
    name = path.name
    suffix = ".textonly_scored.jsonl"
    if name.endswith(suffix):
        name = name[: -len(suffix)]
    return name.replace(".constant.", "_").replace(".constant", "")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, nargs="+", default=DEFAULT_INPUTS)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-svg", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--bins", type=int, default=10)
    args = parser.parse_args()

    summary = build_clean_sufficiency_misleading_figure(
        args.inputs,
        args.output_csv,
        args.output_json,
        args.output_svg,
        args.output_md,
        bins=args.bins,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
