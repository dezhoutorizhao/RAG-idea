# End-to-End Risk-Coverage Curves

Generated: `2026-05-29T05:04:29.942024+00:00`

Datasets: `6`
Retrievers: `['bm25_orbit_pool', 'dense_hash_orbit_pool']`
Generators: `['copy_candidate', 'lexical_guarded']`
Rows: `24`
Protocol complete: `True`
SVG: `paper\figures\end2end_risk_coverage_curves_20260529.svg`

## Aggregate Mean Risk

| Coverage | CSRM | Strongest non-CSRM | Delta |
|---:|---:|---:|---:|
| 0.10 | 0.2417 | 0.3229 | 0.0812 |
| 0.20 | 0.2083 | 0.3146 | 0.1062 |
| 0.30 | 0.2056 | 0.3562 | 0.1507 |
| 0.50 | 0.2000 | 0.3892 | 0.1892 |
| 0.70 | 0.3393 | 0.4101 | 0.0708 |
| 0.90 | 0.4537 | 0.4715 | 0.0178 |
| 1.00 | 0.5008 | 0.5008 | 0.0000 |

## Method Curves

| Method | Mean AURC | Risk@30 mean | Risk@50 mean |
|---|---:|---:|---:|
| corm_max_clean | 0.4906 | 0.4819 | 0.4875 |
| csrm | 0.2889 | 0.2056 | 0.2000 |
| generator_confidence | 0.4919 | 0.4847 | 0.4921 |
| naive_orbit_average | 0.3909 | 0.3583 | 0.3917 |
| retriever_confidence | 0.5007 | 0.4993 | 0.4988 |
| single_set_sure_style | 0.5030 | 0.4944 | 0.5000 |
| strongest_non_csrm | 0.3890 | 0.3562 | 0.3892 |

## Claim Policy

This figure summarizes risk-coverage curves for the local-corpus end-to-end proxy matrix. It is useful Phase 5 visualization evidence, but it is not a full Wikipedia/CoRM-RAG retrieval-generation reproduction.
