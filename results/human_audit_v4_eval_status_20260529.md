# Human Audit V4 Evaluation Status

Ready: `False`
Pack count: `2`
Evaluated pack count: `0`
Allow partial: `False`

| Pack | Selected | Labeled | Pending | Evaluation ready | Evaluated |
|---|---:|---:|---:|---|---|
| hotpot_v4_semanticswap_n100_blind200 | 200 | 0 | 200 | `False` | `False` |
| fever_v4_n100_structbalanced_blind100 | 100 | 0 | 100 | `False` | `False` |

## Failed Gates

hotpot_v4_semanticswap_n100_blind200:
- `non_empty_human_labels`: {'gate': 'non_empty_human_labels', 'actual': 0}
- `all_selected_items_adjudicated`: {'gate': 'all_selected_items_adjudicated', 'required': 200, 'actual': 0}

fever_v4_n100_structbalanced_blind100:
- `non_empty_human_labels`: {'gate': 'non_empty_human_labels', 'actual': 0}
- `all_selected_items_adjudicated`: {'gate': 'all_selected_items_adjudicated', 'required': 100, 'actual': 0}

## Claim Policy

Only packs with adjudicated human labels are evaluated. Pending labels block human-audited claims unless allow_partial is explicitly used for diagnostics.
