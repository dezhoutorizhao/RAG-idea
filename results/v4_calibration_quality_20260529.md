# V4 Calibration Quality

Generated: `2026-05-29T05:04:34.518865+00:00`

Datasets: `6`
Calibration quality supported: `False`

## Aggregate

- Best calibrated target Brier wins: `6/6`.
- Best calibrated target ECE wins: `4/6`.
- Mean best-target Brier reduction vs best reference: `0.1419`.
- Mean best-target ECE reduction vs best reference: `0.1009`.

## Rows

| Dataset | Best target | Brier | Best ref Brier | Brier reduction | ECE | Best ref ECE | ECE reduction | Target met rate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| fever_orbits_v4_n100.constant.structbalanced | csrm_calibrated_isotonic | 0.0040 | 0.2073 | 0.2032 | 0.0084 | 0.0615 | 0.0531 | 1.0000 |
| hotpot_orbits_v4_hardneg_n100 | csrm_calibrated_isotonic | 0.0001 | 0.2219 | 0.2218 | 0.0013 | 0.0663 | 0.0650 | 1.0000 |
| hotpot_orbits_v4_n100.constant.hardmatched | csrm_calibrated_logistic | 0.1965 | 0.2437 | 0.0472 | 0.1091 | 0.0696 | -0.0395 | 0.3333 |
| hotpot_orbits_v4_n100.constant.structbalanced | csrm_calibrated_logistic | 0.1630 | 0.2377 | 0.0747 | 0.1396 | 0.0942 | -0.0092 | 0.6667 |
| hotpot_orbits_v4_semanticswap_n100 | csrm_calibrated_logistic | 0.0711 | 0.2241 | 0.1530 | 0.0826 | 0.2314 | 0.1519 | 0.6667 |
| hotpot_orbits_v4_supportpreserve_n100 | csrm_calibrated_isotonic | 0.0000 | 0.1514 | 0.1514 | 0.0000 | 0.3841 | 0.3841 | 1.0000 |

## Claim Implication

Calibrated CSRM strongly improves Brier score over rule/minimax baselines across all current v4 calibration datasets. ECE improves on most but not all datasets, so calibration should be claimed as empirical calibration-quality evidence, not as a formal risk guarantee.
