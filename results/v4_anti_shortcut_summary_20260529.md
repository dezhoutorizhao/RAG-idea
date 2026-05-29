# V4 Anti-Shortcut Summary

Generated: `2026-05-29T03:57:12.800792+00:00`

Datasets: `6`

## Aggregate

- Raw firewall all passed: `True`.
- Structural-only all passed <= 0.55: `True`; max AUROC: `0.5188`.
- Group split no-overlap all passed: `True`.
- Random-label median AUROC range: `0.4961` to `0.5054`.
- Private metadata upper bound all high: `True`.
- Core anti-shortcut suite passed: `True`.

## Per Dataset

| Dataset | n | max structural AUROC | structural pass | random median | group no-overlap | private metadata AUROC |
|---|---:|---:|---|---:|---|---:|
| fever_orbits_v4_n100_structbalanced | 200 | 0.5001 | `True` | 0.5030 | `True` | 1.0000 |
| hotpot_orbits_v4_hardneg_n100 | 200 | 0.5188 | `True` | 0.4985 | `True` | 1.0000 |
| hotpot_orbits_v4_n100_hardmatched | 200 | 0.5121 | `True` | 0.4982 | `True` | 1.0000 |
| hotpot_orbits_v4_n100_structbalanced | 200 | 0.5000 | `True` | 0.5054 | `True` | 1.0000 |
| hotpot_orbits_v4_semanticswap_n100 | 200 | 0.5009 | `True` | 0.4961 | `True` | 1.0000 |
| hotpot_orbits_v4_supportpreserve_n100 | 200 | 0.5000 | `True` | 0.4986 | `True` | 1.0000 |

## Claim Implication

The primary v4 anti-shortcut suite passes the core non-oracle checks: raw feature firewall, structural-only <= 0.55, source-item group split without overlap, and random-label sanity near 0.5. Private construction metadata remains a high-leakage upper bound, so these fields must stay evaluator-only. This supports leakage-control claims but does not replace human audit or end-to-end RAG evidence.
