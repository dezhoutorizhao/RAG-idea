# CSRM-RAG Audit Protocol

Purpose: verify whether the orbit labels used in the HotpotQA and FEVER v3 stress splits are defensible enough for paper claims.

Pilot audit file:

```text
results/audit_sample_100_v3.jsonl
```

Paper-grade audit candidate file:

```text
results/audit_sample_paper_1000_v3.jsonl
```

The paper-grade file contains 1,000 balanced candidates: 100 orbits from each current HotpotQA and FEVER v3 stress split. Use the pilot file first to calibrate annotation guidelines; use the paper-grade file for final claim validation. The older v2 packs are retained only as historical artifacts and must not be used for final FEVER v3 claims.

Generated annotation packs:

```text
results/audit_pack_100_v3.labels.csv
results/audit_pack_100_v3.review.html
results/audit_pack_100_v3_a1.blind.labels.csv
results/audit_pack_100_v3_a1.blind.review.html
results/audit_pack_100_v3_a2.blind.labels.csv
results/audit_pack_100_v3_a2.blind.review.html
results/audit_pack_paper_1000_v3.labels.csv
results/audit_pack_paper_1000_v3.review.html
results/audit_pack_paper_1000_v3_a1.blind.labels.csv
results/audit_pack_paper_1000_v3_a1.blind.review.html
results/audit_pack_paper_1000_v3_a2.blind.labels.csv
results/audit_pack_paper_1000_v3_a2.blind.review.html
```

Use the blind CSV/HTML pairs for independent human labeling. The non-blind CSV/HTML packs expose expected labels and model scores, so they are diagnostic/adjudication aids rather than the primary evidence source for paper claims.

Each line is one orbit. Fill these fields only:

- `auditor_label_answerable`: `true` if the clean query and every perturbation have enough non-conflicting evidence to support the expected answer or label; otherwise `false`.
- `auditor_failure_type`: short category when the auditor label is false or disagrees with the expected label.
- `auditor_notes`: one short explanation.

For final paper claims, use two independent labels plus an adjudicated final label. Use `adjudicated_label_answerable` as the final label field after disagreements are resolved.

Recommended failure types:

- `missing_evidence`: at least one perturbation lacks a necessary supporting fact or hop.
- `conflicting_evidence`: a perturbation contains evidence supporting the opposite answer or label.
- `distractor_only`: retrieved documents are topical but do not answer or verify the query.
- `ambiguous_question`: the query itself is underspecified or has multiple plausible readings.
- `label_error`: the generated expected label appears wrong.
- `insufficient_context`: the truncated audit text is not enough to decide.

Decision rule:

An orbit is answerable only when all evidence sets in the orbit are answerable. A single failed perturbation makes the orbit not answerable. This matches the CSRM claim: single-set sufficiency is not enough when counterfactual variants expose instability.

To regenerate annotation packs:

```powershell
$env:PYTHONPATH='D:\缝合RAG-idea\src;D:\缝合RAG-idea'
python experiments\export_audit_pack.py --input results\audit_sample_100_v3.jsonl --output-prefix results\audit_pack_100_v3
python experiments\export_audit_pack.py --input results\audit_sample_paper_1000_v3.jsonl --output-prefix results\audit_pack_paper_1000_v3
python experiments\export_audit_pack.py --input results\audit_sample_100_v3.jsonl --output-prefix results\audit_pack_100_v3_a1 --blind --annotator auditor1 --shuffle-seed 20260520
python experiments\export_audit_pack.py --input results\audit_sample_100_v3.jsonl --output-prefix results\audit_pack_100_v3_a2 --blind --annotator auditor2 --shuffle-seed 20260521
python experiments\export_audit_pack.py --input results\audit_sample_paper_1000_v3.jsonl --output-prefix results\audit_pack_paper_1000_v3_a1 --blind --annotator auditor1 --shuffle-seed 20260520
python experiments\export_audit_pack.py --input results\audit_sample_paper_1000_v3.jsonl --output-prefix results\audit_pack_paper_1000_v3_a2 --blind --annotator auditor2 --shuffle-seed 20260521
```

To merge edited CSV labels back into JSONL:

```powershell
python experiments\merge_audit_annotations.py --input results\audit_sample_100_v3.jsonl --labels-csv results\audit_pack_100_v3_a1.blind.labels.csv --output results\audit_sample_100_v3.a1.merged.jsonl
python experiments\merge_audit_annotations.py --input results\audit_sample_100_v3.a1.merged.jsonl --labels-csv results\audit_pack_100_v3_a2.blind.labels.csv --output results\audit_sample_100_v3.a1a2.merged.jsonl
python experiments\merge_audit_annotations.py --input results\audit_sample_paper_1000_v3.jsonl --labels-csv results\audit_pack_paper_1000_v3_a1.blind.labels.csv --output results\audit_sample_paper_1000_v3.a1.merged.jsonl
python experiments\merge_audit_annotations.py --input results\audit_sample_paper_1000_v3.a1.merged.jsonl --labels-csv results\audit_pack_paper_1000_v3_a2.blind.labels.csv --output results\audit_sample_paper_1000_v3.a1a2.merged.jsonl
```

