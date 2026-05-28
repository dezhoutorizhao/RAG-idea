#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Callable, Dict, List

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import (
    CSRMWeights,
    EvidenceDoc,
    EvidenceSet,
    QueryOrbit,
    area_under_risk_coverage,
    calibration_error,
    corm_max_score,
    corm_mean_score,
    csrm_components,
    csrm_score,
    naive_orbit_sufficiency,
    roc_auc,
    risk_coverage_curve,
    selective_risk_at_coverage,
    single_set_sufficiency,
)


def load_orbits(path: Path) -> List[QueryOrbit]:
    orbits = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            raw = json.loads(line)
            try:
                default_split = str(raw.get("split") or "unknown")
                clean = _load_set(raw["clean"], default_split=default_split)
                perturbations = [
                    _load_set(item, default_split=default_split)
                    for item in raw.get("perturbations", [])
                ]
                orbits.append(QueryOrbit(str(raw["orbit_id"]), clean, perturbations))
            except KeyError as exc:
                raise ValueError(f"{path}:{line_no} missing key {exc}") from exc
    return orbits


def evaluate(
    orbits: List[QueryOrbit],
    bootstrap_samples: int = 200,
    bootstrap_seed: int = 13,
) -> Dict[str, dict]:
    labeled = [orbit for orbit in orbits if orbit.clean.label_answerable is not None]
    if not labeled:
        raise ValueError("no labeled orbits found; label_answerable is required")

    labels = [orbit.label_answerable for orbit in labeled]
    methods: Dict[str, Callable[[QueryOrbit], float]] = {
        "corm_max_clean": lambda orbit: corm_max_score(orbit.clean),
        "corm_mean_clean": lambda orbit: corm_mean_score(orbit.clean),
    }
    if _has_verifier_fields(labeled):
        shuffled = _shuffled_perturbation_orbits(labeled)
        methods.update(
            {
                "single_set_sure_style": lambda orbit: single_set_sufficiency(orbit.clean),
                "naive_orbit_average": naive_orbit_sufficiency,
                "csrm": csrm_score,
                "csrm_no_stability": lambda orbit: csrm_score(
                    orbit, CSRMWeights(stability=0.0)
                ),
                "csrm_no_worst_sufficiency": lambda orbit: csrm_score(
                    orbit, CSRMWeights(worst_sufficiency=0.0)
                ),
                "csrm_no_conflict_monotonicity": lambda orbit: csrm_score(
                    orbit, CSRMWeights(conflict_monotonicity=0.0)
                ),
                "csrm_no_answer_consistency": lambda orbit: csrm_score(
                    orbit, CSRMWeights(answer_consistency=0.0)
                ),
                "csrm_no_overlap": lambda orbit: csrm_score(
                    orbit, CSRMWeights(overlap=0.0)
                ),
                "csrm_first_perturbation_only": lambda orbit: csrm_score(
                    _first_perturbation_orbit(orbit)
                ),
                "csrm_shuffled_perturbations": lambda orbit: csrm_score(
                    shuffled[orbit.orbit_id]
                ),
            }
        )

    results = {}
    for name, scorer in methods.items():
        scores = [scorer(orbit) for orbit in labeled]
        results[name] = _evaluate_scores(scores, labels)
        if bootstrap_samples > 0:
            results[name]["bootstrap_ci"] = _bootstrap_ci(
                scores, labels, bootstrap_samples, bootstrap_seed
            )

    payload = {
        "summary": results,
        "splits": _split_summary(labeled),
        "per_split": _per_split_results(labeled, methods),
    }
    if _has_verifier_fields(labeled):
        payload["csrm_components"] = _component_summary(labeled)
    return payload


def _load_set(raw: dict, *, default_split: str = "unknown") -> EvidenceSet:
    docs = []
    for doc in raw.get("docs", []):
        docs.append(
            EvidenceDoc(
                doc_id=str(doc["doc_id"]),
                text=str(doc.get("text", "")),
                corm_score=float(doc.get("corm_score") or 0.0),
                support=float(doc.get("support") or 0.0),
                conflict=float(doc.get("conflict") or 0.0),
                missing=float(doc.get("missing") or 0.0),
            ).clipped()
        )
    return EvidenceSet(
        query=str(raw.get("query") or ""),
        answer=str(raw.get("answer") or ""),
        docs=docs,
        label_answerable=raw.get("label_answerable"),
        split=str(raw.get("split") or default_split),
        metadata=dict(raw.get("metadata") or {}),
    )


def _has_verifier_fields(orbits: List[QueryOrbit]) -> bool:
    for orbit in orbits:
        for item in orbit.all_sets:
            for doc in item.docs:
                if doc.support != 0.0 or doc.conflict != 0.0 or doc.missing != 0.0:
                    return True
    return False


