from csrm_rag import (
    CSRMWeights,
    EvidenceDoc,
    EvidenceSet,
    QueryOrbit,
    corm_max_score,
    csrm_components,
    csrm_score,
    naive_orbit_sufficiency,
    single_set_sufficiency,
)


def _doc(doc_id, support, conflict=0.0, missing=0.0, corm=0.9):
    return EvidenceDoc(
        doc_id=doc_id,
        text=doc_id,
        corm_score=corm,
        support=support,
        conflict=conflict,
        missing=missing,
    )


def _set(split, docs, label=True, support_key="gold"):
    return EvidenceSet(
        query=f"{split} query",
        answer="answer",
        docs=docs,
        label_answerable=label,
        split=split,
        metadata={"support_key": support_key},
    ).normalized()


def test_single_set_sufficiency_penalizes_conflict_and_missingness():
    supported = _set("supported", [_doc("a", 0.9), _doc("b", 0.7)])
    conflicted = _set("conflicted", [_doc("a", 0.9, conflict=0.9), _doc("b", 0.3, missing=0.8)])
    assert single_set_sufficiency(supported) > single_set_sufficiency(conflicted)


def test_csrm_components_detect_answer_inconsistency_and_overlap():
    clean = _set("clean", [_doc("a", 0.9), _doc("b", 0.7)], support_key="gold")
    perturbation = _set("perturbed", [_doc("x", 0.9), _doc("y", 0.7)], support_key="false")
    components = csrm_components(QueryOrbit("o1", clean, [perturbation]))
    assert components.answer_consistency == 0.0
    assert components.overlap == 0.0
    assert components.worst_sufficiency <= components.mean_sufficiency


def test_csrm_penalizes_single_failed_perturbation_more_than_naive_average():
    clean = _set("clean", [_doc("a", 0.9)], support_key="gold")
    stable = _set("stable", [_doc("a", 0.9)], support_key="gold")
    failed = _set("failed", [_doc("x", 0.2, conflict=0.8, missing=0.5)], support_key="false")
    orbit = QueryOrbit("o1", clean, [stable, failed])

    assert csrm_components(orbit).worst_sufficiency < naive_orbit_sufficiency(orbit)
    assert csrm_score(orbit) < naive_orbit_sufficiency(orbit)


def test_csrm_score_can_ablate_answer_consistency():
    clean = _set("clean", [_doc("a", 0.9), _doc("b", 0.7)], support_key="gold")
    perturbation = _set("perturbed", [_doc("a", 0.9), _doc("b", 0.7)], support_key="false")
    orbit = QueryOrbit("o1", clean, [perturbation])
    full = csrm_score(orbit)
    ablated = csrm_score(orbit, CSRMWeights(answer_consistency=0.0))
    assert ablated > full


def test_query_orbit_label_requires_all_sets_answerable():
    clean = _set("clean", [_doc("a", 0.9)], label=True)
    bad_perturbation = _set("perturbed", [_doc("a", 0.9)], label=False)
    orbit = QueryOrbit("o1", clean, [bad_perturbation])
    assert orbit.label_answerable is False


def test_corm_and_naive_scores_are_defined_for_basic_orbit():
    clean = _set("clean", [_doc("a", 0.9, corm=0.8)])
    perturbation = _set("perturbed", [_doc("a", 0.6, corm=0.7)])
    orbit = QueryOrbit("o1", clean, [perturbation])
    assert corm_max_score(clean) == 0.8
    assert naive_orbit_sufficiency(orbit) > 0.0
