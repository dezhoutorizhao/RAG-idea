from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


FORBIDDEN_KEYS = {
    "gold",
    "gold_answer",
    "gold_support",
    "gold_supporting_facts",
    "gold_evidence_ids",
    "gold_doc_ids",
    "support_key",
    "is_support",
    "has_answer",
    "label",
    "label_answerable",
    "heuristic_label",
    "human_label",
    "adjudicated_label",
    "construction_type",
    "perturbation_type",
    "near_miss_type",
    "source_split",
    "split",
}


def assert_no_forbidden_features(obj: Any, path: str = "root") -> None:
    """Reject oracle/evaluation fields before data reaches a scorer."""
    if isinstance(obj, Mapping):
        for key, value in obj.items():
            key_text = str(key)
            if key_text in FORBIDDEN_KEYS or key_text.startswith("gold_"):
                raise ValueError(f"Forbidden oracle feature at {path}.{key_text}")
            assert_no_forbidden_features(value, f"{path}.{key_text}")
        return

    if isinstance(obj, (str, bytes)):
        return

    if isinstance(obj, Sequence):
        for index, value in enumerate(obj):
            assert_no_forbidden_features(value, f"{path}[{index}]")


def strip_forbidden_features(obj: Any) -> Any:
    """Return a deep copy with forbidden keys removed from nested mappings."""
    if isinstance(obj, Mapping):
        return {
            str(key): strip_forbidden_features(value)
            for key, value in obj.items()
            if str(key) not in FORBIDDEN_KEYS and not str(key).startswith("gold_")
        }

    if isinstance(obj, (str, bytes)):
        return obj

    if isinstance(obj, Sequence):
        return [strip_forbidden_features(value) for value in obj]

    return obj
