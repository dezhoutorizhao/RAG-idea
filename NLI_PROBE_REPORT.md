# NLI Set-Level Probe Report

Date: 2026-05-20

Purpose: test whether the CSRM signal survives when support/conflict/missing features are replaced by an independent set-level NLI model rather than the released CoRM-derived verifier features.

Model and command:

```powershell
python experiments\score_orbits_nli.py --input results\audit_sample_paper_1000_v3.jsonl --output results\audit_sample_paper_1000_v3_nli_set.jsonl --model cross-encoder/nli-deberta-v3-small --batch-size 32 --unit set --max-length 384
python experiments\evaluate_orbits.py --input results\audit_sample_paper_1000_v3_nli_set.jsonl --output results\audit_sample_paper_1000_v3_nli_set_eval.json --bootstrap-samples 500
```

Main result on the 1,000-row v3 paper-grade audit sample:

| method | AUROC | Risk@30 | AURC |
| --- | ---: | ---: | ---: |
| CSRM | 0.7353 | 0.6267 | 0.6676 |
| naive orbit average | 0.4880 | 0.8600 | 0.7959 |
| SURE-style single set | 0.4818 | 0.8700 | 0.8202 |
| shuffled perturbations | 0.3281 | 0.9367 | 0.8921 |
| CoRM max clean | 0.5244 | 0.7800 | 0.7838 |

Pilot result on the 100-row v3 audit sample:

| method | AUROC | Risk@30 | AURC |
| --- | ---: | ---: | ---: |
| CSRM | 0.7675 | 0.6000 | 0.6556 |
| naive orbit average | 0.5031 | 0.9000 | 0.7756 |
| SURE-style single set | 0.4766 | 0.9333 | 0.8281 |
| shuffled perturbations | 0.5172 | 0.8000 | 0.8004 |
| CoRM max clean | 0.5256 | 0.8000 | 0.7867 |

Interpretation:

- The CSRM ranking advantage is not tied only to the original CoRM-derived support/conflict/missing features.
- The shuffled-perturbation collapse persists, supporting the orbit-alignment mechanism.
- This is still not human-audited evidence. It should be framed as an automated cross-scorer sensitivity probe, not as primary ground-truth validation.

Artifacts:

- `results/audit_sample_100_v3_nli_set.jsonl`
- `results/audit_sample_100_v3_nli_set_eval.json`
- `results/audit_sample_paper_1000_v3_nli_set.jsonl`
- `results/audit_sample_paper_1000_v3_nli_set_eval.json`
