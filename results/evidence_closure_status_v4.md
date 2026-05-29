# Evidence Closure Status

Generated: `2026-05-29T07:43:16.132263+00:00`

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
- Human audit pending: `1300`; human eval ready: `False`.
- Full CoRM reconstruction ready: `False`; remote storage ready: `False`.
- Claim verifier passed: `True`.

## Results Provenance

- README artifact: `results/README.md`; exists: `True`.
- Provenance steps: `41`; tracked artifacts: `202`.
- Manifest missing artifacts: `0`; missing current-step outputs: `0`; untracked current-step outputs: `0`.
- Claim boundary: This README records artifact provenance for the current evidence package. It does not complete pending human audit labels, full CoRM-RAG reproduction, or unsupported formal/general risk-control claims.

## Reproducibility Bundle

- Artifact checksums: `202`; dataset construction hashes: `42`.
- Checkpoint hash available: `True`; unique seeds: `3`.
- Hidden local path audit passed: `True`; findings: `0`.
- Remote storage ready: `False`.
- Claim boundary: This reproducibility bundle documents the current evidence package. It does not complete human audit labels, full CoRM-RAG reproduction, or general formal risk-control support.

## V4 Calibration Quality

- Supported: `False`; datasets: `6`.
- Brier wins: `6/6`; ECE wins: `4/6`.
- Mean Brier reduction: `0.1604`; mean ECE reduction: `0.1030`.
- ECE non-win datasets: `['hotpot_orbits_v4_n100.constant.hardmatched', 'hotpot_orbits_v4_n100.constant.structbalanced']`.
- Claim implication: Calibrated CSRM variants, including logistic, isotonic, and GBDT calibration, strongly improve Brier score over rule/minimax baselines across all current v4 calibration datasets. ECE improves on most but not all datasets, so calibration should be claimed as empirical calibration-quality evidence, not as a formal risk guarantee.

## V4 Claim-Safe Target Selection

- Recommended primary target: `csrm_calibrated_gbdt`.
- All-win supported: `False`.
- Claim-safe status: `partial`.
- Blocked items: `['LLM-as-judge baseline is still missing.', 'Faithful/full CoRM-RAG baseline remains partial until full reproduction is complete.', 'Human audit labels are incomplete: pending auditor labels=2000, pending adjudicated labels=1000.', 'Text-only verifier main claim is blocked by missing LLM correlation and human labels.']`.

## NeurIPS Readiness Matrix

- Ready for NeurIPS main-track claim: `False`.
- Status counts: `{'blocked': 3, 'fail': 1, 'partial': 5, 'pass': 5}`.
- Hard blockers: `3`; negative/partial evidence items: `6`.

Hard blockers:
- Human-audited orbit labels: Assignment batches ready: True; batch collection complete: False; pending labels: 1300; cannot claim human-audited results.
- Full CoRM-RAG reproduction: Blocked by NTFS/fuseblk storage I/O failures and missing final wiki.faiss/original artifacts. Latest storage probe shows 322.1 GiB available and target_write_probe_passed=False; 6 target-dir file probes failed while writable fallback dirs are ['/home/syk', '/tmp', '/dev/shm'].
- Independent external review: External review packet is ready, but no independent review response is present; place the response at `results\external_review_response_20260529.md`.

