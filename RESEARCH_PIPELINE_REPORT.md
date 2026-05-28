# Research Pipeline Report

Direction: `/research-pipeline "improve method X"` with reference paper CoRM-RAG.

Current status: active, not complete.

## Stage 1: Idea Discovery

Completed initial reading of:

- `缝合方法论.md`
- `NeurIPS低算力缝合选题详细方案.md`
- CoRM-RAG repository README and core training/evaluation scripts.

External literature and novelty check found a critical collision:

- Plain single-set sufficiency calibration is too close to SURE-RAG.

Decision:

- Do not pursue plain SufCal-RAG.
- Use CSRM-RAG: Counterfactual Set Risk Minimization for Selective RAG.
- Surviving novelty claim: single-set sufficiency does not imply counterfactual sufficiency stability across perturbation orbits.
- Fresh 2026-05-20 check adds S2G-RAG, Sufficient Context, Stable-RAG, and counterfactual prompting as adjacent work. The novelty bar now requires orbit-level sufficiency stability and alignment-sensitive ablations, not just another sufficiency verifier.

Artifacts:

- `IDEA_REPORT.md`
- `NOVELTY_AUDIT.md`
- `NOVELTY_AUDIT_UPDATE_20260520.md`
- `EXPERIMENT_PLAN.md`

## Stage 2: Implementation

Implemented a dependency-light CSRM prototype under `src/csrm_rag` and `experiments`.

Implemented:

- Orbit data schema for clean query plus perturbation evidence sets.
- Risk-coverage, AURC, calibration, and AUROC metrics.
- CoRM max/mean document-score baselines.
- SURE-style single-set sufficiency baseline.
- Naive orbit averaging baseline.
- CSRM fixed-weight scoring and component ablations.
- Risk-sensitive CSRM scoring with an explicit `worst_sufficiency` component so a single failed perturbation cannot be hidden by benign perturbation averages.
- CoRM `scored_{dataset}.json` converter.
- HotpotQA distractor orbit builder.
- Group-split logistic calibration experiment.
- NLI verifier smoke script.
- NLI set-level cross-scorer sensitivity probe on v3 audit samples.
- Released CoRM Evidence Critic scoring script for existing orbit JSONL files.
- Stratified audit sampler for human review.
- Multi-seed evaluation summarizer.
- Audit summary and strict review-loop artifacts.
- Claim ledger and local experiment integrity audit.
- Result-to-claim verdict and case-study extraction artifacts.
- Paired bootstrap method-comparison artifacts.
- CoRM-RAG original evaluation reproduction preflight gate.
- CoRM-RAG public release manifest checker.
- CoRM-RAG released-source reconstruction-path audit.
- Supplemental CoRM artifact reconstruction helpers for FAISS and Biased-NQ materialization.
- Machine-readable remote reconstructed-CoRM execution plan.
- Secret-free remote reconstructed-CoRM shell script pack.
- Remote CoRM runtime bootstrap with torch/CUDA, FAISS, Transformers, datasets, and vLLM import readiness.
- Remote HF/Contriever streaming smoke for a small real-Wikipedia FAISS path.
- Remote template Biased-NQ smoke path for API-free plumbing checks.
- Remote reconstructed-eval staging patch to avoid the almost-full root `/tmp`.
- Remote bounded template Biased-NQ eval-smoke script with an `EVAL_MAX_EXAMPLES` cap.
- Remote watcher that will launch the bounded template eval-smoke path once `wiki.faiss` exists.
- Remote isolated partial-index template eval smoke, which validated partial FAISS loading, retrieval, released CoRM critic scoring, vLLM generation, and metric writing on a 200,000-vector index; this is deployment plumbing evidence only.

Current verification:

```text
$env:PYTHONPATH='D:\缝合RAG-idea\src;D:\缝合RAG-idea'; python -m pytest -q
73 passed
```

## Current Results

### Synthetic smoke test

Synthetic results validate the failure-mode logic only; they are not claim-level evidence.

| Method | AUROC | Risk@30% coverage |
|---|---:|---:|
| CoRM max clean | 0.5182 | 0.7667 |
| CoRM mean clean | 0.5215 | 0.7700 |
| SURE-style single set | 0.9859 | 0.3433 |
| Naive orbit average | 0.9639 | 0.3767 |
| CSRM | 1.0000 | 0.3333 |

### HotpotQA heuristic bridge

200 HotpotQA validation examples produced 800 orbit records:

- 200 stable support
- 200 missing hop
- 200 false premise
- 200 distractor

Earlier heuristic run used TF-IDF as a CoRM-score proxy. It showed a useful real-data signal, but was not sufficient because support/conflict/missing and CoRM scores were heuristic.

### HotpotQA with released CoRM critic scores

The released CoRM-RAG Evidence Critic checkpoint was loaded from:

```text
checkpoints/hf/critic-v12-mixed/checkpoint-latest/state.pt
```

`experiments/score_orbits_corm.py` rescored all 800 Hotpot orbit records with the released critic. This does not require the full Wikipedia FAISS index because it scores the already materialized Hotpot contexts.

Artifacts:

- `results/hotpot_orbits_corm_800.jsonl`
- `results/hotpot_orbits_corm_800_eval_fullabl.json`
- `results/hotpot_orbits_corm_800_seed17.jsonl`
- `results/hotpot_orbits_corm_800_seed17_eval_fullabl.json`
- `results/hotpot_orbits_corm_800_seed31.jsonl`
- `results/hotpot_orbits_corm_800_seed31_eval_fullabl.json`
- `results/hotpot_corm_multiseed_summary_fullabl.json`

Main metrics, 800 orbits with 500 bootstrap samples, current risk-sensitive CSRM:

| Method | AUROC | AURC | Risk@30% | Risk@50% |
|---|---:|---:|---:|---:|
| CoRM max clean | 0.5000 | 0.7406 | 0.7500 | 0.7500 |
| SURE-style single set | 0.5000 | 0.7388 | 0.7500 | 0.7500 |
| Naive orbit average | 0.8359 | 0.5817 | 0.5000 | 0.5000 |
| CSRM | 0.9974 | 0.4072 | 0.1667 | 0.5000 |
| CSRM without worst sufficiency | 0.9976 | 0.4059 | 0.1667 | 0.5000 |
| CSRM, first perturbation only | 0.9872 | 0.4217 | 0.1792 | 0.5000 |
| CSRM with shuffled perturbations | 0.0004 | 0.9662 | 1.0000 | 1.0000 |
| CSRM without answer consistency | 0.7517 | 0.6621 | 0.6708 | 0.5000 |
| CSRM without overlap | 0.9885 | 0.4282 | 0.1667 | 0.5000 |

Bootstrap intervals:

- CSRM AUROC 95% CI: 0.993-1.000.
- CSRM Risk@30 95% CI: 0.067-0.271.
- Naive orbit average AUROC 95% CI: 0.812-0.859.
- Naive orbit average Risk@30 95% CI: 0.429-0.558.
- CoRM max clean AUROC 95% CI: 0.452-0.547.
- CoRM max clean Risk@30 95% CI: 0.688-0.808.

Interpretation:

- The main bridge result no longer depends on TF-IDF as the CoRM score.
- The released CoRM critic assigns high document robustness to evidence sets that are still orbit-fragile under missing-hop, false-premise, and distractor perturbations.
- CSRM's gain is not explained by simply averaging over perturbations: naive orbit averaging remains substantially worse.
- The answer/support-signature consistency term is important: removing it drops AUROC from 0.9974 to 0.7517 and raises Risk@30 from 0.1667 to 0.6708.
- The shuffled-perturbation ablation collapses, showing the result depends on correctly aligned counterfactual orbits rather than merely spending more verifier calls.
- Removing worst sufficiency does not hurt on Hotpot, so the current Hotpot mechanism is mostly answer/support consistency and orbit alignment rather than the worst-set term.
- This is still a bridge result, not final NeurIPS evidence, because support and missingness labels still rely on Hotpot supporting-fact structure rather than human audit or a validated verifier.

Multi-seed Hotpot stability, 3 random data seeds of 200 Hotpot examples each:

| Method | AUROC mean | AUROC stdev | Risk@30 mean | Risk@30 stdev |
|---|---:|---:|---:|---:|
| CoRM max clean | 0.5000 | 0.0000 | 0.7497 | 0.0006 |
| SURE-style single set | 0.5000 | 0.0000 | 0.7497 | 0.0006 |
| Naive orbit average | 0.8321 | 0.0128 | 0.5119 | 0.0281 |
| CSRM | 0.9976 | 0.0023 | 0.1669 | 0.0004 |
| CSRM with shuffled perturbations | 0.0001 | 0.0002 | 1.0000 | 0.0000 |
| CSRM without answer consistency | 0.7577 | 0.0132 | 0.6468 | 0.0405 |

Interpretation:

- The Hotpot signal is stable across random sample seeds.
- The answer-consistency ablation remains weak across seeds, which supports the proposed mechanism rather than a single lucky split.
- The shuffled-perturbation ablation fails across seeds, which supports counterfactual alignment as a required part of the method.

Paired bootstrap deltas on the main Hotpot seed:

| Comparison | AUROC improvement 95% CI | Risk@30 reduction 95% CI | AURC reduction 95% CI |
|---|---:|---:|---:|
| CSRM vs CoRM max clean | [0.4487, 0.5424] | [0.5000, 0.6750] | [0.2989, 0.3647] |
| CSRM vs SURE-style single set | [0.4634, 0.5297] | [0.5000, 0.6750] | [0.2898, 0.3694] |
| CSRM vs naive orbit average | [0.1366, 0.1855] | [0.2458, 0.4125] | [0.1432, 0.2054] |

### FEVER v3 fact-verification bridge

Added a second real domain using `copenlu/fever_gold_evidence`.

`experiments/build_fever_orbits.py` constructs SUPPORTS/REFUTES fact-verification orbits from FEVER gold evidence. The current FEVER v3 builder supersedes earlier near-miss builders whose audits found invalid missing-evidence coverage, support keys that exceeded the fixed evidence-set budget, and non-gold high-support feature leakage.

- stable gold evidence
- missing evidence
- opposite-label conflicting evidence
- distractor-only evidence
- fragile mixed orbit with benign perturbations plus one critical conflicting perturbation
- near-miss dilution orbit with high-sufficiency but support-signature-mismatched evidence

Artifacts:

