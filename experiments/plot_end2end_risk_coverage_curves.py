#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag.end2end import evaluate_selective_policy
from csrm_rag.metrics import selective_risk_at_coverage
from experiments.run_end2end_retriever_generator_matrix_v4 import (
    DEFAULT_DATASETS,
    GENERATORS,
    NON_CSRM_METHODS,
    RETRIEVERS,
    DatasetConfig,
    score_end2end_selector_methods,
)


DEFAULT_COVERAGES = [0.10, 0.20, 0.30, 0.50, 0.70, 0.90, 1.00]
DEFAULT_OUTPUT_JSON = Path("results/end2end_risk_coverage_curves_20260529.json")
DEFAULT_OUTPUT_MD = Path("results/end2end_risk_coverage_curves_20260529.md")
DEFAULT_OUTPUT_SVG = Path("paper/figures/end2end_risk_coverage_curves_20260529.svg")


def build_end2end_risk_coverage_curves(
    datasets: Sequence[DatasetConfig],
    *,
    retrievers: Sequence[str] = RETRIEVERS,
    generators: Sequence[str] = GENERATORS,
    top_k: int = 6,
    coverages: Sequence[float] = DEFAULT_COVERAGES,
    output_svg: Path = DEFAULT_OUTPUT_SVG,
) -> dict[str, Any]:
    rows = [
        _row(dataset, retriever, generator, top_k=top_k, coverages=coverages)
        for dataset in datasets
        for retriever in retrievers
        for generator in generators
    ]
    aggregate = _aggregate(rows, coverages)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "datasets": [dataset.name for dataset in datasets],
        "dataset_count": len(datasets),
        "retrievers": list(retrievers),
        "generators": list(generators),
        "top_k": top_k,
        "coverages": list(coverages),
        "row_count": len(rows),
        "rows": rows,
        "aggregate": aggregate,
        "outputs": {"svg": str(output_svg)},
        "protocol_complete": bool(rows)
        and len(set(retrievers)) >= 2
        and len(set(generators)) >= 2
        and all(row["n"] > 0 for row in rows),
        "claim_policy": (
            "This figure summarizes risk-coverage curves for the local-corpus end-to-end "
            "proxy matrix. It is useful Phase 5 visualization evidence, but it is not a "
            "full Wikipedia/CoRM-RAG retrieval-generation reproduction."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# End-to-End Risk-Coverage Curves",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Datasets: `{summary['dataset_count']}`",
        f"Retrievers: `{summary['retrievers']}`",
        f"Generators: `{summary['generators']}`",
        f"Rows: `{summary['row_count']}`",
        f"Protocol complete: `{summary['protocol_complete']}`",
        f"SVG: `{summary['outputs']['svg']}`",
        "",
        "## Aggregate Mean Risk",
        "",
        "| Coverage | CSRM | Strongest non-CSRM | Delta |",
        "|---:|---:|---:|---:|",
    ]
    for point in summary["aggregate"]["csrm_vs_strongest_non_csrm"]:
        lines.append(
            f"| {point['coverage']:.2f} | {_fmt(point['csrm_mean_risk'])} | "
            f"{_fmt(point['strongest_non_csrm_mean_risk'])} | {_fmt(point['mean_risk_reduction'])} |"
        )
    lines.extend(
        [
            "",
            "## Method Curves",
            "",
            "| Method | Mean AURC | Risk@30 mean | Risk@50 mean |",
            "|---|---:|---:|---:|",
        ]
    )
    for method, curve in summary["aggregate"]["method_curves"].items():
        lines.append(
            f"| {method} | {_fmt(curve['mean_aurc'])} | "
            f"{_fmt(_risk_at(curve['points'], 0.30))} | {_fmt(_risk_at(curve['points'], 0.50))} |"
        )
    lines.extend(["", "## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def render_svg(summary: dict[str, Any]) -> str:
    curves = summary["aggregate"]["method_curves"]
    selected = [
        ("csrm", "#b42318", 3.0),
        ("strongest_non_csrm", "#175cd3", 3.0),
        ("naive_orbit_average", "#067647", 2.0),
        ("single_set_sure_style", "#93370d", 2.0),
        ("corm_max_clean", "#7a2e8f", 2.0),
    ]
    width, height = 820, 480
    left, top, plot_w, plot_h = 74, 38, 610, 360

    def xy(coverage: float, risk: float) -> tuple[float, float]:
        return left + coverage * plot_w, top + (1.0 - risk) * plot_h

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;font-size:13px;fill:#1f2937}.title{font-size:20px;font-weight:700}.axis{stroke:#111827;stroke-width:1.2}.grid{stroke:#e5e7eb;stroke-width:1}.legend{font-size:12px}</style>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text class="title" x="74" y="24">End-to-End Proxy Risk-Coverage Curves</text>',
    ]
    for tick in [0.0, 0.25, 0.5, 0.75, 1.0]:
        x, _ = xy(tick, 0.0)
        _, y = xy(0.0, tick)
        lines.append(f'<line class="grid" x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + plot_h}"/>')
        lines.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}"/>')
        lines.append(f'<text x="{x - 10:.1f}" y="{top + plot_h + 24}">{tick:.2f}</text>')
        lines.append(f'<text x="28" y="{y + 4:.1f}">{tick:.2f}</text>')
    lines.append(f'<line class="axis" x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}"/>')
    lines.append(f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}"/>')
    lines.append(f'<text x="{left + plot_w / 2 - 28:.1f}" y="{height - 26}">Coverage</text>')
    lines.append(f'<text transform="translate(18,{top + plot_h / 2 + 42:.1f}) rotate(-90)">Accepted-error risk</text>')

    legend_y = top + 22
    for idx, (method, color, stroke_w) in enumerate(selected):
        if method not in curves:
            continue
        points = curves[method]["points"]
        path = " ".join(
            ("M" if point_idx == 0 else "L") + f" {xy(point['coverage'], point['mean_risk'])[0]:.1f} {xy(point['coverage'], point['mean_risk'])[1]:.1f}"
            for point_idx, point in enumerate(points)
        )
        lines.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{stroke_w}" stroke-linejoin="round"/>')
        y = legend_y + idx * 24
        lines.append(f'<line x1="704" y1="{y}" x2="742" y2="{y}" stroke="{color}" stroke-width="{stroke_w}"/>')
        lines.append(f'<text class="legend" x="750" y="{y + 4}">{method}</text>')
    lines.append("</svg>")
    return "\n".join(lines)


