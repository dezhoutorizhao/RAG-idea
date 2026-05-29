# Text-Only Verifier Status

Generated: `2026-05-29T07:59:32.142864+00:00`

Ready for text-only main claim: `False`

## NLI Probe

- Eval artifact: `results\audit_sample_paper_1000_v3_nli_set_eval.json`.
- Scored artifact: `results\audit_sample_paper_1000_v3_nli_set.jsonl`.
- N: `1000`.
- Directional advantage ready: `True`.

| Baseline | AUROC delta | Risk@30 reduction | AURC reduction | Pass |
|---|---:|---:|---:|---|
| naive_orbit_average | 0.2473 | 0.2333 | 0.1283 | `True` |
| single_set_sure_style | 0.2535 | 0.2433 | 0.1526 | `True` |
| corm_max_clean | 0.2109 | 0.1533 | 0.1162 | `True` |
| corm_mean_clean | 0.2164 | 0.1633 | 0.1192 | `True` |

## LLM Judge Correlation

- Request pack ready: `True`.
- Request count: `1200`.
- Score artifact ready: `False`.
- NLI-paired request pack ready: `True`.
- NLI-paired request count: `1000`.
- NLI-paired score artifact ready: `False`.
- Paired score space ready: `False`.
- Paired batch run status: `blocked`.
- Paired batch blocker: `missing_openai_api_key`.
- Paired batch ready for submission: `False`.
- Paired score normalization status: `blocked`.
- Paired score blocker: `missing_or_empty_batch_output_artifact`.
- Paired parsed scores: `0`.
- Correlation status: `blocked`.
- Correlation blocker: `missing_or_empty_llm_score_artifact`.
- NLI/LLM correlation ready: `False`.

## Success Criteria

| Criterion | Status | Detail |
|---|---|---|
| NLI/text-only scorer beats required weak baselines | `pass` | CSRM has higher AUROC and lower Risk@30/AURC than naive orbit average, single-set SURE-style, and clean-only CoRM reducers. |
| LLM judge and NLI ranking correlation | `blocked` | The NLI-paired LLM judge request pack exists, but no API-backed paired score artifact exists yet. |
| Human-label text-only CSRM evaluation | `blocked` | Human audit v4 adjudicated labels are still pending, so human-label text-only Risk@30/50 cannot be claimed. |

## Claim Policy

This audits the text-only verifier evidence from RAG-idea Section 5.2. It supports only the NLI bridge/probe claim until LLM judge scores and human adjudicated labels are available.
