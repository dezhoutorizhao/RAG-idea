# Human Audit V4 Status

Audit directory: `results\human_audit_v4`

Ready: `False`
Pack count: `3`
Total items: `1300`
Adjudicated labels: `0`
Pending: `1300`
Semantic label schema ready: `True`
Adjudicated ambiguous rate: `None`
Adjudicated ambiguous/error rate: `None`

| Pack | Items | Auditor labeled | Adjudicated | Pending | Ready |
|---|---:|---:|---:|---:|---|
| fever_v4_n100_structbalanced_blind100 | 100 | 0 | 0 | 100 | `False` |
| hotpot_v4_semanticswap_n100_blind200 | 200 | 0 | 0 | 200 | `False` |
| v4_paper1000_mixed_blind1000 | 1000 | 0 | 0 | 1000 | `False` |

## Failed Gates

fever_v4_n100_structbalanced_blind100:
- `all_items_adjudicated`: {'gate': 'all_items_adjudicated', 'required': 100, 'actual': 0}

hotpot_v4_semanticswap_n100_blind200:
- `all_items_adjudicated`: {'gate': 'all_items_adjudicated', 'required': 200, 'actual': 0}

v4_paper1000_mixed_blind1000:
- `all_items_adjudicated`: {'gate': 'all_items_adjudicated', 'required': 1000, 'actual': 0}

## Claim Policy

This report tracks human-audit readiness only. Empty or pending labels do not support human-audited claims.
