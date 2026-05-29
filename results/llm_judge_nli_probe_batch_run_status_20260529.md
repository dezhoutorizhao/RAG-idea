# LLM Judge NLI OpenAI Batch Run Status

Generated: `2026-05-29T07:34:34.667970+00:00`

Action: `preflight`
Status: `blocked`
Blocker: `missing_openai_api_key`
API key ready: `False`
Request file: `results\llm_judge_nli_probe_requests_20260529.jsonl`
Request count: `1000`
Unique custom ids: `1000`
Models: `['gpt-4.1-mini']`
Request file valid: `True`
Execution packet ready: `True`
Endpoint: `/v1/chat/completions`
Completion window: `24h`
Batch output: `results\llm_judge_nli_probe_batch_output_20260529.jsonl`

## Execution Commands

### 1. submit batch after setting OPENAI_API_KEY

```powershell
$env:OPENAI_API_KEY='<set locally>'; python -m experiments.manage_openai_llm_judge_batch --action submit --request-jsonl results\llm_judge_nli_probe_requests_20260529.jsonl --batch-output-jsonl results\llm_judge_nli_probe_batch_output_20260529.jsonl
```

### 2. retrieve completed batch output

```powershell
$env:OPENAI_API_KEY='<set locally>'; python -m experiments.manage_openai_llm_judge_batch --action retrieve --batch-id <batch_id> --request-jsonl results\llm_judge_nli_probe_requests_20260529.jsonl --batch-output-jsonl results\llm_judge_nli_probe_batch_output_20260529.jsonl
```

### 3. normalize judge scores

```powershell
python -m experiments.normalize_llm_judge_batch_responses --batch-output-jsonl results\llm_judge_nli_probe_batch_output_20260529.jsonl --scores-jsonl results\llm_judge_nli_probe_scores_20260529.jsonl
```

### 4. recompute NLI/LLM correlation

```powershell
python -m experiments.compute_llm_nli_correlation
```

### 5. rebuild current evidence package

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_main_tables.ps1
```

## Claim Policy

This manages API-backed LLM judge batch execution for the paired NLI probe. Preflight performs no network calls. Submit/retrieve require an API key and produce execution metadata only; answerable-score normalization and correlation are evaluated by downstream artifacts.
