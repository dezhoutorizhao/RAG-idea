import json

from experiments.summarize_v4_anti_shortcut import render_markdown, summarize_v4_anti_shortcut


def test_summarize_v4_anti_shortcut_aggregates_passed_suite(tmp_path):
    first = tmp_path / "first.anti_shortcut.json"
    second = tmp_path / "second.anti_shortcut.json"
    _write_json(first, _payload(0.51, 0.49, True))
    _write_json(second, _payload(0.53, 0.52, True))

    summary = summarize_v4_anti_shortcut([first, second])

    assert summary["dataset_count"] == 2
    assert summary["aggregate"]["all_raw_firewall_passed"] is True
    assert summary["aggregate"]["all_structural_only_passed_0_55"] is True
    assert summary["aggregate"]["all_group_split_no_overlap"] is True
    assert summary["aggregate"]["random_label_median_all_near_half"] is True
    assert summary["aggregate"]["pass_core_anti_shortcut_suite"] is True
    assert summary["aggregate"]["private_metadata_upper_bound_all_high"] is True


def test_render_markdown_includes_private_metadata_boundary(tmp_path):
    path = tmp_path / "demo.anti_shortcut.json"
    _write_json(path, _payload(0.51, 0.49, True))

    text = render_markdown(summarize_v4_anti_shortcut([path]))

    assert "V4 Anti-Shortcut Summary" in text
    assert "Core anti-shortcut suite passed" in text
    assert "evaluator-only" in text


def _payload(max_structural, random_median, group_passed):
    return {
        "n": 10,
        "positive": 5,
        "negative": 5,
        "raw_firewall_passed": True,
        "structural_only_probe": {
            "max_single_feature_auroc": max_structural,
            "passed_0_55_threshold": max_structural <= 0.55,
        },
        "random_label_sanity": {
            "auroc": {
                "median": random_median,
                "p2_5": 0.42,
                "p97_5": 0.58,
            }
        },
        "group_split_probe": {
            "n_groups": 5,
            "passed_no_group_overlap": group_passed,
        },
        "private_metadata_leakage_upper_bound": {
            "construction_type_oriented_auroc": 1.0,
        },
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
