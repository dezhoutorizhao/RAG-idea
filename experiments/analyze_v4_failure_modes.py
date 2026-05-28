#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import roc_auc, selective_risk_at_coverage
from csrm_rag.baselines.v4_baselines import _orbit_features
from csrm_rag.calibration import OrbitRiskCalibrator, csrm_v4_feature_names, csrm_v4_features, split_groups
from csrm_rag.feature_firewall import assert_no_forbidden_features
from experiments.evaluate_orbits import load_orbits


def analyze_v4_failure_modes(
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_json: Path,
    output_markdown: Path,
    *,
    seed: int = 31,
    train_frac: float = 0.60,
    cal_frac: float = 0.20,
    top_k: int = 8,
) -> dict[str, Any]:
    raw_rows = _read_jsonl(raw_path)
    private_rows = _read_jsonl(private_path)
    orbits = load_orbits(scored_path)
    if not (len(raw_rows) == len(private_rows) == len(orbits)):
        raise ValueError("raw, private, and scored files must have the same number of rows")
    for index, (raw, private, orbit) in enumerate(zip(raw_rows, private_rows, orbits)):
        assert_no_forbidden_features(raw)
        if raw["orbit_id"] != private["orbit_id"] or raw["orbit_id"] != orbit.orbit_id:
            raise ValueError(f"row {index} has misaligned orbit_id values")

    labels = [bool(row["label_answerable"]) for row in private_rows]
    groups = [str(row.get("source_item_group_id") or row["orbit_id"]) for row in raw_rows]
    split = split_groups(groups, labels, train_frac=train_frac, cal_frac=cal_frac, seed=seed)

    train_orbits = [orbits[index] for index in split.train]
    train_labels = [labels[index] for index in split.train]
    cal_orbits = [orbits[index] for index in split.calibration]
    cal_labels = [labels[index] for index in split.calibration]
    test_indices = split.test
    test_orbits = [orbits[index] for index in test_indices]
    test_labels = [labels[index] for index in test_indices]

    target_model = OrbitRiskCalibrator(random_state=seed).fit(
        train_orbits,
        train_labels,
        calibration_orbits=cal_orbits,
        calibration_labels=cal_labels,
    )
    baseline_model = _fit_orbit_baseline(train_orbits, train_labels)
    target_scores = target_model.predict_logistic(test_orbits)
    baseline_scores = baseline_model.predict_proba(
        np.asarray([_orbit_features(orbit) for orbit in test_orbits], dtype=float)
    )[:, 1].tolist()

    cases = []
    for local_index, global_index in enumerate(test_indices):
        raw = raw_rows[global_index]
        private = private_rows[global_index]
        orbit = orbits[global_index]
        label = labels[global_index]
        target_score = target_scores[local_index]
        baseline_score = baseline_scores[local_index]
        features = dict(zip(csrm_v4_feature_names(), csrm_v4_features(orbit)))
        cases.append(
            {
                "orbit_id": raw["orbit_id"],
                "source_item_group_id": raw["source_item_group_id"],
                "dataset": raw.get("dataset"),
                "query": raw.get("query"),
                "candidate_answer": raw.get("candidate_answer"),
                "label_answerable": label,
                "construction_type": private.get("construction_type"),
                "target_score": target_score,
                "baseline_score": baseline_score,
                "score_gap_target_minus_baseline": target_score - baseline_score,
                "features": features,
                "clean_evidence": raw.get("clean_evidence") or [],
                "perturbations": raw.get("perturbations") or [],
            }
        )

    result = {
        "raw_input": str(raw_path),
        "private_input": str(private_path),
        "scored_input": str(scored_path),
        "seed": seed,
        "split_sizes": {
            "train": len(split.train),
            "calibration": len(split.calibration),
            "test": len(split.test),
            "train_groups": len(split.train_groups),
            "calibration_groups": len(split.calibration_groups),
            "test_groups": len(split.test_groups),
        },
        "metrics": {
            "target": _metrics(target_scores, test_labels),
            "baseline_calibrated_logistic_orbit": _metrics(baseline_scores, test_labels),
        },
        "by_construction_type": _by_category(cases, "construction_type"),
        "feature_gaps": _feature_gaps(cases),
        "top_cases": {
            "target_high_false_positive": _strip_case_docs(
                sorted([case for case in cases if not case["label_answerable"]], key=lambda item: item["target_score"], reverse=True)[:top_k]
            ),
            "target_low_false_negative": _strip_case_docs(
                sorted([case for case in cases if case["label_answerable"]], key=lambda item: item["target_score"])[:top_k]
            ),
            "target_over_baseline_on_negative": _strip_case_docs(
                sorted([case for case in cases if not case["label_answerable"]], key=lambda item: item["score_gap_target_minus_baseline"], reverse=True)[:top_k]
            ),
            "baseline_over_target_on_positive": _strip_case_docs(
                sorted([case for case in cases if case["label_answerable"]], key=lambda item: item["score_gap_target_minus_baseline"])[:top_k]
            ),
        },
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    output_markdown.write_text(_render_markdown(result, cases, top_k), encoding="utf-8")
    return result


def _fit_orbit_baseline(train_orbits, train_labels):
    y = np.asarray(train_labels, dtype=bool)
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, class_weight="balanced", random_state=0),
    )
    model.fit(np.asarray([_orbit_features(orbit) for orbit in train_orbits], dtype=float), y)
    return model


