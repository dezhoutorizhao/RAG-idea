# LLM Judge Requests Paired To NLI Probe

Generated: `2026-05-29T04:48:48.277156+00:00`

Model: `gpt-4.1-mini`
Input NLI artifact: `results\audit_sample_paper_1000_v3_nli_set.jsonl`
Requests: `1000`
Request pack ready: `True`
Paired to NLI probe: `True`
API key ready: `False`
Score artifact ready: `False`
Ready for NLI/LLM correlation: `False`

## Splits

| Split | Requests |
|---|---:|
| fever_conflicting_evidence | 100 |
| fever_distractor_only | 100 |
| fever_fragile_mixed | 100 |
| fever_missing_evidence | 100 |
| fever_near_miss_dilution | 100 |
| fever_stable_evidence | 100 |
| hotpot_distractor | 100 |
| hotpot_false_premise | 100 |
| hotpot_missing_hop | 100 |
| hotpot_stable_support | 100 |

## Claim Policy

This materializes LLM-judge requests over the exact NLI scored probe rows, after stripping labels, support keys, and construction metadata from prompts. It is not an LLM/NLI correlation result until API-backed scores are collected.
