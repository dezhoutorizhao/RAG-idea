from __future__ import annotations

from typing import Sequence

from csrm_rag.metrics import area_under_risk_coverage, risk_coverage_curve, selective_risk_at_coverage


def evaluate_selective_policy(scores: Sequence[float], correct: Sequence[bool]) -> dict:
    if len(scores) != len(correct):
        raise ValueError("scores and correct must have the same length")
    if not scores:
        raise ValueError("cannot evaluate an empty selective policy")
    curve = risk_coverage_curve(scores, correct)
    return {
        "n": len(scores),
        "answer_accuracy": sum(bool(item) for item in correct) / len(correct),
        "accepted_error_at_30": selective_risk_at_coverage(scores, correct, 0.30),
        "accepted_error_at_50": selective_risk_at_coverage(scores, correct, 0.50),
        "accepted_error_at_70": selective_risk_at_coverage(scores, correct, 0.70),
        "aurc": area_under_risk_coverage(curve),
        "coverage_at_risk_10": coverage_at_risk(scores, correct, 0.10),
        "coverage_at_risk_20": coverage_at_risk(scores, correct, 0.20),
    }


def coverage_at_risk(scores: Sequence[float], correct: Sequence[bool], risk_target: float) -> dict:
    if not 0.0 <= risk_target <= 1.0:
        raise ValueError("risk_target must be in [0, 1]")
    pairs = sorted(zip(scores, correct), key=lambda item: item[0], reverse=True)
    accepted = 0
    correct_count = 0
    best = {"coverage": 0.0, "risk": 0.0, "threshold": None, "accepted": 0}
    for score, is_correct in pairs:
        accepted += 1
        correct_count += int(bool(is_correct))
        risk = 1.0 - correct_count / accepted
        if risk <= risk_target:
            best = {
                "coverage": accepted / len(pairs),
                "risk": risk,
                "threshold": float(score),
                "accepted": accepted,
            }
    return best