- `results/fever_orbits_nearmiss_1200_v3.jsonl`
- `results/fever_orbits_nearmiss_corm_1200_v3.jsonl`
- `results/fever_orbits_nearmiss_corm_1200_v3_eval.json`
- `results/fever_orbits_nearmiss_corm_1200_v3_seed31_eval.json`
- `results/fever_orbits_nearmiss_corm_1200_v3_seed47_eval.json`
- `results/fever_nearmiss_corm_v3_multiseed_summary.json`
- `results/fever_nearmiss_corm_v3_orbit_consistency_audit.json`

Main metrics, 1,200 FEVER v3 near-miss orbits with released CoRM critic scores:

| Method | AUROC | AURC | Risk@30% | Risk@50% |
|---|---:|---:|---:|---:|
| CoRM max clean | 0.5000 | 0.8292 | 0.8333 | 0.8333 |
| SURE-style single set | 0.5000 | 0.8292 | 0.8306 | 0.8317 |
| Naive orbit average | 0.7755 | 0.7687 | 0.6389 | 0.6667 |
| CSRM | 1.0000 | 0.5295 | 0.4444 | 0.6667 |
| CSRM with shuffled perturbations | 0.0041 | 0.9838 | 1.0000 | 1.0000 |

Multi-seed FEVER v3 near-miss stability, 3 random data seeds:

| Method | AUROC mean | AUROC stdev | Risk@30 mean | Risk@30 stdev |
|---|---:|---:|---:|---:|
| CoRM max clean | 0.5000 | 0.0000 | 0.8333 | 0.0000 |
| SURE-style single set | 0.5000 | 0.0000 | 0.8333 | 0.0028 |
| Naive orbit average | 0.7764 | 0.0020 | 0.6407 | 0.0058 |
| CSRM | 1.0000 | 0.0000 | 0.4444 | 0.0000 |
| CSRM with shuffled perturbations | 0.0327 | 0.0531 | 1.0000 | 0.0000 |

Structural audit:

- `results/fever_nearmiss_corm_v3_orbit_consistency_audit.json`
- `results/fever_nearmiss_corm_v3_seed31_orbit_consistency_audit.json`
- `results/fever_nearmiss_corm_v3_seed47_orbit_consistency_audit.json`
- `passed=true`, `error_count=0`
- Scope: structural and dataset-constraint consistency; it checks source provenance, label-source metadata, labels, split names, perturbation counts/types, support-key lineage, duplicate evidence ids, support-key coverage, support-feature provenance, and verifier-feature ranges. It does not replace human semantic audit.

Interpretation:

- FEVER v3 confirms the second-domain pipeline works with released CoRM critic scores after the support-feature provenance fix.
- CoRM clean scoring and single-set sufficiency fail badly on this fact-verification stress split.
- The near-miss dilution split now differentiates CSRM from naive orbit averaging.
- FEVER also confirms that shuffled perturbation alignment fails.
- This is still heuristic bridge evidence because the near-miss support/conflict/missing fields are deliberately constructed and must be audited.

Paired bootstrap deltas on the main FEVER v3 near-miss seed:

| Comparison | AUROC improvement 95% CI | Risk@30 reduction 95% CI | AURC reduction 95% CI |
|---|---:|---:|---:|
| CSRM vs CoRM max clean | [0.4519, 0.5393] | [0.3250, 0.4500] | [0.2728, 0.3247] |
| CSRM vs naive orbit average | [0.2005, 0.2515] | [0.1056, 0.2833] | [0.2155, 0.2601] |

Note: v3 removes the earlier AURC caveat against SURE-style single-set sufficiency on the main FEVER seed, but this remains a heuristic stress bridge until human semantic audit is complete.

### Held-out calibration

Group split on the released-critic Hotpot orbit file:

- Train: 120 base questions / 480 orbits.
- Calibration: 40 base questions / 160 orbits.
- Test: 40 base questions / 160 orbits.

Artifact:

- `results/hotpot_corm_calibrated_800_worst.json`
- `results/hotpot_corm_calibration_multiseed.json`
- `results/fever_nearmiss_corm_v3_calibration_multiseed.json`

Held-out test metrics:

| Method | AUROC | AURC | Risk@30% | Calibrated coverage | Calibrated risk |
|---|---:|---:|---:|---:|---:|
| CoRM max clean | 0.5000 | 0.7406 | 0.7500 | 0.0500 | 0.7500 |
| SURE-style single set | 0.5000 | 0.7406 | 0.7500 | 0.0250 | 0.7500 |
| Naive orbit average | 0.8220 | 0.5888 | 0.5625 | 0.0125 | 0.5000 |
| CSRM fixed weights | 1.0000 | 0.4021 | 0.1667 | 0.4000 | 0.3750 |
| CSRM logistic calibrated | 0.9996 | 0.4001 | 0.1667 | 0.3375 | 0.2593 |

Interpretation:

- Held-out ranking signal is strong.
- Calibration is not yet good enough to claim a formal risk guarantee. On Hotpot, a calibration threshold targeting risk <= 0.20 transferred to mean test risk 0.2032, max 0.2593, and met the target in 2/3 split seeds.
- FEVER v3 near-miss shows the same pattern: mean calibrated risk 0.2449, max 0.3333, and target met in 1/3 split seeds.
- Zero-coverage threshold choices are treated as vacuous and do not count as risk guarantees.
- Current safe claim is selective-risk reduction, not rigorous risk control.

