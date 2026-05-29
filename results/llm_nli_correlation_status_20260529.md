# LLM/NLI Correlation Status

Generated: `2026-05-29T07:59:32.140338+00:00`

Status: `blocked`
Ready for NLI/LLM correlation claim: `False`
NLI scored rows: `1000`
LLM scored rows: `0`
Paired rows: `0`
Spearman threshold: `0.3`

## Blocker

- Reason: `missing_or_empty_llm_score_artifact`.
- Required score artifact: `results\llm_judge_nli_probe_scores_20260529.jsonl`.

## Claim Policy

This computes ranking correlation between CSRM scores on the exact NLI probe rows and API-backed LLM judge answerable scores. It is only a correlation artifact, not a human-audited or end-to-end RAG result.
