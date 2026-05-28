#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_INPUTS = [
    Path("results/end2end_fever_v4_n100_structbalanced_proxy.json"),
    Path("results/end2end_hotpot_v4_hardneg_n100_proxy.json"),
    Path("results/end2end_hotpot_v4_n100_hardmatched_proxy.json"),
    Path("results/end2end_hotpot_v4_n100_structbalanced_proxy.json"),
    Path("results/end2end_hotpot_v4_semanticswap_n100_proxy.json"),
    Path("results/end2end_hotpot_v4_supportpreserve_n100_proxy.json"),
]

PRIMARY_METHOD = "csrm"
NON_CSRM_METHODS = [
    "clean_retrieval_max",
    "corm_max_clean",
    "single_set_sure_style",
    "naive_orbit_average",
    "generator_confidence",
]


def summarize_end2end_selective_rag_proxy(inputs: Sequence[Path]) -> dict[str, Any]:
    rows = []
    for path in inputs:
        payload = _load_json(path)
        rows.extend(_dataset_rows(path, payload))

    if not rows:
        raise ValueError("at least one end-to-end proxy row is required")

    aggregate = _aggregate(rows)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [str(path) for path in inputs],
        "primary_method": PRIMARY_METHOD,
        "non_csrm_methods": NON_CSRM_METHODS,
        "rows": rows,
        "aggregate": aggregate,
        "claim_implication": _claim_implication(aggregate),
        "notes": [
            "This aggregates the existing materialized v4 end-to-end selective RAG proxy runs.",
            "The proxy generator uses materialized v4 evidence sets and lightweight answer generation; it is not a full CoRM-RAG Wikipedia retrieval-generation reproduction.",
            "Correctness is defined by generated-answer match together with the private answerability label in each proxy file.",
        ],
    }