Negative or partial evidence:
- Text-only semantic verifier (`partial`): NLI cross-scorer evidence is directionally positive against required weak baselines, but LLM-NLI correlation and human-label text-only evaluation are not ready.
- Strong baselines and equal-budget controls (`partial`): Baseline package exists, but CSRM-Rule has losses/ties against strongest learned/context baselines; coverage/budget matrices still mark faithful CoRM as partial, clean-only controls as lower-budget, and LLM judge scores as missing. The LLM judge request pack is ready, but no API-backed score artifact exists. Template multi-sample self-consistency, risk-control abstention baselines, shared calibration-threshold selection, and claim-safe target selection are auditable, but test risk/coverage remains mixed rather than all-win.
- End-to-end selective RAG (`partial`): Proxy evidence now covers two local retrievers and two generators, but remains mixed and is not a full CoRM-RAG Wikipedia retrieval-generation reproduction. The risk-coverage and target-risk coverage artifacts summarize lower accepted-error risk at fixed coverage and higher coverage at fixed target risk, but do not remove the full-reproduction boundary.
- Novelty and positioning (`partial`): Latest novelty audit recommends proceed-with-caution: closest risks are CoRM-RAG, SURE-RAG, Sufficient Context, CF-RAG, and conformal factuality work. Positioning must stay narrow around aligned evidence-orbit selective risk and cannot claim strong novelty until human-audited results and remaining baselines are complete.
- Calibrated orbit risk model (`partial`): Calibration-quality artifact shows Brier wins 6/6 against rule/minimax references, but ECE wins 4/6. This supports empirical calibration-quality wording, not a formal risk guarantee.
- Risk-control claim (`fail`): Hotpot-only empirical transfer is positive; FEVER 0.20 target is negative, so no general/formal claim.

## External Review Packet

- Packet status: `packet_ready`; packet ready: `True`; packet exists: `True`.
- External review completed: `False`; ready for independent-review claim: `False`.
- Missing packet source artifacts: `0`.
- Review response path: `results\external_review_response_20260529.md`.
- Claim policy: This packet prepares the current evidence package for independent external review. It is not itself an external review and does not upgrade any claim until an independent review response is present.

## V4 Strong Baselines

- Baseline files: `6`; comparison files: `6`.
- Method union: `calibrated_logistic_context, calibrated_logistic_orbit, context_sufficiency_clean, corm_max_clean, corm_mean_clean, csrm_rule, equal_budget_ensemble_logistic, equal_budget_mean, equal_budget_min, equal_budget_q25, faithful_sure_multi, retrieval_stability, self_consistency_proxy, template_self_consistency`.
- CSRM-Rule losses vs strongest by AUROC/Risk@30/AURC: `6` / `6` / `6`.
- CSRM-Calibrated-Logistic robust Risk@30 wins/losses: `1` / `1`; AURC robust wins/losses: `1` / `5`.
- Claim implication: The v4 strong-baseline package is present and includes context sufficiency, faithful SURE-style multi-set scoring, equal-budget orbit reducers, retrieval stability, self-consistency, and out-of-fold calibrated logistic context/orbit baselines. It strengthens reviewer-facing baseline coverage, but it is also negative boundary evidence: CSRM-Rule is not an all-win method against the strongest learned/context baselines, and calibrated CSRM should be reported with per-setting caveats.

## Risk-Control Abstention Baselines

- Shared-threshold protocol complete: `True`.
- Baseline present: `True`; method count: `13`.
- Methods: `calibrated_logistic_context, calibrated_logistic_orbit, context_sufficiency_clean, corm_max_clean, corm_mean_clean, equal_budget_ensemble_logistic, equal_budget_mean, equal_budget_min, equal_budget_q25, faithful_sure_multi, retrieval_stability, self_consistency_proxy, template_self_consistency`.
- Claim boundary: This artifact audits non-CSRM risk-control/abstention baselines under the same calibration-threshold protocol as CSRM targets. It is empirical held-out evidence, not a formal conformal guarantee and not a full CoRM-RAG reproduction.

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

## Theory Formalization

- Ready: `True`; files present: `True`; labels present: `True`; concepts present: `True`.
- Section files: `['paper\\sections\\formalization.tex', 'paper\\sections\\theory.tex']`.
- Present labels: `['sec:formalization', 'sec:theory', 'prop:clean-not-orbit', 'prop:single-set-not-orbit', 'prop:orbit-alignment-necessary']`.
- Claim implication: The formalization supports the mechanism-level information-structure claim that clean-only, single-set, and unaligned evidence are insufficient for item-level counterfactual orbit risk. It does not prove empirical all-win behavior, human validity, or a formal risk-control guarantee.

