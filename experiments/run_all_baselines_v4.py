#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import area_under_risk_coverage, risk_coverage_curve, roc_auc, selective_risk_at_coverage
from csrm_rag.baselines import BaselineInputs, baseline_scores
from experiments.evaluate_orbits import load_orbits


def run_all_baselines_v4(
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    raw_rows = _read_jsonl(raw_path)
    private_rows = _read_jsonl(private_path)
    orbits = load_orbits(scored_path)
    if not (len(raw_rows) == len(private_rows) == len(orbits)):
        raise ValueError("raw, private, and scored files must have the same number of rows")
    for index, (raw, private, orbit) in enumerate(zip(raw_rows, private_rows, orbits)):
        if raw["orbit_id"] != private["orbit_id"] or raw["orbit_id"] != orbit.orbit_id:
            raise ValueError(f"row {index} has misaligned orbit_id values")

    labels = [bool(row["label_answerable"]) for row in private_rows]
    groups = [str(row.get("source_item_group_id") or row["orbit_id"]) for row in raw_rows]
    scores = baseline_scores(BaselineInputs(orbits=orbits, labels=labels, groups=groups))
    methods = {name: _metrics(values, labels) for name, values in sorted(scores.items())}
    strongest = _strongest_non_csrm(methods)
    result = {
        "raw_input": str(raw_path),
        "private_input": str(private_path),
        "scored_input": str(scored_path),
        "n": len(orbits),
        "positive": int(sum(labels)),
        "negative": int(len(labels) - sum(labels)),
        "source_item_groups": len(set(groups)),
        "methods": methods,
        "strongest_non_csrm": strongest,
        "csrm_vs_strongest_non_csrm": {
            metric: _delta(methods["csrm_rule"], item["metrics"])
            for metric, item in strongest.items()
        },
        "fairness": {
            "same_input_rows": True,
            "same_scored_evidence": True,
            "logistic_scores": "out-of-fold by source_item_group_id when possible",
            "llm_judge": "not run; no external LLM calls in this baseline batch",
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


def _metrics(scores: Sequence[float], labels: Sequence[bool]) -> dict[str, Any]:
    return {
        "auroc": _safe_auc(scores, labels),
        "risk_at_30": selective_risk_at_coverage(scores, labels, 0.30)["risk"],
        "risk_at_50": selective_risk_at_coverage(scores, labels, 0.50)["risk"],
        "risk_at_70": selective_risk_at_coverage(scores, labels, 0.70)["risk"],
        "aurc": area_under_risk_coverage(risk_coverage_curve(scores, labels)),
        "score_summary": {
            "min": min(scores),
            "mean": sum(scores) / len(scores),
            "max": max(scores),
            "unique": len(set(round(float(score), 10) for score in scores)),
        },
    }


def _strongest_non_csrm(methods: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    candidates = {name: metrics for name, metrics in methods.items() if name != "csrm_rule"}
    by_aurc = min(candidates.items(), key=lambda item: (item[1]["aurc"], item[0]))
    by_risk30 = min(candidates.items(), key=lambda item: (item[1]["risk_at_30"], item[1]["aurc"], item[0]))
    by_auroc = max(
        candidates.items(),
        key=lambda item: (-1.0 if item[1]["auroc"] is None else item[1]["auroc"], -item[1]["aurc"]),
    )
    return {
        "by_aurc": {"method": by_aurc[0], "metrics": by_aurc[1]},
        "by_risk_at_30": {"method": by_risk30[0], "metrics": by_risk30[1]},
        "by_auroc": {"method": by_auroc[0], "metrics": by_auroc[1]},
    }


def _delta(csrm: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    return {
        "auroc_improvement": _none_delta(csrm["auroc"], baseline["auroc"]),
        "risk_at_30_reduction": baseline["risk_at_30"] - csrm["risk_at_30"],
        "risk_at_50_reduction": baseline["risk_at_50"] - csrm["risk_at_50"],
        "aurc_reduction": baseline["aurc"] - csrm["aurc"],
    }


def _safe_auc(scores: Sequence[float], labels: Sequence[bool]) -> float | None:
    try:
        return roc_auc(scores, labels)
    except ValueError:
        return None


def _none_delta(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    return left - right


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no} is not valid JSON") from exc
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--scored", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = run_all_baselines_v4(args.raw, args.private, args.scored, args.output)
    compact = {
        "output": str(args.output),
        "n": result["n"],
        "strongest_non_csrm": {
            metric: item["method"] for metric, item in result["strongest_non_csrm"].items()
        },
        "csrm_vs_strongest_non_csrm": result["csrm_vs_strongest_non_csrm"],
    }
    print(json.dumps(compact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
