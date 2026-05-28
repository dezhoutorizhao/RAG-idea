from experiments.build_hotpot_orbits_v4_support_preserving import _build_support_preserving_records


def test_support_preserving_wrong_answer_keeps_docs_and_changes_candidate_answer():
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

    rows = _build_support_preserving_records(item, local_idx=0, max_docs=4)

    assert [row["orbit_id"] for row in rows] == [
        "hotpot_supportpreserve:unit:stable",
        "hotpot_supportpreserve:unit:wrong_answer",
    ]
    stable_docs = [doc["doc_id"] for doc in rows[0]["perturbations"][0]["docs"]]
    wrong_docs = [doc["doc_id"] for doc in rows[1]["perturbations"][0]["docs"]]
    assert stable_docs == wrong_docs
    assert rows[0]["perturbations"][0]["answer"] == "Paris"
    assert rows[1]["perturbations"][0]["answer"] != "Paris"
    assert rows[1]["perturbations"][0]["label_answerable"] is False
