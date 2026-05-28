from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class EvidenceDoc:
    doc_id: str
    text: str
    corm_score: float
    support: float
    conflict: float
    missing: float

    def clipped(self) -> "EvidenceDoc":
        return EvidenceDoc(
            doc_id=self.doc_id,
            text=self.text,
            corm_score=_clip01(self.corm_score),
            support=_clip01(self.support),
            conflict=_clip01(self.conflict),
            missing=_clip01(self.missing),
        )


@dataclass(frozen=True)
class EvidenceSet:
    query: str
    answer: str
    docs: List[EvidenceDoc]
    label_answerable: bool | None
    split: str
    metadata: Dict[str, str] = field(default_factory=dict)

    def normalized(self) -> "EvidenceSet":
        return EvidenceSet(
            query=self.query,
            answer=self.answer,
            docs=[doc.clipped() for doc in self.docs],
            label_answerable=self.label_answerable,
            split=self.split,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class QueryOrbit:
    orbit_id: str
    clean: EvidenceSet
    perturbations: List[EvidenceSet]

    @property
    def all_sets(self) -> List[EvidenceSet]:
        return [self.clean, *self.perturbations]

    @property
    def label_answerable(self) -> bool:
        if self.clean.label_answerable is None:
            return False
        return self.clean.label_answerable and all(
            item.label_answerable is True for item in self.perturbations
        )


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
