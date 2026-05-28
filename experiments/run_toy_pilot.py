#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Callable, Dict, List

from csrm_rag import (
    EvidenceDoc,
    EvidenceSet,
    QueryOrbit,
    area_under_risk_coverage,
    calibration_error,
    corm_max_score,
    corm_mean_score,
    csrm_score,
    naive_orbit_sufficiency,
    roc_auc,
    risk_coverage_curve,
    selective_risk_at_coverage,
    single_set_sufficiency,
)


def make_doc(
    rng: random.Random,
    doc_id: str,
    profile: str,
    high_corm: bool = True,
) -> EvidenceDoc:
    corm_base = rng.uniform(0.72, 0.96) if high_corm else rng.uniform(0.20, 0.55)
    if profile == "support":
        return EvidenceDoc(doc_id, "supporting evidence", corm_base, rng.uniform(0.72, 0.96), rng.uniform(0.0, 0.15), rng.uniform(0.0, 0.18))
    if profile == "partial":
        return EvidenceDoc(doc_id, "partial evidence", corm_base, rng.uniform(0.42, 0.62), rng.uniform(0.0, 0.20), rng.uniform(0.25, 0.50))
    if profile == "conflict":
        return EvidenceDoc(doc_id, "conflicting evidence", corm_base, rng.uniform(0.30, 0.58), rng.uniform(0.62, 0.92), rng.uniform(0.10, 0.35))
    if profile == "missing":
        return EvidenceDoc(doc_id, "topic match without key fact", corm_base, rng.uniform(0.15, 0.42), rng.uniform(0.0, 0.20), rng.uniform(0.62, 0.95))
    if profile == "distractor":
        return EvidenceDoc(doc_id, "relevant but non-supporting distractor", corm_base, rng.uniform(0.10, 0.36), rng.uniform(0.10, 0.34), rng.uniform(0.34, 0.70))
    raise ValueError(f"unknown profile: {profile}")


def make_set(
    rng: random.Random,
    orbit_id: str,
    suffix: str,
    split: str,
    profiles: List[str],
    label: bool,
    support_key: str,
    stable_doc_ids: bool = False,
) -> EvidenceSet:
    docs = [
        make_doc(rng, f"{orbit_id}-d{i}" if stable_doc_ids else f"{orbit_id}-{suffix}-d{i}", profile)
        for i, profile in enumerate(profiles)
    ]
    return EvidenceSet(
        query=f"{split} query {orbit_id} {suffix}",
        answer=f"answer {orbit_id}",
        docs=docs,
        label_answerable=label,
        split=split,
        metadata={"support_key": support_key},
    ).normalized()


def generate_orbits(n_per_split: int, seed: int) -> List[QueryOrbit]:
    rng = random.Random(seed)
    orbits: List[QueryOrbit] = []
    split_specs = {
        "stable_support": (["support", "support", "partial"], True),
        "fragile_support": (["support", "partial", "distractor"], False),
        "missing_hop": (["partial", "missing", "distractor"], False),
        "conflicting_evidence": (["support", "conflict", "partial"], False),
        "distractor": (["distractor", "distractor", "missing"], False),
    }
    for split, (clean_profiles, label) in split_specs.items():
        for idx in range(n_per_split):
            orbit_id = f"{split}-{idx}"
            clean = make_set(
                rng,
                orbit_id,
                "clean",
                split,
                clean_profiles,
                label,
                support_key=f"{orbit_id}:gold",
                stable_doc_ids=split == "stable_support",
            )
            if split == "stable_support":
                pert_profiles = [
                    ["support", "support", "partial"],
                    ["support", "partial", "support"],
                ]
                pert_label = True
                pert_keys = [f"{orbit_id}:gold", f"{orbit_id}:gold"]
                stable_doc_ids = True
            elif split == "fragile_support":
                pert_profiles = [
                    ["support", "support", "partial"],
                    ["support", "partial", "support"],
                ]
                pert_label = False
                pert_keys = [f"{orbit_id}:false-premise", f"{orbit_id}:false-premise"]
                stable_doc_ids = False
            elif split == "missing_hop":
                pert_profiles = [
                    ["partial", "missing", "missing"],
                    ["distractor", "missing", "partial"],
                ]
                pert_label = False
                pert_keys = [f"{orbit_id}:gold", f"{orbit_id}:gold"]
                stable_doc_ids = False
            elif split == "conflicting_evidence":
                pert_profiles = [
                    ["conflict", "conflict", "partial"],
                    ["support", "conflict", "distractor"],
                ]
                pert_label = False
                pert_keys = [f"{orbit_id}:gold", f"{orbit_id}:false-premise"]
                stable_doc_ids = False
            else:
                pert_profiles = [
                    ["distractor", "missing", "distractor"],
                    ["missing", "distractor", "partial"],
                ]
                pert_label = False
                pert_keys = [f"{orbit_id}:unknown", f"{orbit_id}:unknown"]
                stable_doc_ids = False
            perturbations = [
                make_set(
                    rng,
                    orbit_id,
                    f"p{i}",
                    split,
                    profiles,
                    pert_label,
                    support_key=pert_keys[i],
                    stable_doc_ids=stable_doc_ids,
                )
                for i, profiles in enumerate(pert_profiles)
            ]
            orbits.append(QueryOrbit(orbit_id, clean, perturbations))
    rng.shuffle(orbits)
    return orbits


