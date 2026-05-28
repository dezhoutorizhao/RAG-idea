# EXPERIMENT_PLAN: CSRM-RAG

Date: 2026-05-20

## 1. Main Claim

Reliable RAG needs counterfactual sufficiency stability:

```text
semantic relevance -> document robustness -> single-set sufficiency -> counterfactual set stability
```

CSRM-RAG should improve selective risk under biased and false-premise query perturbations without retraining the generator.

## 2. Hypotheses

H1, bottleneck:

```text
CoRM-RAG can assign high document-level robustness to evidence sets that are insufficient or unstable across cognitive perturbations.
```

H2, mechanism:

```text
A perturbation-orbit score using support stability, missingness stability, conflict monotonicity, answer/support-signature consistency, and evidence overlap detects fragile evidence sets better than max/mean document scores or single-set sufficiency.
```

H3, controlled gain:

```text
At fixed coverage and verifier-call budget, CSRM-RAG lowers selective risk compared with CoRM-RAG thresholding, SURE-style sufficiency thresholding, and naive perturbation averaging.
```

## 3. Data Stages

### Stage 0: Synthetic smoke test

Purpose:

- Validate schemas, metrics, calibration, and failure-mode logic.
- Not used as final evidence.

Splits:

- stable_support
- fragile_support
- missing_hop
- conflicting_evidence
- distractor

Expected result:

- CSRM should accept stable_support and reject fragile_support, missing_hop, conflicting_evidence, and distractor more reliably than max CoRM score and single-set sufficiency.

### Stage 1: CoRM-RAG output extraction

Use `external_repos/CoRM-RAG`:

- run released checkpoint evaluation or adapt cached retrieval outputs if available.
- extract query, perturbation, top-k docs, CoRM scores, generated answer, answer correctness.

Minimum target:

- 500 to 2,000 examples across NQ-clean, biased NQ, and TruthfulQA style settings.

Current blocker:

- The workspace has the released critic checkpoint, but does not have `wiki.faiss`, `wiki_passages.jsonl`, or `biased_nq_test.jsonl`.
- `experiments/check_corm_reproduction_readiness.py` now provides a machine-readable reproduction preflight gate.
- `results/corm_reproduction_preflight.json` currently reports `ready=false` because the required data/index files are missing and the current Python environment lacks `faiss` and `vllm`.
- Until those are available, full CoRM-RAG evaluation cannot be claimed.

### Stage 1a: HotpotQA real-data bridge

Purpose:

- Exercise the CSRM orbit schema and evaluation stack on real multi-hop QA contexts before the full CoRM-RAG data path is available.
- Use HotpotQA supporting facts to create heuristic stable, missing-hop, false-premise, and distractor orbit labels.

Artifacts:

- `experiments/build_hotpot_orbits.py`
- `results/hotpot_orbits_200.jsonl`
- `results/hotpot_orbits_200_eval.json`

Status:

- 200 HotpotQA validation examples produced 800 orbits.
- `experiments/score_orbits_corm.py` now loads the released CoRM-RAG Evidence Critic and rewrites `corm_score` for every Hotpot orbit document.
- With released CoRM critic scores on all 800 Hotpot orbits, CSRM improves AUROC from 0.5000 for CoRM max/mean clean and 0.8359 for naive orbit averaging to 0.9957.
- Risk@30% coverage improves from 0.7500 for CoRM max/mean clean and SURE-style single-set sufficiency, and 0.5000 for naive orbit averaging, to 0.1667 for CSRM.
- This is still a bridge result only; final evidence requires validated verifier labels and human audit.
- After adding a risk-sensitive `worst_sufficiency` component, the current released-critic Hotpot result is AUROC 0.9974 and Risk@30% coverage 0.1667.
- Multi-seed Hotpot validation with three random data seeds gives CSRM AUROC 0.9976 +/- 0.0023 and Risk@30% coverage 0.1669 +/- 0.0004.
- Shuffled-perturbation ablation collapses to AUROC 0.0001 +/- 0.0002 and Risk@30% coverage 1.0000, showing that the gain depends on correct counterfactual orbit alignment rather than merely using extra verifier calls.
- Multi-seed split calibration at risk target 0.20 gives logistic CSRM calibrated-risk mean 0.2032 and max 0.2593, with 2/3 split seeds meeting the target. A newer Clopper-Pearson threshold pressure test improves Hotpot to nonzero coverage and 3/3 empirical target transfer, but it is still not a formal risk guarantee.

