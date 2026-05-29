# Reproduction Commands

## Smoke Test

```powershell
.\scripts\run_smoke.ps1
```

Equivalent command:

```powershell
$env:PYTHONPATH='src'; python -m pytest tests/test_build_results_provenance_readme.py tests/test_build_claims_ledger_markdown.py tests/test_build_reproducibility_bundle.py tests/test_verify_v4_evidence_package.py -q
```

## Main Current-Evidence Tables

```powershell
.\scripts\run_main_tables.ps1
```

This rebuilds the current evidence package, provenance README, reproducibility bundle, and evidence manifest. It does not fabricate human labels or complete full CoRM-RAG reproduction.
