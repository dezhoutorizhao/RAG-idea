# V4 Shared Calibration-Threshold Selection

Generated: `2026-05-29T02:58:14.719513+00:00`

Datasets: `6`
Seeds: `[17, 31, 47]`
Risk targets: `[0.2, 0.3]`
Protocol complete: `True`

## Protocol

- same_source_item_group_split: `True`
- threshold_selected_on: `calibration split`
- threshold_applied_to: `held-out test split`
- selection_rule: `maximize calibration coverage subject to empirical calibration risk <= target`
- score_direction: `higher score means more answerable / safer to accept`

## Target Coverage vs Strongest Baseline

| Risk target | Target | Wins | Ties | Losses | Mean coverage delta | Mean test risk | Missed target rows |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0.20 | csrm_rule | 2 | 5 | 11 | -0.2393 | 0.3315 | 13 |
| 0.20 | csrm_minimax | 3 | 3 | 12 | -0.2407 | 0.3274 | 12 |
| 0.20 | csrm_calibrated_logistic | 2 | 8 | 8 | -0.0861 | 0.2341 | 7 |
| 0.20 | csrm_calibrated_isotonic | 1 | 5 | 12 | -0.0523 | 0.1453 | 4 |
| 0.30 | csrm_rule | 3 | 5 | 10 | -0.1980 | 0.3490 | 11 |
| 0.30 | csrm_minimax | 2 | 6 | 10 | -0.1912 | 0.4294 | 11 |
| 0.30 | csrm_calibrated_logistic | 3 | 7 | 8 | -0.1205 | 0.3191 | 8 |
| 0.30 | csrm_calibrated_isotonic | 1 | 5 | 12 | -0.0917 | 0.1622 | 4 |

## Method Summary

| Risk target | Method | Mean cal coverage | Mean test coverage | Mean test risk | Test target pass rate | No-accept rows |
|---:|---|---:|---:|---:|---:|---:|
| 0.20 | calibrated_logistic_context | 0.0017 | 0.0249 | 0.6444 | 0.0000 | 15 |
| 0.20 | calibrated_logistic_orbit | 0.4838 | 0.4783 | 0.2248 | 0.6111 | 0 |
| 0.20 | context_sufficiency_clean | 0.0015 | 0.0796 | 0.5361 | 0.0000 | 6 |
| 0.20 | corm_max_clean | 0.0000 | 0.0000 | n/a | 0.0000 | 18 |
| 0.20 | corm_mean_clean | 0.0000 | 0.0000 | n/a | 0.0000 | 18 |
| 0.20 | csrm_calibrated_isotonic | 0.3776 | 0.3732 | 0.1453 | 0.7778 | 1 |
| 0.20 | csrm_calibrated_logistic | 0.4767 | 0.4686 | 0.2341 | 0.6111 | 1 |
| 0.20 | csrm_minimax | 0.4072 | 0.4432 | 0.3274 | 0.3333 | 2 |
| 0.20 | csrm_rule | 0.3948 | 0.4465 | 0.3315 | 0.2778 | 2 |
| 0.20 | equal_budget_ensemble_logistic | 0.4778 | 0.4729 | 0.2558 | 0.3333 | 1 |
| 0.20 | equal_budget_mean | 0.2071 | 0.2639 | 0.3784 | 0.0556 | 1 |
| 0.20 | equal_budget_min | 0.2783 | 0.3145 | 0.3123 | 0.2222 | 2 |
| 0.20 | equal_budget_q25 | 0.2320 | 0.2968 | 0.3223 | 0.1667 | 1 |
| 0.20 | faithful_sure_multi | 0.2144 | 0.2556 | 0.3594 | 0.1667 | 2 |
| 0.20 | retrieval_stability | 0.1778 | 0.1847 | 0.0769 | 0.2222 | 12 |
| 0.20 | self_consistency_proxy | 0.0833 | 0.0833 | 0.0000 | 0.1667 | 15 |
| 0.30 | calibrated_logistic_context | 0.0118 | 0.0430 | 0.6444 | 0.0000 | 15 |
| 0.30 | calibrated_logistic_orbit | 0.6227 | 0.6015 | 0.3132 | 0.5000 | 0 |
| 0.30 | context_sufficiency_clean | 0.0133 | 0.1014 | 0.5361 | 0.0000 | 6 |
| 0.30 | corm_max_clean | 0.0000 | 0.0000 | n/a | 0.0000 | 18 |
| 0.30 | corm_mean_clean | 0.0000 | 0.0000 | n/a | 0.0000 | 18 |
| 0.30 | csrm_calibrated_isotonic | 0.4436 | 0.4373 | 0.1622 | 0.7778 | 0 |
| 0.30 | csrm_calibrated_logistic | 0.6018 | 0.5852 | 0.3191 | 0.5556 | 0 |
| 0.30 | csrm_minimax | 0.4738 | 0.5140 | 0.4294 | 0.3889 | 2 |
| 0.30 | csrm_rule | 0.4909 | 0.5348 | 0.3490 | 0.3889 | 2 |
| 0.30 | equal_budget_ensemble_logistic | 0.6041 | 0.5873 | 0.2870 | 0.4444 | 1 |
| 0.30 | equal_budget_mean | 0.3029 | 0.3274 | 0.3822 | 0.1111 | 1 |
| 0.30 | equal_budget_min | 0.4039 | 0.3990 | 0.3682 | 0.3889 | 0 |
| 0.30 | equal_budget_q25 | 0.3416 | 0.3863 | 0.3565 | 0.2222 | 1 |
| 0.30 | faithful_sure_multi | 0.3379 | 0.3719 | 0.3659 | 0.1667 | 1 |
| 0.30 | retrieval_stability | 0.1948 | 0.2037 | 0.1426 | 0.2778 | 12 |
| 0.30 | self_consistency_proxy | 0.0833 | 0.0833 | 0.0000 | 0.1667 | 15 |

## Claim Policy

This artifact closes the protocol-fairness requirement that all methods use the same source-group split and select thresholds only on the calibration split. Test risk can still miss the calibration target, so this is not a formal risk-control guarantee.