Artifacts:

- `results/hotpot_orbits_corm_800.jsonl`
- `results/hotpot_orbits_corm_800_eval_fullabl.json`
- `results/hotpot_corm_calibrated_800_worst.json`
- `results/hotpot_corm_calibration_multiseed.json`
- `results/hotpot_corm_risk_control_cp_multiseed.json`
- `results/hotpot_corm_multiseed_summary_fullabl.json`

### Stage 1b: FEVER real-data bridge

Purpose:

- Add a second real domain with support/refute evidence labels.
- Test whether CSRM behavior transfers from multi-hop QA to fact verification.

Artifacts:

- `experiments/build_fever_orbits.py`
- `results/fever_orbits_nearmiss_1200_v3.jsonl`
- `results/fever_orbits_nearmiss_corm_1200_v3.jsonl`
- `results/fever_orbits_nearmiss_corm_1200_v3_eval.json`
- `results/fever_nearmiss_corm_v3_multiseed_summary.json`
- `results/fever_nearmiss_corm_v3_calibration_multiseed.json`
- `results/fever_nearmiss_corm_v3_risk_control_cp_multiseed.json`
- `results/hotpot_corm_paired_comparison.json`
- `results/fever_nearmiss_corm_v3_paired_comparison.json`
- `results/fever_nearmiss_corm_v3_orbit_consistency_audit.json`
- `results/fever_nearmiss_corm_v3_seed31_orbit_consistency_audit.json`
- `results/fever_nearmiss_corm_v3_seed47_orbit_consistency_audit.json`

Status:

- 200 FEVER validation claims produced 1,200 FEVER v3 orbits across stable, missing, conflicting, distractor, fragile-mixed, and near-miss dilution splits.
- Released CoRM critic scoring was applied to every evidence document.
- The current FEVER v3 builder supersedes earlier versions whose audits found invalid missing-evidence cases, support keys that exceeded the evidence-set budget, and non-gold high-support feature leakage; the main, seed31, and seed47 FEVER v3 orbit audits now report `passed=true` and `error_count=0` under structural plus dataset-constraint checks.
- CoRM clean scoring and SURE-style single-set sufficiency fail under the stress split.
- In the near-miss split, CSRM separates fragile orbits better than naive orbit averaging across three FEVER data seeds: CSRM AUROC 1.0000 versus naive AUROC 0.8000, and CSRM Risk@30% 0.4444 versus naive Risk@30% 0.5556.
- Paired bootstrap on the main FEVER v3 near-miss seed gives positive CSRM-vs-naive confidence intervals for AUROC improvement, Risk@30 reduction, and AURC reduction. The same paired comparison also supports the Hotpot CSRM-vs-naive bridge claim.
- Multi-seed split calibration at risk target 0.20 gives logistic CSRM calibrated-risk mean 0.2449 and max 0.3333, with 1/3 split seeds meeting the target. Clopper-Pearson thresholding still meets the target in only 1/3 FEVER v3 split seeds, so this remains a calibration blocker.
- This remains heuristic bridge evidence because near-miss verifier features are deliberately constructed and require audit.

### Stage 1c: CoRM original reproduction gate

Artifacts:

- `experiments/check_corm_reproduction_readiness.py`
- `results/corm_reproduction_preflight.json`
- `experiments/check_corm_release_manifest.py`
- `results/corm_release_manifest.json`
- `experiments/audit_corm_reproduction_path.py`
- `results/corm_reproduction_path_audit.json`
- `experiments/build_corm_faiss_index.py`
- `experiments/build_corm_biased_nq_test.py`
- `experiments/plan_corm_reconstruction.py`
- `results/corm_reconstruction_plan.json`
- `experiments/materialize_corm_remote_scripts.py`
- `results/corm_remote_scripts_manifest.json`
- `results/corm_remote_scripts/`

Current status:

