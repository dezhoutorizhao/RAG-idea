# End-to-End Selective RAG Proxy Summary

Generated: `2026-05-29T04:48:36.015406+00:00`

## Aggregate

- Evaluated dataset-generator rows: `12`.
- CSRM Risk@30 wins/ties/losses vs strongest non-CSRM: `8` / `2` / `2`.
- CSRM Risk@50 wins/ties/losses vs strongest non-CSRM: `12` / `0` / `0`.
- CSRM AURC wins/ties/losses vs strongest non-CSRM: `8` / `0` / `4`.
- Mean CSRM Risk@30 reduction: `0.1528`.
- Mean CSRM Risk@50 reduction: `0.1917`.
- Mean CSRM AURC reduction: `0.1086`.

## Rows

| Dataset | Generator | Accuracy | CSRM Risk@30 | Best non-CSRM Risk@30 | Delta | CSRM Risk@50 | Best non-CSRM Risk@50 | Delta | CSRM AURC | Best non-CSRM AURC | Delta | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| fever_v4_n100_structbalanced | copy_candidate | 0.5000 | 0.0000 | 0.2333 | 0.2333 | 0.0000 | 0.3500 | 0.3500 | 0.1511 | 0.3313 | 0.1802 | win |
| fever_v4_n100_structbalanced | lexical_guarded | 0.4900 | 0.0000 | 0.2333 | 0.2333 | 0.0200 | 0.3500 | 0.3300 | 0.1589 | 0.3333 | 0.1743 | win |
| hotpot_v4_hardneg_n100 | copy_candidate | 0.5000 | 0.1833 | 0.4500 | 0.2667 | 0.2200 | 0.4700 | 0.2500 | 0.2597 | 0.4636 | 0.2039 | win |
| hotpot_v4_hardneg_n100 | lexical_guarded | 0.5000 | 0.1833 | 0.4500 | 0.2667 | 0.2200 | 0.4700 | 0.2500 | 0.2597 | 0.4636 | 0.2039 | win |
| hotpot_v4_n100_hardmatched | copy_candidate | 0.5000 | 0.4500 | 0.4500 | 0.0000 | 0.4100 | 0.4400 | 0.0300 | 0.4486 | 0.4408 | -0.0078 | mixed_positive |
| hotpot_v4_n100_hardmatched | lexical_guarded | 0.5000 | 0.4500 | 0.4500 | 0.0000 | 0.4100 | 0.4400 | 0.0300 | 0.4486 | 0.4408 | -0.0078 | mixed_positive |
| hotpot_v4_n100_structbalanced | copy_candidate | 0.5000 | 0.4500 | 0.4000 | -0.0500 | 0.4100 | 0.4200 | 0.0100 | 0.4448 | 0.4124 | -0.0324 | loss_or_mixed |
| hotpot_v4_n100_structbalanced | lexical_guarded | 0.5000 | 0.4500 | 0.4000 | -0.0500 | 0.4100 | 0.4200 | 0.0100 | 0.4448 | 0.4124 | -0.0324 | loss_or_mixed |
| hotpot_v4_semanticswap_n100 | copy_candidate | 0.5000 | 0.1500 | 0.2333 | 0.0833 | 0.1500 | 0.2400 | 0.0900 | 0.2280 | 0.2719 | 0.0440 | win |
| hotpot_v4_semanticswap_n100 | lexical_guarded | 0.5000 | 0.1500 | 0.2333 | 0.0833 | 0.1500 | 0.2400 | 0.0900 | 0.2280 | 0.2719 | 0.0440 | win |
| hotpot_v4_supportpreserve_n100 | copy_candidate | 0.5000 | 0.0000 | 0.3833 | 0.3833 | 0.0000 | 0.4300 | 0.4300 | 0.1528 | 0.4193 | 0.2664 | win |
| hotpot_v4_supportpreserve_n100 | lexical_guarded | 0.5000 | 0.0000 | 0.3833 | 0.3833 | 0.0000 | 0.4300 | 0.4300 | 0.1528 | 0.4193 | 0.2664 | win |

## Claim Implication

The proxy supports a directional but not all-win end-to-end selective RAG claim. CSRM improves mean Risk@30/Risk@50 versus the strongest non-CSRM selector, but some Hotpot v4 variants are mixed or negative, so this evidence should be framed as proxy/diagnostic evidence rather than a complete NeurIPS main result.

## Notes

- This aggregates the existing materialized v4 end-to-end selective RAG proxy runs.
- The proxy generator uses materialized v4 evidence sets and lightweight answer generation; it is not a full CoRM-RAG Wikipedia retrieval-generation reproduction.
- Correctness is defined by generated-answer match together with the private answerability label in each proxy file.