def evaluate(orbits: List[QueryOrbit]) -> Dict[str, dict]:
    methods: Dict[str, Callable[[QueryOrbit], float]] = {
        "corm_max_clean": lambda orbit: corm_max_score(orbit.clean),
        "corm_mean_clean": lambda orbit: corm_mean_score(orbit.clean),
        "single_set_sure_style": lambda orbit: single_set_sufficiency(orbit.clean),
        "naive_orbit_average": naive_orbit_sufficiency,
        "csrm": csrm_score,
    }
    labels = [orbit.label_answerable for orbit in orbits]
    results: Dict[str, dict] = {}
    for name, scorer in methods.items():
        scores = [scorer(orbit) for orbit in orbits]
        correct = [(score >= 0.5) == label for score, label in zip(scores, labels)]
        results[name] = {
            "accuracy_at_0_5": sum(correct) / len(correct),
            "auroc": roc_auc(scores, labels),
            "aurc": area_under_risk_coverage(risk_coverage_curve(scores, labels)),
            "calibration": calibration_error(scores, labels, n_bins=10),
            "risk_at_30_coverage": selective_risk_at_coverage(scores, labels, 0.30),
            "risk_at_50_coverage": selective_risk_at_coverage(scores, labels, 0.50),
            "risk_at_70_coverage": selective_risk_at_coverage(scores, labels, 0.70),
            "mean_score_positive": _mean([s for s, y in zip(scores, labels) if y]),
            "mean_score_negative": _mean([s for s, y in zip(scores, labels) if not y]),
        }
    return results


def write_orbits(orbits: List[QueryOrbit], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for orbit in orbits:
            f.write(json.dumps(_orbit_to_dict(orbit), ensure_ascii=False) + "\n")


def _orbit_to_dict(orbit: QueryOrbit) -> dict:
    return {
        "orbit_id": orbit.orbit_id,
        "clean": _set_to_dict(orbit.clean),
        "perturbations": [_set_to_dict(item) for item in orbit.perturbations],
    }


def _set_to_dict(evidence_set: EvidenceSet) -> dict:
    return {
        "query": evidence_set.query,
        "answer": evidence_set.answer,
        "label_answerable": evidence_set.label_answerable,
        "split": evidence_set.split,
        "metadata": evidence_set.metadata,
        "docs": [
            {
                "doc_id": doc.doc_id,
                "text": doc.text,
                "corm_score": doc.corm_score,
                "support": doc.support,
                "conflict": doc.conflict,
                "missing": doc.missing,
            }
            for doc in evidence_set.docs
        ],
    }


def _mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-per-split", type=int, default=200)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output", type=Path, default=Path("results/toy_pilot.json"))
    parser.add_argument("--orbits-output", type=Path)
    args = parser.parse_args()

    orbits = generate_orbits(args.n_per_split, args.seed)
    if args.orbits_output:
        write_orbits(orbits, args.orbits_output)
    results = evaluate(orbits)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
