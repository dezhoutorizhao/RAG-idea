# Clean Sufficiency Misleading Diagnostic

Generated: `2026-05-29T03:17:28.826164+00:00`

Rows: `1200` across `6` scored v4 inputs.
Overall private-label failure rate: `0.5000`.

## High-Sufficiency Failure Rates

| Feature | Threshold policy | Threshold | n | failures | failure rate |
|---|---|---:|---:|---:|---:|
| clean_sufficiency | feature_top_quartile | 0.2390 | 303 | 153 | 0.5050 |
| worst_sufficiency | feature_top_quartile | 0.2253 | 302 | 109 | 0.3609 |
| mean_sufficiency | feature_top_quartile | 0.2309 | 302 | 123 | 0.4073 |

## Outputs

- CSV: `paper\figures\clean_sufficiency_misleading_v4_20260529.csv`
- SVG: `paper\figures\clean_sufficiency_misleading_v4_20260529.svg`
- JSON: `results\clean_sufficiency_misleading_v4_20260529.json`

## Claim Boundary

Private-label diagnostic figure: failure rates come from v4 heuristic/private labels, not human-adjudicated labels.
