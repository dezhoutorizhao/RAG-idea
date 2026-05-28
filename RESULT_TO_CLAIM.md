# Result-to-Claim Verdict

Date: 2026-05-20

Context: CSRM-RAG as a counterfactual selective-risk extension of CoRM-RAG.

Codex MCP reviewer status: unavailable in this environment. This verdict is a local judgment and should be treated as pending independent review.

Integrity status: WARN, from `EXPERIMENT_AUDIT.json`.

## Verdict

claim_supported: partial

confidence: medium

## What Results Support

The current evidence supports a bridge-study claim:

CSRM reduces selective risk on constructed counterfactual evidence orbits compared with CoRM clean document-score thresholding, SURE-style single-set sufficiency, and naive orbit averaging on HotpotQA-derived stress splits. A FEVER v3 near-miss dilution bridge now gives a second real-domain stress setting where CSRM separates fragile orbits better than naive averaging, after support-key budget and non-gold support-feature leakage fixes. The verifier features are still deliberately constructed and must be audited.

Evidence:

- `results/hotpot_orbits_corm_800_eval_fullabl.json`
- `results/hotpot_corm_multiseed_summary_fullabl.json`
- `results/fever_nearmiss_corm_v3_multiseed_summary.json`
- `results/hotpot_corm_paired_comparison.json`
- `results/fever_nearmiss_corm_v3_paired_comparison.json`
- `results/hotpot_corm_calibration_multiseed.json`
- `results/fever_nearmiss_corm_v3_calibration_multiseed.json`
- `results/hotpot_corm_risk_control_cp_multiseed.json`
- `results/fever_nearmiss_corm_v3_risk_control_cp_multiseed.json`
- `results/audit_sample_paper_1000_v3_nli_set_eval.json`
- `NLI_PROBE_REPORT.md`
- `results/corm_reproduction_preflight.json`
- `results/corm_reproduction_path_audit.json`
- `results/claims_verification.json`

The Hotpot result is stable across three random data seeds, and the shuffled-perturbation ablation collapses. FEVER v3 near-miss provides a second real-domain bridge where CSRM beats naive orbit averaging on AUROC and Risk@30, with paired bootstrap confidence intervals above zero for the naive comparison. This supports the claim that correctly aligned counterfactual orbits matter, rather than merely using more verifier calls.

A new set-level NLI probe on the 1,000-row v3 paper-grade audit sample replaces support/conflict/missing features with `cross-encoder/nli-deberta-v3-small` features. CSRM remains better than naive orbit averaging and SURE-style single-set sufficiency on AUROC and Risk@30, and shuffled perturbation alignment again collapses. This strengthens feature-source robustness, but it is still an automated sensitivity probe rather than human-audited evidence.

A conservative Clopper-Pearson threshold-selection pressure test improves the calibration picture only on Hotpot: logistic CSRM has nonzero held-out coverage, mean test risk 0.1472, max test risk 0.2000, and target met in 3/3 split seeds at target risk 0.20. The same procedure on FEVER v3 near-miss has mean test risk 0.1866 but max 0.2593 and target met in only 1/3 seeds. This supports a limited Hotpot-only empirical transfer statement, not a formal or cross-domain risk guarantee.

For CoRM reproduction, the workspace now includes supplemental reconstruction helpers for streaming/sharded Wikipedia encoding, building `wiki.faiss` from Contriever embeddings, and materializing `biased_nq_test.jsonl` from perturbation JSONL. The remote server now also has an import-ready transient runtime with torch/CUDA, FAISS, Transformers, datasets, and vLLM, plus a SHA256-verified uploaded critic checkpoint. A 16-passage real HF/Contriever smoke using `HF_ENDPOINT=https://hf-mirror.com` and `/dev/shm` cache verified streaming Wikipedia input, CUDA Contriever encoding, sharded embeddings, and FAISS construction. A deterministic template fallback can also create a structurally valid 100-row Biased-NQ smoke file without API credentials, the reconstructed eval script has been patched to stage data on `/mnt/ntfs-disk` instead of the almost-full root `/tmp`, a bounded template Biased_NQ eval-smoke path is deployed for post-FAISS plumbing checks, and a watcher is running to trigger that smoke path after `wiki.faiss` appears. An isolated partial-index template smoke has also completed end-to-end on a 200,000-vector FAISS index with two examples, validating retrieval, CoRM critic scoring, Qwen2.5 vLLM generation, and metric writing. The first full Wikipedia run hit an NTFS/fuseblk file-creation failure after forty-four shards; the encoder now has a resume/repair path and the resumed run is active with larger shards. These reduce the engineering gap for a future reconstructed run, but do not convert the current bridge study into an exact reproduction because the full original data/index artifacts, original perturbation file, and full reconstructed evaluation metrics are still absent.

