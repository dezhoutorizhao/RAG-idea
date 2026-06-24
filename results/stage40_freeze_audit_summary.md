# Stage40 Freeze Audit

Generated: `2026-06-24T10:50:10.454957+00:00`
Phase 0 freeze ready: `True`
Strict submission ready: `False`

## Gate Summary

| Gate | Value |
|---|---:|
| `accepted_baseline_count_passed` | `True` |
| `accepted_baseline_registry_passed` | `True` |
| `feature_firewall_passed` | `True` |
| `human_final_reproduced` | `True` |
| `human_overlap_exclusion_recorded` | `True` |
| `id_alignment_passed` | `True` |
| `learned_baseline_boundary_reproduced` | `True` |
| `official_code_or_model_count_passed` | `True` |
| `p0_6_negative_reproduced` | `True` |
| `p1_real_generator_negative_reproduced` | `True` |
| `public_integrity_passed` | `True` |
| `public_manifest_ready` | `True` |
| `public_source_main_reproduced` | `True` |
| `required_artifacts_exist` | `True` |
| `source_item_split_counts_present` | `True` |
| `source_item_split_no_overlap` | `True` |
| `strict_blocker_ledger_present` | `True` |
| `strict_submission_ready` | `False` |

## Key Frozen Results

- Public source primary method: `csrm_calibrated_gbdt`.
- Public source AUROC mean: `0.951535441531113`.
- Public comparison vs calibrated_logistic_orbit AURC reduction mean: `0.00528045960388035`.
- Human-final calibrated_logistic_orbit AUROC mean: `0.7448693239290303`.
- P0.6 selected candidate: `csrm_p0_hybrid_stack_histgb_all`.
- P0.6 negative closure gate: `True`.
- P1 real-generator mean task-aware accuracy: `0.08944444444444447`.

## Boundary

Stage40 freezes the already materialized evidence and confirms that Phase 0 inputs are machine-auditable. It intentionally preserves the strict completion blockers instead of counting them as solved.
