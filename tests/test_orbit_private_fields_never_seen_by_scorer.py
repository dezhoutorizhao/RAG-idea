import json

from csrm_rag.feature_firewall import assert_no_forbidden_features
from csrm_rag.orbit_v4 import legacy_orbit_to_v4, validate_v4_pair


def test_legacy_orbit_to_v4_splits_raw_and_private_fields(tmp_path):
    legacy = {
        "orbit_id": "hotpot:item1:missing_hop",
        "clean": {
            "query": "q",
            "answer": "a",
            "label_answerable": True,
            "split": "hidden",
            "metadata": {"support_key": "hidden", "perturbation_type": "clean"},
            "docs": [
                {
                    "doc_id": "d1",
                    "title": "D1",
                    "text": "visible",
                    "rank": 0,
                    "corm_score": 0.8,
                    "support": 0.9,
                    "is_support": True,
                }
            ],
        },
        "perturbations": [
            {
                "query": "q2",
                "answer": "a",
                "label_answerable": False,
                "metadata": {"support_key": "hidden2", "perturbation_type": "missing"},
                "docs": [{"doc_id": "d2", "title": "D2", "text": "visible2", "rank": 0}],
            }
        ],
    }
    raw, private = legacy_orbit_to_v4(legacy, "hotpot")

    assert_no_forbidden_features(raw)
    assert private["label_answerable"] is False
    assert private["support_key"] == "hidden"
    assert "support" not in raw["clean_evidence"][0]

    raw_path = tmp_path / "raw.jsonl"
    private_path = tmp_path / "private.jsonl"
    raw_path.write_text(json.dumps(raw) + "\n", encoding="utf-8")
    private_path.write_text(json.dumps(private) + "\n", encoding="utf-8")
    summary = validate_v4_pair(raw_path, private_path)
    assert summary["leakage_free_raw"] is True
    assert summary["orbits"] == 1
