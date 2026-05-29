$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
python -m pytest `
  tests/test_build_results_provenance_readme.py `
  tests/test_build_claims_ledger_markdown.py `
  tests/test_build_reproducibility_bundle.py `
  tests/test_compute_llm_nli_correlation.py `
  tests/test_compare_equal_budget_thresholds_v4.py `
  tests/test_materialize_llm_judge_requests_v4.py `
  tests/test_materialize_llm_judge_requests_nli_probe.py `
  tests/test_run_end2end_retriever_generator_matrix_v4.py `
  tests/test_summarize_human_audit_v4_disagreements.py `
  tests/test_summarize_human_audit_v4_mismatch.py `
  tests/test_summarize_text_only_verifier_status.py `
  tests/test_summarize_v4_baseline_budget_parity.py `
  tests/test_summarize_v4_baseline_coverage.py `
  tests/test_summarize_v4_split_threshold_protocol.py `
  tests/test_verify_v4_evidence_package.py `
  -q
