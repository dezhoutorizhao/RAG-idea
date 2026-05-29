# FEVER CP Transfer Sweep

Generated: `2026-05-29T05:36:54.263946+00:00`

Dataset: `FEVER v3 near-miss CoRM 1200`
Primary method: `csrm_logreg_calibrated`

## Target Sweep

| Risk target | Method | Target met | Misses | Test risk mean | Test risk max | Test coverage mean | Transfer supported |
|---:|---|---:|---:|---:|---:|---:|---|
| 0.2000 | csrm_logreg_calibrated | 1/3 | 2 | 0.1866 | 0.2593 | 0.2069 | `False` |
| 0.2000 | csrm_fixed_weights | 1/3 | 2 | 0.2019 | 0.3220 | 0.2139 | `False` |
| 0.2500 | csrm_logreg_calibrated | 1/3 | 2 | 0.2137 | 0.2857 | 0.2153 | `False` |
| 0.2500 | csrm_fixed_weights | 1/3 | 2 | 0.2306 | 0.3220 | 0.2222 | `False` |
| 0.3000 | csrm_logreg_calibrated | 1/3 | 2 | 0.2449 | 0.3333 | 0.2250 | `False` |
| 0.3000 | csrm_fixed_weights | 1/3 | 2 | 0.2379 | 0.3220 | 0.2236 | `False` |
| 0.3500 | csrm_logreg_calibrated | 3/3 | 0 | 0.2562 | 0.3443 | 0.2292 | `True` |
| 0.3500 | csrm_fixed_weights | 3/3 | 0 | 0.2379 | 0.3220 | 0.2236 | `True` |

## Boundary

The primary method first passes all observed seeds at risk target `0.3500` with max test empirical risk `0.3443`.

Failures at risk target `0.2000`:

| Seed | Accepted | Coverage | Errors | Empirical risk | Risk excess |
|---:|---:|---:|---:|---:|---:|
| 31 | 54 | 0.2250 | 14 | 0.2593 | 0.0593 |
| 47 | 52 | 0.2167 | 12 | 0.2308 | 0.0308 |

## Claim Implication

FEVER near-miss is negative evidence for the 0.20 empirical risk-transfer claim: the primary method misses at 0.20 and only passes all observed seeds after relaxing the target to 0.3500. This should be reported as a boundary condition, not as a NeurIPS-level main risk-control result.

This diagnostic sweeps the empirical risk target while keeping the same FEVER near-miss input, split seeds, train/calibration fractions, alpha, and minimum-acceptance rule. It is an empirical transfer stress test, not a distribution-free guarantee.
