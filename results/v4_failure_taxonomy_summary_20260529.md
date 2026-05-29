# V4 Failure Taxonomy Summary

Generated: `2026-05-29T02:19:33.896076+00:00`

Datasets: `6`

## Target vs Baseline

- AUROC wins/ties/losses: `0` / `3` / `3`.
- Risk@30 wins/ties/losses: `1` / `4` / `1`.
- Risk@50 wins/ties/losses: `0` / `4` / `2`.

| Dataset | Target AUROC | Baseline AUROC | Target Risk@30 | Baseline Risk@30 | Target Risk@50 | Baseline Risk@50 | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| fever_v4_n100_structbalanced | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0476 | 0.0476 | tie_or_mixed_positive |
| hotpot_v4_hardneg_n100 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | tie_or_mixed_positive |
| hotpot_v4_n100_hardmatched | 0.8000 | 0.8575 | 0.3333 | 0.1667 | 0.3000 | 0.1500 | mixed_or_loss |
| hotpot_v4_n100_structbalanced | 0.8706 | 0.8735 | 0.0833 | 0.1667 | 0.2105 | 0.1579 | mixed_or_loss |
| hotpot_v4_semanticswap_n100 | 0.9500 | 0.9525 | 0.0000 | 0.0000 | 0.1500 | 0.1500 | mixed_or_loss |
| hotpot_v4_supportpreserve_n100 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | tie_or_mixed_positive |

## Construction Taxonomy

| Construction type | n | positive | negative | Datasets | Target mean | Baseline mean | Target-baseline |
|---|---:|---:|---:|---:|---:|---:|---:|
| stable | 120 | 120 | 0 | 6 | 0.8552 | 0.8635 | -0.0083 |
| hard_missing_hop | 20 | 0 | 20 | 1 | 0.0469 | 0.0464 | 0.0005 |
| semantic_swap | 20 | 0 | 20 | 1 | 0.2405 | 0.2356 | 0.0049 |
| wrong_answer | 20 | 0 | 20 | 1 | 0.0113 | 0.0277 | -0.0165 |
| missing_hop | 16 | 0 | 16 | 2 | 0.3880 | 0.4077 | -0.0197 |
| false_premise | 12 | 0 | 12 | 2 | 0.4555 | 0.3477 | 0.1078 |
| distractor | 11 | 0 | 11 | 3 | 0.1612 | 0.1467 | 0.0145 |
| conflict | 5 | 0 | 5 | 1 | 0.0015 | 0.0014 | 0.0001 |
| fragile_mixed | 5 | 0 | 5 | 1 | 0.0006 | 0.0004 | 0.0002 |
| missing | 5 | 0 | 5 | 1 | 0.1627 | 0.1604 | 0.0024 |
| near_miss_dilution | 4 | 0 | 4 | 1 | 0.0006 | 0.0004 | 0.0002 |

## Recurring Feature Gaps

| Feature | top-3 appearances | top-5 appearances | mean absolute gap | max absolute gap |
|---|---:|---:|---:|---:|
| min_sufficiency | 4 | 6 | 0.0516 | 0.0988 |
| clean_to_worst_gap | 4 | 6 | 0.0514 | 0.0988 |
| verifier_entropy | 3 | 4 | 0.0544 | 0.0990 |
| retrieval_overlap | 3 | 3 | 0.1776 | 0.6007 |
| answer_consistency | 1 | 1 | 0.1667 | 1.0000 |
| orbit_answer_flip_rate | 1 | 1 | 0.1667 | 1.0000 |
| support_signature_consistency | 1 | 1 | 0.1667 | 1.0000 |
| max_conflict | 1 | 1 | 0.0115 | 0.0439 |
| naive_orbit_average | 0 | 4 | 0.0249 | 0.0494 |
| mean_sufficiency | 0 | 2 | 0.0249 | 0.0494 |
| mean_missing | 0 | 1 | 0.0135 | 0.0302 |
| sufficiency_variance | 0 | 0 | 0.0017 | 0.0037 |

## Case Gallery Coverage

- baseline_over_target_on_positive: `48` cases.
- target_high_false_positive: `48` cases.
- target_low_false_negative: `48` cases.
- target_over_baseline_on_negative: `48` cases.

## Claim Implication

The v4 failure taxonomy is now machine-readable across FEVER and Hotpot variants. It supports a paper narrative around counterfactual sufficiency instability and documents mixed target-vs-baseline behavior. It remains heuristic/private-label analysis until human audit v4 adjudication is complete.
