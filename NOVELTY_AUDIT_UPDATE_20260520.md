# Novelty Audit Update - 2026-05-20

Scope: fresh literature check for CSRM-RAG after recovering session `019e41ac-628a-7a81-91af-926c54edd17b`. This update supplements `NOVELTY_AUDIT.md`.

## Sources Checked

- CoRM-RAG: https://arxiv.org/abs/2605.01302
- SURE-RAG: https://arxiv.org/abs/2605.03534
- S2G-RAG: https://arxiv.org/abs/2604.23783
- Controlling Risk of RAG with Counterfactual Prompting: https://arxiv.org/abs/2409.16146
- Sufficient Context: https://arxiv.org/abs/2411.06037
- Stable-RAG: https://arxiv.org/abs/2601.02993

## Updated Collision Map

| Work | Closest overlap | Collision risk | CSRM-RAG distinction |
| --- | --- | --- | --- |
| CoRM-RAG | Counterfactual query perturbations and document-level evidence critic | Very high, because CSRM-RAG is explicitly built from CoRM-RAG | CSRM changes the decision unit from independent documents to a query-centered orbit of evidence sets and evaluates selective risk over orbit stability. |
| SURE-RAG | Set-level sufficiency, conflict, uncertainty, selective answering | Very high for any "single retrieved set is sufficient" claim | CSRM must avoid claiming plain set sufficiency as novelty; its surviving claim is that one sufficient set can still be counterfactually unstable across perturbation orbits. |
| S2G-RAG | Iterative sufficiency and missing-gap judgment | Medium-high for "detect missing evidence" framing | S2G controls iterative retrieval gaps; CSRM scores the robustness of already materialized evidence-set orbits under perturbations and abstention. |
| Counterfactual Prompting for RAG risk | Counterfactual inputs for risk control and abstention | Medium | That work perturbs prompts to assess answer confidence; CSRM compares aligned evidence-set orbits and uses orbit-level selective risk. |
| Sufficient Context | Context sufficiency and abstention | Medium | It motivates sufficiency as a bottleneck but does not introduce counterfactual orbit stability or alignment-sensitive perturbation ablations. |
| Stable-RAG | Stability under retrieved-document permutations | Medium | It studies ordering/permutation-induced hallucination; CSRM studies evidence sufficiency stability under cognitive/query perturbations and support-key alignment. |

## Current Novelty Position

The safest novelty claim is:

> A single evidence set that appears sufficient can still be unsafe if its support/conflict/missing profile is unstable across answer-preserving cognitive perturbation orbits. CSRM-RAG operationalizes this as an orbit-level selective-risk score and shows that correctly aligned perturbation orbits matter beyond document robustness, single-set sufficiency, and naive perturbation averaging.

This remains plausibly distinct from the closest papers because the mechanism and evaluation unit are different:

- CoRM-RAG: document-level robustness to perturbed queries.
- SURE-RAG: one evidence set for one query-answer pair.
- S2G-RAG: iterative retrieval controller for missing gaps.
- Sufficient Context: classifies whether a context is enough to answer.
- Stable-RAG: retrieved-document order stability.
- Counterfactual Prompting: prompt-level confidence/risk assessment.

## Main Reviewer Risk

The largest risk is that reviewers see CSRM-RAG as "CoRM-RAG plus SURE-RAG plus perturbation ensembling." The current experiments reduce but do not eliminate that risk:

- Positive: CSRM beats CoRM clean scoring, SURE-style single-set sufficiency, naive orbit averaging, and shuffled perturbations on Hotpot and FEVER v3 bridge data.
- Positive: the NLI set-level probe suggests the signal is not tied only to one verifier-feature source.
- Weak: labels remain heuristic rather than human-audited.
- Weak: full CoRM-RAG reproduction is blocked by unavailable data/index artifacts and missing runtime dependencies.
- Weak: calibration is not strong enough for a formal risk guarantee.

## Required Framing for a NeurIPS-Grade Paper

Use:

- "counterfactual sufficiency stability"
- "orbit-level selective risk"
- "aligned perturbation orbits"
- "feature-source sensitivity probe"
- "bridge study pending human audit"

Avoid:

- "we solve robust RAG"
- "verified risk guarantee"
- "human-audited"
- "full CoRM-RAG reproduction"
- "new evidence sufficiency verifier" unless the verifier is validated separately

## Minimum Additional Evidence To Raise Novelty Confidence

1. Human-audit the v3 pilot and paper-grade stress labels.
2. Show CSRM continues to beat SURE-style and naive perturbation averaging on adjudicated labels.
3. Include the NLI set-level probe only as sensitivity evidence.
4. Add a direct comparison table against CoRM-RAG, SURE-RAG, S2G-RAG, Sufficient Context, Stable-RAG, and Counterfactual Prompting in the paper.
5. If full CoRM-RAG data cannot be obtained, explicitly position the result as a released-critic bridge study rather than an end-to-end reproduction.

## Quick Recheck - 2026-05-21

Additional primary-source spot checks:

- CoRM-RAG: https://arxiv.org/abs/2605.01302
- SURE-RAG: https://arxiv.org/abs/2605.03534
- Causal-Counterfactual RAG: https://arxiv.org/abs/2509.14435
- Beyond Relevance / RAG Information Coverage: https://arxiv.org/abs/2603.08819

No checked source weakens the main collision assessment. The nearest collision is still CoRM-RAG plus SURE-RAG: CoRM-RAG owns document-level counterfactual robustness under cognitive perturbations, while SURE-RAG owns set-level sufficiency/uncertainty aggregation. Causal-Counterfactual RAG broadens the counterfactual-RAG terminology risk, and information-coverage work reinforces that relevance is not enough, but neither directly claims aligned evidence-set orbit stability as the evaluation unit.

Updated writing constraint: the paper should not present CSRM-RAG as a new generic counterfactual RAG framework. It must be framed narrowly as an orbit-level stability layer over evidence sufficiency, with shuffled-orbit and naive-orbit baselines as the key novelty defense.
