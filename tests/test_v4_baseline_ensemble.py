from csrm_rag.baselines.v4_baselines import (
    BASELINE_METHODS,
    ENSEMBLE_FEATURE_METHODS,
    _score_feature_matrix,
)


def test_equal_budget_ensemble_is_registered_without_csrm_features():
    assert "equal_budget_ensemble_logistic" in BASELINE_METHODS
    assert "csrm_rule" not in ENSEMBLE_FEATURE_METHODS
    assert "calibrated_logistic_orbit" not in ENSEMBLE_FEATURE_METHODS


def test_score_feature_matrix_uses_requested_method_order():
    scores = {
        "a": [0.1, 0.2],
        "b": [0.3, 0.4],
    }

    assert _score_feature_matrix(scores, ["b", "a"]) == [[0.3, 0.1], [0.4, 0.2]]
