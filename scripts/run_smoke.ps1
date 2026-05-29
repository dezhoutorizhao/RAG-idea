$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
python -m pytest `
  tests/test_build_results_provenance_readme.py `
  tests/test_build_reproducibility_bundle.py `
  tests/test_verify_v4_evidence_package.py `
  -q
