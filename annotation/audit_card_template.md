# Human Audit V4 Card Template

Use this template when reviewing a single blinded `audit_id`. Do not add hidden
fields such as `orbit_id`, construction type, heuristic label, CSRM score, or
retrieval score to the card.

## Audit ID

`<audit_id>`

## Query Or Claim

`<query_or_claim>`

## Candidate Answer Or FEVER Label

`<candidate_answer_or_label>`

## Clean Evidence Set

1. `<title>`: `<evidence text>`
2. `<title>`: `<evidence text>`

## Perturbation Evidence Sets

### Perturbation 1

1. `<title>`: `<evidence text>`
2. `<title>`: `<evidence text>`

### Perturbation 2

1. `<title>`: `<evidence text>`
2. `<title>`: `<evidence text>`

## Required Label

`label_semantic`:

- `stable_answerable`: every shown evidence set supports the same candidate
  answer or FEVER label.
- `fragile`: the clean evidence appears sufficient, but at least one
  perturbation loses support, contradicts the candidate, or becomes distractor
  only.
- `unanswerable`: the clean evidence itself is insufficient.
- `ambiguous`: the question, claim, candidate, or evidence cannot be resolved
  from the shown text.
- `annotation_error`: the card is malformed, duplicated, unreadable, or has a
  display/construction issue.

`label_answerable` projection:

- `answerable` for `stable_answerable`
- `fragile` for `fragile` or `unanswerable`
- `unsure` for `ambiguous` or `annotation_error`

`failure_type` when not `stable_answerable`:

- `missing_evidence`
- `conflicting_evidence`
- `distractor_only`
- `ambiguous_or_insufficient`
- `answer_label_mismatch`
- `other`

`confidence`: `1`, `2`, or `3`

`notes`: short evidence-based explanation, preferably naming the failing
evidence set.

## Blindness Checklist

- No construction labels are visible.
- No heuristic or private labels are visible.
- No CSRM, NLI, baseline, retrieval, or generation scores are visible.
- The decision is based only on the query/claim, candidate, clean evidence, and
  perturbation evidence.
