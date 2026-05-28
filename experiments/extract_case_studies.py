#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Iterable, List

from csrm_rag import (
    QueryOrbit,
    corm_max_score,
    csrm_score,
    naive_orbit_sufficiency,
    single_set_sufficiency,
)
from experiments.evaluate_orbits import load_orbits


Scorer = Callable[[QueryOrbit], float]


METHODS: dict[str, Scorer] = {
    "corm_max_clean": lambda orbit: corm_max_score(orbit.clean),
    "single_set_sure_style": lambda orbit: single_set_sufficiency(orbit.clean),
    "naive_orbit_average": naive_orbit_sufficiency,
    "csrm": csrm_score,
}


def extract_case_studies(
    input_path: Path,
    output_json: Path,
    output_md: Path,
    per_category: int,
    max_doc_chars: int,
) -> dict:
    orbits = load_orbits(input_path)
    rows = [_score_orbit(orbit) for orbit in orbits]
    thresholds = {
        name: _threshold_at_coverage([row["scores"][name] for row in rows], coverage=0.30)
        for name in METHODS
    }
    categories = {
        "naive_false_accept_csrm_reject": _top_cases(
            rows,
            lambda row: (
                not row["label"]
                and row["scores"]["naive_orbit_average"] >= thresholds["naive_orbit_average"]
                and row["scores"]["csrm"] < thresholds["csrm"]
            ),
            lambda row: row["scores"]["naive_orbit_average"] - row["scores"]["csrm"],
            per_category,
        ),
        "corm_false_accept_csrm_reject": _top_cases(
            rows,
            lambda row: (
                not row["label"]
                and row["scores"]["corm_max_clean"] >= thresholds["corm_max_clean"]
                and row["scores"]["csrm"] < thresholds["csrm"]
            ),
            lambda row: row["scores"]["corm_max_clean"] - row["scores"]["csrm"],
            per_category,
        ),
        "csrm_true_accept": _top_cases(
            rows,
            lambda row: row["label"] and row["scores"]["csrm"] >= thresholds["csrm"],
            lambda row: row["scores"]["csrm"],
            per_category,
        ),
        "csrm_false_accept_failure": _top_cases(
            rows,
            lambda row: (not row["label"]) and row["scores"]["csrm"] >= thresholds["csrm"],
            lambda row: row["scores"]["csrm"],
            per_category,
        ),
        "single_set_false_accept_csrm_reject": _top_cases(
            rows,
            lambda row: (
                not row["label"]
                and row["scores"]["single_set_sure_style"] >= thresholds["single_set_sure_style"]
                and row["scores"]["csrm"] < thresholds["csrm"]
            ),
            lambda row: row["scores"]["single_set_sure_style"] - row["scores"]["csrm"],
            per_category,
        ),
    }

    payload = {
        "input": str(input_path),
        "thresholds_at_30_coverage": thresholds,
        "case_counts": {name: len(items) for name, items in categories.items()},
        "categories": {
            name: [_case_payload(row["orbit"], row["scores"], max_doc_chars) for row in items]
            for name, items in categories.items()
        },
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    output_md.write_text(_markdown(payload), encoding="utf-8")
    return payload


def _score_orbit(orbit: QueryOrbit) -> dict:
    return {
        "orbit": orbit,
        "label": orbit.label_answerable,
        "scores": {name: scorer(orbit) for name, scorer in METHODS.items()},
    }


def _threshold_at_coverage(scores: List[float], coverage: float) -> float:
    if not scores:
        return 1.0
    ordered = sorted(scores, reverse=True)
    index = max(0, min(len(ordered) - 1, int(coverage * len(ordered)) - 1))
    return ordered[index]


def _top_cases(rows: Iterable[dict], predicate, key, limit: int) -> list[dict]:
    selected = [row for row in rows if predicate(row)]
    return sorted(selected, key=key, reverse=True)[:limit]


def _case_payload(orbit: QueryOrbit, scores: dict, max_doc_chars: int) -> dict:
    return {
        "orbit_id": orbit.orbit_id,
        "split": orbit.clean.split,
        "label_answerable": orbit.label_answerable,
        "answer": orbit.clean.answer,
        "scores": scores,
        "clean": _set_payload(orbit.clean, max_doc_chars),
        "perturbations": [_set_payload(item, max_doc_chars) for item in orbit.perturbations],
    }


def _set_payload(evidence_set, max_doc_chars: int) -> dict:
    return {
        "query": evidence_set.query,
        "label_answerable": evidence_set.label_answerable,
        "support_key": evidence_set.metadata.get("support_key"),
        "perturbation_type": evidence_set.metadata.get("perturbation_type"),
        "docs": [
            {
                "doc_id": doc.doc_id,
                "corm_score": doc.corm_score,
                "support": doc.support,
                "conflict": doc.conflict,
                "missing": doc.missing,
                "text": doc.text[:max_doc_chars],
            }
            for doc in evidence_set.docs[:3]
        ],
    }


def _markdown(payload: dict) -> str:
    lines = [
        "# Case Studies",
        "",
        f"Input: `{payload['input']}`",
        "",
        "Thresholds at 30% coverage:",
        "",
    ]
    for method, threshold in payload["thresholds_at_30_coverage"].items():
        lines.append(f"- `{method}`: {threshold:.6f}")
    lines.append("")

    for category, cases in payload["categories"].items():
        lines.extend([f"## {category}", ""])
        if not cases:
            lines.extend(["No cases found.", ""])
            continue
        for case in cases:
            lines.append(f"### {case['orbit_id']}")
            lines.append("")
            lines.append(f"- Split: `{case['split']}`")
            lines.append(f"- Label answerable: `{case['label_answerable']}`")
            lines.append(f"- Answer: `{case['answer']}`")
            score_text = ", ".join(
                f"{name}={value:.4f}" for name, value in sorted(case["scores"].items())
            )
            lines.append(f"- Scores: {score_text}")
            lines.append(f"- Clean query: {case['clean']['query']}")
            if case["perturbations"]:
                first = case["perturbations"][0]
                lines.append(f"- First perturbation: {first['query']}")
                lines.append(f"- First perturbation support key: `{first['support_key']}`")
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--per-category", type=int, default=3)
    parser.add_argument("--max-doc-chars", type=int, default=500)
    args = parser.parse_args()
    extract_case_studies(
        input_path=args.input,
        output_json=args.output_json,
        output_md=args.output_md,
        per_category=args.per_category,
        max_doc_chars=args.max_doc_chars,
    )


if __name__ == "__main__":
    main()
