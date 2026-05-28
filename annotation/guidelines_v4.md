# Human Audit v4 Guidelines

## Goal

Human Audit v4 checks whether each orbit is semantically answerable from the
shown evidence, without exposing construction labels, hidden heuristic labels,
retrieval scores, model scores, or orbit identifiers.

Annotators should judge the evidence directly. Do not infer the answer from the
file name, item order, dataset split, or any expected pattern.

## What To Label

For each `audit_id`, read:

- the query or claim;
- the candidate answer or candidate FEVER label;
- the clean evidence set;
- every perturbation evidence set.

Set `label_answerable` to:

- `answerable`: every shown evidence set contains enough information to support
  the candidate answer or candidate FEVER label;
- `fragile`: at least one evidence set is missing required support, contains
  contradictory evidence, or only contains distractors;
- `unsure`: the item cannot be judged confidently from the shown text.

For FEVER-style items, `SUPPORTS` is answerable only when the evidence supports
the claim. `REFUTES` is answerable only when the evidence refutes the claim.

## Failure Types

Use one value in `failure_type` when the label is `fragile` or `unsure`:

- `missing_evidence`: key evidence needed for the candidate answer is absent;
- `conflicting_evidence`: evidence contradicts the candidate answer;
- `distractor_only`: the retrieved documents are unrelated or insufficient;
- `ambiguous_or_insufficient`: evidence is partial or ambiguous;
- `answer_label_mismatch`: the candidate answer or FEVER label itself is wrong;
- `other`: use only when none of the above applies.

Use `supported_all_sets` when the label is `answerable`.

## Confidence

Use integer confidence from 1 to 3:

- `1`: weak confidence;
- `2`: moderate confidence;
- `3`: high confidence.

## Notes

Keep notes short and evidence-based. Mention which evidence set fails when
possible, for example `perturbation 2 missing capital-city evidence`.

## Blindness Requirements

Annotators must not see or use:

- `orbit_id`;
- `source_item_group_id`;
- construction type such as stable, missing, distractor, conflict;
- hidden heuristic labels;
- retrieval scores;
- CSRM, NLI, or baseline model scores.