- The released checkpoint is available.
- Full original evaluation remains blocked by missing full `wiki.faiss`, `wiki_passages.jsonl`, `biased_nq_test.jsonl`, and perturbation generation/staging. Remote `faiss` and `vllm` now import in the transient runtime.
- The available released source partially scripts `wiki_passages.jsonl`, but no exact released-script producer is detected for `wiki.faiss` or `biased_nq_test.jsonl`.
- Direct CoRM-RAG reproduction claims require either original artifacts from the authors or an explicitly documented reconstruction path for the FAISS index and Biased-NQ file.
- Supplemental reconstruction scripts now exist for streaming/sharded Wikipedia encoding, building `wiki.faiss` from `wiki_embeddings.npy` / `embeddings_shard_*.npy`, and materializing `biased_nq_test.jsonl` from perturbation JSONL. Any run using these scripts must be described as reconstructed-pipeline evidence unless original-artifact equivalence is verified.
- A remote execution plan now targets `/mnt/ntfs-disk/csrm_corm_reconstruction` on `192.168.103.101`, keeps secrets out of scripts, uses `/dev/shm` for transient runtime plus HuggingFace cache, defaults to `HF_ENDPOINT=https://hf-mirror.com` unless overridden, and runs `run_eval.sh` from the CoRM `src` directory.
- The remote execution plan is materialized into an ordered shell script pack under `results/corm_remote_scripts/`; the manifest reports no embedded secret markers.
- `results/corm_remote_runtime_status.json` records that the remote transient `/dev/shm` runtime can import torch/CUDA, FAISS, Transformers, datasets, and vLLM.
- `results/corm_remote_checkpoint_status.json` records that the remote checkpoint upload is SHA256-verified.
- `results/corm_streaming_encoder_remote_smoke.json` records that staged JSONL input can be converted into sharded embeddings and a FAISS index on the remote server. `results/corm_streaming_encoder_remote_hf_smoke.json` records that the remote mirror endpoint plus `/dev/shm` cache can stream real Wikipedia, encode 16 passages with `facebook/contriever-msmarco` on CUDA, and build a 768-dimensional FAISS index. Full reconstructed evaluation is still not executed because the full Wikipedia/FAISS/Biased-NQ artifacts are missing.

Verifier note:

- Generic doc-level and early set-level NLI smoke tests were not reliable as primary Hotpot multi-hop sufficiency labels.
- A later set-level NLI probe over the v3 audit samples is useful as cross-scorer sensitivity evidence, but it is still not validated enough to become the primary verifier or a substitute for human audit.

### Stage 2: Controlled sufficiency stress split

Datasets:

- HotpotQA for multi-hop missing evidence.
- FEVER for support/refute/NEI.
- Natural Questions or TruthfulQA for biased query perturbations.

Labels:

- answerable
- insufficient
- conflicting
- missing
- fragile_under_perturbation

Human audit:

- At least 100 examples per split.
- Report agreement and reject ambiguous examples.

Current audit preparation:

