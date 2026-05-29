import json

from experiments.summarize_mechanism_ablation import (
    render_markdown,
    summarize_mechanism_ablation,
)


def test_summarize_mechanism_ablation_computes_deltas(tmp_path):
    path = tmp_path / "summary.json"
    _write_json(
        path,
        {
            "aggregate": {
                "csrm": _method(0.9, 0.1, 0.2, 0.2),
                "csrm_shuffled_perturbations": _method(0.1, 0.9, 0.8, 0.9),
                "csrm_no_answer_consistency": _method(0.8, 0.2, 0.3, 0.3),
            }
        },
    )

    summary = summarize_mechanism_ablation([path])

    shuffled = summary["aggregate"]["by_method"]["csrm_shuffled_perturbations"]
    assert shuffled["auroc_drop_mean"] == 0.8
    assert shuffled["risk30_increase_mean"] == 0.8
    assert shuffled["strong_mechanism_evidence"] is True
    no_answer = summary["aggregate"]["by_method"]["csrm_no_answer_consistency"]
    assert no_answer["strong_mechanism_evidence"] is True


def test_render_markdown_mentions_weak_component_boundary(tmp_path):
    path = tmp_path / "summary.json"
    _write_json(
        path,
        {
            "aggregate": {
                "csrm": _method(0.9, 0.1, 0.2, 0.2),
                "csrm_no_worst_sufficiency": _method(0.91, 0.1, 0.2, 0.19),
            }
        },
    )

    text = render_markdown(summarize_mechanism_ablation([path]))

    assert "Mechanism Ablation Summary" in text
    assert "weak or redundant" in text
    assert "csrm_no_worst_sufficiency" in text


def _method(auroc, risk30, risk50, aurc):
    return {
        "auroc": {"mean": auroc},
        "risk_at_30": {"mean": risk30},
        "risk_at_50": {"mean": risk50},
        "aurc": {"mean": aurc},
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
