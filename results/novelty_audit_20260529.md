# Novelty Audit Update

Generated: `2026-05-29T08:23:28.772614+00:00`
Search date: `2026-05-29`

Method: CSRM-RAG: counterfactual sufficiency stability and calibrated selective risk over aligned evidence-set orbits for robust RAG.

Overall novelty score: `6.5/10`
Recommendation: `proceed_with_caution`
Ready for strong novelty claim: `False`

## Core Claims

| Claim | Novelty | Closest prior | Assessment |
|---|---|---|---|
| Aligned evidence-set orbits expose fragile RAG items that clean sufficiency misses. | `medium` | CoRM-RAG; Sufficient Context; SURE-RAG | Plausible if positioned as orbit-level counterfactual stability rather than plain sufficiency. |
| CSRM estimates selective item risk from orbit statistics under equal verifier-call budgets. | `medium` | SURE-RAG; CoRM-RAG | Novelty depends on human-audited orbit labels and strong equal-budget baselines; current evidence is partial. |
| Orbit alignment is a necessary mechanism for counterfactual selective RAG. | `medium-high` | CF-RAG; CoRM-RAG | Mechanism is defensible after shuffled-alignment ablation and formalization, but needs careful distinction from counterfactual-query methods. |
| CSRM provides formal/general risk control for robust RAG. | `low` | Conformal factuality for RAG; CoRM-RAG risk-aware abstention | Do not claim. Current FEVER evidence is negative at the 0.20 target. |

## Closest Prior Work

| Paper | Year | Venue/status | Overlap | Difference | Risk |
|---|---:|---|---|---|---|
| [Beyond Semantic Relevance: Counterfactual Risk Minimization for Robust Retrieval-Augmented Generation](https://arxiv.org/abs/2605.01302) | 2026 | arXiv 2605.01302 | Direct parent paper: counterfactual risk minimization for robust RAG and risk-aware abstention. | CSRM-RAG must be framed as a selective risk detector and audit protocol over aligned evidence-set orbits, not as a new CoRM-RAG retriever. | `high` |
| [SURE-RAG: Sufficiency and Uncertainty-Aware Evidence Verification for Selective Retrieval-Augmented Generation](https://arxiv.org/abs/2605.03534) | 2026 | arXiv 2605.03534 | Closest sufficiency-verifier and selective-RAG abstention work. | SURE-RAG focuses on sufficiency/uncertainty verification; CSRM-RAG novelty must come from counterfactual orbit stability and aligned perturbation evidence. | `high` |
| [Sufficient Context: A New Lens on Retrieval Augmented Generation Systems](https://research.google/pubs/sufficient-context-a-new-lens-on-retrieval-augmented-generation-systems-2/) | 2025 | ICLR 2025 | Defines sufficient context and uses sufficiency for guided abstention. | It does not provide item-level counterfactual evidence-orbit risk estimation or aligned orbit ablations. | `medium` |
| [Counterfactual Reasoning for Retrieval-Augmented Generation](https://openreview.net/forum?id=9U51rOnGko) | 2026 | ICLR 2026 | Counterfactual queries and arbitration for robust RAG. | CF-RAG uses counterfactual query reasoning; CSRM-RAG must emphasize evidence-set orbit stability and selective risk under equal verifier budget. | `high` |
| [Causal-Counterfactual RAG: The Integration of Causal-Counterfactual Reasoning into RAG](https://arxiv.org/abs/2509.14435) | 2025 | arXiv 2509.14435 | Causal and counterfactual reasoning integrated into RAG. | Broader causal-counterfactual answer generation; not the same as calibrated orbit-level selective risk detection. | `medium` |
| [Is Conformal Factuality for RAG-based LLMs Robust? Novel Metrics and Systematic Insights](https://arxiv.org/abs/2603.16817) | 2026 | arXiv 2603.16817 | Robust factuality and calibration-style guarantees for RAG. | Relevant to risk-control claims; current CSRM-RAG evidence is empirical and must not claim formal conformal coverage. | `medium` |

## Positioning

Frame the contribution as an audit-grade, leakage-controlled, aligned evidence-orbit selective-risk protocol built on top of CoRM-style critic scores. Avoid claiming a new retrieval paradigm, formal risk control, or all-win superiority.

## Required To Upgrade

- Complete the 1000-item Human Audit v4 labels and report human-label metrics.
- Obtain API-backed LLM-judge baseline/correlation scores or remove LLM-judge claims.
- Keep full CoRM-RAG reproduction unsupported until the storage/index artifacts are repaired.
- Write related work around SURE-RAG, Sufficient Context, CF-RAG, and CoRM-RAG as closest neighbors.

## Claim Policy

This is a current literature-positioning audit, not proof of novelty. It supports a narrow proceed-with-caution framing and highlights prior-work risks that must be disclosed in any NeurIPS submission.
