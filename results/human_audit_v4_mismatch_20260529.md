# Human Audit V4 Heuristic-Human Mismatch

Audit directory: `results\human_audit_v4`

Mismatch artifact ready: `True`
Human audit complete: `False`

## Aggregate

- Binary comparable labels: `0`
- Binary mismatches: `0`
- Binary mismatch rate: `None`
- Semantic comparable labels: `0`
- Semantic mismatches: `0`
- Semantic mismatch rate: `None`

## Packs

| Pack | Items | Pending | Binary comparable | Binary mismatch rate | Semantic comparable | Semantic mismatch rate |
|---|---:|---:|---:|---:|---:|---:|
| fever_v4_n100_structbalanced_blind100 | 100 | 100 | 0 | None | 0 | None |
| hotpot_v4_semanticswap_n100_blind200 | 200 | 200 | 0 | None | 0 | None |
| v4_paper1000_mixed_blind1000 | 1000 | 1000 | 0 | None | 0 | None |

## Claim Policy

This artifact compares heuristic labels with adjudicated human labels only when adjudicated labels exist. Pending labels are excluded from mismatch rates.