def _row(
    dataset: DatasetConfig,
    retriever: str,
    generator: str,
    *,
    top_k: int,
    coverages: Sequence[float],
) -> dict[str, Any]:
    scored = score_end2end_selector_methods(dataset, retriever, generator, top_k=top_k)
    method_metrics = {
        method: evaluate_selective_policy(scores, scored["correct"])
        for method, scores in scored["methods"].items()
    }
    strongest = _strongest_non_csrm(method_metrics)
    curve_by_method = {
        method: _coverage_points(scores, scored["correct"], coverages)
        for method, scores in scored["methods"].items()
    }
    curve_by_method["strongest_non_csrm"] = curve_by_method[strongest["method"]]
    return {
        "dataset": dataset.name,
        "retriever": retriever,
        "generator": generator,
        "n": scored["n"],
        "answer_accuracy": scored["answer_accuracy"],
        "strongest_non_csrm": strongest,
        "curves": curve_by_method,
    }


def _coverage_points(scores: Sequence[float], correct: Sequence[bool], coverages: Sequence[float]) -> list[dict[str, Any]]:
    return [
        {
            "coverage": float(coverage),
            "risk": float(selective_risk_at_coverage(scores, correct, coverage)["risk"]),
        }
        for coverage in coverages
    ]


def _strongest_non_csrm(method_metrics: dict[str, Any]) -> dict[str, Any]:
    candidates = []
    for method in NON_CSRM_METHODS:
        if method not in method_metrics:
            continue
        metrics = method_metrics[method]
        candidates.append(
            {
                "method": method,
                "aurc": float(metrics["aurc"]),
                "risk30": float(metrics["accepted_error_at_30"]["risk"]),
                "risk50": float(metrics["accepted_error_at_50"]["risk"]),
            }
        )
    if not candidates:
        raise ValueError("no non-CSRM methods found")
    return min(candidates, key=lambda item: (item["risk30"], item["risk50"], item["aurc"]))


def _aggregate(rows: Sequence[dict[str, Any]], coverages: Sequence[float]) -> dict[str, Any]:
    methods = sorted({method for row in rows for method in row["curves"]})
    method_curves = {method: _mean_curve(rows, method, coverages) for method in methods}
    csrm = method_curves["csrm"]["points"]
    strongest = method_curves["strongest_non_csrm"]["points"]
    return {
        "method_curves": method_curves,
        "csrm_vs_strongest_non_csrm": [
            {
                "coverage": c_point["coverage"],
                "csrm_mean_risk": c_point["mean_risk"],
                "strongest_non_csrm_mean_risk": s_point["mean_risk"],
                "mean_risk_reduction": s_point["mean_risk"] - c_point["mean_risk"],
            }
            for c_point, s_point in zip(csrm, strongest)
        ],
        "csrm_lower_risk_coverage_count": sum(
            1 for c_point, s_point in zip(csrm, strongest) if c_point["mean_risk"] < s_point["mean_risk"]
        ),
        "coverage_count": len(coverages),
    }


def _mean_curve(rows: Sequence[dict[str, Any]], method: str, coverages: Sequence[float]) -> dict[str, Any]:
    points = []
    for index, coverage in enumerate(coverages):
        risks = [row["curves"][method][index]["risk"] for row in rows if method in row["curves"]]
        points.append({"coverage": float(coverage), "mean_risk": _mean(risks), "row_count": len(risks)})
    return {"points": points, "mean_aurc": _aurc(points)}


def _aurc(points: Sequence[dict[str, Any]]) -> float:
    ordered = sorted(points, key=lambda item: item["coverage"])
    area = 0.0
    prev_coverage = 0.0
    prev_risk = ordered[0]["mean_risk"]
    for point in ordered:
        coverage = point["coverage"]
        area += (coverage - prev_coverage) * ((prev_risk + point["mean_risk"]) / 2.0)
        prev_coverage = coverage
        prev_risk = point["mean_risk"]
    if prev_coverage < 1.0:
        area += (1.0 - prev_coverage) * prev_risk
    return area


def _risk_at(points: Sequence[dict[str, Any]], coverage: float) -> float | None:
    for point in points:
        if abs(point["coverage"] - coverage) < 1e-12:
            return point["mean_risk"]
    return None


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)


def _fmt(value: Any) -> str:
    return "n/a" if value is None else f"{float(value):.4f}"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--output-svg", type=Path, default=DEFAULT_OUTPUT_SVG)
    parser.add_argument("--top-k", type=int, default=6)
    args = parser.parse_args()

    summary = build_end2end_risk_coverage_curves(
        DEFAULT_DATASETS,
        top_k=args.top_k,
        output_svg=args.output_svg,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    args.output_svg.parent.mkdir(parents=True, exist_ok=True)
    args.output_svg.write_text(render_svg(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
