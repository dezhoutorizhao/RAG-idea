from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .stress_split import EvidenceSet, QueryOrbit


@dataclass(frozen=True)
class CSRMWeights:
    clean_sufficiency: float = 0.15
    mean_sufficiency: float = 0.05
    worst_sufficiency: float = 0.35
    stability: float = 0.10
    conflict_monotonicity: float = 0.10
    answer_consistency: float = 0.20
    overlap: float = 0.05

    def normalized(self) -> "CSRMWeights":
        total = (
            self.clean_sufficiency
            + self.mean_sufficiency
            + self.worst_sufficiency
            + self.stability
            + self.conflict_monotonicity
            + self.answer_consistency
            + self.overlap
        )
        if total <= 0:
            raise ValueError("at least one CSRM weight must be positive")
        return CSRMWeights(
            clean_sufficiency=self.clean_sufficiency / total,
            mean_sufficiency=self.mean_sufficiency / total,
            worst_sufficiency=self.worst_sufficiency / total,
            stability=self.stability / total,
            conflict_monotonicity=self.conflict_monotonicity / total,
            answer_consistency=self.answer_consistency / total,
            overlap=self.overlap / total,
        )


@dataclass(frozen=True)
class CSRMComponents:
    clean_sufficiency: float
    mean_sufficiency: float
    worst_sufficiency: float
    stability: float
    conflict_monotonicity: float
    answer_consistency: float
    overlap: float


def corm_max_score(evidence_set: EvidenceSet) -> float:
    if not evidence_set.docs:
        return 0.0
    return float(max(doc.corm_score for doc in evidence_set.docs))


def corm_mean_score(evidence_set: EvidenceSet) -> float:
    if not evidence_set.docs:
        return 0.0
    return float(np.mean([doc.corm_score for doc in evidence_set.docs]))


def single_set_sufficiency(evidence_set: EvidenceSet) -> float:
    if not evidence_set.docs:
        return 0.0
    support = max(doc.support for doc in evidence_set.docs)
    mean_support = float(np.mean([doc.support for doc in evidence_set.docs]))
    conflict = max(doc.conflict for doc in evidence_set.docs)
    missing = float(np.mean([doc.missing for doc in evidence_set.docs]))
    score = 0.55 * support + 0.20 * mean_support - 0.15 * conflict - 0.10 * missing
    return _clip01(score)


def naive_orbit_sufficiency(orbit: QueryOrbit) -> float:
    return float(np.mean([single_set_sufficiency(item) for item in orbit.all_sets]))


def csrm_score(orbit: QueryOrbit, weights: CSRMWeights | None = None) -> float:
    weights = (weights or CSRMWeights()).normalized()
    components = csrm_components(orbit)
    score = (
        weights.clean_sufficiency * components.clean_sufficiency
        + weights.mean_sufficiency * components.mean_sufficiency
        + weights.worst_sufficiency * components.worst_sufficiency
        + weights.stability * components.stability
        + weights.conflict_monotonicity * components.conflict_monotonicity
        + weights.answer_consistency * components.answer_consistency
        + weights.overlap * components.overlap
    )
    return _clip01(score)


def csrm_components(orbit: QueryOrbit) -> CSRMComponents:
    set_scores = [single_set_sufficiency(item) for item in orbit.all_sets]
    return CSRMComponents(
        clean_sufficiency=set_scores[0],
        mean_sufficiency=float(np.mean(set_scores)),
        worst_sufficiency=float(min(set_scores)),
        stability=_clip01(1.0 - float(np.std(set_scores))),
        conflict_monotonicity=_conflict_monotonicity(orbit),
        answer_consistency=_answer_consistency(orbit),
        overlap=_mean_doc_overlap(orbit),
    )


def _conflict_monotonicity(orbit: QueryOrbit) -> float:
    clean_conflict = _max_conflict(orbit.clean)
    if not orbit.perturbations:
        return 1.0
    penalties = []
    for item in orbit.perturbations:
        pert_conflict = _max_conflict(item)
        pert_support = single_set_sufficiency(item)
        clean_support = single_set_sufficiency(orbit.clean)
        support_drop = max(0.0, clean_support - pert_support)
        conflict_rise = max(0.0, pert_conflict - clean_conflict)
        penalties.append(max(support_drop, conflict_rise))
    return _clip01(1.0 - float(np.mean(penalties)))


def _mean_doc_overlap(orbit: QueryOrbit) -> float:
    clean_ids = {doc.doc_id for doc in orbit.clean.docs}
    if not clean_ids or not orbit.perturbations:
        return 1.0
    overlaps = []
    for item in orbit.perturbations:
        pert_ids = {doc.doc_id for doc in item.docs}
        union = clean_ids | pert_ids
        overlaps.append(len(clean_ids & pert_ids) / len(union) if union else 1.0)
    return float(np.mean(overlaps))


def _answer_consistency(orbit: QueryOrbit) -> float:
    clean_key = orbit.clean.metadata.get("support_key", orbit.clean.answer)
    if not orbit.perturbations:
        return 1.0
    matches = []
    for item in orbit.perturbations:
        pert_key = item.metadata.get("support_key", item.answer)
        matches.append(1.0 if pert_key == clean_key else 0.0)
    return float(np.mean(matches))


def _max_conflict(evidence_set: EvidenceSet) -> float:
    if not evidence_set.docs:
        return 0.0
    return float(max(doc.conflict for doc in evidence_set.docs))


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
