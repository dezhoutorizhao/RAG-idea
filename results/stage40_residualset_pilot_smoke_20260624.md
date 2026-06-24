# Stage40 ResidualSet Pilot

Generated: `2026-06-24T11:31:35.436596+00:00`
Baseline: `calibrated_logistic_orbit`
Datasets: `['hotpot_qa/distractor', 'copenlu/fever_gold_evidence', 'bdsaglam/musique']`
Seeds: `[17]`
Scope ready: `False`
Any Phase1 candidate gate: `False`

## Candidate Summary

| Candidate | Positive datasets | Phase1 gate | Mean AURC reduction | Mean Risk@30 reduction | Min dataset AUROC delta | Min slice AUROC delta |
|---|---:|---:|---:|---:|---:|---:|
| `deep_sets_residual` | 0/3 | False | 0.0003 | 0.0000 | 0.0000 | NA |
| `set_transformer_residual` | 0/3 | False | -0.0082 | 0.0000 | -0.0208 | NA |
| `set_transformer_full` | 0/3 | False | -0.1328 | -0.5167 | -0.6042 | NA |
| `mlp_parameter_matched` | 0/3 | False | -0.4303 | -0.6667 | -1.0000 | NA |

## Dataset Scope

- `hotpot_qa/distractor`: status `ok`, groups `20`, scope pass `False`.
- `copenlu/fever_gold_evidence`: status `ok`, groups `20`, scope pass `False`.
- `bdsaglam/musique`: status `ok`, groups `20`, scope pass `False`.

## Claim Boundary

This is a Stage40 Phase 1 pilot over the existing public-source n1000 artifacts. It tests ResidualSet-style architectures against calibrated_logistic_orbit under source-item-group splits. It is not a human-final or independent-stream claim.
