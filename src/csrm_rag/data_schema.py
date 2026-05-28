from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .feature_firewall import assert_no_forbidden_features


@dataclass(frozen=True)
class OrbitRaw:
    orbit_id: str
    source_item_group_id: str
    dataset: str
    query: str
    candidate_answer: str
    clean_evidence: list[dict[str, Any]]
    perturbations: list[dict[str, Any]]
    retrieval_scores: list[float] = field(default_factory=list)
    generator_outputs: list[str] = field(default_factory=list)
    verifier_outputs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "orbit_id": self.orbit_id,
            "source_item_group_id": self.source_item_group_id,
            "dataset": self.dataset,
            "query": self.query,
            "candidate_answer": self.candidate_answer,
            "clean_evidence": self.clean_evidence,
            "perturbations": self.perturbations,
            "retrieval_scores": self.retrieval_scores,
            "generator_outputs": self.generator_outputs,
            "verifier_outputs": self.verifier_outputs,
        }
        assert_no_forbidden_features(payload)
        return payload


@dataclass(frozen=True)
class OrbitPrivateEvalOnly:
    orbit_id: str
    source_item_group_id: str
    dataset: str
    label_answerable: bool
    construction_type: str
    label_source: str
    gold_answer: str | None = None
    gold_supporting_facts: list[Any] = field(default_factory=list)
    gold_evidence_ids: list[str] = field(default_factory=list)
    heuristic_label: str | None = None
    human_label: str | None = None
    adjudicated_label: str | None = None
    support_key: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "orbit_id": self.orbit_id,
            "source_item_group_id": self.source_item_group_id,
            "dataset": self.dataset,
            "label_answerable": self.label_answerable,
            "construction_type": self.construction_type,
            "label_source": self.label_source,
            "gold_answer": self.gold_answer,
            "gold_supporting_facts": self.gold_supporting_facts,
            "gold_evidence_ids": self.gold_evidence_ids,
            "heuristic_label": self.heuristic_label,
            "human_label": self.human_label,
            "adjudicated_label": self.adjudicated_label,
            "support_key": self.support_key,
        }
