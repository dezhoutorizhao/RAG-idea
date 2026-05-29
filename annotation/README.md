# Human Audit V4 Annotation Package

This directory contains the blind annotation workflow for Human Audit v4.
It is designed to validate orbit-level semantic answerability without exposing
construction labels, heuristic labels, oracle fields, retrieval scores, or CSRM
scores to annotators.

## Files

- `guidelines_v4.md`: annotator-facing labeling rules and blindness policy.
- `label_schema_v4.json`: CSV row schema for primary semantic labels and the
  backward-compatible binary projection.
- `audit_card_template.md`: compact card template for manual review or
  annotator onboarding.
- `export_blind_audit_pack_v4.py`: exports blinded HTML, JSONL items, and
  per-auditor CSV label sheets.
- `merge_audit_labels_v4.py`: merges completed auditor CSVs with private
  metadata after labeling.
- `compute_agreement_v4.py`: computes binary and semantic inter-annotator
  agreement summaries.
- `adjudicate_labels_v4.py`: creates adjudicated labels and a manual
  adjudication template for unresolved items.

## Primary Label Space

Annotators fill `label_semantic` with one of:

- `stable_answerable`
- `fragile`
- `unanswerable`
- `ambiguous`
- `annotation_error`

The legacy `label_answerable` field is retained only as a binary projection for
existing evaluation code. It must not be treated as the primary Human Audit v4
label.

## Current Claim Boundary

This package prepares and validates the audit protocol. Empty label sheets and
pending adjudications do not support human-audited claims.
