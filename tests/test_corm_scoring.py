from experiments.score_orbits_corm import _iter_docs, _load_records


def test_load_records_respects_max_orbits(tmp_path):
    path = tmp_path / "orbits.jsonl"
    path.write_text(
        "\n".join(
            [
                '{"orbit_id":"a","clean":{"query":"q1","docs":[]}}',
                '{"orbit_id":"b","clean":{"query":"q2","docs":[]}}',
            ]
        ),
        encoding="utf-8",
    )

    records = _load_records(path, max_orbits=1)

    assert [record["orbit_id"] for record in records] == ["a"]


def test_iter_docs_yields_clean_and_perturbation_queries():
    records = [
        {
            "clean": {
                "query": "clean query",
                "docs": [{"doc_id": "clean-doc", "text": "clean evidence"}],
            },
            "perturbations": [
                {
                    "query": "perturbed query",
                    "docs": [{"doc_id": "pert-doc", "text": "perturbed evidence"}],
                }
            ],
        }
    ]

    pairs = list(_iter_docs(records))

    assert [(query, doc["doc_id"]) for query, doc in pairs] == [
        ("clean query", "clean-doc"),
        ("perturbed query", "pert-doc"),
    ]
