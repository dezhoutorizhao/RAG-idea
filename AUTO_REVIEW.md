# Auto Review Loop

Direction: CSRM-RAG as an improvement over CoRM-RAG for counterfactual selective RAG.

Status: Round 1 strict self-review complete. This is not yet a positive submission decision.

## Round 1 Review

Score: 5.5 / 10 for a NeurIPS main-track target.

### Strengths

- The novelty claim is sharper than single-set sufficiency: the method targets counterfactual sufficiency stability across perturbation orbits.
- HotpotQA bridge results are strong under released CoRM Evidence Critic scores, not only TF-IDF proxies.
- Main Hotpot result is stable across three random data seeds.
- Baselines include CoRM max/mean clean scoring, SURE-style single-set sufficiency, naive orbit averaging, first-perturbation-only, and component ablations.
- Shuffled-perturbation ablation collapses, showing the gain is not explained by simply using more verifier calls; correct orbit alignment matters.
- Answer/support-signature consistency ablation is consistently weak, supporting a concrete mechanism.

### Major Weaknesses

- The main labels are still structural heuristics from Hotpot supporting facts and FEVER gold evidence, not human-audited labels.
- The original FEVER second-domain split was too easy for naive orbit averaging. A near-miss dilution split now differentiates CSRM from naive averaging, but it is still heuristic and unaudited.
- Full CoRM-RAG retrieval-generation reproduction on NQ/Biased-NQ/TruthfulQA is blocked by missing `wiki.faiss`, `wiki_passages.jsonl`, `biased_nq_test.jsonl`, and `faiss`.
- No validated verifier replaces the failed generic NLI smoke attempt.
- The current results are selective-risk/orbit-detection results, not full RAG generation quality results.
- Calibration still fails to provide a formal risk guarantee; the claim must remain risk reduction rather than guaranteed risk control.

### Required Fixes Before Submission Claim

1. Complete the 100-orbit human audit and report agreement, disagreements, and exclusion rules.
2. Human-audit the FEVER near-miss dilution split or replace it with a naturally labeled second-domain stress split.
3. Either acquire the original CoRM-RAG evaluation data or explicitly frame the paper as a stress-test extension using released critic scores over independently constructed orbits.
4. Add a validated verifier or a clear human-label protocol for support, conflict, and missingness fields.
5. Add failure cases and limitations with examples, especially where near-miss labels are heuristic and where calibration does not transfer.

### Fixes Implemented After Review

- Added `experiments/summarize_audit.py` and `AUDIT_PROTOCOL.md`.
- Added `csrm_shuffled_perturbations` and `csrm_no_worst_sufficiency` ablations.
- Recomputed Hotpot and FEVER evaluation files with the new ablations.
- Confirmed current test suite passes.

### Current Decision

Needs manual follow-up and stronger evidence before it can be called NeurIPS main-track ready.
