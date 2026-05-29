# Evidence Closure Status

Generated: `2026-05-29T02:23:57.036365+00:00`

Verdict: non-human bridge evidence is substantially closed, but full CoRM reconstruction and general formal risk control remain unsupported. Human audit v3 is explicitly excluded from this closure by user request.

## HotpotQA Bridge

| Method | AUROC | Risk@30 | AURC |
|---|---:|---:|---:|
| csrm | 0.9976 | 0.1669 | 0.4049 |
| naive_orbit_average | 0.8321 | 0.5119 | 0.5829 |
| corm_max_clean | 0.5000 | 0.7497 | 0.7444 |
| single_set_sure_style | 0.5000 | 0.7497 | 0.7375 |
| csrm_shuffled_perturbations | 0.0001 | 1.0000 | 0.9633 |

## FEVER v3 Near-Miss Bridge

| Method | AUROC | Risk@30 | AURC |
|---|---:|---:|---:|
| csrm | 1.0000 | 0.4444 | 0.5301 |
| naive_orbit_average | 0.7764 | 0.6407 | 0.7719 |
| corm_max_clean | 0.5000 | 0.8333 | 0.8306 |
| single_set_sure_style | 0.5000 | 0.8333 | 0.8264 |
| csrm_shuffled_perturbations | 0.0327 | 1.0000 | 0.9778 |

## NLI Cross-Scorer Probe

| Method | AUROC | Risk@30 | AURC |
|---|---:|---:|---:|
| csrm | 0.7353 | 0.6267 | 0.6676 |
| naive_orbit_average | 0.4880 | 0.8600 | 0.7959 |
| corm_max_clean | 0.5244 | 0.7800 | 0.7838 |
| single_set_sure_style | 0.4818 | 0.8700 | 0.8202 |
| csrm_shuffled_perturbations | 0.3281 | 0.9367 | 0.8921 |

## Risk Control

- Hotpot CP empirical transfer: `True`; formal guarantee: `False`; target misses: `0`.
- FEVER CP empirical transfer: `False`; formal guarantee: `False`; target misses: `2`.
- FEVER CP target sweep: 0.20 supported `False` with `2` misses; first observed all-seed pass at `0.3500` with max test risk `0.3443`.
- FEVER CP claim implication: FEVER near-miss is negative evidence for the 0.20 empirical risk-transfer claim: the primary method misses at 0.20 and only passes all observed seeds after relaxing the target to 0.3500. This should be reported as a boundary condition, not as a NeurIPS-level main risk-control result.

## Current Evidence Reproduction

- Ready for NeurIPS main claim: `False`.
- Human audit pending: `300`; human eval ready: `False`.
- Full CoRM reconstruction ready: `False`; remote storage ready: `False`.
- Claim verifier passed: `True`.

## Results Provenance

- README artifact: `results/README.md`; exists: `True`.
- Provenance steps: `16`; tracked artifacts: `86`.
- Manifest missing artifacts: `0`; missing current-step outputs: `0`; untracked current-step outputs: `0`.
- Claim boundary: This README records artifact provenance for the current evidence package. It does not complete pending human audit labels, full CoRM-RAG reproduction, or unsupported formal/general risk-control claims.

## Reproducibility Bundle

- Artifact checksums: `86`; dataset construction hashes: `41`.
- Checkpoint hash available: `True`; unique seeds: `3`.
- Hidden local path audit passed: `True`; findings: `0`.
- Remote storage ready: `False`.
- Claim boundary: This reproducibility bundle documents the current evidence package. It does not complete human audit labels, full CoRM-RAG reproduction, or general formal risk-control support.

## NeurIPS Readiness Matrix

- Ready for NeurIPS main-track claim: `False`.
- Status counts: `{'blocked': 3, 'fail': 1, 'partial': 2, 'pass': 4}`.
- Hard blockers: `3`; negative/partial evidence items: `3`.

Hard blockers:
- Human-audited orbit labels: Pending labels: 300; cannot claim human-audited results.
- Full CoRM-RAG reproduction: Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts.
- Independent external review: Not rerun after latest evidence package; requires explicit external/subagent review or another approved review path.

Negative or partial evidence:
- Strong baselines and equal-budget controls (`partial`): Baseline package exists, but CSRM-Rule has losses/ties against strongest learned/context baselines; claims must use calibrated/proxy wording with caveats.
- End-to-end selective RAG (`partial`): Proxy evidence is directional but mixed and not a full CoRM-RAG retrieval-generation reproduction.
- Risk-control claim (`fail`): Hotpot-only empirical transfer is positive; FEVER 0.20 target is negative, so no general/formal claim.

## V4 Strong Baselines

