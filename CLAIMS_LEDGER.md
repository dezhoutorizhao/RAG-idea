# Claims Ledger

Generated: `2026-05-29T07:16:40.916853+00:00`

Claims: `28`; verified pass/fail: `28` / `0`.

Declared status counts: `{'supported_bridge': 5, 'supported_secondary_bridge': 1, 'unsupported_until_audited': 1, 'supported_artifact': 12, 'unsupported_until_preflight_passes': 1, 'unsupported_until_stronger_calibration': 1, 'supported_partial_pressure_test': 1, 'supported_blocker': 3, 'supported_operational_status': 1, 'supported_structural_audit': 1, 'supported_probe': 1}`.
Verification status counts: `{'pass': 28}`.

## Claim Index

| ID | Declared status | Verification | Evidence files | Checks |
|---|---|---|---|---:|
| `C1_hotpot_main_gain` | `supported_bridge` | `pass` | `results/hotpot_orbits_corm_800_eval_fullabl.json` | `4` |
| `C2_hotpot_multiseed_stability` | `supported_bridge` | `pass` | `results/hotpot_corm_multiseed_summary_fullabl.json` | `2` |
| `C3_orbit_alignment_required` | `supported_bridge` | `pass` | `results/hotpot_corm_multiseed_summary_fullabl.json` | `2` |
| `C4_answer_consistency_mechanism` | `supported_bridge` | `pass` | `results/hotpot_corm_multiseed_summary_fullabl.json` | `2` |
| `C5_fever_second_domain_sanity` | `supported_secondary_bridge` | `pass` | `results/fever_nearmiss_corm_v3_multiseed_summary.json` | `3` |
| `C6_human_audit_not_complete` | `unsupported_until_audited` | `pass` | `results/audit_sample_100_v3_summary.json` | `2` |
| `C7_case_studies_available` | `supported_artifact` | `pass` | `results/fever_nearmiss_v3_case_studies.json`<br>`results/hotpot_case_studies.json` | `3` |
| `C8_paired_bootstrap_positive_deltas` | `supported_bridge` | `pass` | `results/fever_nearmiss_corm_v3_paired_comparison.json`<br>`results/hotpot_corm_paired_comparison.json` | `4` |
| `C9_corm_original_reproduction_blocked` | `unsupported_until_preflight_passes` | `pass` | `results/corm_reproduction_preflight.json` | `2` |
| `C10_calibrated_risk_guarantee_not_supported` | `unsupported_until_stronger_calibration` | `pass` | `results/fever_nearmiss_corm_v3_calibration_multiseed.json`<br>`results/hotpot_corm_calibration_multiseed.json` | `4` |
| `C14_cp_risk_control_partial_hotpot_only` | `supported_partial_pressure_test` | `pass` | `results/fever_nearmiss_corm_v3_risk_control_cp_multiseed.json`<br>`results/hotpot_corm_risk_control_cp_multiseed.json` | `5` |
| `C15_corm_reproduction_path_blocked` | `supported_blocker` | `pass` | `results/corm_reproduction_path_audit.json` | `5` |
| `C16_corm_supplemental_reconstruction_tools` | `supported_artifact` | `pass` | `results/corm_reproduction_path_audit.json` | `3` |
| `C17_corm_reconstruction_plan_ready` | `supported_artifact` | `pass` | `results/corm_reconstruction_plan.json` | `5` |
| `C18_corm_remote_script_pack_materialized` | `supported_artifact` | `pass` | `results/corm_remote_scripts_manifest.json` | `4` |
| `C19_corm_remote_runtime_ready` | `supported_artifact` | `pass` | `results/corm_remote_runtime_status.json` | `5` |
| `C20_corm_remote_checkpoint_uploaded` | `supported_artifact` | `pass` | `results/corm_remote_checkpoint_status.json` | `3` |
| `C21_corm_streaming_encoder_smoke` | `supported_artifact` | `pass` | `results/corm_streaming_encoder_remote_smoke.json` | `4` |
| `C22_corm_hf_streaming_encoder_smoke` | `supported_artifact` | `pass` | `results/corm_streaming_encoder_remote_hf_smoke.json` | `6` |
| `C23_corm_template_biased_nq_smoke` | `supported_artifact` | `pass` | `results/corm_template_biased_nq_remote_smoke.json` | `5` |
| `C24_corm_eval_stage_dir_patch` | `supported_artifact` | `pass` | `results/corm_eval_stage_dir_patch_status.json` | `5` |
| `C25_corm_template_smoke_eval_readiness` | `supported_artifact` | `pass` | `results/corm_template_smoke_eval_readiness_status.json` | `6` |
| `C26_corm_template_smoke_eval_watcher` | `supported_operational_status` | `pass` | `results/corm_template_smoke_eval_watcher_status.json` | `4` |
| `C11_structural_consistency_audits_pass` | `supported_structural_audit` | `pass` | `results/fever_nearmiss_corm_v3_orbit_consistency_audit.json`<br>`results/fever_nearmiss_corm_v3_seed31_orbit_consistency_audit.json`<br>`results/fever_nearmiss_corm_v3_seed47_orbit_consistency_audit.json`<br>`results/hotpot_orbit_consistency_audit.json` | `8` |
| `C12_nli_set_probe_cross_scorer` | `supported_probe` | `pass` | `results/audit_sample_paper_1000_v3_nli_set_eval.json` | `6` |
| `C13_hf_release_checkpoint_only` | `supported_blocker` | `pass` | `results/corm_release_manifest.json` | `3` |
| `C27_corm_partial_template_eval_smoke` | `supported_artifact` | `pass` | `results/corm_partial_template_eval_smoke_status.json` | `8` |
| `C28_corm_full_wikipedia_reconstruction_storage_blocked` | `supported_blocker` | `pass` | `results/corm_full_wikipedia_job_status.json` | `6` |

