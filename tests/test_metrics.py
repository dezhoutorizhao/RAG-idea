from csrm_rag.metrics import (
    RiskCoveragePoint,
    area_under_risk_coverage,
    calibration_error,
    roc_auc,
    selective_risk_at_coverage,
)


def test_roc_auc_handles_ties_with_average_ranks():
    assert roc_auc([0.1, 0.4, 0.4, 0.9], [False, True, False, True]) == 0.875


def test_selective_risk_accepts_top_scores():
    result = selective_risk_at_coverage([0.9, 0.8, 0.2, 0.1], [True, False, False, True], 0.5)
    assert result["accepted"] == 2
    assert result["accuracy"] == 0.5
    assert result["risk"] == 0.5


def test_calibration_error_is_zero_for_perfect_bins():
    result = calibration_error([1.0, 0.0], [True, False], n_bins=2)
    assert result["ece"] == 0.0
    assert result["mce"] == 0.0


def test_area_under_risk_coverage_integrates_sorted_curve():
    points = [
        RiskCoveragePoint(threshold=0.9, coverage=0.5, risk=0.2, accuracy=0.8),
        RiskCoveragePoint(threshold=0.0, coverage=1.0, risk=0.4, accuracy=0.6),
    ]
    assert area_under_risk_coverage(points) == 0.25
