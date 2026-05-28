# Experiment Audit Report

Date: 2026-05-20

Auditor: local deterministic claim-ledger verifier. Cross-model MCP audit was requested by the skill design, but no codex MCP tool is available in this environment, so this report must not be described as independent cross-model review.

Project: CSRM-RAG

## Overall Verdict: WARN

Integrity status: warn.

The current result files support several bridge-study claims and one automated cross-scorer sensitivity probe, but they do not support a final NeurIPS submission claim. The main unresolved issues are missing human audit, missing validated verifier labels, and missing full CoRM-RAG retrieval-generation reproduction.

## Automated Claim Verification

Machine-readable ledger:

- `CLAIMS_LEDGER.json`

Verification output:

- `results/claims_verification.json`

Status:

- Total claims checked: 19
- Passed checks: 19
- Failed checks: 0

## Checks

### A. Ground Truth Provenance: WARN

HotpotQA labels are derived from dataset supporting facts and constructed perturbation records. FEVER labels are derived from `copenlu/fever_gold_evidence`.

This is real dataset structure, not model-output ground truth. However, the stress-orbit answerability labels are still constructed heuristics, not completed human audit.

### B. Score Normalization: PASS

The claim ledger checks raw metrics in JSON result files. The reported comparisons use AUROC, AURC, risk at fixed coverage, calibration metrics, and accuracy fields directly from evaluation outputs.

No claim in `CLAIMS_LEDGER.json` depends on normalizing a model score by its own maximum or minimum.

### C. Result File Existence and Number Matching: PASS

All claim-referenced result files exist and all checked numbers match the ledger:

- `results/hotpot_orbits_corm_800_eval_fullabl.json`
- `results/hotpot_corm_multiseed_summary_fullabl.json`
- `results/fever_orbits_nearmiss_corm_1200_v3_eval.json`
- `results/fever_nearmiss_corm_v3_multiseed_summary.json`
- `experiments/summarize_calibration_seeds.py`
- `results/hotpot_corm_calibration_multiseed.json`
- `results/fever_nearmiss_corm_v3_calibration_multiseed.json`
- `experiments/evaluate_risk_control_cp.py`
- `results/hotpot_corm_risk_control_cp_multiseed.json`
- `results/fever_nearmiss_corm_v3_risk_control_cp_multiseed.json`
- `experiments/check_corm_reproduction_readiness.py`
- `results/corm_reproduction_preflight.json`
- `experiments/audit_corm_reproduction_path.py`
- `results/corm_reproduction_path_audit.json`
- `experiments/build_corm_faiss_index.py`
- `experiments/build_corm_biased_nq_test.py`
- `experiments/plan_corm_reconstruction.py`
- `results/corm_reconstruction_plan.json`
- `experiments/materialize_corm_remote_scripts.py`
- `results/corm_remote_scripts_manifest.json`
- `results/corm_remote_scripts/`
- `results/corm_remote_runtime_status.json`
- `experiments/export_audit_pack.py`
- `experiments/merge_audit_annotations.py`
- `experiments/summarize_adjudication.py`
- `experiments/evaluate_audited_orbits.py`
- `experiments/check_audit_readiness.py`
- `results/audit_pack_100_v3.labels.csv`
- `results/audit_pack_100_v3.review.html`
- `results/audit_pack_100_v3.manifest.json`
- `results/audit_pack_100_v3_a1.blind.labels.csv`
- `results/audit_pack_100_v3_a1.blind.review.html`
- `results/audit_pack_100_v3_a1.blind.manifest.json`
- `results/audit_pack_100_v3_a2.blind.labels.csv`
- `results/audit_pack_100_v3_a2.blind.review.html`
- `results/audit_pack_100_v3_a2.blind.manifest.json`
- `results/audit_pack_paper_1000_v3.labels.csv`
- `results/audit_pack_paper_1000_v3.review.html`
- `results/audit_pack_paper_1000_v3.manifest.json`
- `results/audit_pack_paper_1000_v3_a1.blind.labels.csv`
- `results/audit_pack_paper_1000_v3_a1.blind.review.html`
- `results/audit_pack_paper_1000_v3_a1.blind.manifest.json`
- `results/audit_pack_paper_1000_v3_a2.blind.labels.csv`
- `results/audit_pack_paper_1000_v3_a2.blind.review.html`
- `results/audit_pack_paper_1000_v3_a2.blind.manifest.json`
- `results/audit_sample_100_v3_summary.json`
- `results/audit_sample_100_v3_adjudication.json`
- `results/audit_sample_100_v3_readiness.json`
- `results/audit_sample_100_v3_adjudicated_readiness.json`
- `results/audit_sample_paper_1000_v3_summary.json`
- `results/audit_sample_paper_1000_v3_adjudication.json`
- `results/audit_sample_paper_1000_v3_readiness.json`
- `results/audit_sample_paper_1000_v3_adjudicated_readiness.json`
- `results/audit_sample_100_v3_nli_set_eval.json`
- `results/audit_sample_paper_1000_v3_nli_set_eval.json`
- `NLI_PROBE_REPORT.md`
- `experiments/check_corm_release_manifest.py`
- `results/corm_release_manifest.json`

