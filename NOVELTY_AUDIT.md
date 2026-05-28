# NOVELTY_AUDIT

Date: 2026-05-20

Goal: decide what remains novel enough for NeurIPS main track after reading the project plans and checking current literature.

## 1. Evidence Sources

Local sources:

- `缝合方法论.md`
- `NeurIPS低算力缝合选题详细方案.md`
- `external_repos/CoRM-RAG/README.md`
- `external_repos/CoRM-RAG/src/run_evaluation.py`
- `external_repos/CoRM-RAG/src/train_critic.py`

External sources checked:

- CoRM-RAG, arXiv 2605.01302, submitted 2026-05-02.
- SURE-RAG, arXiv 2605.03534, submitted 2026-05-05.
- S2G-RAG, arXiv 2604.23783.
- Controlling Risk of RAG with Counterfactual Prompting, arXiv 2409.16146.
- Sufficient Context, arXiv 2411.06037.
- Stable-RAG, arXiv 2601.02993.
- FaithfulRAG, ACL 2025 long paper.
- Related "beyond relevance / utility-centric retrieval / information coverage" search results.

See `NOVELTY_AUDIT_UPDATE_20260520.md` for the latest collision map.

## 2. Closest Work Map

| Work | Main unit | Core bottleneck | Why it matters here |
|---|---|---|---|
| CoRM-RAG | document-query pair | semantic relevance is not decision robustness | Base method X and perturbation mechanism |
| FaithfulRAG | fact conflict between parametric and retrieved knowledge | context faithfulness under knowledge conflict | strong conflict baseline, not a perturbation-orbit method |
| SURE-RAG | evidence set for one query-answer pair | retrieval is not verification; sufficiency is set-level | directly overlaps with the original SufCal-RAG plan |
| S2G-RAG | iterative evidence memory | missing-gap judgment during multi-turn retrieval | raises the bar for any "gap detection" framing |
| Sufficient Context | context classification | whether retrieved context is enough to answer | supports the bottleneck but overlaps with plain sufficiency |
| Stable-RAG | document-order permutations | retrieved-order instability | adjacent stability work; distinct from query/evidence orbit stability |
| Beyond Relevance / coverage work | retrieval stack and generation coverage | relevance does not ensure information coverage | supports the problem but also raises novelty bar |

## 3. Rejected Claim

Rejected:

```text
Document-level robustness does not imply set-level evidence sufficiency, so we add a set-level sufficiency critic.
```

Reason:

- This is essentially SURE-RAG's abstract-level claim.
- Even if implemented on top of CoRM-RAG, reviewers can argue it is an obvious composition of CoRM-RAG and SURE-RAG.
- Novelty level after SURE-RAG: likely N1/N2, maybe N3 only with unusually strong experiments.

## 4. Surviving Claim

Surviving:

```text
Single-set sufficiency does not imply counterfactual sufficiency stability.
```

More precise:

```text
For robust RAG under biased or false-premise queries, an evidence set is reliable only if its answer support, missingness, and conflict profile remain stable across a controlled orbit of cognitive perturbations that should preserve the underlying answer.
```

This is meaningfully different from:

- CoRM-RAG: document-level robustness under perturbations.
- SURE-RAG: set-level sufficiency for one query-answer-evidence tuple.
- FaithfulRAG: conflict with parametric knowledge.

## 5. Novelty Gate Score

| Criterion | Score | Evidence |
|---|---:|---|
| New bottleneck | high | counterfactual fragility of evidence sufficiency is not the same as relevance, document robustness, or single-set sufficiency |
| Mechanism specificity | medium-high | perturbation orbit, stability score, conflict monotonicity, conformal selective threshold |
| Avoids simple module stacking | medium-high | the key unit changes from a set to an orbit of sets |
| Low-compute feasibility | medium | can reuse CoRM-RAG outputs and small verifier; full RAG evaluation still has engineering cost |
| Experimental falsifiability | high | can construct fragile-orbit stress splits and compare with max score, mean score, and SURE-style aggregation |
| NeurIPS main-track potential | conditional | requires real data, human audit, strong baselines, and no obvious win by SURE-RAG plus threshold |

Overall novelty target: N4 if the stress split reveals a systematic failure in CoRM-RAG and SURE-RAG style baselines.

Update after the 2026-05-20 check: N4 remains possible only if the paper foregrounds counterfactual sufficiency stability and orbit alignment. A plain "set sufficiency verifier" or "counterfactual prompting for abstention" framing is no longer novel enough.

## 6. Required Anti-Scoop Controls

The paper must include these comparisons:

- CoRM-RAG document max score threshold.
- CoRM-RAG document mean score threshold.
- SURE-style single-set sufficiency score.
- SURE-style score plus more conservative threshold.
- Naive perturbation ensemble that averages single-set sufficiency over perturbations.
- CSRM-RAG with stability terms removed.
- CSRM-RAG with conflict monotonicity removed.

The method is not NeurIPS-ready unless it beats the naive perturbation ensemble at comparable coverage and verifier-call budget.

## 7. Red Flags

Stop or pivot if any of these occur:

- SURE-style single-set sufficiency plus threshold already matches CSRM.
- Gains appear only on a synthetic split and not on HotpotQA, NQ, FEVER, or TruthfulQA-style data.
- The perturbation generator changes the answer instead of only changing cognitive framing.
- Human audit shows labels are ambiguous or shortcut-driven.
- The final method needs substantially more LLM calls than baselines.
