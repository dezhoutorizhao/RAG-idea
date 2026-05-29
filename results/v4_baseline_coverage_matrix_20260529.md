# V4 Baseline Coverage Matrix

Generated: `2026-05-29T08:06:47.678994+00:00`
Source: `results\v4_strong_baseline_summary_20260529.json`

All required baselines present: `False`
Status counts: `{'present': 6, 'partial': 1, 'missing': 1}`

## Method Union

`calibrated_logistic_context, calibrated_logistic_orbit, context_sufficiency_clean, corm_max_clean, corm_mean_clean, csrm_rule, equal_budget_ensemble_logistic, equal_budget_mean, equal_budget_min, equal_budget_q25, faithful_sure_multi, retrieval_stability, self_consistency_proxy, template_self_consistency`

## Required Baselines

| Requirement | Status | Matched methods | Missing methods | Boundary |
|---|---|---|---|---|
| faithful_or_official_corm_rag | `partial` | `corm_max_clean, corm_mean_clean` | `` | CoRM-derived clean/context reducers are present, but full faithful CoRM-RAG risk-aware end-to-end reproduction remains blocked. |
| faithful_sure_style_multi_evidence | `present` | `faithful_sure_multi` | `` | Multi-evidence SURE-style sufficiency aggregation is present. |
| context_sufficiency_classifier | `present` | `context_sufficiency_clean, calibrated_logistic_context` | `` | Context-sufficiency and learned context-only baselines are present. |
| llm_judge | `missing` | `` | `llm_judge, llm_as_judge` | No explicit LLM-as-judge baseline artifact is present in the current v4 baseline method union. Self-consistency proxy should not be reported as an LLM judge. |
| self_consistency | `present` | `template_self_consistency` | `` | A deterministic template multi-sample generation self-consistency baseline is present; the older self_consistency_proxy remains lower-evidence diagnostic support. |
| equal_budget_orbit_ensemble | `present` | `equal_budget_mean, equal_budget_min, equal_budget_q25, equal_budget_ensemble_logistic` | `` | Equal-budget reducers and out-of-fold logistic ensemble are present. |
| retrieval_stability | `present` | `retrieval_stability` | `` | Retrieval-stability shortcut baseline is present. |
| calibrated_logistic_baseline | `present` | `calibrated_logistic_context, calibrated_logistic_orbit` | `` | Learned calibrated context/orbit baselines are present. |

## Claim Policy

This matrix audits coverage of required strong-baseline families. It does not upgrade proxy or partial baselines into faithful end-to-end baselines.