- Baseline files: `6`; comparison files: `6`.
- Method union: `calibrated_logistic_context, calibrated_logistic_orbit, context_sufficiency_clean, corm_max_clean, corm_mean_clean, csrm_rule, equal_budget_ensemble_logistic, equal_budget_mean, equal_budget_min, equal_budget_q25, faithful_sure_multi, retrieval_stability, self_consistency_proxy`.
- CSRM-Rule losses vs strongest by AUROC/Risk@30/AURC: `6` / `6` / `6`.
- CSRM-Calibrated-Logistic robust Risk@30 wins/losses: `1` / `1`; AURC robust wins/losses: `1` / `5`.
- Claim implication: The v4 strong-baseline package is present and includes context sufficiency, faithful SURE-style multi-set scoring, equal-budget orbit reducers, retrieval stability, self-consistency, and out-of-fold calibrated logistic context/orbit baselines. It strengthens reviewer-facing baseline coverage, but it is also negative boundary evidence: CSRM-Rule is not an all-win method against the strongest learned/context baselines, and calibrated CSRM should be reported with per-setting caveats.

## V4 Failure Taxonomy

- Datasets: `6`; construction buckets: `11`.
- AUROC wins/ties/losses vs calibrated logistic orbit: `0` / `3` / `3`.
- Risk@30 wins/ties/losses vs calibrated logistic orbit: `1` / `4` / `1`.
- Risk@50 wins/ties/losses vs calibrated logistic orbit: `0` / `4` / `2`.
- Case gallery coverage: `{'baseline_over_target_on_positive': 48, 'target_high_false_positive': 48, 'target_low_false_negative': 48, 'target_over_baseline_on_negative': 48}`.
- Recurring top feature gaps: `min_sufficiency, clean_to_worst_gap, verifier_entropy, retrieval_overlap, answer_consistency`.
- Claim implication: The v4 failure taxonomy is now machine-readable across FEVER and Hotpot variants. It supports a paper narrative around counterfactual sufficiency instability and documents mixed target-vs-baseline behavior. It remains heuristic/private-label analysis until human audit v4 adjudication is complete.

V4 case-study gallery:
- Cases: `192` from `6` inputs.
- Bucket coverage: `{'baseline_over_target_on_positive': 48, 'target_high_false_positive': 48, 'target_low_false_negative': 48, 'target_over_baseline_on_negative': 48}`.
- Outputs: `paper\case_studies\v4_case_gallery_20260529.jsonl` and `paper\case_studies\v4_case_gallery_20260529.md`.
- Claim boundary: Diagnostic case gallery exported from private-label v4 failure analyses; not human-adjudicated evidence.

Clean-sufficiency misleading diagnostic:
- Rows: `1200` across `6` datasets; overall private-label failure rate: `0.5000`.
- Top-quartile clean sufficiency threshold/failure rate/n: `0.2390` / `0.5050` / `303`.
- Top-quartile worst sufficiency threshold/failure rate/n: `0.2253` / `0.3609` / `302`.
- Outputs: `paper\figures\clean_sufficiency_misleading_v4_20260529.svg` and `paper\figures\clean_sufficiency_misleading_v4_20260529.csv`.
- Claim boundary: Private-label diagnostic figure: failure rates come from v4 heuristic/private labels, not human-adjudicated labels.

V4 anti-shortcut suite:
- Datasets: `6`; core suite passed: `True`.
- Raw firewall all passed: `True`; group split no-overlap all passed: `True`.
- Structural-only all passed <= 0.55: `True`; max single-feature AUROC: `0.5188`.
- Random-label median AUROC range: `0.4961` to `0.5054`.
- Private metadata upper bound all high: `True`.
- Claim implication: The primary v4 anti-shortcut suite passes the core non-oracle checks: raw feature firewall, structural-only <= 0.55, source-item group split without overlap, and random-label sanity near 0.5. Private construction metadata remains a high-leakage upper bound, so these fields must stay evaluator-only. This supports leakage-control claims but does not replace human audit or end-to-end RAG evidence.

## Mechanism Ablation

- Datasets: `2`; strong alignment evidence: `True`.
- Shuffled perturbations mean AUROC drop / Risk@30 increase / AURC increase: `0.9824` / `0.6943` / `0.5031`.
- No-answer-consistency mean AUROC drop / Risk@30 increase: `0.1239` / `0.2399`.
- No-worst-sufficiency mean AUROC drop / Risk@30 increase: `-0.0004` / `0.0000`.
- Weak or negative standalone component evidence: `['csrm_no_answer_consistency', 'csrm_no_worst_sufficiency']`.
- Claim implication: Mechanism ablations strongly support orbit alignment as necessary: shuffled perturbations collapse on both Hotpot and FEVER. Answer consistency is important on Hotpot and mildly positive on FEVER. Worst-sufficiency removal is not consistently harmful in the current bridge artifacts, so it should be framed as a weak or redundant component rather than a required standalone mechanism.

## End-to-End Selective RAG Proxy

- Rows: `12`; all-win: `False`; has losses/mixed rows: `True`.
- Risk@30 wins/ties/losses vs strongest non-CSRM: `8` / `2` / `2`.
- Risk@50 wins/ties/losses vs strongest non-CSRM: `12` / `0` / `0`.
- AURC wins/ties/losses vs strongest non-CSRM: `8` / `0` / `4`.
- Mean Risk@30/Risk@50/AURC reduction: `0.1528` / `0.1917` / `0.1086`.
- Claim implication: The proxy supports a directional but not all-win end-to-end selective RAG claim. CSRM improves mean Risk@30/Risk@50 versus the strongest non-CSRM selector, but some Hotpot v4 variants are mixed or negative, so this evidence should be framed as proxy/diagnostic evidence rather than a complete NeurIPS main result.

