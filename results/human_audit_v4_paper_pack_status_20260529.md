# Human Audit V4 Paper Pack Status

Generated: `2026-05-29T06:33:26.520269+00:00`

Pack name: `v4_paper1000_mixed_blind1000`
Selected items: `1000`
Paper pack ready for labeling: `True`
Human labels complete: `False`
Pending adjudicated labels: `1000`
Selected label counts: `{'true': 200, 'false': 800, 'unknown': 0}`

## Sources

| Source | Rows | Raw | Private | Scored |
|---|---:|---|---|---|
| hotpot_v4_base_n100 | `400` | `results\hotpot_orbits_v4_n100.constant.raw.jsonl` | `results\hotpot_orbits_v4_n100.private_eval.jsonl` | `results\hotpot_orbits_v4_n100.constant.textonly_scored.jsonl` |
| fever_v4_base_n100 | `600` | `results\fever_orbits_v4_n100.constant.raw.jsonl` | `results\fever_orbits_v4_n100.private_eval.jsonl` | `results\fever_orbits_v4_n100.constant.textonly_scored.jsonl` |

## Artifacts

- combined_raw: `results\human_audit_v4\v4_paper1000_mixed_blind1000.sources.raw.jsonl`
- combined_private: `results\human_audit_v4\v4_paper1000_mixed_blind1000.sources.private_eval.jsonl`
- combined_scored: `results\human_audit_v4\v4_paper1000_mixed_blind1000.sources.textonly_scored.jsonl`
- manifest: `results\human_audit_v4\v4_paper1000_mixed_blind1000.manifest.json`
- items_jsonl: `results\human_audit_v4\v4_paper1000_mixed_blind1000.items.jsonl`
- review_html: `results\human_audit_v4\v4_paper1000_mixed_blind1000.review.html`
- label_csvs.auditor1: `results\human_audit_v4\v4_paper1000_mixed_blind1000.auditor1.labels.csv`
- label_csvs.auditor2: `results\human_audit_v4\v4_paper1000_mixed_blind1000.auditor2.labels.csv`
- merged_labels: `results\human_audit_v4\v4_paper1000_mixed_blind1000.merged_labels.jsonl`
- agreement: `results\human_audit_v4\v4_paper1000_mixed_blind1000.agreement.json`
- adjudicated_labels: `results\human_audit_v4\v4_paper1000_mixed_blind1000.adjudicated_labels.jsonl`
- adjudication_template: `results\human_audit_v4\v4_paper1000_mixed_blind1000.adjudication_template.csv`
- readiness: `results\human_audit_v4\v4_paper1000_mixed_blind1000.readiness.json`

## Claim Policy

This materializes a paper-grade 1000-item Human Audit v4 blind pack. It is ready for human labeling but contains no completed human labels yet, so it does not support human-audited result claims.
