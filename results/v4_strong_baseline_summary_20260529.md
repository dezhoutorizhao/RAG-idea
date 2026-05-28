# V4 Strong Baseline Coverage

Generated: `2026-05-28T19:23:01.344855+00:00`

## Baseline Package

- Baseline files: `6`.
- Comparison files: `6`.
- Method union: `calibrated_logistic_context, calibrated_logistic_orbit, context_sufficiency_clean, corm_max_clean, corm_mean_clean, csrm_rule, equal_budget_ensemble_logistic, equal_budget_mean, equal_budget_min, equal_budget_q25, faithful_sure_multi, retrieval_stability, self_consistency_proxy`.

## CSRM-Rule vs Strongest Non-CSRM

- By AUROC strongest: wins/ties/losses = `0` / `0` / `6`.
- By Risk@30 strongest: wins/ties/losses = `0` / `0` / `6`.
- By AURC strongest: wins/ties/losses = `0` / `0` / `6`.

| Dataset | Strongest by AUROC | AUROC delta | Risk@30 delta | Risk@50 delta | AURC delta | Verdict |
|---|---|---:|---:|---:|---:|---|
| fever_v4_n100_structbalanced | equal_budget_ensemble_logistic | 0.0000 | 0.0000 | 0.0000 | -0.0031 | loss |
| hotpot_v4_hardneg_n100 | retrieval_stability | -0.1748 | -0.1833 | -0.2200 | -0.1157 | loss |
| hotpot_v4_n100_hardmatched | calibrated_logistic_orbit | -0.1556 | -0.1833 | -0.1300 | -0.1061 | loss |
| hotpot_v4_n100_structbalanced | calibrated_logistic_orbit | -0.1996 | -0.2833 | -0.1800 | -0.1772 | loss |
| hotpot_v4_semanticswap_n100 | calibrated_logistic_orbit | -0.0618 | -0.0833 | -0.0800 | -0.0416 | loss |
| hotpot_v4_supportpreserve_n100 | self_consistency_proxy | 0.0000 | 0.0000 | 0.0000 | -0.0278 | loss |

## Calibrated Targets vs All Non-CSRM Baselines

| Target | Metric | Robust wins | Ties | Losses | Mean worst-case delta |
|---|---|---:|---:|---:|---:|
| csrm_rule | auroc_improvement | 0 | 2 | 4 | -0.1036 |
| csrm_rule | risk_at_30_reduction | 0 | 2 | 4 | -0.1352 |
| csrm_rule | risk_at_50_reduction | 0 | 2 | 4 | -0.1163 |
| csrm_rule | aurc_reduction | 0 | 0 | 6 | -0.1108 |
| csrm_minimax | auroc_improvement | 0 | 2 | 4 | -0.0925 |
| csrm_minimax | risk_at_30_reduction | 0 | 2 | 4 | -0.1117 |
| csrm_minimax | risk_at_50_reduction | 0 | 2 | 4 | -0.0921 |
| csrm_minimax | aurc_reduction | 0 | 0 | 6 | -0.1078 |
| csrm_calibrated_logistic | auroc_improvement | 0 | 4 | 2 | -0.0140 |
| csrm_calibrated_logistic | risk_at_30_reduction | 1 | 4 | 1 | -0.0132 |
| csrm_calibrated_logistic | risk_at_50_reduction | 0 | 4 | 2 | -0.0242 |
| csrm_calibrated_logistic | aurc_reduction | 1 | 0 | 5 | -0.0359 |
| csrm_calibrated_isotonic | auroc_improvement | 0 | 3 | 3 | -0.0241 |
| csrm_calibrated_isotonic | risk_at_30_reduction | 0 | 3 | 3 | -0.0304 |
| csrm_calibrated_isotonic | risk_at_50_reduction | 0 | 3 | 3 | -0.0347 |
| csrm_calibrated_isotonic | aurc_reduction | 2 | 1 | 3 | -0.0405 |

## Claim Implication

The v4 strong-baseline package is present and includes context sufficiency, faithful SURE-style multi-set scoring, equal-budget orbit reducers, retrieval stability, self-consistency, and out-of-fold calibrated logistic context/orbit baselines. It strengthens reviewer-facing baseline coverage, but it is also negative boundary evidence: CSRM-Rule is not an all-win method against the strongest learned/context baselines, and calibrated CSRM should be reported with per-setting caveats.