## CoRM Reconstruction

- Preflight ready: `False`.
- Missing required artifacts: `5`.
- Remote status: `failed_storage_io_after_fresh_250k_recovery`.
- Complete embedding shards: `52`; latest: `embeddings_shard_000051.npy`.
- FAISS exists: `False`.
- Terminal failure: The 250k-shard resume wrote embeddings_shard_000051.npy completely, then failed while writing/flushing wiki_passages.jsonl with OSError [Errno 5] Input/output error on the NTFS/fuseblk mount.

Latest storage probe:
- Target: `/mnt/ntfs-disk` (fuseblk, capacity `84%`).
- Reported available: `322.1444` GiB; minimum met: `True`.
- Write probe passed: `False`; storage-ready: `False`.
- Write probe error: `mktemp: 无法通过模板 “/mnt/ntfs-disk/csrm_write_probe.XXXXXX” 创建目录: 设备上没有空间`.
- GPU query: `0, NVIDIA GeForce RTX 4090, 24564, 24076; 1, NVIDIA GeForce RTX 4090, 24564, 24097`.

Latest ext4 cleanup dry run:
- Target: `/home/syk`; mode: `dry_run`; destructive operations executed: `False`.
- Cleanup steps planned: `3`; minimum free required: `180.0` GiB.
- Docker JSON logs bytes: `143790630971`.
- Root cache: `31G	/root/.cache`; user cache: `19G	/home/syk/.cache`.

## Latest V4 Hotpot Diagnostic

Semantic-swap n100:
- Construction audit passed: `True`; failed groups: `0`.
- Perturbation doc overlap: `1.0000`; text changed rate: `1.0000`; answer-mention reduced rate: `1.0000`.
- Structural-only max AUROC: `0.5009`.
- CSRM-Rule AUROC/Risk@30/AURC: `0.9031` / `0.1500` / `0.2280`.
- Strongest non-CSRM: `calibrated_logistic_orbit` with AUROC `0.9649`.
- CSRM-Calibrated-Logistic AUROC mean: `0.9658`; vs calibrated logistic orbit AUROC delta mean: `0.0000`.
- Human-audited labels complete: `False` (labeled `0`, pending `200`).

Human audit v4 aggregate:
- Ready: `False`; packs: `2`; items: `300`.
- Adjudicated labels: `0`; pending: `300`.

Human audit v4 evaluation gate:
- Ready: `False`; evaluated packs: `0/2`; allow partial: `False`.

## Claim Boundary

Allowed claims:
- CSRM has strong bridge evidence on HotpotQA-derived orbits with released CoRM critic scores.
- CSRM has secondary bridge evidence on FEVER v3 near-miss orbits.
- Orbit alignment is necessary under the implemented shuffled-perturbation ablation.
- The directional CSRM ranking survives an automated NLI cross-scorer sensitivity probe.
- Hotpot-only empirical risk-target transfer is supported under the conservative CP pressure test.
- Hotpot semantic-swap v4 is a leakage-controlled diagnostic where self-consistency and retrieval-stability shortcuts fail.
- The v4 failure taxonomy and case gallery are machine-readable diagnostics across FEVER and Hotpot variants, with heuristic/private-label status until human audit v4 is complete.
- A paper-facing v4 case-study gallery has been exported from failure-analysis top cases for qualitative inspection.
- A private-label diagnostic figure shows that high clean text-only sufficiency still contains many v4 orbit failures; this supports the qualitative motivation but not a human-audited claim.
- The primary v4 anti-shortcut suite passes raw-firewall, structural-only, group-split, and random-label sanity checks across six n100 variants.
- Mechanism ablations strongly support orbit alignment as necessary; shuffled perturbations collapse across Hotpot and FEVER bridge settings.

Disallowed claims:
- Full original CoRM-RAG retrieval-generation reproduction is complete.
- A general formal risk-control guarantee is established.
- The results are human-audited.
- The method solves robust RAG generally across tasks.
- CSRM significantly beats the strongest learned orbit baseline on Hotpot semantic-swap v4.
- The v4 failure taxonomy is human-adjudicated evidence.

Remaining non-human blockers:
- Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts; an ext4 cleanup path exists but needs explicit approval before deleting logs/caches.
- FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.
- Independent external review has not been rerun after the latest storage-status update.
- End-to-end selective RAG evidence is currently proxy-only and mixed on some Hotpot v4 variants; it is not a full CoRM-RAG reproduction.
- V4 strong baselines are present, but CSRM-Rule loses or ties the strongest learned/context baselines; main claims must use calibrated/proxy wording with caveats.

Remaining human-audit blockers:
- Human audit v4 packs are prepared for Hotpot semantic-swap blind200 and FEVER structbalanced blind100, but adjudicated labels are pending for all 300 items.

## Verification

Claim verifier: `28/28` passed, `0` failed.