def _evaluate_scores(scores: List[float], labels: List[bool]) -> dict:
    correct = [(score >= 0.5) == label for score, label in zip(scores, labels)]
    curve = risk_coverage_curve(scores, labels)
    return {
        "n": len(labels),
        "positive": int(sum(labels)),
        "negative": int(len(labels) - sum(labels)),
        "accuracy_at_0_5": sum(correct) / len(correct),
        "auroc": _safe_roc_auc(scores, labels),
        "aurc": area_under_risk_coverage(curve),
        "calibration": calibration_error(scores, labels),
        "risk_at_30_coverage": selective_risk_at_coverage(scores, labels, 0.30),
        "risk_at_50_coverage": selective_risk_at_coverage(scores, labels, 0.50),
        "risk_at_70_coverage": selective_risk_at_coverage(scores, labels, 0.70),
    }


def _safe_roc_auc(scores: List[float], labels: List[bool]) -> float | None:
    try:
        return roc_auc(scores, labels)
    except ValueError:
        return None


def _bootstrap_ci(
    scores: List[float],
    labels: List[bool],
    samples: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    n = len(labels)
    aurocs = []
    risks_30 = []
    aurcs = []
    for _ in range(samples):
        idx = [rng.randrange(n) for _ in range(n)]
        boot_scores = [scores[i] for i in idx]
        boot_labels = [labels[i] for i in idx]
        auc = _safe_roc_auc(boot_scores, boot_labels)
        if auc is not None:
            aurocs.append(auc)
        risks_30.append(selective_risk_at_coverage(boot_scores, boot_labels, 0.30)["risk"])
        aurcs.append(area_under_risk_coverage(risk_coverage_curve(boot_scores, boot_labels)))
    return {
        "auroc": _percentile_ci(aurocs),
        "risk_at_30_coverage": _percentile_ci(risks_30),
        "aurc": _percentile_ci(aurcs),
        "samples": samples,
        "seed": seed,
    }


def _percentile_ci(values: List[float]) -> dict | None:
    if not values:
        return None
    ordered = sorted(values)
    lo = ordered[int(0.025 * (len(ordered) - 1))]
    mid = ordered[int(0.500 * (len(ordered) - 1))]
    hi = ordered[int(0.975 * (len(ordered) - 1))]
    return {"p2_5": lo, "median": mid, "p97_5": hi}


def _split_summary(orbits: List[QueryOrbit]) -> dict:
    summary: Dict[str, dict] = {}
    for orbit in orbits:
        split = orbit.clean.split
        item = summary.setdefault(split, {"n": 0, "positive": 0, "negative": 0})
        item["n"] += 1
        if orbit.label_answerable:
            item["positive"] += 1
        else:
            item["negative"] += 1
    return summary


def _per_split_results(
    orbits: List[QueryOrbit],
    methods: Dict[str, Callable[[QueryOrbit], float]],
) -> dict:
    by_split: Dict[str, List[QueryOrbit]] = {}
    for orbit in orbits:
        by_split.setdefault(orbit.clean.split, []).append(orbit)

    output = {}
    for split, split_orbits in by_split.items():
        labels = [orbit.label_answerable for orbit in split_orbits]
        output[split] = {}
        for name, scorer in methods.items():
            scores = [scorer(orbit) for orbit in split_orbits]
            output[split][name] = _evaluate_scores(scores, labels)
    return output


def _component_summary(orbits: List[QueryOrbit]) -> dict:
    fields = [
        "clean_sufficiency",
        "mean_sufficiency",
        "worst_sufficiency",
        "stability",
        "conflict_monotonicity",
        "answer_consistency",
        "overlap",
    ]
    groups = {
        "all": orbits,
        "positive": [orbit for orbit in orbits if orbit.label_answerable],
        "negative": [orbit for orbit in orbits if not orbit.label_answerable],
    }
    summary = {}
    for group_name, group_orbits in groups.items():
        summary[group_name] = {"n": len(group_orbits)}
        if not group_orbits:
            continue
        component_values = [csrm_components(orbit) for orbit in group_orbits]
        for field in fields:
            values = [getattr(item, field) for item in component_values]
            summary[group_name][field] = sum(values) / len(values)
    return summary


def _first_perturbation_orbit(orbit: QueryOrbit) -> QueryOrbit:
    if not orbit.perturbations:
        return orbit
    return QueryOrbit(orbit.orbit_id, orbit.clean, [orbit.perturbations[0]])


def _shuffled_perturbation_orbits(orbits: List[QueryOrbit]) -> dict[str, QueryOrbit]:
    if len(orbits) < 2:
        return {orbit.orbit_id: orbit for orbit in orbits}
    ordered = sorted(orbits, key=lambda orbit: orbit.orbit_id)
    rotated = ordered[1:] + ordered[:1]
    return {
        orbit.orbit_id: QueryOrbit(
            orbit.orbit_id,
            orbit.clean,
            donor.perturbations,
        )
        for orbit, donor in zip(ordered, rotated)
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-samples", type=int, default=200)
    parser.add_argument("--bootstrap-seed", type=int, default=13)
    args = parser.parse_args()

    results = evaluate(
        load_orbits(args.input),
        bootstrap_samples=args.bootstrap_samples,
        bootstrap_seed=args.bootstrap_seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