## Novelty Audit

- Search date: `2026-05-29`.
- Recommendation: `proceed_with_caution`; score: `6.5/10`; strong novelty ready: `False`.
- Closest prior risks: Beyond Semantic Relevance: Counterfactual Risk Minimization for Robust Retrieval-Augmented Generation (2026, high), SURE-RAG: Sufficiency and Uncertainty-Aware Evidence Verification for Selective Retrieval-Augmented Generation (2026, high), Sufficient Context: A New Lens on Retrieval Augmented Generation Systems (2025, medium), Counterfactual Reasoning for Retrieval-Augmented Generation (2026, high), Causal-Counterfactual RAG: The Integration of Causal-Counterfactual Reasoning into RAG (2025, medium).
- Required to upgrade: `['Complete the 1000-item Human Audit v4 labels and report human-label metrics.', 'Obtain API-backed LLM-judge baseline/correlation scores or remove LLM-judge claims.', 'Keep full CoRM-RAG reproduction unsupported until the storage/index artifacts are repaired.', 'Write related work around SURE-RAG, Sufficient Context, CF-RAG, and CoRM-RAG as closest neighbors.']`.
- Claim policy: This is a current literature-positioning audit, not proof of novelty. It supports a narrow proceed-with-caution framing and highlights prior-work risks that must be disclosed in any NeurIPS submission.

## End-to-End Selective RAG Proxy

- Rows: `12`; all-win: `False`; has losses/mixed rows: `True`.
- Risk@30 wins/ties/losses vs strongest non-CSRM: `8` / `2` / `2`.
- Risk@50 wins/ties/losses vs strongest non-CSRM: `12` / `0` / `0`.
- AURC wins/ties/losses vs strongest non-CSRM: `8` / `0` / `4`.
- Mean Risk@30/Risk@50/AURC reduction: `0.1528` / `0.1917` / `0.1086`.
- Claim implication: The proxy supports a directional but not all-win end-to-end selective RAG claim. CSRM improves mean Risk@30/Risk@50 versus the strongest non-CSRM selector, but some Hotpot v4 variants are mixed or negative, so this evidence should be framed as proxy/diagnostic evidence rather than a complete NeurIPS main result.

## End-to-End Retriever-Generator Matrix

- Datasets: `6`; retrievers: `['bm25_orbit_pool', 'dense_hash_orbit_pool']`; generators: `['copy_candidate', 'lexical_guarded']`.
- Rows: `24`; all-win: `False`; has losses/mixed rows: `True`.
- Risk@30 wins/ties/losses vs strongest non-CSRM: `16` / `4` / `4`.
- Risk@50 wins/ties/losses vs strongest non-CSRM: `24` / `0` / `0`.
- AURC wins/ties/losses vs strongest non-CSRM: `16` / `0` / `8`.
- Mean Risk@30/Risk@50/AURC reduction: `0.1507` / `0.1892` / `0.1068`.
- Claim policy: This matrix expands the end-to-end proxy to two retrieval policies and two generators over the materialized v4 orbit corpus. It is still a local-corpus proxy, not a full Wikipedia retrieval-generation reproduction.

## End-to-End Risk-Coverage Curves

- Rows: `24`; coverage points: `7`; CSRM lower-risk points: `6`.
- Risk@30 mean CSRM / strongest non-CSRM / reduction: `0.2056` / `0.3562` / `0.1507`.
- Risk@50 mean CSRM / strongest non-CSRM / reduction: `0.2000` / `0.3892` / `0.1892`.
- SVG: `paper\figures\end2end_risk_coverage_curves_20260529.svg`.
- Claim policy: This figure summarizes risk-coverage curves for the local-corpus end-to-end proxy matrix. It is useful Phase 5 visualization evidence, but it is not a full Wikipedia/CoRM-RAG retrieval-generation reproduction.

