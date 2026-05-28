from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .data_schema import OrbitPrivateEvalOnly, OrbitRaw
from .feature_firewall import assert_no_forbidden_features


def legacy_orbit_to_v4(raw_orbit: dict, dataset: str) -> tuple[dict, dict]:
    orbit_id = str(raw_orbit["orbit_id"])
    source_item_group_id = orbit_id.rsplit(":", 1)[0]
    clean = raw_orbit["clean"]
    perturbations = list(raw_orbit.get("perturbations") or [])
    construction_type = orbit_id.rsplit(":", 1)[-1]

    raw = OrbitRaw(
        orbit_id=orbit_id,
        source_item_group_id=source_item_group_id,
        dataset=dataset,
        query=str(clean.get("query") or ""),
        candidate_answer=str(clean.get("answer") or ""),
        clean_evidence=_visible_docs(clean.get("docs") or []),
        perturbations=[
            {
                "query": str(item.get("query") or ""),
                "candidate_answer": str(item.get("answer") or ""),
                "evidence": _visible_docs(item.get("docs") or []),
            }
            for item in perturbations
        ],
        retrieval_scores=_retrieval_scores([clean, *perturbations]),
    ).to_dict()

    private = OrbitPrivateEvalOnly(
        orbit_id=orbit_id,
        source_item_group_id=source_item_group_id,
        dataset=dataset,
        label_answerable=bool(_orbit_label(clean, perturbations)),
        construction_type=construction_type,
        label_source=str((clean.get("metadata") or {}).get("label_source") or "legacy_heuristic"),
        gold_answer=str(clean.get("answer") or ""),
        heuristic_label="stable_answerable" if _orbit_label(clean, perturbations) else "fragile",
        support_key=str((clean.get("metadata") or {}).get("support_key") or ""),
    ).to_dict()

    assert_no_forbidden_features(raw)
    return raw, private


def write_v4_jsonl(orbits: Iterable[dict], raw_path: Path, private_path: Path, dataset: str) -> int:
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    private_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with raw_path.open("w", encoding="utf-8") as raw_file, private_path.open(
        "w", encoding="utf-8"
    ) as private_file:
        for orbit in orbits:
            raw, private = legacy_orbit_to_v4(orbit, dataset)
            raw_file.write(json.dumps(raw, ensure_ascii=False) + "\n")
            private_file.write(json.dumps(private, ensure_ascii=False) + "\n")
            count += 1
    return count


def validate_v4_pair(raw_path: Path, private_path: Path) -> dict:
    raw_rows = _read_jsonl(raw_path)
    private_rows = _read_jsonl(private_path)
    raw_ids = [row["orbit_id"] for row in raw_rows]
    private_ids = [row["orbit_id"] for row in private_rows]
    if raw_ids != private_ids:
        raise ValueError("raw/private orbit ids differ or are not aligned")
    for row in raw_rows:
        assert_no_forbidden_features(row)
    group_ids = {row["source_item_group_id"] for row in raw_rows}
    return {
        "raw_path": str(raw_path),
        "private_path": str(private_path),
        "orbits": len(raw_rows),
        "source_item_groups": len(group_ids),
        "leakage_free_raw": True,
        "aligned_private_eval": True,
    }


def _visible_docs(docs: list[dict]) -> list[dict]:
    visible = []
    for rank, doc in enumerate(docs):
        visible.append(
            {
                "doc_id": str(doc.get("doc_id") or doc.get("title") or rank),
                "title": str(doc.get("title") or ""),
                "text": str(doc.get("text") or ""),
                "rank": int(doc.get("rank", rank)),
                "retrieval_score": float(doc.get("corm_score") or doc.get("retrieval_score") or 0.0),
            }
        )
    return visible


def _retrieval_scores(sets: list[dict]) -> list[float]:
    scores = []
    for item in sets:
        for doc in item.get("docs") or []:
            scores.append(float(doc.get("corm_score") or doc.get("retrieval_score") or 0.0))
    return scores


def _orbit_label(clean: dict, perturbations: list[dict]) -> bool:
    if clean.get("label_answerable") is not True:
        return False
    return all(item.get("label_answerable") is True for item in perturbations)


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no} is not valid JSON") from exc
    return rows
