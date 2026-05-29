$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
python -m pytest `
  tests/test_build_results_provenance_readme.py `
  tests/test_build_claims_ledger_markdown.py `
  tests/test_build_reproducibility_bundle.py `
  tests/test_summarize_human_audit_v4_disagreements.py `
  tests/test_summarize_human_audit_v4_mismatch.py `
  tests/test_summarize_v4_baseline_coverage.py `
  tests/test_verify_v4_evidence_package.py `
  -q