## Claims

### C1_hotpot_main_gain

- Declared status: `supported_bridge`.
- Verification status: `pass` (4/4 checks passed).
- Claim: On the HotpotQA bridge split with released CoRM critic scores, CSRM lowers selective risk versus CoRM clean scoring, SURE-style single-set sufficiency, and naive orbit averaging.
- Evidence files:
  - `results/hotpot_orbits_corm_800_eval_fullabl.json`
- Limitations:
  - Bridge split uses structural labels from Hotpot supporting facts, not completed human audit.
  - Full CoRM-RAG retrieval-generation evaluation is not reproduced.

### C2_hotpot_multiseed_stability

- Declared status: `supported_bridge`.
- Verification status: `pass` (2/2 checks passed).
- Claim: The HotpotQA bridge gain is stable across three random data seeds.
- Evidence files:
  - `results/hotpot_corm_multiseed_summary_fullabl.json`
- Limitations:
  - All seeds are from the same HotpotQA validation source.

### C3_orbit_alignment_required

- Declared status: `supported_bridge`.
- Verification status: `pass` (2/2 checks passed).
- Claim: CSRM's gain is not explained by using more perturbation calls alone; shuffled perturbation alignment collapses performance.
- Evidence files:
  - `results/hotpot_corm_multiseed_summary_fullabl.json`
- Limitations:
  - The shuffled ablation tests orbit alignment, not all possible verifier-call budget confounds.

### C4_answer_consistency_mechanism

- Declared status: `supported_bridge`.
- Verification status: `pass` (2/2 checks passed).
- Claim: Answer/support-signature consistency is a necessary mechanism on HotpotQA bridge splits.
- Evidence files:
  - `results/hotpot_corm_multiseed_summary_fullabl.json`
- Limitations:
  - Mechanism evidence is strongest for HotpotQA; FEVER v3 near-miss is a deliberately constructed heuristic stress split pending audit.

### C5_fever_second_domain_sanity

- Declared status: `supported_secondary_bridge`.
- Verification status: `pass` (3/3 checks passed).
- Claim: FEVER v3 near-miss dilution provides a second real-domain stress bridge where CSRM separates fragile orbits better than naive orbit averaging after support-key budget and non-gold support-feature audits.
- Evidence files:
  - `results/fever_nearmiss_corm_v3_multiseed_summary.json`
- Limitations:
  - The FEVER v3 near-miss split supersedes earlier builder versions whose audits exposed invalid missing-evidence coverage and non-gold high-support feature leakage.
  - The near-miss split still uses deliberately hard verifier-feature assignments and remains a heuristic stress bridge until human semantic audit is complete.

### C6_human_audit_not_complete