### D. Dead Code Detection: WARN

The core evaluation path is covered by tests and result files. However, this local audit does not perform full static call-graph analysis. Treat dead-code detection as not fully audited.

### E. Scope Assessment: WARN

Evidence scope:

- HotpotQA bridge: strong, three random data seeds, released CoRM critic scores.
- FEVER bridge: second-domain v3 near-miss stress check that differentiates CSRM from naive orbit averaging and passes structural plus dataset-constraint audits including support-feature provenance, but still heuristic and not human-audited.
- NLI set-level probe: automated sensitivity evidence showing the CSRM ranking pattern persists when support/conflict/missing features are replaced by set-level `cross-encoder/nli-deberta-v3-small` scores on the v3 paper-grade audit sample.
- Conservative risk-control pressure test: Clopper-Pearson thresholding gives Hotpot-only empirical target transfer for logistic CSRM, but FEVER v3 near-miss still misses the 0.20 target in two of three split seeds; this remains pressure-test evidence, not a formal guarantee.
- Human audit: pilot and paper-grade candidate files plus non-blind diagnostic packs and shuffled blind annotator packs are prepared; partial CSV merge, inter-annotator agreement, adjudicated-label metric recomputation, and readiness gates are scripted, but labels are not filled.
- Full CoRM-RAG reproduction: blocked by preflight failure in `results/corm_reproduction_preflight.json`; the released checkpoint is local and now uploaded to the remote workspace with SHA256 verification, and remote CUDA/runtime imports are available. Required data/index files are still missing.
- Reproduction-path audit: `results/corm_reproduction_path_audit.json` shows the available repository partially scripts `wiki_passages.jsonl`, but does not expose an exact producer for `wiki.faiss` or `biased_nq_test.jsonl`.
- Supplemental reconstruction tools: this workspace now has a FAISS builder from `wiki_embeddings.npy` / shard files and a Biased-NQ materializer from perturbation JSONL. These help future reconstruction attempts but are not upstream released artifacts.
- Reconstruction execution plan: `results/corm_reconstruction_plan.json` gives a remote `/mnt/ntfs-disk` plan for environment setup, streaming Wikipedia encoding, FAISS construction, perturbation materialization, and reconstructed evaluation. Runtime setup and checkpoint staging have been executed; full data generation and evaluation have not.
- Remote script pack and runtime: `results/corm_remote_scripts/` materializes the plan into ordered shell scripts and `results/corm_remote_scripts_manifest.json` reports no embedded secret markers. The pack now includes a bounded template Biased-NQ eval-smoke script and a post-FAISS watcher for plumbing checks. The deployed eval scripts now put the transient runtime Python on `PATH` and default to runtime-compatible Qwen2.5 generators for reconstructed runs. A remote `/dev/shm` runtime was bootstrapped and now imports torch/CUDA, FAISS, Transformers, datasets, and vLLM; this is runtime readiness only, not full reconstructed evaluation evidence.
- Remote checkpoint and streaming smoke: `results/corm_remote_checkpoint_status.json` records remote SHA256 verification for the 5.2GB checkpoint. `results/corm_streaming_encoder_remote_smoke.json` records a staged-JSONL/dummy-backend smoke where the streaming encoder wrote sharded embeddings and FAISS indexed them. `results/corm_streaming_encoder_remote_hf_smoke.json` records a real 16-passage HF/Contriever/CUDA smoke through `HF_ENDPOINT=https://hf-mirror.com` with `/dev/shm` cache. Full Wikipedia generation has now been launched but is not complete.
- Full Wikipedia job: `results/corm_full_wikipedia_job_status.json` records that the first full remote Wikipedia/Contriever/FAISS construction attempt failed on the NTFS/fuseblk mount with `Errno 28` while opening `embeddings_shard_000044.npy`. The encoder has been patched with `--resume` support to repair the one-shard passage/embedding mismatch and continue with larger 1,000,000-passage shards; the first resumed 2.9GB shard has now been written successfully, but the final `wiki.faiss` and streaming/FAISS manifests are still absent. This is recovery progress toward reconstruction, not completed evaluation evidence.
- Biased-NQ template fallback: `results/corm_template_biased_nq_remote_smoke.json` records that the remote server can generate deterministic template perturbations and a structurally valid Biased-NQ-format smoke file without API credentials. This is only a plumbing fallback, not original Biased-NQ evidence.
- Evaluation staging patch: `results/corm_eval_stage_dir_patch_status.json` records that the remote reconstructed-eval scripts now avoid the almost-full root `/tmp` by using a configurable large stage directory and optional FAISS symlink mode. This is deployment-readiness evidence, not evaluation evidence.
- Template eval-smoke readiness: `results/corm_template_smoke_eval_readiness_status.json` records that a bounded template Biased_NQ eval-smoke script has been deployed and syntax-checked, that `EVAL_MAX_EXAMPLES` is wired through `run_eval.sh` to `run_evaluation.py`, and that the remote script now uses the transient runtime `PATH` plus a Qwen2.5 smoke generator. This is readiness evidence only for the full-index watcher path.
- Template eval-smoke watcher: `results/corm_template_smoke_eval_watcher_status.json` records that a remote watcher is running and waiting for `wiki.faiss` before launching the bounded template Biased_NQ smoke evaluation. This is operational readiness only, not full-index evaluation evidence.
- Partial template eval smoke: `results/corm_partial_template_eval_smoke_status.json` records an isolated 200,000-vector partial-index run that completed retrieval, released CoRM critic scoring, vLLM generation, and metric writing for two template Biased_NQ examples. This is deployment plumbing evidence only, not a performance result.
- Public release manifest: `results/corm_release_manifest.json` confirms the Hugging Face release contains the critic checkpoint but not `wiki.faiss`, `wiki_passages.jsonl`, or `biased_nq_test.jsonl`.