## End-to-End Coverage at Target Risk

- Source rows: `24`; target-risk rows: `72`; targets: `[0.2, 0.3, 0.4]`.
- CSRM higher mean coverage target count: `3` / `3`.
- Row-level wins/ties/losses vs strongest non-CSRM: `40` / `28` / `4`.
- Coverage-at-target-risk supported: `True`.
- Claim policy: This artifact reports coverage at fixed accepted-error risk targets for the same local-corpus end-to-end proxy matrix as the risk-coverage curve. It is not a full Wikipedia/CoRM-RAG reproduction and should not be used as human-audited evidence.

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
- Docker JSON logs bytes: `143951079035`.
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
- Ready: `False`; packs: `3`; items: `1300`.
- Adjudicated labels: `0`; pending: `1300`.

Human audit v4 evaluation gate:
- Ready: `False`; evaluated packs: `0/3`; allow partial: `False`.

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
- The theory/formalization module states the orbit-risk object and information-structure rationale for clean-only, single-set, and aligned-orbit evidence.
- The novelty audit supports a narrow proceed-with-caution positioning around aligned evidence-orbit selective risk.
- The calibrated orbit risk model improves Brier score over rule/minimax baselines across current v4 calibration artifacts; ECE evidence is mostly positive but mixed.
- The claim-safe target-selection audit recommends calibrated CSRM wording with explicit caveats rather than CSRM-Rule or all-win wording.

Disallowed claims:
- Full original CoRM-RAG retrieval-generation reproduction is complete.
- A general formal risk-control guarantee is established.
- The results are human-audited.
- The method solves robust RAG generally across tasks.
- CSRM significantly beats the strongest learned orbit baseline on Hotpot semantic-swap v4.
- The v4 failure taxonomy is human-adjudicated evidence.
- Calibration establishes a formal risk-control guarantee.
- The theory/formalization module proves empirical all-win behavior or replaces human audit.
- CSRM-RAG has a closed strong novelty claim independent of CoRM-RAG, SURE-RAG, Sufficient Context, and CF-RAG.
- CSRM-Rule or any calibrated CSRM target is an all-win method against the current strong-baseline suite.

Remaining non-human blockers:
- Full CoRM reconstruction is blocked by remote NTFS/fuseblk I/O failures and missing local artifacts; an ext4 cleanup path exists but needs explicit approval before deleting logs/caches.
- FEVER v3 does not pass the current CP empirical-transfer target, so formal/general risk-control wording remains unsupported.
- External review packet is ready, but independent review remains pending; place the response at results\external_review_response_20260529.md.
- End-to-end selective RAG evidence is currently proxy-only: fixed-coverage and fixed-risk views are directionally positive, but some Hotpot v4 variants remain mixed and this is not a full CoRM-RAG reproduction.
- V4 strong baselines are present, but CSRM-Rule loses or ties the strongest learned/context baselines; main claims must use calibrated/proxy wording with caveats.
- Claim-safe target selection recommends csrm_calibrated_gbdt only with caveats; all-win support is False, and blockers remain: LLM-as-judge baseline is still missing.; Faithful/full CoRM-RAG baseline remains partial until full reproduction is complete.; Human audit labels are incomplete: pending auditor labels=2000, pending adjudicated labels=1000.; Text-only verifier main claim is blocked by missing LLM correlation and human labels.
- V4 calibrated orbit risk improves Brier on all current calibration artifacts, but ECE is mixed, so calibration remains partial evidence rather than a closed formal-risk claim.
- Novelty positioning remains proceed-with-caution because closely related 2025-2026 work exists; strong novelty claims require narrower wording and completed human-audit/baseline evidence.

Remaining human-audit blockers:
- Human audit v4 packs are prepared, including the paper-grade mixed blind1000 pack, but adjudicated labels are pending for all 1300 items.

## Verification

Claim verifier: `28/28` passed, `0` failed.
