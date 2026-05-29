# Mechanism Ablation Summary

Generated: `2026-05-29T01:54:01.670424+00:00`

Datasets: `2`

## Aggregate by Method

| Method | Datasets | AUROC drop mean | Risk@30 increase mean | AURC increase mean | Strong mechanism evidence |
|---|---:|---:|---:|---:|---|
| corm_max_clean | 2 | 0.4988 | 0.4858 | 0.3200 | `True` |
| csrm_no_answer_consistency | 2 | 0.1239 | 0.2399 | 0.1344 | `False` |
| csrm_no_worst_sufficiency | 1 | -0.0004 | 0.0000 | -0.0008 | `False` |
| csrm_shuffled_perturbations | 2 | 0.9824 | 0.6943 | 0.5031 | `True` |
| naive_orbit_average | 2 | 0.1945 | 0.2706 | 0.2099 | `True` |
| single_set_sure_style | 2 | 0.4988 | 0.4858 | 0.3144 | `True` |

## Per Dataset

| Dataset | Method | CSRM AUROC | Method AUROC | AUROC drop | Risk@30 increase | AURC increase |
|---|---|---:|---:|---:|---:|---:|
| hotpot_corm_multiseed | csrm_no_answer_consistency | 0.9976 | 0.7577 | 0.2399 | 0.4799 | 0.2606 |
| hotpot_corm_multiseed | csrm_no_worst_sufficiency | 0.9976 | 0.9980 | -0.0004 | 0.0000 | -0.0008 |
| hotpot_corm_multiseed | csrm_shuffled_perturbations | 0.9976 | 0.0001 | 0.9974 | 0.8331 | 0.5584 |
| hotpot_corm_multiseed | naive_orbit_average | 0.9976 | 0.8321 | 0.1654 | 0.3450 | 0.1780 |
| hotpot_corm_multiseed | single_set_sure_style | 0.9976 | 0.5000 | 0.4976 | 0.5828 | 0.3326 |
| hotpot_corm_multiseed | corm_max_clean | 0.9976 | 0.5000 | 0.4976 | 0.5828 | 0.3395 |
| fever_nearmiss_corm_v3_multiseed | csrm_no_answer_consistency | 1.0000 | 0.9921 | 0.0079 | 0.0000 | 0.0082 |
| fever_nearmiss_corm_v3_multiseed | csrm_shuffled_perturbations | 1.0000 | 0.0327 | 0.9673 | 0.5556 | 0.4477 |
| fever_nearmiss_corm_v3_multiseed | naive_orbit_average | 1.0000 | 0.7764 | 0.2236 | 0.1963 | 0.2418 |
| fever_nearmiss_corm_v3_multiseed | single_set_sure_style | 1.0000 | 0.5000 | 0.5000 | 0.3889 | 0.2963 |
| fever_nearmiss_corm_v3_multiseed | corm_max_clean | 1.0000 | 0.5000 | 0.5000 | 0.3889 | 0.3004 |

## Claim Implication

Mechanism ablations strongly support orbit alignment as necessary: shuffled perturbations collapse on both Hotpot and FEVER. Answer consistency is important on Hotpot and mildly positive on FEVER. Worst-sufficiency removal is not consistently harmful in the current bridge artifacts, so it should be framed as a weak or redundant component rather than a required standalone mechanism.
