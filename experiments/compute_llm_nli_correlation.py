#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import csrm_score
from csrm_rag.verifiers.llm_judge import parse_llm_judge_response
from experiments.evaluate_orbits import load_orbits


DEFAULT_NLI_SCORED = Path("results/audit_sample_paper_1000_v3_nli_set.jsonl")
DEFAULT_LLM_SCORES = Path("results/llm_judge_nli_probe_scores_20260529.jsonl")
DEFAULT_OUTPUT_JSON = Path("results/llm_nli_correlation_status_20260529.json")
DEFAULT_OUTPUT_MD = Path("results/llm_nli_correlation_status_20260529.md")


def compute_llm_nli_correlation(
    nli_scored_jsonl: Path,
    llm_scores_jsonl: Path,
    *,
    spearman_minimum: float = 0.30,
) -> dict[str, Any]:
    nli_scores = _nli_csrm_scores(nli_scored_jsonl)
    if not llm_scores_jsonl.exists() or llm_scores_jsonl.stat().st_size == 0:
        return _blocked_summary(
            nli_scored_jsonl,
            llm_scores_jsonl,
            nli_scores,
            reason="missing_or_empty_llm_score_artifact",
            spearman_minimum=spearman_minimum,
        )

    llm_scores = _load_llm_scores(llm_scores_jsonl)
    paired_ids = sorted(set(nli_scores) & set(llm_scores))
    if len(paired_ids) < 2:
        return _blocked_summary(
            nli_scored_jsonl,
            llm_scores_jsonl,
            nli_scores,
            reason="fewer_than_two_paired_scores",
            spearman_minimum=spearman_minimum,
            llm_score_count=len(llm_scores),
            paired_count=len(paired_ids),
        )

    nli_values = [nli_scores[orbit_id] for orbit_id in paired_ids]
    llm_values = [llm_scores[orbit_id] for orbit_id in paired_ids]
    correlations = {
        "pearson": _pearson(nli_values, llm_values),
        "spearman": _spearman(nli_values, llm_values),
        "kendall_tau_b": _kendall_tau_b(nli_values, llm_values),
    }
    spearman = correlations["spearman"]
    ready = (
        len(paired_ids) == len(nli_scores)
        and spearman is not None
        and spearman >= spearman_minimum
    )
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "nli_scored_jsonl": str(nli_scored_jsonl),
        "llm_scores_jsonl": str(llm_scores_jsonl),
        "nli_score_count": len(nli_scores),
        "llm_score_count": len(llm_scores),
        "paired_count": len(paired_ids),
        "missing_llm_for_nli_count": len(set(nli_scores) - set(llm_scores)),
        "extra_llm_not_in_nli_count": len(set(llm_scores) - set(nli_scores)),
        "correlations": correlations,
        "spearman_minimum": spearman_minimum,
        "ready_for_nli_llm_correlation_claim": ready,
        "status": "pass" if ready else "fail",
        "claim_policy": (
            "This computes ranking correlation between CSRM scores on the exact NLI "
            "probe rows and API-backed LLM judge answerable scores. It is only a "
            "correlation artifact, not a human-audited or end-to-end RAG result."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# LLM/NLI Correlation Status",
        "",
        f"Generated: `{summary['generated_at_utc']}`",
        "",
        f"Status: `{summary['status']}`",
        f"Ready for NLI/LLM correlation claim: `{summary['ready_for_nli_llm_correlation_claim']}`",
        f"NLI scored rows: `{summary['nli_score_count']}`",
        f"LLM scored rows: `{summary.get('llm_score_count')}`",
        f"Paired rows: `{summary.get('paired_count')}`",
        f"Spearman threshold: `{summary['spearman_minimum']}`",
        "",
    ]
    if summary["status"] == "blocked":
        lines.extend(
            [
                "## Blocker",
                "",
                f"- Reason: `{summary['blocker_reason']}`.",
                f"- Required score artifact: `{summary['llm_scores_jsonl']}`.",
                "",
            ]
        )
    else:
        corr = summary["correlations"]
        lines.extend(
            [
                "## Correlations",
                "",
                f"- Pearson: `{_fmt(corr.get('pearson'))}`.",
                f"- Spearman: `{_fmt(corr.get('spearman'))}`.",
                f"- Kendall tau-b: `{_fmt(corr.get('kendall_tau_b'))}`.",
                "",
            ]
        )
    lines.extend(["## Claim Policy", "", summary["claim_policy"], ""])
    return "\n".join(lines)


