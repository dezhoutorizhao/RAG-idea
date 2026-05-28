import pytest

from csrm_rag.feature_firewall import assert_no_forbidden_features, strip_forbidden_features


def test_firewall_rejects_nested_oracle_fields():
    payload = {"orbit": {"docs": [{"text": "x", "is_support": True}]}}
    with pytest.raises(ValueError, match="is_support"):
        assert_no_forbidden_features(payload)


def test_firewall_allows_text_only_visible_fields():
    assert_no_forbidden_features(
        {
            "orbit_id": "o1",
            "query": "question",
            "candidate_answer": "answer",
            "clean_evidence": [{"doc_id": "d1", "text": "visible", "retrieval_score": 0.3}],
        }
    )


def test_strip_forbidden_features_removes_nested_keys():
    payload = {
        "doc_id": "d1",
        "text": "visible",
        "gold_answer": "hidden",
        "metadata": {"support_key": "hidden", "source": "visible"},
    }
    assert strip_forbidden_features(payload) == {
        "doc_id": "d1",
        "text": "visible",
        "metadata": {"source": "visible"},
    }