### Conservative risk-control pressure test

Added artifact:

- `experiments/evaluate_risk_control_cp.py`
- `results/hotpot_corm_risk_control_cp_multiseed.json`
- `results/fever_nearmiss_corm_v3_risk_control_cp_multiseed.json`

This uses a one-sided Clopper-Pearson upper bound on calibration-set selective risk to choose the largest non-vacuous threshold satisfying target risk 0.20 at 90% confidence, then evaluates that fixed threshold on held-out test groups.

| Split | Method | Test coverage | Test risk | Target met |
|---|---|---:|---:|---:|
| Hotpot | CSRM logistic calibrated | 0.2938 mean / 0.3125 max | 0.1472 mean / 0.2000 max | 3/3 |
| FEVER v3 near-miss | CSRM logistic calibrated | 0.2069 mean / 0.2250 max | 0.1866 mean / 0.2593 max | 1/3 |

Interpretation:

- The conservative rule improves the Hotpot calibration story from 2/3 to 3/3 target transfer with nonzero coverage.
- FEVER v3 still fails in two of three split seeds, so this does not support a cross-domain or formal risk guarantee.
- Because the bound is estimated on calibration groups and checked empirically on held-out groups, it should be written as a pressure test, not as distribution-free risk control.

### NLI verifier smoke

Doc-level and set-level NLI smoke runs completed:

- `results/hotpot_orbits_nli_smoke.jsonl`
- `results/hotpot_orbits_nli_smoke_eval.json`
- `results/hotpot_orbits_nli_set_smoke.jsonl`
- `results/hotpot_orbits_nli_set_smoke_eval.json`

Finding:

- Generic NLI on the hypothesis "for this question, the answer is X" is unreliable for Hotpot multi-hop sufficiency.
- It often gives low support even when the full supporting set is present.
- Do not use these NLI scores as final verifier evidence without redesigning the verifier task.

### NLI set-level cross-scorer probe

To test whether the CSRM signal is tied only to the original verifier-feature source, the v3 audit samples were rescored with `cross-encoder/nli-deberta-v3-small` at set level. This replaces support/conflict/missing features with off-the-shelf NLI probabilities while keeping the same orbit structure and heuristic labels.

Artifacts:

- `results/audit_sample_100_v3_nli_set.jsonl`
- `results/audit_sample_100_v3_nli_set_eval.json`
- `results/audit_sample_paper_1000_v3_nli_set.jsonl`
- `results/audit_sample_paper_1000_v3_nli_set_eval.json`
- `NLI_PROBE_REPORT.md`

Main paper-grade probe metrics, 1,000 v3 audit-sample orbits:

| Method | AUROC | AURC | Risk@30% |
|---|---:|---:|---:|
| CoRM max clean | 0.5244 | 0.7838 | 0.7800 |
| SURE-style single set | 0.4818 | 0.8202 | 0.8700 |
| Naive orbit average | 0.4880 | 0.7959 | 0.8600 |
| CSRM | 0.7353 | 0.6676 | 0.6267 |
| CSRM with shuffled perturbations | 0.3281 | 0.8921 | 0.9367 |

Interpretation:

- CSRM's directional gain persists under an independent set-level NLI feature source.
- Shuffled perturbation alignment again collapses, supporting the orbit-alignment mechanism.
- This is not human-audited evidence and should be presented only as automated sensitivity analysis.

### Human audit preparation

Prepared stratified audit samples across Hotpot and the current FEVER v3 stress splits:

- `experiments/sample_audit_orbits.py`
- `experiments/export_audit_pack.py`
- `experiments/merge_audit_annotations.py`
- `experiments/summarize_audit.py`
- `experiments/summarize_adjudication.py`
- `experiments/evaluate_audited_orbits.py`
- `experiments/check_audit_readiness.py`
- `results/audit_sample_100_v3.jsonl`
- `results/audit_pack_100_v3.labels.csv`
- `results/audit_pack_100_v3.review.html`
- `results/audit_pack_100_v3.manifest.json`
- `results/audit_pack_100_v3_a1.blind.labels.csv`
- `results/audit_pack_100_v3_a1.blind.review.html`
- `results/audit_pack_100_v3_a1.blind.manifest.json`
- `results/audit_pack_100_v3_a2.blind.labels.csv`
- `results/audit_pack_100_v3_a2.blind.review.html`
- `results/audit_pack_100_v3_a2.blind.manifest.json`
- `results/audit_sample_100_v3_summary.json`
- `results/audit_sample_100_v3_adjudication.json`
- `results/audit_sample_100_v3_readiness.json`
- `results/audit_sample_100_v3_adjudicated_readiness.json`
- `results/audit_sample_paper_1000_v3.jsonl`
- `results/audit_pack_paper_1000_v3.labels.csv`
- `results/audit_pack_paper_1000_v3.review.html`
- `results/audit_pack_paper_1000_v3.manifest.json`
- `results/audit_pack_paper_1000_v3_a1.blind.labels.csv`
- `results/audit_pack_paper_1000_v3_a1.blind.review.html`
- `results/audit_pack_paper_1000_v3_a1.blind.manifest.json`
- `results/audit_pack_paper_1000_v3_a2.blind.labels.csv`
- `results/audit_pack_paper_1000_v3_a2.blind.review.html`
- `results/audit_pack_paper_1000_v3_a2.blind.manifest.json`
- `results/audit_sample_paper_1000_v3_summary.json`
- `results/audit_sample_paper_1000_v3_adjudication.json`
- `results/audit_sample_paper_1000_v3_readiness.json`
- `results/audit_sample_paper_1000_v3_adjudicated_readiness.json`