def _blocked_summary(
    nli_scored_jsonl: Path,
    llm_scores_jsonl: Path,
    nli_scores: dict[str, float],
    *,
    reason: str,
    spearman_minimum: float,
    llm_score_count: int = 0,
    paired_count: int = 0,
) -> dict[str, Any]:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "nli_scored_jsonl": str(nli_scored_jsonl),
        "llm_scores_jsonl": str(llm_scores_jsonl),
        "nli_score_count": len(nli_scores),
        "llm_score_count": llm_score_count,
        "paired_count": paired_count,
        "spearman_minimum": spearman_minimum,
        "ready_for_nli_llm_correlation_claim": False,
        "status": "blocked",
        "blocker_reason": reason,
        "claim_policy": (
            "This computes ranking correlation between CSRM scores on the exact NLI "
            "probe rows and API-backed LLM judge answerable scores. It is only a "
            "correlation artifact, not a human-audited or end-to-end RAG result."
        ),
    }


def _nli_csrm_scores(path: Path) -> dict[str, float]:
    return {orbit.orbit_id: csrm_score(orbit) for orbit in load_orbits(path)}


def _load_llm_scores(path: Path) -> dict[str, float]:
    scores: dict[str, float] = {}
    for row in _read_jsonl(path):
        orbit_id = _orbit_id(row)
        if not orbit_id:
            raise ValueError(f"{path} contains row without orbit_id/custom_id")
        score = _llm_score(row)
        if orbit_id in scores:
            raise ValueError(f"{path} contains duplicate orbit_id {orbit_id}")
        scores[orbit_id] = score
    return scores


def _orbit_id(row: dict[str, Any]) -> str | None:
    metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    return row.get("orbit_id") or row.get("custom_id") or metadata.get("orbit_id")


def _llm_score(row: dict[str, Any]) -> float:
    if "answerable_score" in row:
        return _score01(row["answerable_score"])
    parsed = row.get("parsed")
    if isinstance(parsed, dict) and "answerable_score" in parsed:
        return _score01(parsed["answerable_score"])
    content = _openai_batch_content(row)
    if content is not None:
        return _score01(parse_llm_judge_response(content)["answerable_score"])
    raise ValueError("LLM score row does not contain answerable_score or OpenAI batch response content")


def _openai_batch_content(row: dict[str, Any]) -> str | None:
    response = row.get("response")
    if not isinstance(response, dict):
        return None
    body = response.get("body")
    if not isinstance(body, dict):
        return None
    choices = body.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    return content if isinstance(content, str) else None


def _score01(value: Any) -> float:
    score = float(value)
    if not 0.0 <= score <= 1.0:
        raise ValueError("answerable_score must be in [0, 1]")
    return score


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    dx = [x - mean_x for x in xs]
    dy = [y - mean_y for y in ys]
    denom = math.sqrt(sum(x * x for x in dx) * sum(y * y for y in dy))
    if denom == 0:
        return None
    return sum(x * y for x, y in zip(dx, dy)) / denom


def _spearman(xs: list[float], ys: list[float]) -> float | None:
    return _pearson(_ranks(xs), _ranks(ys))


def _ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda idx: values[idx])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        avg_rank = (start + 1 + end) / 2.0
        for idx in order[start:end]:
            ranks[idx] = avg_rank
        start = end
    return ranks


def _kendall_tau_b(xs: list[float], ys: list[float]) -> float | None:
    concordant = discordant = tie_x = tie_y = 0
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            dx = _sign(xs[i] - xs[j])
            dy = _sign(ys[i] - ys[j])
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                tie_x += 1
            elif dy == 0:
                tie_y += 1
            elif dx == dy:
                concordant += 1
            else:
                discordant += 1
    denom = math.sqrt((concordant + discordant + tie_x) * (concordant + discordant + tie_y))
    if denom == 0:
        return None
    return (concordant - discordant) / denom


def _sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def _fmt(value: float | None) -> str:
    return "None" if value is None else f"{value:.4f}"


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


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nli-scored-jsonl", type=Path, default=DEFAULT_NLI_SCORED)
    parser.add_argument("--llm-scores-jsonl", type=Path, default=DEFAULT_LLM_SCORES)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--spearman-minimum", type=float, default=0.30)
    args = parser.parse_args()

    summary = compute_llm_nli_correlation(
        args.nli_scored_jsonl,
        args.llm_scores_jsonl,
        spearman_minimum=args.spearman_minimum,
    )
    _write_json(args.output_json, summary)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
