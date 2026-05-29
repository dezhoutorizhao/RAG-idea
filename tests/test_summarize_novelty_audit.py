from experiments.summarize_novelty_audit import render_markdown, summarize_novelty_audit


def test_summarize_novelty_audit_keeps_cautious_boundary():
    summary = summarize_novelty_audit()

    assert summary["recommendation"] == "proceed_with_caution"
    assert summary["novelty_ready_for_strong_claim"] is False
    assert any("SURE-RAG" in row["paper"] for row in summary["closest_prior_work"])
    assert any("CoRM-RAG" in row["closest_prior"] for row in summary["core_claims"])


def test_render_markdown_lists_prior_work_links():
    text = render_markdown(summarize_novelty_audit())

    assert "Novelty Audit Update" in text
    assert "https://arxiv.org/abs/2605.01302" in text
    assert "Ready for strong novelty claim: `False`" in text
