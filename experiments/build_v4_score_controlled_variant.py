#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag.feature_firewall import assert_no_forbidden_features


def build_v4_score_controlled_variant(
    raw_input: Path,
    raw_output: Path,
    report_output: Path | None = None,
    mode: str = "constant",
    constant_score: float = 0.5,
) -> dict:
    if mode not in {"constant", "rank"}:
        raise ValueError(f"unknown score-control mode: {mode}")
    if not 0.0 <= constant_score <= 1.0:
        raise ValueError("constant_score must be in [0, 1]")

    rows = _read_jsonl(raw_input)
    controlled_rows = []
    before = []
    after = []
    for row in rows:
        assert_no_forbidden_features(row)
        before.extend(_collect_scores(row))
        controlled = copy.deepcopy(row)
        _rewrite_evidence_set(controlled.get("clean_evidence") or [], mode, constant_score)
        for perturbation in controlled.get("perturbations") or []:
            _rewrite_evidence_set(perturbation.get("evidence") or [], mode, constant_score)
        controlled["retrieval_scores"] = _collect_scores(controlled)
        after.extend(controlled["retrieval_scores"])
        controlled.setdefault("metadata", {})
        controlled["metadata"]["score_control"] = {
            "mode": mode,
            "constant_score": constant_score if mode == "constant" else None,
            "note": "Visible retrieval scores are normalized for anti-shortcut diagnostics only.",
        }
        controlled_rows.append(controlled)

    _write_jsonl(raw_output, controlled_rows)
    report = {
        "raw_input": str(raw_input),
        "raw_output": str(raw_output),
        "mode": mode,
        "constant_score": constant_score if mode == "constant" else None,
        "orbits": len(controlled_rows),
        "score_summary_before": _score_summary(before),
        "score_summary_after": _score_summary(after),
        "intended_use": "Controlled anti-shortcut diagnostic; not a replacement for real retrieval evidence.",
    }
    if report_output:
        report_output.parent.mkdir(parents=True, exist_ok=True)
        report_output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def _rewrite_evidence_set(docs: list[dict], mode: str, constant_score: float) -> None:
    scores = _controlled_scores(len(docs), mode, constant_score)
    for index, (doc, score) in enumerate(zip(docs, scores)):
        doc["rank"] = int(doc.get("rank", index))
        doc["retrieval_score"] = score
        if "corm_score" in doc:
            doc["corm_score"] = score


def _controlled_scores(n_docs: int, mode: str, constant_score: float) -> list[float]:
    if n_docs <= 0:
        return []
    if mode == "constant":
        return [float(constant_score)] * n_docs
    if n_docs == 1:
        return [1.0]
    return [1.0 - (index / (n_docs - 1)) for index in range(n_docs)]


def _collect_scores(row: dict) -> list[float]:
    scores = [float(doc.get("retrieval_score") or 0.0) for doc in row.get("clean_evidence") or []]
    for perturbation in row.get("perturbations") or []:
        scores.extend(float(doc.get("retrieval_score") or 0.0) for doc in perturbation.get("evidence") or [])
    return scores


def _score_summary(values: Sequence[float]) -> dict:
    if not values:
        return {"n": 0, "min": None, "mean": None, "max": None, "unique_values": 0}
    return {
        "n": len(values),
        "min": min(values),
        "mean": sum(values) / len(values),
        "max": max(values),
        "unique_values": len(set(values)),
    }


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


def _write_jsonl(path: Path, rows: Sequence[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--mode", choices=["constant", "rank"], default="constant")
    parser.add_argument("--constant-score", type=float, default=0.5)
    args = parser.parse_args()
    report = build_v4_score_controlled_variant(
        raw_input=args.raw,
        raw_output=args.output,
        report_output=args.report_output,
        mode=args.mode,
        constant_score=args.constant_score,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
