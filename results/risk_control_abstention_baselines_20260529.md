# Risk-Control Abstention Baselines

Generated: `2026-05-29T06:12:34.570119+00:00`
Input: `results\v4_shared_threshold_selection_20260529.json`
Shared-threshold protocol complete: `True`
Baseline present: `True`

## Baseline Methods

`calibrated_logistic_context, calibrated_logistic_orbit, context_sufficiency_clean, corm_max_clean, corm_mean_clean, equal_budget_ensemble_logistic, equal_budget_mean, equal_budget_min, equal_budget_q25, faithful_sure_multi, retrieval_stability, self_consistency_proxy, template_self_consistency`

## By Risk Target

| Risk target | Methods | Best pass-rate method | Pass rate | Best mean-risk-valid coverage method | Coverage | Mean risk |
|---:|---:|---|---:|---|---:|---:|
| 0.2000 | 13 | calibrated_logistic_orbit | 0.6111 | retrieval_stability | 0.1847 | 0.0769 |
| 0.3000 | 13 | equal_budget_ensemble_logistic | 0.5556 | equal_budget_ensemble_logistic | 0.6119 | 0.2756 |

## Claim Boundary

This artifact audits non-CSRM risk-control/abstention baselines under the same calibration-threshold protocol as CSRM targets. It is empirical held-out evidence, not a formal conformal guarantee and not a full CoRM-RAG reproduction.
