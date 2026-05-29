# LLM Judge NLI Score Normalization

Generated: `2026-05-29T04:22:10.975936+00:00`

Status: `blocked`
Batch output: `results\llm_judge_nli_probe_batch_output_20260529.jsonl`
Score output: `results\llm_judge_nli_probe_scores_20260529.jsonl`
Rows seen: `0`
Parsed scores: `0`
Errors: `0`
Require all success: `True`
Ready for correlation: `False`

## Blocker

- Reason: `missing_or_empty_batch_output_artifact`.

## Claim Policy

This normalizes API-backed LLM judge batch responses into answerable-score rows for the paired NLI probe. It is an ingestion artifact only; the correlation claim is evaluated separately.
