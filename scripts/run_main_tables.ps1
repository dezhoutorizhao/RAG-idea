$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"

python -m experiments.reproduce_current_evidence_v4 `
  --output-json results\current_evidence_reproduction_20260529.json `
  --output-md results\current_evidence_reproduction_20260529.md

python -m experiments.verify_v4_evidence_package `
  --output-json results\v4_evidence_package_manifest_20260529.json `
  --output-md results\v4_evidence_package_manifest_20260529.md

python -m experiments.summarize_neurips_readiness `
  --output-json results\neurips_readiness_matrix_20260529.json `
  --output-md results\neurips_readiness_matrix_20260529.md

python -m experiments.verify_v4_evidence_package `
  --output-json results\v4_evidence_package_manifest_20260529.json `
  --output-md results\v4_evidence_package_manifest_20260529.md

python -m experiments.verify_claims `
  --output results\claims_verification.json

python -m experiments.build_claims_ledger_markdown `
  --output-md CLAIMS_LEDGER.md `
  --output-json results\claims_ledger_markdown_summary_20260529.json

python -m experiments.build_results_provenance_readme `
  --output-json results\results_provenance_manifest_20260529.json `
  --output-md results\README.md

python -m experiments.build_reproducibility_bundle

python -m experiments.summarize_evidence_closure `
  --output-json results\evidence_closure_status_v4.json `
  --output-md results\evidence_closure_status_v4.md

python -m experiments.verify_v4_evidence_package `
  --output-json results\v4_evidence_package_manifest_20260529.json `
  --output-md results\v4_evidence_package_manifest_20260529.md