The audit file contains editable fields:

- `auditor_label_answerable`
- `auditor_failure_type`
- `auditor_notes`

Validation:

- 100 JSONL records parse successfully.
- Split counts are balanced across Hotpot and FEVER stress types.
- Current pilot labeled count is 0/100, so pilot audit completion rate is 0%.
- Current paper-grade candidate labeled count is 0/1,000, with 100 pending orbits in each current stress split.
- Current double-label and adjudication completion rates are 0% for both audit files.
- Current single-annotator and adjudicated-label readiness gates are `ready=false` for both pilot and paper-grade audit files.
- Non-blind CSV/HTML packs are generated for diagnostic review and adjudication support.
- Shuffled blind CSV/HTML packs are generated for two independent annotators on both pilot and paper-grade audit files; these hide expected labels, source answerability labels, and model scores.

This does not satisfy the human-audit gate yet; it only prepares the artifact for manual labeling.

Audited metric recomputation, inter-annotator agreement summaries, blind-label merging, and readiness checks are now scripted. After labels are filled from the blind packs, run `experiments/summarize_adjudication.py` and `experiments/check_audit_readiness.py`; only if the adjudicated readiness report passes should `experiments/evaluate_audited_orbits.py` results be used for audited risk-coverage, AUROC, AURC, and per-split claims.

### Review loop

Round 1 strict review is recorded in:

- `AUTO_REVIEW.md`

Current review score: 5.5 / 10 for a NeurIPS main-track target.

Decision:

- Needs manual follow-up and stronger evidence before it can be called submission-ready.

### Integrity audit

The experiment-audit skill could not be run as an independent cross-model MCP audit because no codex MCP tool is available in this environment. A local deterministic claim-ledger verifier was added instead.

Artifacts:

- `CLAIMS_LEDGER.json`
- `experiments/verify_claims.py`
- `results/claims_verification.json`
- `EXPERIMENT_AUDIT.md`
- `EXPERIMENT_AUDIT.json`

Current audit verdict:

- Overall: WARN.
- Claim-ledger checks: 27/27 passed.
- Integrity limitations: human audit is incomplete, verifier labels remain heuristic despite an automated NLI cross-scorer sensitivity probe, FEVER v3 near-miss now differentiates CSRM from naive averaging and passes structural plus dataset-constraint audits but remains semantically unaudited, conservative risk-control thresholding is Hotpot-only, and full CoRM-RAG retrieval-generation reproduction is missing. The current released CoRM source also lacks exact producers for `wiki.faiss` and `biased_nq_test.jsonl`; supplemental reconstruction helpers, a remote execution plan, a secret-free shell script pack, an import-ready remote runtime, a verified remote checkpoint, a staged-input streaming encoder smoke, a 16-passage real HF/Contriever smoke, an API-free template Biased-NQ smoke, a remote eval-staging patch, a bounded template eval-smoke path, a post-FAISS smoke watcher, and an isolated partial-index template eval smoke now exist, but no full reconstructed CoRM run has completed.

### Result-to-claim

Current result-to-claim verdict:

- `RESULT_TO_CLAIM.md`
- `RESULT_TO_CLAIM.json`

Verdict:

- `claim_supported`: partial.
- `confidence`: medium.
- `integrity_status`: warn.

Supported current claim:

- CSRM reduces selective risk on HotpotQA-derived and FEVER v3 near-miss counterfactual evidence orbits versus CoRM clean scoring, SURE-style single-set sufficiency, and naive orbit averaging when using released CoRM critic scores.
- The same directional ranking pattern persists on the v3 paper-grade audit sample when support/conflict/missing features are replaced with set-level NLI features, as sensitivity evidence only.
- Conservative Clopper-Pearson thresholding supports Hotpot-only empirical risk-target transfer for logistic CSRM at target risk 0.20, but not cross-domain risk control.

Unsupported current claims:

- General robust RAG superiority across tasks.
- Formal calibrated risk guarantee; FEVER v3 still misses the target in two of three split seeds under conservative thresholding.
- Human-audited validity.
- Full CoRM-RAG NQ/Biased-NQ/TruthfulQA reproduction.

### Failure and limitation cases

Representative case-study artifacts:

- `experiments/extract_case_studies.py`
- `results/hotpot_case_studies.json`
- `results/hotpot_case_studies.md`
- `results/fever_nearmiss_v3_case_studies.json`
- `results/fever_nearmiss_v3_case_studies.md`

Current use:

- Supports paper-level failure and limitation analysis.
- Does not replace human audit because cases are selected from heuristic-label bridge data.

## Environment and Blockers

Available:

- PyTorch/CUDA.
- Released CoRM critic checkpoint.
- Current visible GPU previously observed as 1x NVIDIA GeForce RTX 3080.
- Remote server `192.168.103.101:22` has 2x RTX 4090 and a writable `/mnt/ntfs-disk` mount with about 300 GB free; root is effectively full, so remote work must use `/mnt/ntfs-disk`.