- Declared status: `unsupported_until_audited`.
- Verification status: `pass` (2/2 checks passed).
- Claim: Human audit is prepared but not complete.
- Evidence files:
  - `results/audit_sample_100_v3_summary.json`
- Limitations:
  - No human-audited performance claim can be made yet.

### C7_case_studies_available

- Declared status: `supported_artifact`.
- Verification status: `pass` (3/3 checks passed).
- Claim: Representative Hotpot and FEVER case studies have been extracted for failure and limitation analysis.
- Evidence files:
  - `results/fever_nearmiss_v3_case_studies.json`
  - `results/hotpot_case_studies.json`
- Limitations:
  - Case studies are selected from heuristic-label bridge data and must not replace human audit.

### C8_paired_bootstrap_positive_deltas

- Declared status: `supported_bridge`.
- Verification status: `pass` (4/4 checks passed).
- Claim: Paired bootstrap comparisons show positive selective-risk reductions for CSRM versus naive orbit averaging on both Hotpot and FEVER v3 near-miss bridge splits.
- Evidence files:
  - `results/fever_nearmiss_corm_v3_paired_comparison.json`
  - `results/hotpot_corm_paired_comparison.json`
- Limitations:
  - Paired bootstrap is computed over bridge labels; it does not resolve human-audit or verifier-validity gaps.

### C9_corm_original_reproduction_blocked

- Declared status: `unsupported_until_preflight_passes`.
- Verification status: `pass` (2/2 checks passed).
- Claim: Full CoRM-RAG original NQ/Biased-NQ/TruthfulQA reproduction is not complete in the current environment.
- Evidence files:
  - `results/corm_reproduction_preflight.json`
- Limitations:
  - The released Evidence Critic checkpoint is present, but original end-to-end reproduction still requires data/index files and runtime dependencies.
  - This claim is a blocker statement, not a performance result.

### C10_calibrated_risk_guarantee_not_supported

- Declared status: `unsupported_until_stronger_calibration`.
- Verification status: `pass` (4/4 checks passed).
- Claim: Current split-calibrated CSRM results do not support a formal risk guarantee at target risk 0.20.
- Evidence files:
  - `results/fever_nearmiss_corm_v3_calibration_multiseed.json`
  - `results/hotpot_corm_calibration_multiseed.json`
- Limitations:
  - The calibrated model improves ranking quality, but threshold transfer misses the 0.20 risk target in one of three split seeds on Hotpot and two of three FEVER v3 near-miss split seeds.
  - Zero-coverage thresholds are treated as vacuous and do not count as formal guarantees.

### C14_cp_risk_control_partial_hotpot_only

- Declared status: `supported_partial_pressure_test`.
- Verification status: `pass` (5/5 checks passed).
- Claim: A conservative Clopper-Pearson calibration pressure test supports empirical risk-target transfer for logistic CSRM on Hotpot only; FEVER v3 near-miss still fails the 0.20 target in two of three split seeds, so no general formal risk-control claim is supported.
- Evidence files:
  - `results/fever_nearmiss_corm_v3_risk_control_cp_multiseed.json`
  - `results/hotpot_corm_risk_control_cp_multiseed.json`
- Limitations:
  - The Clopper-Pearson bound is applied to calibration-set selective risk only; held-out target hits are empirical transfer checks, not distribution-free guarantees under domain or split shift.
  - The FEVER v3 near-miss bridge still misses the target in two of three split seeds for logistic CSRM.
  - Baselines without a feasible non-vacuous threshold remain zero-coverage under this conservative target and should not be counted as successful risk control.

### C15_corm_reproduction_path_blocked

- Declared status: `supported_blocker`.
- Verification status: `pass` (5/5 checks passed).
- Claim: The released CoRM-RAG repository does not expose a complete scripted path to rebuild the runtime artifacts required by run_eval.sh: wiki_passages.jsonl is partially scripted, but wiki.faiss and biased_nq_test.jsonl lack exact detected producers.
- Evidence files:
  - `results/corm_reproduction_path_audit.json`
- Limitations:
  - This is a source-path audit of the currently available repository, not proof that authors cannot provide the missing artifacts out of band.
  - Manual reconstruction may still be possible by adding a FAISS builder and recreating the Biased-NQ perturbation file, but that would no longer be a direct reproduction of the released evaluation pipeline.
  - The remote server has sufficient GPU hardware but currently lacks the ML runtime stack; environment setup alone does not solve the missing exact data/index generation path.

