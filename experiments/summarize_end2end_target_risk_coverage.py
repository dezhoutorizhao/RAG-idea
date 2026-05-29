#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_INPUT = Path("results/end2end_risk_coverage_curves_20260529.json")
DEFAULT_OUTPUT_JSON = Path("results/end2end_target_risk_coverage_20260529.json")
DEFAULT_OUTPUT_MD = Path("results/end2end_target_risk_coverage_20260529.md")
DEFAULT_RISK_TARGETS = [0.20, 0.30, 0.40]
PRIMARY_METHOD = "csrm"
REFERENCE_METHOD = "strongest_non_csrm"


def summarize_end2end_target_risk_coverage(
    input_path: Path,
    *,
    risk_targets: Sequence[float] = DEFAULT_RISK_TARGETS,
) -> dict[str, Any]:
    payload = _load_json(input_path)
    rows = [
        _target_row(row, target)
        for row in payload.get("rows", [])
        for target in risk_targets
    ]
    aggregate = _aggregate(rows, risk_targets)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": str(input_path),
        "risk_targets": list(risk_targets),
        "row_count": len(rows),
        "source_matrix_row_count": payload.get("row_count"),
        "datasets": payload.get("datasets", []),
        "retrievers": payload.get("retrievers", []),
        "generators": payload.get("generators", []),
        "rows": rows,
        "aggregate": aggregate,
        "coverage_at_target_risk_supported": aggregate["csrm_higher_coverage_target_count"] >= 1,
        "claim_policy": (
            "This artifact reports coverage at fixed accepted-error risk targets for the same "
            "local-corpus end-to-end proxy matrix as the risk-coverage curve. It is not a "
            "full Wikipedia/CoRM-RAG reproduction and should not be used as human-audited evidence."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    lines = [
        "# End-to-End Coverage at Target Risk",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Source rows: `{summary['source_matrix_row_count']}`",
        f"Risk targets: `{summary['risk_targets']}`",
        f"Coverage-at-target-risk supported: `{summary['coverage_at_target_risk_supported']}`",
        "",
        "## Aggregate",
        "",
        "| Target risk | CSRM mean coverage | Strongest non-CSRM mean coverage | Delta | Wins | Ties | Losses |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in aggregate["by_target"]:
        lines.append(
            f"| {_fmt(item['target_risk'])} | {_fmt(item['csrm_mean_coverage'])} | "
            f"{_fmt(item['strongest_non_csrm_mean_coverage'])} | {_fmt(item['mean_coverage_delta'])} | "
            f"{item['wins']} | {item['ties']} | {item['losses']} |"
        )
    lines.extend(
        [
            "",
            "## Claim Policy",
            "",
            summary["claim_policy"],
            "",
        ]
    )
    return "\n".join(lines)


def _target_row(row: dict[str, Any], target: float) -> dict[str, Any]:
    csrm = _coverage_at_target(row["curves"][PRIMARY_METHOD], target)
    strongest = _coverage_at_target(row["curves"][REFERENCE_METHOD], target)
    delta = csrm["coverage"] - strongest["coverage"]
    return {
        "dataset": row.get("dataset"),
        "retriever": row.get("retriever"),
        "generator": row.get("generator"),
        "target_risk": float(target),
        "csrm_coverage": csrm["coverage"],
        "csrm_best_risk": csrm["best_risk"],
        "strongest_non_csrm_coverage": strongest["coverage"],
        "strongest_non_csrm_best_risk": strongest["best_risk"],
        "coverage_delta": delta,
        "verdict": "win" if delta > 1e-12 else "tie" if abs(delta) <= 1e-12 else "loss",
    }


def _coverage_at_target(points: Sequence[dict[str, Any]], target: float) -> dict[str, float]:
    feasible = [point for point in points if float(point["risk"]) <= target + 1e-12]
    if feasible:
        best = max(feasible, key=lambda item: float(item["coverage"]))
        return {"coverage": float(best["coverage"]), "best_risk": float(best["risk"])}
    best_risk = min(float(point["risk"]) for point in points) if points else 0.0
    return {"coverage": 0.0, "best_risk": best_risk}


def _aggregate(rows: Sequence[dict[str, Any]], risk_targets: Sequence[float]) -> dict[str, Any]:
    by_target = []
    for target in risk_targets:
        target_rows = [row for row in rows if abs(row["target_risk"] - target) < 1e-12]
        by_target.append(
            {
                "target_risk": float(target),
                "row_count": len(target_rows),
                "csrm_mean_coverage": _mean(row["csrm_coverage"] for row in target_rows),
                "strongest_non_csrm_mean_coverage": _mean(
                    row["strongest_non_csrm_coverage"] for row in target_rows
                ),
                "mean_coverage_delta": _mean(row["coverage_delta"] for row in target_rows),
                "wins": sum(1 for row in target_rows if row["verdict"] == "win"),
                "ties": sum(1 for row in target_rows if row["verdict"] == "tie"),
                "losses": sum(1 for row in target_rows if row["verdict"] == "loss"),
            }
        )
    return {
        "by_target": by_target,
        "csrm_higher_coverage_target_count": sum(
            1 for item in by_target if item["mean_coverage_delta"] > 1e-12
        ),
        "target_count": len(risk_targets),
        "wins": sum(row["verdict"] == "win" for row in rows),
        "ties": sum(row["verdict"] == "tie" for row in rows),
        "losses": sum(row["verdict"] == "loss" for row in rows),
    }


def _mean(values) -> float:
    values = [float(value) for value in values]
    return sum(values) / len(values) if values else 0.0


def _fmt(value: Any) -> str:
    return "n/a" if value is None else f"{float(value):.4f}"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--risk-targets", type=float, nargs="+", default=DEFAULT_RISK_TARGETS)
    args = parser.parse_args()

    summary = summarize_end2end_target_risk_coverage(args.input, risk_targets=args.risk_targets)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
