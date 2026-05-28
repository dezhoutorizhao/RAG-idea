from experiments.build_hotpot_orbits_v4_semantic_swap import _build_semantic_swap_records


def test_semantic_swap_keeps_answer_and_doc_ids_but_changes_evidence_text():
    item = {
        "id": "unit",
        "question": "Which city hosts the river festival founded by Ada?",
        "answer": "Paris",
        "context": {
            "title": ["Ada", "Festival", "Berlin", "Lyon", "Music", "Food"],
            "sentences": [
                ["Ada founded the River Light Festival."],
                ["The River Light Festival is hosted in Paris."],
                ["Berlin is mentioned as background."],
                ["Lyon has another river event."],
                ["Music festivals often use city parks."],
                ["Food events happen near rivers."],
            ],
        },
        "supporting_facts": {"title": ["Ada", "Festival"], "sent_id": [0, 0]},
    }

    rows = _build_semantic_swap_records(item, local_idx=0, max_docs=4)

    assert [row["orbit_id"] for row in rows] == [
        "hotpot_semanticswap:unit:stable",
        "hotpot_semanticswap:unit:semantic_swap",
    ]
    stable = rows[0]["perturbations"][0]
    swapped = rows[1]["perturbations"][0]
    assert stable["answer"] == swapped["answer"] == "Paris"
    assert [doc["doc_id"] for doc in stable["docs"]] == [doc["doc_id"] for doc in swapped["docs"]]
    assert "Paris" in " ".join(doc["text"] for doc in stable["docs"])
    assert "Paris" not in " ".join(doc["text"] for doc in swapped["docs"])
    assert swapped["label_answerable"] is False
