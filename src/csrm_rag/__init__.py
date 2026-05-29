"""Counterfactual Set Risk Minimization utilities for RAG experiments."""

from .critic import (
    CSRMComponents,
    CSRMWeights,
    corm_max_score,
    corm_mean_score,
    csrm_components,
    csrm_score,
    naive_orbit_sufficiency,
    single_set_sufficiency,
)
from .feature_firewall import FORBIDDEN_KEYS, assert_no_forbidden_features
from .metrics import (
    area_under_risk_coverage,
    average_precision,
    calibration_error,
    risk_coverage_curve,
    roc_auc,
    selective_risk_at_coverage,
)
from .stress_split import EvidenceDoc, EvidenceSet, QueryOrbit

__all__ = [
    "CSRMWeights",
    "CSRMComponents",
    "EvidenceDoc",
    "EvidenceSet",
    "QueryOrbit",
    "FORBIDDEN_KEYS",
    "assert_no_forbidden_features",
    "calibration_error",
    "area_under_risk_coverage",
    "average_precision",
    "corm_max_score",
    "corm_mean_score",
    "csrm_score",
    "csrm_components",
    "naive_orbit_sufficiency",
    "risk_coverage_curve",
    "roc_auc",
    "selective_risk_at_coverage",
    "single_set_sufficiency",
]
