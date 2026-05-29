# V4 Split and Threshold Protocol

Generated: `2026-05-29T08:23:28.681804+00:00`
Source: `results\v4_strong_baseline_summary_20260529.json`
Threshold source: `results\v4_shared_threshold_selection_20260529.json`

Baseline files: `6`
Comparison files: `6`
Source-item group split supported: `True`
Shared calibration-threshold claim supported: `True`
Protocol complete: `True`
Status counts: `{'pass': 7, 'partial': 0, 'missing': 0}`

## Protocol Matrix

| Requirement | Status | Evidence | Boundary |
|---|---|---|---|
| same_input_rows | `pass` | baseline files with fairness flag: 6<br>fairness.same_input_rows is true in every loaded baseline artifact | The audit is limited to loaded v4 baseline artifacts referenced by the strong-baseline summary. |
| same_scored_evidence | `pass` | baseline files with fairness flag: 6<br>fairness.same_scored_evidence is true in every loaded baseline artifact | This verifies shared scored evidence files, not external LLM judge calls. |
| source_item_group_split | `pass` | comparison files: 6<br>each per-seed result records train/calibration/test source-item group counts | The comparison script uses source_item_group_id groups; this does not by itself add human labels. |
| out_of_fold_logistic_baseline_split | `pass` | standalone baseline artifacts record logistic_scores='out-of-fold by source_item_group_id when possible'<br>baseline files checked: 6 | This covers standalone baseline scoring; train/test comparison artifacts train learned baselines inside each split. |
| target_calibration_split | `pass` | comparison artifacts include train_frac, cal_frac, seeds, and calibration split sizes<br>calibrated CSRM targets are fit with train and calibration orbits before test scoring | This supports calibrated CSRM targets, not a universal baseline threshold-selection protocol. |
| shared_calibration_threshold_selection | `pass` | threshold artifact datasets: 6<br>seeds: [17, 31, 47]<br>risk targets: [0.2, 0.3]<br>protocol complete: True | The shared-threshold protocol is now auditable. Test risk may still miss the calibration target, so this closes protocol fairness rather than proving formal risk control. |
| failed_baselines_reported | `pass` | v4 strong-baseline summary records losses/ties/wins against strongest baselines<br>coverage and budget-parity matrices preserve partial/missing baseline boundaries | Negative and partial baseline evidence must remain in the paper-facing limitations. |

## Claim Policy

This audit covers the route-plan requirements that comparisons use the same inputs, same group split, and same threshold-selection protocol. It supports the current ranking and fixed-coverage comparison scope, but it does not claim a shared calibration-threshold selective-RAG protocol because that experiment has not been run for every baseline.