def _metrics(scores: Sequence[float], labels: Sequence[bool]) -> dict[str, Any]:
    return {
        "auroc": _safe_auc(scores, labels),
        "risk_at_30": selective_risk_at_coverage(scores, labels, 0.30)["risk"],
        "risk_at_50": selective_risk_at_coverage(scores, labels, 0.50)["risk"],
        "mean_score_positive": _mean([score for score, label in zip(scores, labels) if label]),
        "mean_score_negative": _mean([score for score, label in zip(scores, labels) if not label]),
    }


def _by_category(cases: Sequence[dict[str, Any]], key: str) -> dict[str, Any]:
    output = {}
    for case in cases:
        category = str(case.get(key) or "unknown")
        output.setdefault(category, []).append(case)
    return {
        category: {
            "n": len(rows),
            "positive": sum(row["label_answerable"] for row in rows),
            "negative": sum(not row["label_answerable"] for row in rows),
            "target_mean": _mean([row["target_score"] for row in rows]),
            "baseline_mean": _mean([row["baseline_score"] for row in rows]),
            "target_minus_baseline_mean": _mean([row["score_gap_target_minus_baseline"] for row in rows]),
        }
        for category, rows in sorted(output.items())
    }


def _feature_gaps(cases: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    names = csrm_v4_feature_names()
    positives = [case for case in cases if case["label_answerable"]]
    negatives = [case for case in cases if not case["label_answerable"]]
    rows = []
    for name in names:
        pos_mean = _mean([case["features"][name] for case in positives])
        neg_mean = _mean([case["features"][name] for case in negatives])
        rows.append(
            {
                "feature": name,
                "positive_mean": pos_mean,
                "negative_mean": neg_mean,
                "positive_minus_negative": pos_mean - neg_mean,
                "absolute_gap": abs(pos_mean - neg_mean),
            }
        )
    return sorted(rows, key=lambda item: item["absolute_gap"], reverse=True)


def _strip_case_docs(cases: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    keep = []
    for case in cases:
        keep.append(
            {
                key: value
                for key, value in case.items()
                if key not in {"clean_evidence", "perturbations", "features"}
            }
            | {
                "top_features": sorted(
                    [
                        {"feature": name, "value": value}
                        for name, value in case["features"].items()
                    ],
                    key=lambda item: abs(float(item["value"])),
                    reverse=True,
                )[:6]
            }
        )
    return keep


def _render_markdown(result: dict[str, Any], cases: Sequence[dict[str, Any]], top_k: int) -> str:
    lines = [
        "# V4 Failure Analysis",
        "",
        f"Seed: `{result['seed']}`",
        "",
        "## Metrics",
        "",
        "| Method | AUROC | Risk@30 | Risk@50 | Mean positive score | Mean negative score |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, metrics in result["metrics"].items():
        lines.append(
            f"| {name} | {_fmt(metrics['auroc'])} | {_fmt(metrics['risk_at_30'])} | {_fmt(metrics['risk_at_50'])} | {_fmt(metrics['mean_score_positive'])} | {_fmt(metrics['mean_score_negative'])} |"
        )
    lines.extend(["", "## Construction Types", ""])
    lines.append("| Type | n | positive | negative | target mean | baseline mean | target-baseline |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for category, item in result["by_construction_type"].items():
        lines.append(
            f"| {category} | {item['n']} | {item['positive']} | {item['negative']} | {_fmt(item['target_mean'])} | {_fmt(item['baseline_mean'])} | {_fmt(item['target_minus_baseline_mean'])} |"
        )
    lines.extend(["", "## Largest Feature Gaps", ""])
    lines.append("| Feature | positive mean | negative mean | gap |")
    lines.append("|---|---:|---:|---:|")
    for item in result["feature_gaps"][:12]:
        lines.append(
            f"| {item['feature']} | {_fmt(item['positive_mean'])} | {_fmt(item['negative_mean'])} | {_fmt(item['positive_minus_negative'])} |"
        )
    lines.extend(["", "## Case Gallery", ""])
    buckets = [
        ("High-scoring false positives", sorted([case for case in cases if not case["label_answerable"]], key=lambda item: item["target_score"], reverse=True)[:top_k]),
        ("Low-scoring false negatives", sorted([case for case in cases if case["label_answerable"]], key=lambda item: item["target_score"])[:top_k]),
        ("Target over baseline on negatives", sorted([case for case in cases if not case["label_answerable"]], key=lambda item: item["score_gap_target_minus_baseline"], reverse=True)[:top_k]),
        ("Baseline over target on positives", sorted([case for case in cases if case["label_answerable"]], key=lambda item: item["score_gap_target_minus_baseline"])[:top_k]),
    ]
    for title, rows in buckets:
        lines.extend(["", f"### {title}", ""])
        for case in rows:
            lines.extend(_render_case(case))
    return "\n".join(lines) + "\n"


def _render_case(case: dict[str, Any]) -> list[str]:
    lines = [
        f"#### {case['orbit_id']}",
        "",
        f"- label_answerable: `{case['label_answerable']}`",
        f"- construction_type: `{case['construction_type']}`",
        f"- target_score: `{case['target_score']:.4f}`",
        f"- baseline_score: `{case['baseline_score']:.4f}`",
        f"- target_minus_baseline: `{case['score_gap_target_minus_baseline']:.4f}`",
        f"- query: {case['query']}",
        f"- candidate_answer: `{case['candidate_answer']}`",
        "",
        "Clean evidence:",
    ]
    for doc in (case.get("clean_evidence") or [])[:2]:
        lines.append(f"- `{doc.get('title') or doc.get('doc_id')}`: {_short(doc.get('text') or '')}")
    lines.append("")
    lines.append("First perturbation evidence:")
    perturbations = case.get("perturbations") or []
    if perturbations:
        lines.append(f"- query: {perturbations[0].get('query')}")
        for doc in (perturbations[0].get("evidence") or [])[:2]:
            lines.append(f"- `{doc.get('title') or doc.get('doc_id')}`: {_short(doc.get('text') or '')}")
    else:
        lines.append("- none")
    lines.append("")
    return lines


def _safe_auc(scores: Sequence[float], labels: Sequence[bool]) -> float | None:
    try:
        return roc_auc(scores, labels)
    except ValueError:
        return None


def _mean(values: Sequence[float]) -> float:
    return float(np.mean(values)) if values else 0.0


def _fmt(value: float | None) -> str:
    if value is None:
        return ""
    return f"{float(value):.4f}"


def _short(text: str, limit: int = 260) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


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
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-markdown", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=31)
    parser.add_argument("--train-frac", type=float, default=0.60)
    parser.add_argument("--cal-frac", type=float, default=0.20)
    parser.add_argument("--top-k", type=int, default=8)
    args = parser.parse_args()

    result = analyze_v4_failure_modes(
        args.raw,
        args.private,
        args.scored,
        args.output_json,
        args.output_markdown,
        seed=args.seed,
        train_frac=args.train_frac,
        cal_frac=args.cal_frac,
        top_k=args.top_k,
    )
    compact = {
        "output_json": str(args.output_json),
        "output_markdown": str(args.output_markdown),
        "seed": result["seed"],
        "metrics": result["metrics"],
    }
    print(json.dumps(compact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
