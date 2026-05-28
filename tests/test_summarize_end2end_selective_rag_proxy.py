import json

from experiments.summarize_end2end_selective_rag_proxy import (
    render_markdown,
    summarize_end2end_selective_rag_proxy,
)


def test_summarize_end2end_proxy_counts_mixed_results(tmp_path):
    path = tmp_path / "end2end_toy_proxy.json"
    _write_json(path, _payload())

    summary = summarize_end2end_selective_rag_proxy([path])

    assert summary["aggregate"]["row_count"] == 2
    assert summary["aggregate"]["risk30_wins"] == 1
    assert summary["aggregate"]["risk30_losses"] == 1
    assert summary["aggregate"]["all_win"] is False
    assert summary["aggregate"]["has_losses"] is True
    assert "not all-win" in summary["claim_implication"]


def test_render_markdown_includes_proxy_limitations(tmp_path):
    path = tmp_path / "end2end_toy_proxy.json"
    _write_json(path, _payload())

    summary = summarize_end2end_selective_rag_proxy([path])
    text = render_markdown(summary)

    assert "End-to-End Selective RAG Proxy Summary" in text
    assert "copy_candidate" in text
    assert "not a full CoRM-RAG" in text


def _payload():
    return {
        "n": 10,
        "results": {
            "copy_candidate": {
                "answer_accuracy": 0.5,
                "methods": {
                    "csrm": _metrics(0.1, 0.2, 0.25, 0.4),
                    "naive_orbit_average": _metrics(0.3, 0.4, 0.5, 0.2),
                    "corm_max_clean": _metrics(0.4, 0.4, 0.45, 0.1),
                },
            },
            "lexical_guarded": {
                "answer_accuracy": 0.5,
                "methods": {
                    "csrm": _metrics(0.4, 0.3, 0.35, 0.2),
                    "naive_orbit_average": _metrics(0.2, 0.3, 0.30, 0.2),
                    "corm_max_clean": _metrics(0.5, 0.4, 0.50, 0.1),
                },
            },
        },
    }


def _metrics(risk30, risk50, aurc, cov20):
    return {
        "accepted_error_at_30": {"risk": risk30},
        "accepted_error_at_50": {"risk": risk50},
        "accepted_error_at_70": {"risk": risk50},
        "coverage_at_risk_20": {"coverage": cov20},
        "aurc": aurc,
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