- `experiments/sample_audit_orbits.py` creates a stratified audit JSONL from Hotpot and FEVER orbit files.
- `experiments/export_audit_pack.py` exports editable label CSV files and read-only HTML evidence views; `--blind` hides expected labels, source answerability labels, and model scores for independent annotation.
- `experiments/merge_audit_annotations.py` merges edited full or partial CSV labels back into the audit JSONL files.
- `results/audit_sample_100_v3.jsonl` contains 100 balanced audit candidates with blank auditor fields across the current HotpotQA and FEVER v3 stress splits.
- `results/audit_sample_paper_1000_v3.jsonl` contains 1,000 paper-grade audit candidates across the current HotpotQA and FEVER v3 stress splits.
- `results/audit_pack_100_v3.labels.csv` and `results/audit_pack_100_v3.review.html` provide the pilot diagnostic labeling interface.
- `results/audit_pack_paper_1000_v3.labels.csv` and `results/audit_pack_paper_1000_v3.review.html` provide the paper-grade diagnostic labeling interface.
- `results/audit_pack_100_v3_a1.blind.*` and `results/audit_pack_100_v3_a2.blind.*` provide shuffled blind pilot packs for two independent annotators.
- `results/audit_pack_paper_1000_v3_a1.blind.*` and `results/audit_pack_paper_1000_v3_a2.blind.*` provide shuffled blind paper-grade packs for two independent annotators.
- `results/audit_pack_100_v3.manifest.json` and `results/audit_pack_paper_1000_v3.manifest.json` record the generated pack paths and editable columns.
- `experiments/summarize_audit.py` reports audit completion, agreement with expected labels, disagreements, and per-split status.
- `experiments/summarize_adjudication.py` reports double-label completion, raw agreement, Cohen's kappa, unresolved disagreements, and adjudication coverage.
- `experiments/evaluate_audited_orbits.py` recomputes the same selective-risk metrics using the configured label field as the only label source once human labels are available.
- `experiments/check_audit_readiness.py` enforces the audit readiness gates before audited metrics can be used for paper claims.
- `results/audit_sample_100_v3_summary.json` currently reports 0/100 labeled items.
- `results/audit_sample_100_v3_adjudication.json` currently reports 0 double-labeled and 0 adjudicated items.
- `results/audit_sample_100_v3_readiness.json` currently reports `ready=false`.
- `results/audit_sample_100_v3_adjudicated_readiness.json` currently reports `ready=false` for final adjudicated labels.
- `results/audit_sample_paper_1000_v3_summary.json` currently reports 0/1,000 labeled items.
- `results/audit_sample_paper_1000_v3_adjudication.json` currently reports 0 double-labeled and 0 adjudicated items.
- `results/audit_sample_paper_1000_v3_readiness.json` currently reports `ready=false`.
- `results/audit_sample_paper_1000_v3_adjudicated_readiness.json` currently reports `ready=false` for final adjudicated labels.
- `CLAIMS_LEDGER.json` and `experiments/verify_claims.py` verify that current reported bridge claims match result files.
- `EXPERIMENT_AUDIT.md` records a WARN verdict: local claim verification passes, but independent cross-model audit, human audit, validated verifier labels, and full CoRM-RAG reproduction are still missing.
- `RESULT_TO_CLAIM.md` records a partial verdict: Hotpot and FEVER v3 near-miss bridge claims are supported, but general robust-RAG, calibrated-guarantee, and human-audited claims are not.
- `experiments/extract_case_studies.py` generates Hotpot and FEVER case studies for wins, false accepts, and failures.
- This is not yet a completed human audit; the 100-item pilot and 1,000-item paper-grade candidate files are prepared but unlabeled.

## 4. Methods

Baselines:

- BM25 or Contriever retrieval.
- CoRM-RAG.
- CoRM-RAG max document score threshold.
- CoRM-RAG mean document score threshold.
- SURE-style single-set sufficiency aggregation.
- Naive perturbation ensemble of single-set sufficiency.
- LLM-as-judge verifier if budget allows.

Ours:

- CSRM lexical or verifier-feature prototype.
- CSRM with DeBERTa-base or DeBERTa-v3-base verifier.
- CSRM with conformal threshold selected on calibration split.

## 5. Metrics

Average task metrics:

- EM/F1 for QA.
- Citation precision if citations exist.

Reliability metrics:

- AUROC for answerability, missingness, conflict, and fragility.
- ECE and MCE.
- Selective risk at coverage 30, 50, 70.
- Area under risk-coverage curve.
- Counterfactual instability rate.
- Answer/support-signature inconsistency under perturbation.

Bottleneck-specific metrics:

- Fragile-orbit rejection rate.
- Stable-support preservation rate.
- Conflict monotonicity violation rate.
- Perturbation answer-flip rate.

## 6. Ablations

Required:

- no CoRM document scores.
- no support stability.
- no evidence overlap stability.
- no answer/support-signature consistency.
- no conflict monotonicity.
- clean query only.
- one perturbation only.
- naive average over perturbations.
- same number of verifier calls but shuffled perturbations.

## 7. NeurIPS Completion Gate

The project is not complete until all are true:

- At least two real datasets or domains.
- At least three strong baselines, including CoRM-RAG and SURE-style sufficiency.
- At least one human-audited stress split.
- Multi-seed or bootstrap confidence intervals for main metrics.
- Controlled compute and verifier-call budget.
- Failure cases and limitations.
- Evidence that gains are not explained by stricter thresholding or more verifier calls.