Still missing for full CoRM-RAG reproduction:

- `wiki.faiss`
- `wiki_passages.jsonl`
- `biased_nq_test.jsonl`
- `faiss` Python package
- `vllm` Python package

Released-source reconstruction-path audit:

- `experiments/audit_corm_reproduction_path.py`
- `results/corm_reproduction_path_audit.json`
- `reconstructability_status=blocked`
- `supplemental_reconstructability_status=available`
- `src/encode_wikipedia.py` partially scripts `wiki_passages.jsonl` and `wiki_embeddings.npy`.
- No `faiss.write_index` call is present in the available repository, so there is no exact released-script producer for `wiki.faiss`.
- `run_evaluation.py` consumes `biased_nq_test.jsonl`, but no exact builder for that file is detected in the available repository.

Supplemental reconstruction helpers:

- `experiments/build_corm_faiss_index.py` builds a FAISS inner-product index from `wiki_embeddings.npy` or `embeddings_shard_*.npy`.
- `experiments/build_corm_biased_nq_test.py` validates perturbation JSONL and materializes the schema consumed by `run_evaluation.py` as `biased_nq_test.jsonl`.
- These scripts make a reconstructed run more feasible on the remote 4090 server, but results must be reported as reconstructed-pipeline evidence unless exact equivalence to the authors' original artifacts is established.

Reconstructed execution plan:

- `experiments/plan_corm_reconstruction.py`
- `results/corm_reconstruction_plan.json`
- `experiments/materialize_corm_remote_scripts.py`
- `results/corm_remote_scripts_manifest.json`
- `results/corm_remote_scripts/`
- `results/corm_remote_runtime_status.json`
- `results/corm_remote_checkpoint_status.json`
- `results/corm_streaming_encoder_remote_smoke.json`
- `results/corm_streaming_encoder_remote_hf_smoke.json`
- `results/corm_full_wikipedia_job_status.json`
- `results/corm_template_biased_nq_remote_smoke.json`
- `results/corm_eval_stage_dir_patch_status.json`
- `status=planned_not_executed`
- `remote_root=/mnt/ntfs-disk/csrm_corm_reconstruction`
- The plan covers remote directory setup, runtime bootstrap/install, streaming Wikipedia passage/embedding generation, FAISS construction, perturbation generation or staging, Biased-NQ materialization, and reconstructed `run_eval.sh` execution from `external_repos/CoRM-RAG/src`.
- Current local missing reconstruction inputs: `wiki_passages`, `wiki_embeddings`, `wiki_faiss`, `perturbations`, and `biased_nq_test`.
- The materialized script pack has ordered scripts `01_prepare_env.sh` through `05_watch_and_run_template_smoke_eval.sh`, including optional template smoke scripts; its manifest reports `contains_secret_markers=false`.
- Remote runtime status: `results/corm_remote_runtime_status.json` records an import-ready transient `/dev/shm/csrm_corm_runtime` environment with torch `2.4.0+cu121`, CUDA available on 2 GPUs, FAISS, Transformers, datasets, and vLLM `0.5.5`. This is not reproduction evidence.
- Remote checkpoint status: `results/corm_remote_checkpoint_status.json` records that the 5.2GB critic checkpoint was uploaded to `/mnt/ntfs-disk/csrm_corm_reconstruction/workspace/checkpoints/.../state.pt` and SHA256 matched the local file.
- Streaming encoder status: `experiments/encode_corm_wikipedia_streaming.py` avoids the upstream all-in-memory Wikipedia encoder by writing `wiki_passages.jsonl` and `embeddings_shard_*.npy` incrementally. `results/corm_streaming_encoder_remote_smoke.json` records a remote staged-JSONL/dummy-backend smoke that produced two embedding shards and a two-vector FAISS index. `results/corm_streaming_encoder_remote_hf_smoke.json` records a real HF/Contriever/CUDA smoke using `HF_ENDPOINT=https://hf-mirror.com` and `/dev/shm` cache: 16 Wikipedia passages, two 768-dimensional embedding shards, and a 16-vector FAISS index.
- Full Wikipedia job status: `results/corm_full_wikipedia_job_status.json` records repeated NTFS/fuseblk storage failures and the current 1M-shard recovery. The initial full run and the first 1M resume proved that complete 2.9GB shards can be written, but later 4M and 2M attempts produced partial `embeddings_shard_000049.npy` files at 7.3GB, 2.0GB, and 4.3GB with `Errno 5`/partial-write errors. The encoder now validates `.npy` data size during resume, drops incomplete last shards, repairs `wiki_passages.jsonl` in place to the completed embedding prefix, and writes `.npy` data in row chunks. At 2026-05-26T22:39:06+08:00 the 1,000,000-passages-per-shard resume had successfully written `embeddings_shard_000049.npy` as a complete 3,072,000,128-byte NPY with mmap shape `(1000000, 768)`, `wiki_passages.jsonl` had advanced to 9,199,996 rows, 50 complete shards were present through `embeddings_shard_000049.npy`, and the encoder was still running under launcher PID `1789071` with encoder PID `1789077`. `wiki.faiss` and the streaming/FAISS manifests were still absent. This is recovery progress only, not completed evaluation evidence.
- Biased-NQ fallback status: `results/corm_template_biased_nq_remote_smoke.json` records that the remote template fallback generated 100 NQ validation rows, 500 deterministic perturbation slots, and a structurally valid `biased_nq_test.template_smoke.jsonl`. This is API-free plumbing evidence only; it is not the original OpenAI-generated Biased-NQ artifact.
- Evaluation staging status: `results/corm_eval_stage_dir_patch_status.json` records that remote `run_eval.sh` and `04_run_reconstructed_eval.sh` pass shell syntax checks after deploying an `EVAL_STAGE_DIR`/`SKIP_FAISS_COPY` patch. This avoids trying to stage a full `wiki.faiss` under the almost-full root `/tmp`.
- Template eval-smoke readiness: `results/corm_template_smoke_eval_readiness_status.json` records that `run_eval.sh` now forwards `EVAL_MAX_EXAMPLES`, `run_evaluation.py` accepts `--max_examples`, and a separate `04_run_template_biased_nq_smoke_eval.sh` script is deployed and syntax-checked for bounded Biased_NQ smoke evaluation after `wiki.faiss` exists. The deployed scripts now put the transient runtime Python on `PATH` and default the template smoke generator to `Qwen/Qwen2.5-0.5B-Instruct` because the current remote Transformers/vLLM stack does not recognize Qwen3. This is readiness evidence only for the full-index watcher path.
- Template eval-smoke watcher: `results/corm_template_smoke_eval_watcher_status.json` records that the previous watcher PID `342843` was stopped and the redeployable remote script pack was removed after the second storage failure to free NTFS file records. It should be redeployed only after `wiki.faiss` exists or after the storage situation is stable. This is operational status only and has produced no full-index watcher metrics.
- Partial template eval smoke: `results/corm_partial_template_eval_smoke_status.json` records an isolated partial-index smoke run using the first four embedding shards. It built a 200,000-vector flat FAISS index, evaluated two template Biased_NQ examples with `rerank_depth=5` and `Qwen/Qwen2.5-0.5B-Instruct`, and wrote `evaluation_results.json`. This validates deployment plumbing and generator compatibility only; the two-example accuracy is 0.0 and must not be used as performance evidence.

