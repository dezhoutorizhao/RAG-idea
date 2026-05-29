from experiments.summarize_theory_formalization import (
    render_markdown,
    summarize_theory_formalization,
)


def test_summarize_theory_formalization_passes_with_required_sections(tmp_path):
    sections = tmp_path / "paper" / "sections"
    sections.mkdir(parents=True)
    (sections / "formalization.tex").write_text(
        "\\section{Formalization}\\label{sec:formalization}\n"
        "orbit risk, clean-only selector, single-set sufficiency, orbit alignment\n",
        encoding="utf-8",
    )
    (sections / "theory.tex").write_text(
        "\\section{Theory}\\label{sec:theory}\n"
        "\\label{prop:clean-not-orbit}\n"
        "\\label{prop:single-set-not-orbit}\n"
        "\\label{prop:orbit-alignment-necessary}\n"
        "Scope and non-claims\n",
        encoding="utf-8",
    )

    summary = summarize_theory_formalization(tmp_path)

    assert summary["theory_module_ready"] is True
    assert summary["all_labels_present"] is True
    assert summary["all_concepts_present"] is True


def test_render_markdown_lists_claim_boundary(tmp_path):
    sections = tmp_path / "paper" / "sections"
    sections.mkdir(parents=True)
    (sections / "formalization.tex").write_text("", encoding="utf-8")
    (sections / "theory.tex").write_text("", encoding="utf-8")

    text = render_markdown(summarize_theory_formalization(tmp_path))

    assert "Theory Formalization Status" in text
    assert "does not prove empirical all-win behavior" in text
