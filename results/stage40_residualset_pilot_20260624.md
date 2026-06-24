# Stage40 ResidualSet Pilot

Generated: `2026-06-24T11:38:25.083046+00:00`
Baseline: `calibrated_logistic_orbit`
Datasets: `['hotpot_qa/distractor', 'copenlu/fever_gold_evidence', 'bdsaglam/musique']`
Seeds: `[17, 31, 47, 59, 71]`
Scope ready: `False`
Any Phase1 candidate gate: `False`

## Candidate Summary

| Candidate | Positive datasets | Phase1 gate | Mean AURC reduction | Mean Risk@30 reduction | Min dataset AUROC delta | Min slice AUROC delta |
|---|---:|---:|---:|---:|---:|---:|
| `deep_sets_residual` | 1/3 | False | 0.0266 | 0.0004 | 0.0000 | NA |
| `set_transformer_residual` | 1/3 | False | 0.0264 | 0.0024 | -0.0013 | NA |
| `set_transformer_full` | 1/3 | False | 0.0251 | 0.0005 | -0.0029 | NA |
| `mlp_parameter_matched` | 1/3 | False | 0.0252 | 0.0004 | -0.0002 | NA |

## Dataset Scope

- `hotpot_qa/distractor`: status `ok`, groups `993`, scope pass `True`.
- `copenlu/fever_gold_evidence`: status `ok`, groups `652`, scope pass `False`.
- `bdsaglam/musique`: status `ok`, groups `884`, scope pass `True`.

## Claim Boundary

This is a Stage40 Phase 1 pilot over the existing public-source n1000 artifacts. It tests ResidualSet-style architectures against calibrated_logistic_orbit under source-item-group splits. It is not a human-final or independent-stream claim.