Public release check:

- `experiments/check_corm_release_manifest.py`
- `results/corm_release_manifest.json`
- Hugging Face query succeeded for `PeiyangLiu/CoRM-RAG` and found `.gitattributes`, `README.md`, and `critic-v12-mixed/checkpoint-latest/state.pt`.
- The queried HF release did not contain `wiki.faiss`, `wiki_passages.jsonl`, or `biased_nq_test.jsonl`.
- GitHub API querying was rate-limited in the latest run, so the stronger conclusion is limited to the HF release plus local preflight.

Machine-readable preflight:

- `experiments/check_corm_reproduction_readiness.py`
- `results/corm_reproduction_preflight.json`

Current preflight status: `ready=false`, with 5 missing required artifacts. Therefore the full CoRM-RAG retrieval-generation evaluation has not been reproduced.

## 2026-05-27 Non-Human Evidence Closure Update

Artifacts added or refreshed:

- `experiments/summarize_evidence_closure.py`
- `results/evidence_closure_status.json`
- `EVIDENCE_CLOSURE_REPORT.md`
- `results/corm_full_wikipedia_job_status.json`
- `results/corm_full_reproduction_execution_attempt_20260527.json`
- `results/claims_verification.json`

Updated statistical checks:

- Hotpot paired bootstrap comparison was rerun with 5000 bootstrap samples. The CSRM-vs-naive 95% lower bounds remain positive: AUROC improvement lower bound `0.1379`, Risk@30 reduction lower bound `0.2500`.
- FEVER v3 paired bootstrap comparison was rerun with 5000 bootstrap samples. The CSRM-vs-naive 95% lower bounds remain positive: AUROC improvement lower bound `0.1996`, Risk@30 reduction lower bound `0.1056`.
- Hotpot and all three FEVER v3 orbit consistency audits were rerun and passed with `error_count=0`.
- Claim verification now reports `28/28` checked claims passing.

Remote reconstruction update:

- The full Wikipedia reconstruction is no longer running.
- The 250k-shard recovery successfully produced a complete `embeddings_shard_000051.npy` with shape `(250000, 768)`, giving 52 mmap-valid embedding shard files.
- The run then failed while writing/flushing `wiki_passages.jsonl` with `OSError: [Errno 5] Input/output error`.
- The remote machine has no sufficiently large reliable user-writable ext4/XFS target: root ext4 has only about 19-20GB free, `/dev/shm` has about 13GB free, and the only large persistent target is `/mnt/ntfs-disk` on NTFS/fuseblk, which has repeatedly produced `Errno 5` and `Errno 28`.
- `wiki.faiss` still does not exist, and `results/corm_reproduction_preflight.json` remains `ready=false`.

Full reproduction execution attempt:

- A direct local full reproduction is blocked: local `D:` has about 51GB free, local GPU is a 10GB RTX 3080, and the required CoRM data/index artifacts plus local `faiss`/`vllm` modules are absent.
- A direct remote full reproduction is blocked: both RTX 4090 GPUs are idle, but `/mnt/ntfs-disk` now rejects even one-line write probes inside the reconstruction directories with "No space left on device"; `/home/syk`, `/tmp`, and `/dev/shm` are writable but have only about 20GB ext4 plus 13GB tmpfs available.
- A mitigation path was implemented for future execution on reliable storage: the streaming encoder can write passage shards, the FAISS builder can write sharded FAISS indexes, and `run_evaluation.py` can read a sharded FAISS manifest and passage-shard directory.
- The sharded remote smoke could not start because creating `/mnt/ntfs-disk/csrm_corm_reconstruction_sharded_smoke` failed with the same storage error.

