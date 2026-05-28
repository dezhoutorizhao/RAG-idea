from experiments.build_hotpot_orbits_v4_hardneg import _build_hard_negative_records


def test_build_hard_negative_records_pairs_stable_with_one_hop_removed_negative():
    item = {
        "id": "unit",
        "question": "Which city hosts the river festival founded by Ada?",
        "answer": "Paris",
        "context": {
            "title": ["Ada", "Festival", "Paris guide", "River note", "Music", "Food", "Travel"],
            "sentences": [
                ["Ada founded the River Light Festival."],
                ["The River Light Festival is hosted in Paris."],
                ["Paris is a city with river festivals."],
                ["A river note mentions Paris events."],
                ["Music festivals often use city parks."],
                ["Food events happen near rivers."],
                ["Travel guides describe Paris."],
            ],
        },
        "supporting_facts": {"title": ["Ada", "Festival"], "sent_id": [0, 0]},
    }

    rows = _build_hard_negative_records(item, local_idx=0, max_docs=4, candidate_pool=5)

    assert [row["orbit_id"] for row in rows] == [
        "hotpot_hardneg:unit:stable",
        "hotpot_hardneg:unit:hard_missing_hop",
    ]
    stable_docs = rows[0]["perturbations"][0]["docs"]
    negative_docs = rows[1]["perturbations"][0]["docs"]
    assert len(stable_docs) == len(negative_docs) == 4
    assert rows[0]["perturbations"][0]["label_answerable"] is True
    assert rows[1]["perturbations"][0]["label_answerable"] is False
    stable_supports = {doc["title"] for doc in stable_docs if doc["support"] > 0.8}
    negative_supports = {doc["title"] for doc in negative_docs if doc["support"] > 0.8}
    assert stable_supports == {"Ada", "Festival"}
    assert len(negative_supports) == 1
