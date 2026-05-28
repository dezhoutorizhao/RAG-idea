# IDEA_REPORT: improve method X from CoRM-RAG

Date: 2026-05-20

Direction: improve CoRM-RAG, ref paper `Beyond Semantic Relevance: Counterfactual Risk Minimization for Robust Retrieval-Augmented Generation`.

Target bar: NeurIPS main track. The idea must be at least N4 under `缝合方法论.md`: it must identify a new bottleneck and solve it with a mechanism-level design, not only add a verifier or threshold.

## 1. Source Reading

### From `缝合方法论.md`

The project must follow a bottleneck-first route:

- Start from a reproducible failure mode, not from a module.
- Extract mechanisms from papers, not surface structures.
- Prove complementarity with controlled ablations.
- Use bottleneck-specific metrics, not only average scores.
- Pass novelty, feasibility, and ablation gates before writing claims.

The relevant route is Route A, "瓶颈诊断型": diagnose a bottleneck, connect cross-paper mechanisms, implement the smallest necessary operator, then prove it with stress splits and ablations.

### From `NeurIPS低算力缝合选题详细方案.md`

The original Topic 1 proposal is:

- Base method: CoRM-RAG.
- Known CoRM-RAG contribution: semantic relevance does not imply decision robustness under false premise or confirmation bias.
- Proposed next bottleneck in the local plan: document-level robustness does not imply set-level evidence sufficiency.
- Low-compute recipe: use released CoRM-RAG critic, build a stress split, train a small set-level critic, and evaluate selective risk.

This is a strong starting point, but it is no longer sufficient as a standalone novelty claim because of the newly identified SURE-RAG overlap.

## 2. Literature and Novelty Update

### Core references verified

- CoRM-RAG, arXiv 2605.01302, submitted 2026-05-02. It aligns retrieval with decision safety through cognitive perturbations and a document-level Evidence Critic.
- FaithfulRAG, ACL 2025 long paper. It targets fact-level conflict between parametric knowledge and retrieved context.
- SURE-RAG, arXiv 2605.03534, submitted 2026-05-05. It explicitly frames evidence sufficiency as a set-level property and aggregates pair-level claim-evidence verifier outputs into coverage, disagreement, conflict, uncertainty, and selective decision signals.

### Novelty consequence

The original "SufCal-RAG" idea is now too close to SURE-RAG:

```text
question + candidate answer + retrieved evidence
  -> pair-level support/refute/insufficient verifier
  -> set-level coverage/conflict/uncertainty
  -> selective answer or abstain
```

That design is likely N1 or N2 after SURE-RAG, not NeurIPS main track. It can only serve as a baseline.

## 3. New Research Thesis

Title candidate:

```text
Counterfactual Set Risk Minimization for Selective Retrieval-Augmented Generation
```

Short name:

```text
CSRM-RAG
```

One-sentence thesis:

```text
Document-level robustness and set-level sufficiency are both incomplete unless the evidence set remains sufficient under cognitive query perturbations; reliable RAG requires calibrating the counterfactual stability of evidence support across a perturbation orbit.
```

Core bottleneck:

```text
CoRM-RAG can select individually robust documents, and SURE-RAG can verify sufficiency for a single retrieved set, but neither directly asks whether the evidence set remains sufficient when the user query is counterfactually perturbed by false premises, confirmation bias, missing-hop framing, or entity-swapped assumptions.
```

## 4. Mechanism Card

Method: CSRM-RAG.

Solved bottleneck: evidence set sufficiency can be spuriously high for a clean query but counterfactually fragile under biased or false-premise variants.

Core mechanism:

- Build a perturbation orbit `P(q) = {q, q_1, ..., q_m}` using CoRM-RAG-style cognitive perturbations.
- Retrieve or reuse top-k evidence sets for each perturbation.
- Score each set with support, coverage, conflict, missingness, and retrieval uncertainty.
- Add counterfactual invariance terms: support stability, answer/support-signature stability, evidence overlap stability, and conflict monotonicity.
- Calibrate selective generation using a threshold selected on a calibration split.

Inputs and outputs:

- Input: query, candidate answer, top-k evidence documents, document-level CoRM scores, optional pair-level verifier probabilities.
- Output: answerability probability, counterfactual fragility score, abstention decision, and interpretable diagnostics.

Inductive bias:

- A genuinely sufficient evidence set should remain sufficient under non-answer-changing cognitive perturbations.
- A false-premise or missing-hop perturbation should increase abstention probability unless new evidence resolves it.

Computational profile:

- Does not retrain the generator.
- Can reuse CoRM-RAG critic and a small verifier.
- First pilot can be run with rule features or DeBERTa-base style pair verification.

## 5. Candidate Ideas

### Idea 1: CSRM-RAG, Counterfactual Set Risk Minimization

Novelty level: N4 target.

Why it is not SURE-RAG:

- SURE-RAG verifies one evidence set for one query-answer pair.
- CSRM-RAG verifies whether sufficiency is stable across a cognitive perturbation orbit.
- The main metric is counterfactual selective risk, not only single-set Macro-F1 or risk-coverage.

Minimal implementation:

- Represent each example as a query orbit with per-perturbation evidence sets.
- Aggregate set scores per perturbation.
- Penalize fragile cases where clean support is high but perturbed support collapses, conflict rises, or answer support changes.
- Selectively answer only when both clean sufficiency and counterfactual stability pass calibration thresholds.

Key hypotheses:

- H1: CoRM-RAG and SURE-style single-set scores fail on counterfactually fragile evidence sets.
- H2: Adding perturbation-orbit stability lowers selective risk at fixed coverage.
- H3: The gain remains after controlling for number of verifier calls and document scores.

Decision: selected as the main pipeline idea.

### Idea 2: Minimal Counterfactual Evidence Hitting Set

Novelty level: N3 to N4 if supported.

Mechanism:

- Extract atomic answer claims.
- Find a minimal evidence subset that covers every claim across clean and perturbed queries.
- Abstain when no stable hitting set exists.

Risk:

- May collapse into an engineering variant of SURE-RAG if the atomic claim extraction is weak.

Decision: keep as an ablation or analysis module inside Idea 1.

### Idea 3: Conflict Monotonicity Calibration

Novelty level: N3.

Mechanism:

- Under false-premise perturbations, true evidence should either refute the premise or increase uncertainty, not silently preserve confidence.
- Use monotonicity constraints on conflict and uncertainty across perturbations.

Risk:

- Too narrow as a standalone paper.

Decision: use as one component and diagnostic in Idea 1.

## 6. Gate 1 Decision

AUTO_PROCEED is true in the research-pipeline skill. The top-ranked idea is selected:

```text
Idea 1: CSRM-RAG, Counterfactual Set Risk Minimization for Selective RAG.
```

Reason:

- It directly addresses the SURE-RAG novelty collision.
- It remains anchored to CoRM-RAG's counterfactual perturbation mechanism.
- It yields a clean NeurIPS-level claim: RAG reliability has a fourth layer, counterfactual sufficiency stability, beyond relevance, document robustness, and single-set sufficiency.

## 7. Immediate Next Stage

Implementation should start with a local, dependency-light pilot:

1. Implement schemas for query perturbation orbits and evidence sets.
2. Implement baseline scores: max CoRM document score, mean CoRM score, SURE-style sufficiency score.
3. Implement CSRM score: clean sufficiency plus counterfactual stability, answer/support-signature consistency, evidence overlap, and conflict monotonicity.
4. Run a synthetic stress split to validate metric behavior.
5. Replace synthetic verifier features with actual CoRM-RAG outputs and a small NLI verifier in the next stage.