### C16_corm_supplemental_reconstruction_tools

- Declared status: `supported_artifact`.
- Verification status: `pass` (3/3 checks passed).
- Claim: This workspace now contains supplemental tools for a documented CoRM artifact reconstruction attempt: a FAISS builder from wiki embeddings and a Biased-NQ materializer from perturbation JSONL.
- Evidence files:
  - `results/corm_reproduction_path_audit.json`
- Limitations:
  - These are supplemental reconstruction helpers, not upstream CoRM-RAG release files.
  - Running the full reconstruction still requires Wikipedia embeddings/passages, perturbation generation or original perturbation JSONL, FAISS, vLLM, and enough disk/GPU resources.
  - Results from reconstructed artifacts must be reported as reconstructed-pipeline evidence unless exact equivalence to the authors' original artifacts is established.

### C17_corm_reconstruction_plan_ready

- Declared status: `supported_artifact`.
- Verification status: `pass` (5/5 checks passed).
- Claim: A machine-readable remote reconstruction plan now exists for running a documented CoRM reconstructed pipeline on the /mnt/ntfs-disk server workspace without writing secrets into scripts.
- Evidence files:
  - `results/corm_reconstruction_plan.json`
- Limitations:
  - The plan has not been executed; it is an execution artifact, not a reproduced result.
  - The plan still requires full Wikipedia encoding, FAISS construction, perturbation generation or staging, and vLLM evaluation.
  - The plan intentionally omits passwords and API keys; secrets must be provided by the caller or secure environment variables.

### C18_corm_remote_script_pack_materialized

- Declared status: `supported_artifact`.
- Verification status: `pass` (4/4 checks passed).
- Claim: The remote CoRM reconstruction plan has been materialized into an ordered, secret-free shell script pack for execution on the /mnt/ntfs-disk server workspace.
- Evidence files:
  - `results/corm_remote_scripts_manifest.json`
- Limitations:
  - The full ordered script pack has not been run end-to-end on the remote server; targeted runtime-bootstrap and staged-input smoke paths have been exercised separately.
  - The scripts still require full Wikipedia/FAISS generation, API credentials or staged perturbations, and substantial compute.
  - The script pack deliberately uses environment-variable references for secrets rather than embedding secret values.

### C19_corm_remote_runtime_ready

- Declared status: `supported_artifact`.
- Verification status: `pass` (5/5 checks passed).
- Claim: The remote CoRM reconstruction environment now has an import-ready Python runtime with torch/CUDA, FAISS, Transformers, datasets, and vLLM available under the transient /dev/shm runtime root.
- Evidence files:
  - `results/corm_remote_runtime_status.json`
- Limitations:
  - The runtime is transient because it lives under /dev/shm and must be recreated after a reboot.
  - This is runtime readiness only, not reconstructed evaluation evidence.
  - The CoRM checkpoint is now staged separately, but Wikipedia/FAISS/Biased-NQ artifacts have not been generated.

### C20_corm_remote_checkpoint_uploaded

- Declared status: `supported_artifact`.
- Verification status: `pass` (3/3 checks passed).
- Claim: The 5.2GB released CoRM Evidence Critic checkpoint has been uploaded to the remote reconstruction workspace and verified by SHA256.
- Evidence files:
  - `results/corm_remote_checkpoint_status.json`
- Limitations:
  - Checkpoint staging is necessary for reconstructed evaluation but does not produce any evaluation metric.
  - Data/index artifacts are still missing.

### C21_corm_streaming_encoder_smoke

- Declared status: `supported_artifact`.
- Verification status: `pass` (4/4 checks passed).
- Claim: The supplemental streaming Wikipedia encoder can consume staged JSONL input on the remote server, write sharded embeddings, and feed the supplemental FAISS builder without using the full Wikipedia dataset in memory.
- Evidence files:
  - `results/corm_streaming_encoder_remote_smoke.json`
- Limitations:
  - The smoke uses a dummy embedding backend and staged two-row JSONL input; it is an engineering path check, not full Wikipedia evidence.
  - Default direct huggingface.co access timed out on the server; C22 records that the HF Contriever/Wikipedia path works when launched with the mirror endpoint and /dev/shm cache, and a full Wikipedia construction job has been launched but is not complete.

