# V4 Claim-Safe Target Selection

Generated: `2026-05-29T07:59:36.702380+00:00`
Recommended primary target: `csrm_calibrated_gbdt`
All-win supported: `False`
Claim-safe status: `partial`

## Candidate Targets

| Method | Robust wins | Ties | Losses | Mean worst-case delta | Brier wins | ECE wins | Recommendation |
|---|---:|---:|---:|---:|---:|---:|---|
| csrm_calibrated_gbdt | 13 | 18 | 5 | 0.0183 | 4 | 1 | primary_with_caveats |
| csrm_calibrated_logistic | 3 | 19 | 14 | -0.0183 | 0 | 1 | secondary_or_ablation |
| csrm_calibrated_isotonic | 3 | 16 | 17 | -0.0256 | 2 | 4 | secondary_or_ablation |

## Missing Or Partial Baselines

| Requirement | Status | Boundary |
|---|---|---|
| faithful_or_official_corm_rag | `partial` | CoRM-derived clean/context reducers are present, but full faithful CoRM-RAG risk-aware end-to-end reproduction remains blocked. |
| llm_judge | `missing` | No explicit LLM-as-judge baseline artifact is present in the current v4 baseline method union. Self-consistency proxy should not be reported as an LLM judge. |

## Blocked Items

- LLM-as-judge baseline is still missing.
- Faithful/full CoRM-RAG baseline remains partial until full reproduction is complete.
- Human audit labels are incomplete: pending auditor labels=2000, pending adjudicated labels=1000.
- Text-only verifier main claim is blocked by missing LLM correlation and human labels.

## Allowed Wording

- Use `csrm_calibrated_gbdt` as the current paper-facing target only with caveats.
- Claim empirical calibrated-orbit selective-risk evidence, not all-win behavior.
- Report CSRM-Rule as a mechanism baseline with negative evidence against strong learned/context baselines.
- State that LLM-as-judge, human audit, and full CoRM-RAG reproduction remain open blockers.

## Disallowed Wording

- CSRM-Rule is the primary method against strong learned/context baselines.
- CSRM or any calibrated variant is all-win across the current v4 strong-baseline suite.
- The strong-baseline evidence is complete without an LLM-as-judge baseline.
- The current results are human-audited.
- The calibrated model establishes a formal risk-control guarantee.

## Claim Policy

This artifact selects the safest paper-facing target wording from the current strong-baseline and calibration evidence. It is a claim-boundary audit, not a new human label source, LLM judge run, or full CoRM-RAG reproduction.
