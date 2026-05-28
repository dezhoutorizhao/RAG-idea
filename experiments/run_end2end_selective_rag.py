#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import corm_max_score, csrm_score, naive_orbit_sufficiency, single_set_sufficiency
from csrm_rag.end2end import evaluate_selective_policy, generate_answer
from experiments.evaluate_orbits import load_orbits


def run_end2end_selective_rag(
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_path: Path,
    *,
    generators: list[str],
) -> dict[str, Any]:
    raw_rows = _read_jsonl(raw_path)
    private_by_id = {row["orbit_id"]: row for row in _read_jsonl(private_path)}
    scored_orbits = {orbit.orbit_id: orbit for orbit in load_orbits(scored_path)}
    if not raw_rows:
        raise ValueError(f"{raw_path} contains no rows")

    selector_scores = _selector_scores(raw_rows, scored_orbits)
    generator_results = {}
    for generator in generators:
        outputs = []
        correct = []
        gen_conf = []
        for row in raw_rows:
            private = private_by_id.get(row["orbit_id"])
            if private is None:
                raise ValueError(f"missing private row for orbit_id={row['orbit_id']}")
            generated = generate_answer(row, private, generator)
            outputs.append(
                {
                    "orbit_id": row["orbit_id"],
                    "answer": generated.answer,
                    "confidence": generated.confidence,
                    "correct": generated.correct,
                }
            )
            correct.append(generated.correct)
            gen_conf.append(generated.confidence)

        methods = dict(selector_scores)
        methods["generator_confidence"] = gen_conf
        generator_results[generator] = {
            "answer_accuracy": sum(correct) / len(correct),
            "methods": {
                name: evaluate_selective_policy(scores, correct)
                for name, scores in sorted(methods.items())
            },
            "outputs": outputs,
        }

    result = {
        "raw_input": str(raw_path),
        "private_input": str(private_path),
        "scored_input": str(scored_path),
        "n": len(raw_rows),
        "generators": generators,
        "selector_methods": sorted(selector_scores),
        "results": generator_results,
        "notes": [
            "This is an end-to-end selective RAG proxy over materialized v4 evidence sets.",
            "Correctness requires both generated answer match and answerable evidence label.",
            "It is not a full CoRM-RAG reproduction with fresh Wikipedia retrieval/generation.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


def _selector_scores(raw_rows: list[dict[str, Any]], scored_orbits: dict[str, Any]) -> dict[str, list[float]]:
    methods = {
        "clean_retrieval_max": [],
        "corm_max_clean": [],
        "single_set_sure_style": [],
        "naive_orbit_average": [],
        "csrm": [],
    }
    for row in raw_rows:
        orbit_id = row["orbit_id"]
        orbit = scored_orbits.get(orbit_id)
        if orbit is None:
            raise ValueError(f"missing scored row for orbit_id={orbit_id}")
        methods["clean_retrieval_max"].append(_clean_retrieval_max(row))
        methods["corm_max_clean"].append(corm_max_score(orbit.clean))
        methods["single_set_sure_style"].append(single_set_sufficiency(orbit.clean))
        methods["naive_orbit_average"].append(naive_orbit_sufficiency(orbit))
        methods["csrm"].append(csrm_score(orbit))
    return methods


def _clean_retrieval_max(row: dict[str, Any]) -> float:
    scores = [float(doc.get("retrieval_score") or 0.0) for doc in row.get("clean_evidence") or []]
    if not scores:
        return 0.0
    return max(0.0, min(1.0, max(scores)))


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
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--generator",
        action="append",
        dest="generators",
        default=[],
        choices=["copy_candidate", "lexical_guarded"],
    )
    args = parser.parse_args()

    generators = args.generators or ["copy_candidate", "lexical_guarded"]
    result = run_end2end_selective_rag(
        args.raw,
        args.private,
        args.scored,
        args.output,
        generators=generators,
    )
    compact = {
        "output": str(args.output),
        "n": result["n"],
        "generators": result["generators"],
        "selector_methods": result["selector_methods"],
    }
    print(json.dumps(compact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