Current non-human evidence boundary:

- Closed as bridge evidence: Hotpot released-critic bridge, FEVER v3 near-miss secondary bridge, shuffled-orbit alignment ablation, answer-consistency mechanism, paired bootstrap, structural audits, NLI cross-scorer probe, case studies, CoRM release/path blockers, and remote reconstruction engineering status.
- Not closed as performance evidence: full original CoRM-RAG retrieval-generation reproduction.
- Not closed as theory/evaluation evidence: general formal risk-control guarantee; Hotpot-only empirical CP transfer is supported, but FEVER v3 still misses the target.
- Explicitly excluded by the user in this step: human audit v3.

## NeurIPS Gate Status

Not complete.

Satisfied or partially satisfied:

- Two real-data bridge domains: HotpotQA distractor and FEVER gold evidence.
- Strong baselines in the bridge: released CoRM critic score, SURE-style single-set sufficiency, naive orbit averaging.
- Bootstrap confidence intervals for the main bridge metrics.
- Three Hotpot data seeds with released CoRM critic scoring.
- Ablations for answer consistency, overlap, stability, conflict monotonicity, and first perturbation only.
- Same-call-budget shuffled-perturbation ablation.
- Claim ledger with 28/28 checked claims matching result files, including the explicit CoRM-RAG reproduction blocker, calibration-guarantee blockers, Clopper-Pearson risk-control pressure test, structural plus dataset-constraint audit claim, NLI cross-scorer probe claim, HF release-data blocker, released-source reconstruction-path blocker, supplemental reconstruction-tool artifact, remote reconstruction-plan artifact, materialized remote script-pack artifact, remote runtime-readiness artifact, remote checkpoint-staging artifact, staged-input streaming encoder smoke artifact, real HF/Contriever streaming encoder smoke artifact, template Biased-NQ smoke artifact, remote eval-staging patch artifact, bounded template eval-smoke readiness artifact, post-FAISS template-smoke watcher artifact, isolated partial-index template eval-smoke artifact, and the latest full-Wikipedia reconstruction storage blocker.
- Case-study artifacts for wins, false accepts, and failures.
- Two bridge domains now differentiate CSRM from naive orbit averaging: HotpotQA structurally labeled orbits and FEVER v3 near-miss dilution orbits.
- Paired bootstrap deltas for CSRM versus main baselines.
- Automated NLI set-level probe showing directional feature-source robustness.

Not yet satisfied:

- Full CoRM-RAG reproduction on its intended datasets.
- Exact released-source reconstruction path for the missing CoRM data/index artifacts. Supplemental reconstruction helpers exist, but original-artifact equivalence is not established.
- Executed full reconstructed CoRM run. A plan, regenerated script pack, import-ready remote runtime, staged checkpoint, staged-input streaming smoke, small real HF/Contriever/FAISS smoke, eval-staging patch, bounded template eval-smoke path, isolated partial-index eval smoke, and repeated full Wikipedia/FAISS construction attempts exist, but no full remote reconstructed evaluation metrics have been produced. The latest attempt is blocked by NTFS/fuseblk I/O failure after shard `000051`.
- Human-audited stress split. Pilot and paper-grade audit samples exist, but neither is labeled.
- Validated verifier labels beyond Hotpot supporting-fact heuristics and the current automated NLI sensitivity probe.
- Calibration strong enough for formal risk control. The conservative Clopper-Pearson pressure test helps Hotpot but still fails FEVER v3.
- Multi-seed main experiment across at least two domains. HotpotQA and FEVER v3 near-miss both have three data seeds, but FEVER remains heuristic and unaudited.
- Strict auto-review loop. Round 1 self-review exists, but it is not a full external multi-round positive review.
- Paper-level failure-case analysis and limitations.
- Case-study artifacts and audited-label evaluation code exist, but final paper-level analysis still needs completed human labels.
- Independent cross-model experiment audit. Local deterministic audit exists, but the MCP-based independent audit was unavailable.

## Next Required Work

1. Fill `results/audit_sample_100_v3.jsonl` with pilot human labels and compute agreement/error rates.
2. Fill `results/audit_sample_paper_1000_v3.jsonl` after the pilot audit protocol is validated.
3. Treat the current NLI set-level result as sensitivity analysis; add a verifier protocol that is actually validated for multi-hop answerability before using verifier-derived labels as primary evidence.
4. Improve calibration if the final paper needs formal risk-control language; current conservative thresholding supports only Hotpot empirical transfer and still fails FEVER v3.
5. Move the full CoRM reconstruction to reliable persistent ext4/XFS storage or obtain author-provided artifacts; continuing on `/mnt/ntfs-disk` is no longer evidence-efficient. Then run `results/corm_reproduction_preflight.json` until `ready=true`; reconstruction still requires generated Wikipedia passages, FAISS index construction, perturbation generation or staging, and Biased-NQ materialization.
6. Run a strict independent review loop after audited metrics are available.
