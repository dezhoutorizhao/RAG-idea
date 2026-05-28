from experiments.train_calibrated_csrm import group_split, train_and_evaluate
from experiments.run_toy_pilot import generate_orbits


def test_group_split_keeps_orbits_from_same_base_together():
    orbits = generate_orbits(n_per_split=4, seed=1)
    split = group_split(orbits, train_frac=0.5, cal_frac=0.25, seed=3)
    group_membership = {}
    for name in ["train", "calibration", "test"]:
        for orbit in split[name]:
            group_id = orbit.orbit_id
            assert group_id not in group_membership
            group_membership[group_id] = name


def test_train_and_evaluate_outputs_held_out_methods():
    orbits = generate_orbits(n_per_split=20, seed=2)
    result = train_and_evaluate(
        orbits,
        train_frac=0.5,
        cal_frac=0.25,
        seed=5,
        risk_target=0.4,
    )
    assert result["split_sizes"]["test"] > 0
    assert "csrm_logreg_calibrated" in result["methods"]
    assert "test" in result["methods"]["csrm_logreg_calibrated"]
    assert result["methods"]["csrm_logreg_calibrated"]["test"]["auroc"] is not None
