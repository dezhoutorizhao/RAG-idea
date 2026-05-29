import json

from experiments.summarize_text_only_verifier_status import (
    render_markdown,
    summarize_text_only_verifier_status,
)


def test_text_only_verifier_status_tracks_nli_pass_and_missing_llm_scores(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    _write_json(results / "audit_sample_paper_1000_v3_nli_set_eval.json", _nli_eval())
    (results / "audit_sample_paper_1000_v3_nli_set.jsonl").write_text("{}\n", encoding="utf-8")
    _write_json(
        results / "llm_judge_v4_request_status_20260529.json",
        {
            "request_pack_ready": True,
            "request_count": 1200,
            "score_artifact_ready": False,
        },
    )
    _write_json(
        results / "llm_judge_nli_probe_request_status_20260529.json",
        {
            "request_pack_ready": True,
            "paired_to_nli_probe": True,
            "request_count": 1000,
            "score_artifact_ready": False,
        },
    )
    _write_json(
        results / "llm_judge_nli_probe_score_status_20260529.json",
        {
            "status": "blocked",
            "blocker_reason": "missing_or_empty_batch_output_artifact",
            "parsed_score_count": 0,
        },
    )
    _write_json(
        results / "llm_nli_correlation_status_20260529.json",
        {
            "status": "blocked",
            "blocker_reason": "missing_or_empty_llm_score_artifact",
            "ready_for_nli_llm_correlation_claim": False,
        },
    )
    _write_json(results / "human_audit_v4_status_20260529.json", {"ready": False, "pending": 300})

    summary = summarize_text_only_verifier_status(tmp_path)

    assert summary["nli_probe"]["directional_advantage_ready"] is True
    assert len(summary["nli_probe"]["required_baseline_comparisons"]) == 4
    assert summary["llm_judge"]["request_pack_ready"] is True
    assert summary["llm_judge"]["paired_request_pack_ready"] is True
    assert summary["llm_judge"]["paired_request_count"] == 1000
    assert summary["llm_judge"]["paired_score_status"] == "blocked"
    assert summary["llm_judge"]["correlation_status"] == "blocked"
    assert summary["llm_judge"]["nli_llm_correlation_ready"] is False
    assert summary["ready_for_text_only_main_claim"] is False
    statuses = {item["criterion"]: item["status"] for item in summary["success_criteria"]}
    assert statuses["NLI/text-only scorer beats required weak baselines"] == "pass"
    assert statuses["LLM judge and NLI ranking correlation"] == "blocked"
    assert statuses["Human-label text-only CSRM evaluation"] == "blocked"


def test_text_only_verifier_markdown_lists_comparisons(tmp_path):
    results = tmp_path / "results"
    results.mkdir()
    _write_json(results / "audit_sample_paper_1000_v3_nli_set_eval.json", _nli_eval())
    (results / "audit_sample_paper_1000_v3_nli_set.jsonl").write_text("{}\n", encoding="utf-8")
    _write_json(results / "llm_judge_v4_request_status_20260529.json", {"request_pack_ready": True})
    _write_json(
        results / "llm_judge_nli_probe_request_status_20260529.json",
        {"request_pack_ready": True, "paired_to_nli_probe": True, "request_count": 1000},
    )
    _write_json(
        results / "llm_judge_nli_probe_score_status_20260529.json",
        {
            "status": "blocked",
            "blocker_reason": "missing_or_empty_batch_output_artifact",
            "parsed_score_count": 0,
        },
    )
    _write_json(
        results / "llm_nli_correlation_status_20260529.json",
        {
            "status": "blocked",
            "blocker_reason": "missing_or_empty_llm_score_artifact",
            "ready_for_nli_llm_correlation_claim": False,
        },
    )
    _write_json(results / "human_audit_v4_status_20260529.json", {"ready": False})

    text = render_markdown(summarize_text_only_verifier_status(tmp_path))

    assert "Text-Only Verifier Status" in text
    assert "naive_orbit_average" in text
    assert "NLI-paired request pack ready: `True`" in text
    assert "Paired score normalization status: `blocked`" in text
    assert "Correlation status: `blocked`" in text
    assert "NLI/LLM correlation ready: `False`" in text


def _nli_eval():
    def row(auroc, risk, aurc):
        return {
            "auroc": auroc,
            "aurc": aurc,
            "n": 1000,
            "risk_at_30_coverage": {"risk": risk},
        }

    return {
        "summary": {
            "csrm": row(0.7353, 0.6267, 0.6676),
            "naive_orbit_average": row(0.4880, 0.8600, 0.7959),
            "single_set_sure_style": row(0.4818, 0.8700, 0.8202),
            "corm_max_clean": row(0.5244, 0.7800, 0.7838),
            "corm_mean_clean": row(0.5189, 0.7900, 0.7869),
        }
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