### C22_corm_hf_streaming_encoder_smoke

- Declared status: `supported_artifact`.
- Verification status: `pass` (6/6 checks passed).
- Claim: The supplemental streaming Wikipedia encoder can stream real Wikipedia through a reachable HuggingFace mirror on the remote server, encode passages with facebook/contriever-msmarco on CUDA, and build a FAISS index from sharded 768-dimensional embeddings.
- Evidence files:
  - `results/corm_streaming_encoder_remote_hf_smoke.json`
- Limitations:
  - This is a 16-passage engineering smoke, not a full Wikipedia index or CoRM evaluation.
  - The HuggingFace/model cache lives under /dev/shm and is transient.
  - The resulting FAISS index is supplemental reconstructed-pipeline infrastructure, not the authors' original wiki.faiss artifact.

### C23_corm_template_biased_nq_smoke

- Declared status: `supported_artifact`.
- Verification status: `pass` (5/5 checks passed).
- Claim: When OpenAI-compatible API credentials are unavailable, the reconstructed pipeline has a deterministic template fallback that can produce structurally valid NQ perturbations and a Biased-NQ-format smoke file on the remote server.
- Evidence files:
  - `results/corm_template_biased_nq_remote_smoke.json`
- Limitations:
  - The template fallback is for reconstructed-pipeline smoke tests only.
  - It is not the authors' OpenAI-generated perturbation set and must not be reported as original Biased-NQ evidence.
  - It does not remove the need for API-generated or author-provided perturbations for serious reproduction claims.

### C24_corm_eval_stage_dir_patch

- Declared status: `supported_artifact`.
- Verification status: `pass` (5/5 checks passed).
- Claim: The reconstructed CoRM evaluation scripts have been patched and redeployed so staging can use a large persistent stage directory and symlink wiki.faiss instead of copying it under the almost-full root filesystem.
- Evidence files:
  - `results/corm_eval_stage_dir_patch_status.json`
- Limitations:
  - This is deployment-readiness evidence only, not a reconstructed CoRM evaluation result.
  - The patch does not create wiki.faiss, wiki_passages.jsonl, original Biased-NQ perturbations, or any evaluation metrics.
  - Symlink mode depends on the final FAISS file staying available under the remote persistent data directory.

### C25_corm_template_smoke_eval_readiness

- Declared status: `supported_artifact`.
- Verification status: `pass` (6/6 checks passed).
- Claim: A bounded template Biased-NQ reconstructed-eval smoke path has been generated, deployed, and syntax-checked so the first post-FAISS evaluation can run a small, explicitly smoke-labeled Biased_NQ path before any full reconstructed evaluation.
- Evidence files:
  - `results/corm_template_smoke_eval_readiness_status.json`
- Limitations:
  - This is readiness evidence for the full-index watcher-triggered smoke path; that path has not run and has produced no full-index metrics.
  - The path uses deterministic template perturbations and must not be reported as original Biased-NQ evidence.
  - The deployed script now uses a Qwen2.5 generator because the current remote Transformers/vLLM stack does not recognize Qwen3; this is a runtime-compatible reconstructed smoke choice, not an original-artifact equivalence claim.

### C26_corm_template_smoke_eval_watcher

- Declared status: `supported_operational_status`.
- Verification status: `pass` (4/4 checks passed).
- Claim: The post-FAISS template Biased_NQ smoke watcher was intentionally paused after the second NTFS/fuseblk storage failure so file records could be preserved for the active full-index reconstruction job.
- Evidence files:
  - `results/corm_template_smoke_eval_watcher_status.json`
- Limitations:
  - This is operational status evidence only; the watcher is not currently running.
  - The watcher should be redeployed only after wiki.faiss exists or after the storage situation is stable.
  - The eventual full-index smoke result, if produced, remains reconstructed-pipeline plumbing evidence rather than original Biased-NQ or full CoRM-RAG reproduction evidence.

### C11_structural_consistency_audits_pass

