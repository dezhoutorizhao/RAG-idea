import json
from dataclasses import asdict

from experiments.run_toy_pilot import generate_orbits
from experiments.summarize_calibration_seeds import (
    run_calibration_seeds,
    summarize_calibration_files,
)


def test_run_calibration_seeds_reports_target_transfer(tmp_path):
    path = tmp_path / "orbits.jsonl"
    rows = [_orbit_to_dict(orbit) for orbit in generate_orbits(n_per_split=18, seed=3)]
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    result = run_calibration_seeds(
        path,
        [11, 13],
        train_frac=0.5,
        cal_frac=0.25,
        risk_target=0.4,
        methods=["csrm_fixed_weights"],
    )

    assert result["n_seeds"] == 2
    assert result["aggregate"]["csrm_fixed_weights"]["target_met_count"] >= 0
    assert "risk_excess_over_target" in result["aggregate"]["csrm_fixed_weights"]


def test_summarize_calibration_files_aggregates_existing_outputs(tmp_path):
    first = tmp_path / "a.json"
    second = tmp_path / "b.json"
    for path, risk in [(first, 0.1), (second, 0.3)]:
        path.write_text(
            json.dumps(
                {
                    "risk_target": 0.2,
                    "methods": {
                        "m": {
                            "test": {
                                "auroc": 0.9,
                                "aurc": 0.4,
                                "risk_at_30_coverage": {"risk": 0.25},
                                "calibrated_threshold": 0.7,
                                "calibrated_coverage": 0.5,
                                "calibrated_risk": risk,
                                "calibrated_accuracy": 1.0 - risk,
                            }
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

    result = summarize_calibration_files([first, second], methods=["m"])

    assert result["aggregate"]["m"]["calibrated_risk"]["mean"] == 0.2
    assert result["aggregate"]["m"]["target_met_count"] == 1
    assert result["aggregate"]["m"]["formal_risk_guarantee_supported"] is False


def test_summarize_calibration_files_rejects_vacuous_zero_coverage_guarantee(tmp_path):
    first = tmp_path / "a.json"
    first.write_text(
        json.dumps(
            {
                "risk_target": 0.2,
                "methods": {
                    "m": {
                        "test": {
                            "auroc": 0.5,
                            "aurc": 0.5,
                            "risk_at_30_coverage": {"risk": 0.8},
                            "calibrated_threshold": 1.0,
                            "calibrated_coverage": 0.0,
                            "calibrated_risk": 0.0,
                            "calibrated_accuracy": 0.0,
                        }
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    result = summarize_calibration_files([first], methods=["m"])

    assert result["aggregate"]["m"]["target_met_count"] == 1
    assert result["aggregate"]["m"]["zero_coverage_count"] == 1
    assert result["aggregate"]["m"]["formal_risk_guarantee_supported"] is False


def _orbit_to_dict(orbit):
    return {
        "orbit_id": orbit.orbit_id,
        "clean": _set_to_dict(orbit.clean),
        "perturbations": [_set_to_dict(item) for item in orbit.perturbations],
    }


def _set_to_dict(evidence_set):
    return {
        "query": evidence_set.query,
        "answer": evidence_set.answer,
        "label_answerable": evidence_set.label_answerable,
        "split": evidence_set.split,
        "metadata": evidence_set.metadata,
        "docs": [asdict(doc) for doc in evidence_set.docs],
    }
