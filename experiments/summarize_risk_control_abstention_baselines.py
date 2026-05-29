#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_INPUT = Path("results/v4_shared_threshold_selection_20260529.json")
DEFAULT_OUTPUT_JSON = Path("results/risk_control_abstention_baselines_20260529.json")
DEFAULT_OUTPUT_MD = Path("results/risk_control_abstention_baselines_20260529.md")


def summarize_risk_control_abstention_baselines(input_path: Path) -> dict[str, Any]:
    payload = _load_json(input_path)
    rows = [
        row
        for row in payload.get("aggregate", {}).get("method_summary", [])
        if row.get("family") == "baseline"
    ]
    by_target = [_target_summary(rows, target) for target in payload.get("risk_targets", [])]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": str(input_path),
        "shared_threshold_protocol_complete": payload.get("shared_threshold_protocol_complete"),
        "risk_targets": payload.get("risk_targets", []),
        "baseline_methods": sorted({row["method"] for row in rows}),
        "baseline_method_count": len({row["method"] for row in rows}),
        "rows": rows,
        "by_target": by_target,
        "risk_control_abstention_baseline_present": bool(rows)
        and bool(payload.get("shared_threshold_protocol_complete")),
        "claim_boundary": (
            "This artifact audits non-CSRM risk-control/abstention baselines under the same "
            "calibration-threshold protocol as CSRM targets. It is empirical held-out evidence, "
            "not a formal conformal guarantee and not a full CoRM-RAG reproduction."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Risk-Control Abstention Baselines",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        f"Input: `{summary['input']}`",
        f"Shared-threshold protocol complete: `{summary['shared_threshold_protocol_complete']}`",
        f"Baseline present: `{summary['risk_control_abstention_baseline_present']}`",
        "",
        "## Baseline Methods",
        "",
        "`" + ", ".join(summary["baseline_methods"]) + "`",
        "",
        "## By Risk Target",
        "",
        "| Risk target | Methods | Best pass-rate method | Pass rate | Best mean-risk-valid coverage method | Coverage | Mean risk |",
        "|---:|---:|---|---:|---|---:|---:|",
    ]
    for item in summary["by_target"]:
        best_pass = item.get("best_by_test_target_pass_rate") or {}
        best_cov = item.get("best_mean_coverage_with_mean_risk_at_target") or {}
        lines.append(
            f"| {_fmt(item['risk_target'])} | {item['method_count']} | "
            f"{best_pass.get('method', 'n/a')} | {_fmt(best_pass.get('test_target_pass_rate'))} | "
            f"{best_cov.get('method', 'n/a')} | {_fmt(best_cov.get('mean_test_coverage'))} | "
            f"{_fmt(best_cov.get('mean_test_risk'))} |"
        )
    lines.extend(["", "## Claim Boundary", "", summary["claim_boundary"], ""])
    return "\n".join(lines)


def _target_summary(rows: Sequence[dict[str, Any]], risk_target: float) -> dict[str, Any]:
    target_rows = [row for row in rows if abs(float(row.get("risk_target", -1.0)) - float(risk_target)) < 1e-12]
    risk_valid_rows = [
        row
        for row in target_rows
        if row.get("mean_test_risk") is not None and float(row["mean_test_risk"]) <= float(risk_target) + 1e-12
    ]
    return {
        "risk_target": float(risk_target),
        "method_count": len(target_rows),
        "methods_with_nonzero_acceptance": sum(1 for row in target_rows if row.get("no_accept_rows", 0) < row.get("row_count", 0)),
        "methods_with_mean_risk_at_target": len(risk_valid_rows),
        "best_by_test_target_pass_rate": _best(
            target_rows,
            key="test_target_pass_rate",
        ),
        "best_mean_coverage_with_mean_risk_at_target": _best(
            risk_valid_rows,
            key="mean_test_coverage",
        ),
    }


def _best(rows: Sequence[dict[str, Any]], *, key: str) -> dict[str, Any] | None:
    valid = [row for row in rows if row.get(key) is not None]
    if not valid:
        return None
    row = max(valid, key=lambda item: float(item[key]))
    return {
        "method": row.get("method"),
        "row_count": row.get("row_count"),
        "test_target_pass_rate": row.get("test_target_pass_rate"),
        "mean_test_coverage": row.get("mean_test_coverage"),
        "mean_test_risk": row.get("mean_test_risk"),
        "no_accept_rows": row.get("no_accept_rows"),
    }


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
    args = parser.parse_args()

    summary = summarize_risk_control_abstention_baselines(args.input)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
