# V4 End-to-End Retriever-Generator Matrix

Generated: `2026-05-29T03:57:08.296754+00:00`

Datasets: `6`
Retrievers: `['bm25_orbit_pool', 'dense_hash_orbit_pool']`
Generators: `['copy_candidate', 'lexical_guarded']`
Rows: `24`
Protocol complete: `True`

## Aggregate

- CSRM Risk@30 wins/ties/losses: `16` / `4` / `4`.
- CSRM Risk@50 wins/ties/losses: `24` / `0` / `0`.
- CSRM AURC wins/ties/losses: `16` / `0` / `8`.
- Mean Risk@30 reduction: `0.1528`.
- Mean Risk@50 reduction: `0.1908`.
- Mean AURC reduction: `0.1079`.

## Rows

| Dataset | Retriever | Generator | Accuracy | CSRM Risk@30 | Best Risk@30 | Delta | CSRM Risk@50 | Best Risk@50 | Delta | CSRM AURC | Best AURC | Delta | Verdict |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| fever_v4_n100_structbalanced | bm25_orbit_pool | copy_candidate | 0.5000 | 0.0000 | 0.2333 | 0.2333 | 0.0000 | 0.3500 | 0.3500 | 0.1511 | 0.3313 | 0.1802 | win |
| fever_v4_n100_structbalanced | bm25_orbit_pool | lexical_guarded | 0.4900 | 0.0000 | 0.2333 | 0.2333 | 0.0200 | 0.3500 | 0.3300 | 0.1589 | 0.3333 | 0.1743 | win |
| fever_v4_n100_structbalanced | dense_hash_orbit_pool | copy_candidate | 0.5000 | 0.0000 | 0.2333 | 0.2333 | 0.0000 | 0.3500 | 0.3500 | 0.1511 | 0.3313 | 0.1802 | win |
| fever_v4_n100_structbalanced | dense_hash_orbit_pool | lexical_guarded | 0.4900 | 0.0000 | 0.2333 | 0.2333 | 0.0200 | 0.3500 | 0.3300 | 0.1589 | 0.3333 | 0.1743 | win |
| hotpot_v4_hardneg_n100 | bm25_orbit_pool | copy_candidate | 0.5000 | 0.1833 | 0.4500 | 0.2667 | 0.2200 | 0.4700 | 0.2500 | 0.2597 | 0.4636 | 0.2039 | win |
| hotpot_v4_hardneg_n100 | bm25_orbit_pool | lexical_guarded | 0.5000 | 0.1833 | 0.4500 | 0.2667 | 0.2200 | 0.4700 | 0.2500 | 0.2597 | 0.4636 | 0.2039 | win |
| hotpot_v4_hardneg_n100 | dense_hash_orbit_pool | copy_candidate | 0.5000 | 0.1833 | 0.4500 | 0.2667 | 0.2200 | 0.4700 | 0.2500 | 0.2597 | 0.4636 | 0.2039 | win |
| hotpot_v4_hardneg_n100 | dense_hash_orbit_pool | lexical_guarded | 0.5000 | 0.1833 | 0.4500 | 0.2667 | 0.2200 | 0.4500 | 0.2300 | 0.2597 | 0.4486 | 0.1889 | win |
| hotpot_v4_n100_hardmatched | bm25_orbit_pool | copy_candidate | 0.5000 | 0.4500 | 0.4500 | 0.0000 | 0.4100 | 0.4400 | 0.0300 | 0.4486 | 0.4408 | -0.0078 | mixed_positive |
| hotpot_v4_n100_hardmatched | bm25_orbit_pool | lexical_guarded | 0.5000 | 0.4500 | 0.4500 | 0.0000 | 0.4100 | 0.4400 | 0.0300 | 0.4486 | 0.4408 | -0.0078 | mixed_positive |
| hotpot_v4_n100_hardmatched | dense_hash_orbit_pool | copy_candidate | 0.5000 | 0.4500 | 0.4500 | 0.0000 | 0.4100 | 0.4400 | 0.0300 | 0.4486 | 0.4408 | -0.0078 | mixed_positive |
| hotpot_v4_n100_hardmatched | dense_hash_orbit_pool | lexical_guarded | 0.5000 | 0.4500 | 0.4500 | 0.0000 | 0.4100 | 0.4400 | 0.0300 | 0.4486 | 0.4408 | -0.0078 | mixed_positive |
| hotpot_v4_n100_structbalanced | bm25_orbit_pool | copy_candidate | 0.5000 | 0.4500 | 0.4000 | -0.0500 | 0.4100 | 0.4200 | 0.0100 | 0.4448 | 0.4124 | -0.0324 | loss_or_mixed |
| hotpot_v4_n100_structbalanced | bm25_orbit_pool | lexical_guarded | 0.5000 | 0.4500 | 0.4000 | -0.0500 | 0.4100 | 0.4200 | 0.0100 | 0.4448 | 0.4124 | -0.0324 | loss_or_mixed |
| hotpot_v4_n100_structbalanced | dense_hash_orbit_pool | copy_candidate | 0.5000 | 0.4500 | 0.4000 | -0.0500 | 0.4100 | 0.4200 | 0.0100 | 0.4448 | 0.4124 | -0.0324 | loss_or_mixed |
| hotpot_v4_n100_structbalanced | dense_hash_orbit_pool | lexical_guarded | 0.5000 | 0.4500 | 0.4000 | -0.0500 | 0.4100 | 0.4200 | 0.0100 | 0.4448 | 0.4124 | -0.0324 | loss_or_mixed |
| hotpot_v4_semanticswap_n100 | bm25_orbit_pool | copy_candidate | 0.5000 | 0.1500 | 0.2333 | 0.0833 | 0.1500 | 0.2400 | 0.0900 | 0.2280 | 0.2719 | 0.0440 | win |
| hotpot_v4_semanticswap_n100 | bm25_orbit_pool | lexical_guarded | 0.5000 | 0.1500 | 0.2333 | 0.0833 | 0.1500 | 0.2400 | 0.0900 | 0.2280 | 0.2719 | 0.0440 | win |
| hotpot_v4_semanticswap_n100 | dense_hash_orbit_pool | copy_candidate | 0.5000 | 0.1500 | 0.2333 | 0.0833 | 0.1500 | 0.2400 | 0.0900 | 0.2280 | 0.2719 | 0.0440 | win |
| hotpot_v4_semanticswap_n100 | dense_hash_orbit_pool | lexical_guarded | 0.5000 | 0.1500 | 0.2333 | 0.0833 | 0.1500 | 0.2400 | 0.0900 | 0.2280 | 0.2719 | 0.0440 | win |
| hotpot_v4_supportpreserve_n100 | bm25_orbit_pool | copy_candidate | 0.5000 | 0.0000 | 0.3833 | 0.3833 | 0.0000 | 0.4300 | 0.4300 | 0.1528 | 0.4193 | 0.2664 | win |
| hotpot_v4_supportpreserve_n100 | bm25_orbit_pool | lexical_guarded | 0.5000 | 0.0000 | 0.3833 | 0.3833 | 0.0000 | 0.4300 | 0.4300 | 0.1528 | 0.4193 | 0.2664 | win |
| hotpot_v4_supportpreserve_n100 | dense_hash_orbit_pool | copy_candidate | 0.5000 | 0.0000 | 0.3833 | 0.3833 | 0.0000 | 0.4300 | 0.4300 | 0.1528 | 0.4193 | 0.2664 | win |
| hotpot_v4_supportpreserve_n100 | dense_hash_orbit_pool | lexical_guarded | 0.5000 | 0.0000 | 0.3833 | 0.3833 | 0.0000 | 0.4300 | 0.4300 | 0.1528 | 0.4193 | 0.2664 | win |

## Claim Policy

This matrix expands the end-to-end proxy to two retrieval policies and two generators over the materialized v4 orbit corpus. It is still a local-corpus proxy, not a full Wikipedia retrieval-generation reproduction.
