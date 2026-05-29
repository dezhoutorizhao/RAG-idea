# Human Audit V4 Batch Collection

Generated: `2026-05-29T07:34:22.152542+00:00`
Pack name: `v4_paper1000_mixed_blind1000`
Source items: `1000`
Collection ready: `True`
Human labels complete: `False`
Pending auditor labels: `2000`
Pending adjudicated labels: `1000`

## Auditors

| Auditor | Batches | Rows | Labeled | Pending | Completion |
|---|---:|---:|---:|---:|---:|
| auditor1 | 5 | 1000 | 0 | 1000 | `0.000` |
| auditor2 | 5 | 1000 | 0 | 1000 | `0.000` |

## Artifacts

- collected_label_csvs[1]: `results\human_audit_v4_collection\v4_paper1000_mixed_blind1000.auditor1.collected.labels.csv`
- collected_label_csvs[2]: `results\human_audit_v4_collection\v4_paper1000_mixed_blind1000.auditor2.collected.labels.csv`
- merged_labels: `results\human_audit_v4_collection\v4_paper1000_mixed_blind1000.merged_labels.jsonl`
- agreement: `results\human_audit_v4_collection\v4_paper1000_mixed_blind1000.agreement.json`
- adjudicated_labels: `results\human_audit_v4_collection\v4_paper1000_mixed_blind1000.adjudicated_labels.jsonl`
- adjudication_template: `results\human_audit_v4_collection\v4_paper1000_mixed_blind1000.adjudication_template.csv`
- readiness: `results\human_audit_v4_collection\v4_paper1000_mixed_blind1000.readiness.json`

## Claim Policy

This collects completed assignment batches into merge/adjudication artifacts. It supports human-audit claims only when human_labels_complete and readiness.ready are both true.
