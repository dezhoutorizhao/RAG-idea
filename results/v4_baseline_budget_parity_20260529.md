# V4 Baseline Budget Parity

Generated: `2026-05-29T04:07:11.683292+00:00`
Source: `results\v4_strong_baseline_summary_20260529.json`

Method count: `14`
Status counts: `{'equal_orbit_budget': 8, 'lower_budget_control': 4, 'missing': 1, 'proxy_equal_orbit_budget': 1, 'target_method': 1}`
Same input rows across files: `True`
Same scored evidence across files: `True`
Full budget-parity claim supported: `False`

## Method Budgets

| Method | Status | Evidence scope | Verifier-call budget | LLM calls | Boundary |
|---|---|---|---|---:|---|
| calibrated_logistic_context | `lower_budget_control` | clean_set_only | clean evidence features only | `0` | Learned context-only baseline; lower evidence budget than orbit-level methods. |
| calibrated_logistic_orbit | `equal_orbit_budget` | all_orbit_sets | all scored evidence sets in the orbit | `0` | Learned orbit-feature baseline using the same scored orbit evidence batch. |
| context_sufficiency_clean | `lower_budget_control` | clean_set_only | clean evidence only | `0` | Single-set context sufficiency control; not equal to orbit-level call budget. |
| corm_max_clean | `lower_budget_control` | clean_set_only | clean evidence only | `0` | Uses less orbit evidence than CSRM; keep as a control, not an equal-orbit-budget baseline. |
| corm_mean_clean | `lower_budget_control` | clean_set_only | clean evidence only | `0` | Uses less orbit evidence than CSRM; keep as a control, not an equal-orbit-budget baseline. |
| csrm_rule | `target_method` | all_orbit_sets | all scored evidence sets in the orbit | `0` | Target method used as the budget reference. |
| equal_budget_ensemble_logistic | `equal_orbit_budget` | non_csrm_baseline_scores | same non-CSRM score batch, out-of-fold by source group when possible | `0` | Equal-budget score-fusion baseline; excludes CSRM-specific scores. |
| equal_budget_mean | `equal_orbit_budget` | all_orbit_sets | all scored evidence sets in the orbit | `0` | Equal-budget naive orbit aggregation baseline. |
| equal_budget_min | `equal_orbit_budget` | all_orbit_sets | all scored evidence sets in the orbit | `0` | Equal-budget worst-set orbit aggregation baseline. |
| equal_budget_q25 | `equal_orbit_budget` | all_orbit_sets | all scored evidence sets in the orbit | `0` | Equal-budget quantile orbit aggregation baseline. |
| faithful_sure_multi | `equal_orbit_budget` | all_orbit_sets | all scored evidence sets in the orbit | `0` | Uses the same scored orbit evidence batch as CSRM. |
| retrieval_stability | `equal_orbit_budget` | all_orbit_sets | all scored evidence sets in the orbit | `0` | Uses the same scored orbit evidence batch as CSRM, with retrieval-stability aggregation. |
| self_consistency_proxy | `proxy_equal_orbit_budget` | all_orbit_sets | all scored evidence sets in the orbit | `0` | Proxy over existing answer consistency features; not a fresh multi-sample generation baseline. |
| template_self_consistency | `equal_orbit_budget` | all_orbit_sets | all scored evidence sets in the orbit | `0` | Deterministic multi-template generation self-consistency over the same scored orbit evidence. |
| llm_judge | `missing` | not_run | not run | `not run` | No explicit LLM-as-judge baseline artifact exists in this batch. |

## Claim Policy

This audit documents baseline budget parity. It supports equal-orbit-budget claims only for methods marked equal_orbit_budget, and explicitly excludes clean-only controls, proxy self-consistency, and the missing LLM judge baseline from full parity claims.
