# LLM Judge NLI OpenAI Batch Run Status

Generated: `2026-05-29T04:48:48.305748+00:00`

Action: `preflight`
Status: `blocked`
Blocker: `missing_openai_api_key`
API key ready: `False`
Request file: `results\llm_judge_nli_probe_requests_20260529.jsonl`
Request count: `1000`
Request file valid: `True`
Endpoint: `/v1/chat/completions`
Completion window: `24h`
Batch output: `results\llm_judge_nli_probe_batch_output_20260529.jsonl`

## Claim Policy

This manages API-backed LLM judge batch execution for the paired NLI probe. Preflight performs no network calls. Submit/retrieve require an API key and produce execution metadata only; answerable-score normalization and correlation are evaluated by downstream artifacts.