`results/corm_reconstruction_plan.json` now records the remote `/mnt/ntfs-disk` execution plan for a reconstructed CoRM run, including environment setup, streaming Wikipedia encoding with `--resume`, FAISS construction, perturbation staging/generation, Biased-NQ materialization, and `run_eval.sh` invocation from the correct `src` directory. `results/corm_streaming_encoder_remote_smoke.json` verifies the staged-input sharded-embedding path with a dummy backend. `results/corm_streaming_encoder_remote_hf_smoke.json` verifies a small real Wikipedia/Contriever/CUDA/FAISS path through the mirror endpoint. `results/corm_partial_template_eval_smoke_status.json` verifies isolated partial-index eval plumbing only. No full reconstructed CoRM evaluation metrics exist yet.

`results/corm_remote_scripts/` materializes that plan into ordered shell scripts with a manifest that checks for embedded secret markers. This reduces execution error for the remote run, but still does not provide evaluation metrics.

## What Results Do Not Support

The results do not yet support a final broad NeurIPS main-track claim that CSRM is generally better for robust RAG.

Missing or weak areas:

- Human audit is not complete.
- FEVER v3 near-miss now differentiates CSRM from naive orbit averaging, and the current FEVER v3 orbit files pass structural plus dataset-constraint audits including support-feature provenance. It remains a heuristic stress bridge rather than human-audited evidence.
- Full CoRM-RAG retrieval-generation evaluation on NQ/Biased-NQ/TruthfulQA is not reproduced; the machine-readable preflight currently reports `ready=false`. A source-path audit also shows the available repository partially scripts `wiki_passages.jsonl`, but does not expose exact producers for `wiki.faiss` or `biased_nq_test.jsonl`. Default direct HuggingFace access still times out on the remote server, but the mirror plus `/dev/shm` cache path passed a 16-passage HF/Contriever smoke; full Wikipedia/FAISS data generation is now running remotely but remains incomplete. The partial-index smoke is explicitly not a substitute for full retrieval-generation reproduction.
- Generic NLI verifier scoring is useful as a cross-scorer sensitivity probe, but it is not validated enough to become the primary semantic verifier.
- Calibration does not yet justify a formal risk guarantee. The original empirical-threshold calibration misses the 0.20 risk target in one of three Hotpot split seeds and two of three FEVER v3 split seeds; a more conservative Clopper-Pearson threshold pressure test fixes Hotpot across the same three seeds but still misses FEVER v3 in two of three seeds.

## Suggested Claim Revision

Safe current claim:

Counterfactual sufficiency stability exposes a failure mode of document-level robustness and single-set sufficiency. On HotpotQA-derived stress orbits and FEVER v3 near-miss stress orbits scored with the released CoRM critic, CSRM reduces selective risk versus CoRM clean scoring, SURE-style single-set sufficiency, and naive orbit averaging; this improvement depends on correctly aligned perturbation orbits and answer/support-signature consistency. The claim remains a bridge-study claim until human audit and validated verifier labels are complete.

Optional sensitivity-analysis sentence:

The same ranking pattern persists on the v3 paper-grade audit sample when support/conflict/missing features are replaced with set-level NLI features from `cross-encoder/nli-deberta-v3-small`, suggesting that the orbit-stability signal is not only an artifact of one verifier feature source.

Unsafe current claim:

CSRM is submission-ready as a general robust RAG method with verified risk guarantees.

## Next Experiments Needed

1. Complete human audit for `results/audit_sample_100_v3.jsonl` using the shuffled blind annotator packs.
2. Complete paper-grade human audit for `results/audit_sample_paper_1000_v3.jsonl` after the pilot protocol is stable, also using blind annotator packs.
3. Add two independent labels and an `adjudicated_label_answerable` final label for paper claims; expected labels and model scores should remain hidden until adjudication.
4. Report double-label agreement and Cohen's kappa with `experiments/summarize_adjudication.py`.
5. Pass audit readiness with `experiments/check_audit_readiness.py`, using `--label-field adjudicated_label_answerable` for final claims.
6. Recompute metrics on audited labels with `experiments/evaluate_audited_orbits.py`, using the adjudicated label field for final claims.
7. Human-audit the FEVER v3 near-miss split or replace it with a naturally labeled second-domain stress split.
8. Improve calibration if a risk-guarantee claim is desired; current Clopper-Pearson thresholding supports only Hotpot-only empirical transfer and still fails FEVER v3.
9. Add a validated support/conflict/missing verifier or explicitly frame those fields as heuristic.
10. Execute or refine `results/corm_reconstruction_plan.json` on the remote `/mnt/ntfs-disk` workspace, then run `experiments/check_corm_reproduction_readiness.py` until `ready=true`; report any resulting metrics as reconstructed-pipeline evidence unless original-artifact equivalence is established.
11. Run independent review after audited results are available.

## Case Study Artifacts

- `results/hotpot_case_studies.json`
- `results/hotpot_case_studies.md`
- `results/fever_nearmiss_v3_case_studies.json`
- `results/fever_nearmiss_v3_case_studies.md`
