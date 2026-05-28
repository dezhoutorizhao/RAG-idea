#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from build_fever_orbits import build_fever_orbits
from csrm_rag.orbit_v4 import write_v4_jsonl


def build_fever_orbits_v4(
    raw_output: Path,
    private_output: Path,
    max_examples: int,
    split: str,
    seed: int,
    perturbation_limit: int | None,
) -> dict:
    with TemporaryDirectory() as temp_dir:
        legacy_path = Path(temp_dir) / "fever_legacy.jsonl"
        build_fever_orbits(legacy_path, max_examples=max_examples, split=split, seed=seed)
        legacy_rows = _read_jsonl(legacy_path)
        count = write_v4_jsonl(
            legacy_rows,
            raw_path=raw_output,
            private_path=private_output,
            dataset="copenlu/fever_gold_evidence",
            perturbation_limit=perturbation_limit,
        )
    return {
        "dataset": "copenlu/fever_gold_evidence",
        "raw_output": str(raw_output),
        "private_output": str(private_output),
        "orbits": count,
        "split": split,
        "seed": seed,
        "max_examples": max_examples,
        "perturbation_limit": perturbation_limit,
    }


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-output", type=Path, default=Path("results/fever_orbits_v4.raw.jsonl"))
    parser.add_argument(
        "--private-output",
        type=Path,
        default=Path("results/fever_orbits_v4.private_eval.jsonl"),
    )
    parser.add_argument("--max-examples", type=int, default=200)
    parser.add_argument("--split", default="validation")
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument(
        "--perturbation-limit",
        type=int,
        default=1,
        help="Export the same maximum number of perturbations per orbit; use -1 to keep all.",
    )
    args = parser.parse_args()
    perturbation_limit = None if args.perturbation_limit < 0 else args.perturbation_limit
    summary = build_fever_orbits_v4(
        raw_output=args.raw_output,
        private_output=args.private_output,
        max_examples=args.max_examples,
        split=args.split,
        seed=args.seed,
        perturbation_limit=perturbation_limit,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