- Declared status: `supported_structural_audit`.
- Verification status: `pass` (8/8 checks passed).
- Claim: The current HotpotQA and FEVER v3 orbit files pass structural and dataset-constraint consistency checks for source provenance, label-source metadata, generated labels, split names, perturbation counts/types, support-key lineage, duplicate evidence ids, support-key coverage, support-feature provenance, and verifier-feature ranges.
- Evidence files:
  - `results/fever_nearmiss_corm_v3_orbit_consistency_audit.json`
  - `results/fever_nearmiss_corm_v3_seed31_orbit_consistency_audit.json`
  - `results/fever_nearmiss_corm_v3_seed47_orbit_consistency_audit.json`
  - `results/hotpot_orbit_consistency_audit.json`
- Limitations:
  - This deterministic audit checks implemented structural and dataset-provenance invariants only; it does not replace human semantic labeling.
  - The audit proves that the current generated orbit files satisfy implemented invariants; it does not prove that every heuristic label is semantically correct.

### C12_nli_set_probe_cross_scorer

- Declared status: `supported_probe`.
- Verification status: `pass` (6/6 checks passed).
- Claim: On the v3 paper-grade audit sample rescored with an independent set-level NLI verifier, CSRM still improves AUROC and Risk@30 versus naive orbit averaging, SURE-style single-set sufficiency, and shuffled perturbation alignment.
- Evidence files:
  - `results/audit_sample_paper_1000_v3_nli_set_eval.json`
- Limitations:
  - This is an automated cross-scorer probe using `cross-encoder/nli-deberta-v3-small`, not a validated human semantic audit.
  - The labels remain the v3 heuristic audit-sample labels; this result tests feature-source robustness, not final ground-truth validity.
  - The NLI verifier is set-level and off-the-shelf, so it should be presented as sensitivity analysis rather than primary evidence.

### C13_hf_release_checkpoint_only

- Declared status: `supported_blocker`.
- Verification status: `pass` (3/3 checks passed).
- Claim: The public Hugging Face release for CoRM-RAG contains the released critic checkpoint but does not contain the data/index artifacts required for full original retrieval-generation reproduction.
- Evidence files:
  - `results/corm_release_manifest.json`
- Limitations:
  - This claim is limited to the Hugging Face model release queried in `results/corm_release_manifest.json`.
  - GitHub API querying may be rate-limited; the blocker claim should be read together with the local preflight report.
  - The data artifacts could still be obtainable from authors or rebuilt from upstream sources, but they are not present in the queried HF release.

### C27_corm_partial_template_eval_smoke

- Declared status: `supported_artifact`.
- Verification status: `pass` (8/8 checks passed).
- Claim: An isolated partial-index template Biased_NQ smoke evaluation completed on the remote server, validating FAISS loading, retrieval, released CoRM critic scoring, vLLM generation, metric writing, runtime PATH wiring, and a Qwen2.5 generator fallback on a 200,000-vector reconstructed index.
- Evidence files:
  - `results/corm_partial_template_eval_smoke_status.json`
- Limitations:
  - This is an isolated four-shard partial-index smoke using deterministic template perturbations; it is not a full Wikipedia/FAISS index and not original Biased-NQ evidence.
  - The evaluation uses only two examples and produced accuracy 0.0, so it must not be used as a performance claim.
  - The result validates deployment plumbing and identifies the runtime-compatible generator path while the full reconstruction remains incomplete.

### C28_corm_full_wikipedia_reconstruction_storage_blocked

- Declared status: `supported_blocker`.
- Verification status: `pass` (6/6 checks passed).
- Claim: The full Wikipedia/FAISS reconstruction attempt made additional progress to a complete 250k-passage shard 000051, but the current remote path is blocked by NTFS/fuseblk storage I/O failures before wiki.faiss can be built.
- Evidence files:
  - `results/corm_full_wikipedia_job_status.json`
- Limitations:
  - This is documented reconstruction progress plus a storage blocker, not a completed original CoRM-RAG reproduction.
  - A reliable ext4/XFS persistent target or author-provided artifacts are still needed before reporting full retrieval-generation metrics.
  - Continuing on the current NTFS/fuseblk mount is not evidence-efficient because both embedding shard writes and wiki_passages.jsonl writes have repeatedly failed.

## Claim Boundary

This markdown ledger mirrors CLAIMS_LEDGER.json and results/claims_verification.json. It documents support and limitations; it does not upgrade bridge, proxy, or pending human-audit evidence into NeurIPS-ready main-claim support.
