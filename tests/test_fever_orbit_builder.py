from experiments.build_fever_orbits import _build_records


def test_fever_missing_split_omits_single_gold_doc():
    item = {
        "id": "claim-1",
        "claim": "A claim.",
        "label": "SUPPORTS",
        "evidence": [["Gold_Page", 1, "Gold evidence sentence."]],
    }
    pools = {
        "SUPPORTS": [
            {
                "doc_id": "Other_Support:1",
                "title": "Other Support",
                "text": "Other support.",
                "label": "SUPPORTS",
                "retrieval_score": 0.0,
            }
        ],
        "REFUTES": [
            {
                "doc_id": "Refute_Page:1",
                "title": "Refute Page",
                "text": "Refuting evidence.",
                "label": "REFUTES",
                "retrieval_score": 0.0,
            }
        ],
        "all": [
            {
                "doc_id": "Distractor_Page:1",
                "title": "Distractor Page",
                "text": "Background evidence.",
                "label": "REFUTES",
                "retrieval_score": 0.0,
            },
            {
                "doc_id": "Refute_Page:1",
                "title": "Refute Page",
                "text": "Refuting evidence.",
                "label": "REFUTES",
                "retrieval_score": 0.0,
            },
        ],
    }

    records = _build_records(item, pools, 0)
    missing = next(record for record in records if record["orbit_id"].endswith(":missing"))

    missing_doc_ids = {
        doc["doc_id"] for doc in missing["perturbations"][0]["docs"]
    }
    assert "Gold_Page:1" not in missing_doc_ids