def render_markdown(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    lines = [
        "# End-to-End Selective RAG Proxy Summary",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        "## Aggregate",
        "",
        f"- Evaluated dataset-generator rows: `{aggregate['row_count']}`.",
        f"- CSRM Risk@30 wins/ties/losses vs strongest non-CSRM: "
        f"`{aggregate['risk30_wins']}` / `{aggregate['risk30_ties']}` / `{aggregate['risk30_losses']}`.",
        f"- CSRM Risk@50 wins/ties/losses vs strongest non-CSRM: "
        f"`{aggregate['risk50_wins']}` / `{aggregate['risk50_ties']}` / `{aggregate['risk50_losses']}`.",
        f"- CSRM AURC wins/ties/losses vs strongest non-CSRM: "
        f"`{aggregate['aurc_wins']}` / `{aggregate['aurc_ties']}` / `{aggregate['aurc_losses']}`.",
        f"- Mean CSRM Risk@30 reduction: `{_fmt(aggregate['mean_risk30_reduction'])}`.",
        f"- Mean CSRM Risk@50 reduction: `{_fmt(aggregate['mean_risk50_reduction'])}`.",
        f"- Mean CSRM AURC reduction: `{_fmt(aggregate['mean_aurc_reduction'])}`.",
        "",
        "## Rows",
        "",
        "| Dataset | Generator | Accuracy | CSRM Risk@30 | Best non-CSRM Risk@30 | Delta | CSRM Risk@50 | Best non-CSRM Risk@50 | Delta | CSRM AURC | Best non-CSRM AURC | Delta | Verdict |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary["rows"]:
        lines.append(
            "| "
            f"{row['dataset']} | {row['generator']} | {_fmt(row['answer_accuracy'])} | "
            f"{_fmt(row['csrm']['risk30'])} | {_fmt(row['best_non_csrm']['risk30'])} | "
            f"{_fmt(row['deltas']['risk30_reduction'])} | "
            f"{_fmt(row['csrm']['risk50'])} | {_fmt(row['best_non_csrm']['risk50'])} | "
            f"{_fmt(row['deltas']['risk50_reduction'])} | "
            f"{_fmt(row['csrm']['aurc'])} | {_fmt(row['best_non_csrm']['aurc'])} | "
            f"{_fmt(row['deltas']['aurc_reduction'])} | {row['verdict']} |"
        )
    lines.extend(["", "## Claim Implication", "", summary["claim_implication"], ""])
    lines.extend(["## Notes", ""])
    lines.extend(f"- {note}" for note in summary["notes"])
    lines.append("")
    return "\n".join(lines)


def _dataset_rows(path: Path, payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    dataset = _dataset_name(path)
    for generator, result in sorted(payload["results"].items()):
        methods = result["methods"]
        csrm = _method_metrics(methods[PRIMARY_METHOD])
        best_non_csrm = _best_non_csrm(methods)
        deltas = {
            "risk30_reduction": best_non_csrm["risk30"] - csrm["risk30"],
            "risk50_reduction": best_non_csrm["risk50"] - csrm["risk50"],
            "aurc_reduction": best_non_csrm["aurc"] - csrm["aurc"],
            "coverage_at_risk20_gain": csrm["coverage_at_risk20"] - best_non_csrm["coverage_at_risk20"],
        }
        rows.append(
            {
                "artifact": str(path),
                "dataset": dataset,
                "n": payload["n"],
                "generator": generator,
                "answer_accuracy": result["answer_accuracy"],
                "csrm": csrm,
                "best_non_csrm": best_non_csrm,
                "deltas": deltas,
                "verdict": _row_verdict(deltas),
            }
        )
    return rows


def _method_metrics(metrics: dict[str, Any]) -> dict[str, float]:
    return {
        "risk30": float(metrics["accepted_error_at_30"]["risk"]),
        "risk50": float(metrics["accepted_error_at_50"]["risk"]),
        "risk70": float(metrics["accepted_error_at_70"]["risk"]),
        "coverage_at_risk20": float(metrics["coverage_at_risk_20"]["coverage"]),
        "aurc": float(metrics["aurc"]),
    }


def _best_non_csrm(methods: dict[str, Any]) -> dict[str, Any]:
    candidates = []
    for name in NON_CSRM_METHODS:
        if name not in methods:
            continue
        metrics = _method_metrics(methods[name])
        candidates.append({"method": name, **metrics})
    if not candidates:
        raise ValueError("no non-CSRM methods found")
    return min(candidates, key=lambda item: (item["risk30"], item["risk50"], item["aurc"]))


def _aggregate(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "risk30_wins": _count(rows, "risk30_reduction", positive=True),
        "risk30_ties": _count(rows, "risk30_reduction", zero=True),
        "risk30_losses": _count(rows, "risk30_reduction", negative=True),
        "risk50_wins": _count(rows, "risk50_reduction", positive=True),
        "risk50_ties": _count(rows, "risk50_reduction", zero=True),
        "risk50_losses": _count(rows, "risk50_reduction", negative=True),
        "aurc_wins": _count(rows, "aurc_reduction", positive=True),
        "aurc_ties": _count(rows, "aurc_reduction", zero=True),
        "aurc_losses": _count(rows, "aurc_reduction", negative=True),
        "mean_risk30_reduction": _mean(row["deltas"]["risk30_reduction"] for row in rows),
        "mean_risk50_reduction": _mean(row["deltas"]["risk50_reduction"] for row in rows),
        "mean_aurc_reduction": _mean(row["deltas"]["aurc_reduction"] for row in rows),
        "mean_coverage_at_risk20_gain": _mean(
            row["deltas"]["coverage_at_risk20_gain"] for row in rows
        ),
        "all_win": all(row["verdict"] == "win" for row in rows),
        "has_losses": any(row["verdict"] == "loss_or_mixed" for row in rows),
    }


def _row_verdict(deltas: dict[str, float]) -> str:
    if deltas["risk30_reduction"] > 1e-12 and deltas["risk50_reduction"] >= -1e-12:
        return "win"
    if abs(deltas["risk30_reduction"]) <= 1e-12 and deltas["risk50_reduction"] > 1e-12:
        return "mixed_positive"
    return "loss_or_mixed"


def _count(
    rows: Sequence[dict[str, Any]],
    key: str,
    *,
    positive: bool = False,
    zero: bool = False,
    negative: bool = False,
) -> int:
    count = 0
    for row in rows:
        value = row["deltas"][key]
        if positive and value > 1e-12:
            count += 1
        if zero and abs(value) <= 1e-12:
            count += 1
        if negative and value < -1e-12:
            count += 1
    return count


def _mean(values: Sequence[float]) -> float:
    values = list(values)
    return sum(values) / len(values)


def _claim_implication(aggregate: dict[str, Any]) -> str:
    if aggregate["all_win"]:
        return (
            "The proxy supports a broad end-to-end selective RAG advantage claim, subject to "
            "the proxy limitation and pending human labels."
        )
    return (
        "The proxy supports a directional but not all-win end-to-end selective RAG claim. "
        "CSRM improves mean Risk@30/Risk@50 versus the strongest non-CSRM selector, but "
        "some Hotpot v4 variants are mixed or negative, so this evidence should be framed "
        "as proxy/diagnostic evidence rather than a complete NeurIPS main result."
    )


def _dataset_name(path: Path) -> str:
    name = path.name
    prefix = "end2end_"
    suffix = "_proxy.json"
    if name.startswith(prefix):
        name = name[len(prefix) :]
    if name.endswith(suffix):
        name = name[: -len(suffix)]
    return name


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.4f}"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, nargs="+", default=DEFAULT_INPUTS)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    summary = summarize_end2end_selective_rag_proxy(args.inputs)
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
