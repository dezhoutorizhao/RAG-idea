import json
import math
from dataclasses import asdict

from experiments.evaluate_risk_control_cp import (
    clopper_pearson_upper_bound,
    evaluate_threshold,
    run_risk_control_seeds,
    select_threshold_with_cp_bound,
)
from experiments.run_toy_pilot import generate_orbits


def test_clopper_pearson_upper_bound_handles_zero_errors():
    upper = clopper_pearson_upper_bound(errors=0, n=10, alpha=0.1)

    assert math.isclose(upper, 1.0 - 0.1 ** 0.1)


def test_clopper_pearson_upper_bound_increases_with_errors():
    lower = clopper_pearson_upper_bound(errors=0, n=20, alpha=0.1)
    higher = clopper_pearson_upper_bound(errors=2, n=20, alpha=0.1)

    assert lower < higher


def test_select_threshold_respects_tied_scores():
    selection = select_threshold_with_cp_bound(
        [0.9, 0.9, 0.8, 0.1],
        [True, True, False, False],
        risk_target=0.6,
        alpha=0.2,
        min_accepts=1,
    )

    assert selection["threshold"] == 0.9
    assert selection["accepted"] == 2
    assert selection["errors"] == 0
    assert selection["cp_feasible"] is True


def test_evaluate_threshold_marks_vacuous_selection_as_not_met():
    result = evaluate_threshold([0.1, 0.2], [True, False], None, risk_target=0.2)

    assert result["coverage"] == 0.0
    assert result["empirical_risk"] is None
    assert result["target_met"] is False


def test_run_risk_control_seeds_reports_empirical_transfer(tmp_path):
    path = tmp_path / "orbits.jsonl"
    rows = [_orbit_to_dict(orbit) for orbit in generate_orbits(n_per_split=24, seed=4)]
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

    result = run_risk_control_seeds(
        path,
        [11, 13],
        train_frac=0.5,
        cal_frac=0.25,
        risk_target=0.5,
        alpha=0.2,
        min_accepts=2,
        methods=["csrm_fixed_weights"],
    )

    summary = result["aggregate"]["csrm_fixed_weights"]
    assert result["n_seeds"] == 2
    assert "calibration_cp_upper_bound" in summary
    assert summary["formal_risk_guarantee_supported"] is False


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