Claims must avoid words such as "comprehensive", "guaranteed", or "submission-ready".

### F. Evaluation Type Classification

- HotpotQA bridge: real dataset structure with heuristic orbit labels.
- FEVER bridge: real dataset structure with heuristic orbit labels.
- Synthetic toy: synthetic proxy only.
- Human audit: unavailable; pilot sample is 0/100 labeled and paper-grade candidate sample is 0/1,000 labeled. Double-label and adjudication completion rates are 0%; readiness reports are all `ready=false`.

## Claim Impact

- C1 Hotpot main gain: supported as bridge evidence only.
- C2 Hotpot multiseed stability: supported as bridge evidence only.
- C3 orbit alignment required: supported by shuffled-perturbation ablation.
- C4 answer consistency mechanism: supported on Hotpot bridge splits.
- C5 FEVER second domain: supported as a secondary heuristic bridge after the FEVER v3 builder fixes and near-miss dilution split; still not human-audited evidence.
- C6 human audit: explicitly unsupported until labels are completed.
- C7 case studies: supported as analysis artifacts only; not a replacement for human audit.
- C8 paired bootstrap deltas: supported on bridge labels; not a replacement for audit or full reproduction.
- C9 CoRM-RAG original reproduction: explicitly unsupported until the preflight gate passes and end-to-end evaluation metrics are produced.
- C10 calibrated risk guarantee: explicitly unsupported; split-calibrated logistic CSRM misses the 0.20 risk target in one of three Hotpot split seeds and two of three FEVER v3 split seeds.
- C14 Clopper-Pearson risk-control pressure test: supported as Hotpot-only empirical target transfer; explicitly not a formal guarantee and still fails FEVER v3 in two of three split seeds.
- C15 CoRM reproduction path audit: supported as an additional blocker; exact source scripts for `wiki.faiss` and `biased_nq_test.jsonl` are not present in the current released repository.
- C16 CoRM supplemental reconstruction tools: supported as artifacts for future documented reconstruction attempts; not evidence that original CoRM reproduction is complete.
- C17 CoRM reconstruction plan: supported as a planned execution artifact for the remote server; not evidence that reconstructed evaluation has run.
- C18 CoRM remote script pack: supported as a materialized execution artifact; not evidence that reconstructed evaluation has run.
- C19 CoRM remote runtime: supported as import-readiness evidence for the remote environment; not evidence that reconstructed evaluation has run.
- C20 CoRM remote checkpoint: supported as remote staging evidence with SHA256 verification; not evidence that reconstructed evaluation has run.
- C21 CoRM streaming encoder smoke: supported as staged-input engineering smoke evidence; not full Wikipedia or evaluation evidence.
- C22 CoRM HF streaming encoder smoke: supported as small real Wikipedia/Contriever/CUDA/FAISS engineering smoke evidence; not full Wikipedia or evaluation evidence.
- C23 CoRM template Biased-NQ smoke: supported as API-free plumbing evidence; not original Biased-NQ evidence.
- C24 CoRM eval stage dir patch: supported as deployment-readiness evidence; not reconstructed evaluation evidence.
- C25 CoRM template eval-smoke readiness: supported as deployment-readiness evidence for the full-index watcher path; the runtime PATH and Qwen2.5 generator defaults are now patched.
- C26 CoRM template eval-smoke watcher: supported as operational readiness evidence; no full-index watcher metrics have been produced.
- C27 CoRM partial template eval-smoke: supported as isolated deployment-plumbing evidence only; two-example partial-index accuracy is not performance evidence.
- C11 structural consistency audits: supported as deterministic structural and dataset-constraint evidence for current Hotpot and FEVER v3 orbit files; not a substitute for human semantic audit.
- C12 NLI set-level probe: supported as automated cross-scorer sensitivity evidence; not a substitute for validated verifier labels or human audit.
- C13 HF release manifest: supported as a reproduction blocker for the queried Hugging Face release; not proof that the data cannot be obtained from authors or rebuilt.

## Required Actions

1. Complete pilot human labeling using the blind annotator packs for `results/audit_sample_100_v3.jsonl`.
2. Complete paper-grade human labeling using the blind annotator packs for `results/audit_sample_paper_1000_v3.jsonl` after the pilot protocol is stable.
3. Recompute audited metrics after filtering ambiguous or incorrect labels.
4. Add a validated verifier or demote verifier-derived claims to heuristic analysis.
5. Improve calibration and validate it on audited multi-domain labels before making any formal risk-control claim; the current Clopper-Pearson pressure test is Hotpot-only.
6. Make `results/corm_reproduction_preflight.json` pass, then reproduce full CoRM-RAG original evaluation; otherwise explicitly frame this as an independent stress-test study using the released critic.
7. Run independent external review once audited results are available.