Inspect the `.merged.jsonl` files before replacing the original audit files. The merge script intentionally rejects identical input/output paths to prevent accidental truncation.

After labeling, run:

```powershell
$env:PYTHONPATH='D:\缝合RAG-idea\src;D:\缝合RAG-idea'
python experiments\summarize_audit.py --input results\audit_sample_100_v3.jsonl --output results\audit_sample_100_v3_summary.json
python experiments\summarize_audit.py --input results\audit_sample_paper_1000_v3.jsonl --output results\audit_sample_paper_1000_v3_summary.json
python experiments\summarize_adjudication.py --input results\audit_sample_100_v3.jsonl --output results\audit_sample_100_v3_adjudication.json
python experiments\summarize_adjudication.py --input results\audit_sample_paper_1000_v3.jsonl --output results\audit_sample_paper_1000_v3_adjudication.json
python experiments\check_audit_readiness.py --input results\audit_sample_100_v3.jsonl --output results\audit_sample_100_v3_readiness.json --min-labeled-total 100 --min-labeled-per-split 10
python experiments\check_audit_readiness.py --input results\audit_sample_paper_1000_v3.jsonl --output results\audit_sample_paper_1000_v3_readiness.json --min-labeled-total 1000 --min-labeled-per-split 100
python experiments\check_audit_readiness.py --input results\audit_sample_100_v3.jsonl --output results\audit_sample_100_v3_adjudicated_readiness.json --min-labeled-total 100 --min-labeled-per-split 10 --label-field adjudicated_label_answerable
python experiments\check_audit_readiness.py --input results\audit_sample_paper_1000_v3.jsonl --output results\audit_sample_paper_1000_v3_adjudicated_readiness.json --min-labeled-total 1000 --min-labeled-per-split 100 --label-field adjudicated_label_answerable
```

Then recompute audited metrics:

```powershell
python experiments\evaluate_audited_orbits.py --input results\audit_sample_100_v3.jsonl --output results\audit_sample_100_v3_eval_audited.json
python experiments\evaluate_audited_orbits.py --input results\audit_sample_paper_1000_v3.jsonl --output results\audit_sample_paper_1000_v3_eval_audited.json
python experiments\evaluate_audited_orbits.py --input results\audit_sample_100_v3.jsonl --output results\audit_sample_100_v3_eval_adjudicated.json --label-field adjudicated_label_answerable
python experiments\evaluate_audited_orbits.py --input results\audit_sample_paper_1000_v3.jsonl --output results\audit_sample_paper_1000_v3_eval_adjudicated.json --label-field adjudicated_label_answerable
```

`evaluate_audited_orbits.py` ignores unlabeled records, rejects invalid labels, and uses the configured `--label-field` as the only evaluation label source. Do not report audited metrics until the labeled count is large enough for the intended claim.

`check_audit_readiness.py` is the gatekeeper for claim readiness. The audit is not paper-ready unless `ready` is `true`; failures include too few labels, too few labels in any split, invalid labels, or expected/auditor disagreements that lack both `auditor_failure_type` and `auditor_notes`.

Current status as of 2026-05-20:

- `results/audit_sample_100_v3_summary.json`: 0/100 labeled; readiness `ready=false`.
- `results/audit_sample_paper_1000_v3_summary.json`: 0/1,000 labeled; readiness `ready=false`.
- `results/audit_sample_100_v3_adjudication.json`: 0 double-labeled and 0 adjudicated.
- `results/audit_sample_paper_1000_v3_adjudication.json`: 0 double-labeled and 0 adjudicated.

Pilot minimum:

- 100 labeled orbits.
- Agreement with expected labels reported overall and by split.
- Every disagreement inspected and either corrected, excluded as ambiguous, or reported as a limitation.

Paper-ready minimum:

- 100 labeled orbits per stress split when using the current 10-split setup.
- Independent annotators use the blind packs; expected labels and model scores must remain hidden until adjudication.
- Final claim metrics use `adjudicated_label_answerable`, not a single annotator field.
- Per-split agreement and disagreement analysis.
- Double-label agreement and Cohen's kappa reported by `summarize_adjudication.py`.
- Every disagreement inspected and either corrected, excluded as ambiguous, or reported as a limitation.
- Final claims computed on audited labels, not on the heuristic bridge labels alone.
