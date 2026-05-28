import json

from experiments.audit_hotpot_semantic_swap import audit_hotpot_semantic_swap


def test_audit_hotpot_semantic_swap_passes_valid_pair(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    output = tmp_path / "audit.json"
    raw_rows = [
        _raw("g:stable", "g", "Paris"),
        _raw("g:semantic_swap", "g", "Berlin"),
    ]
    private_rows = [
        _private("g:stable", "g", True, "stable"),
        _private("g:semantic_swap", "g", False, "semantic_swap"),
    ]
    _write_jsonl(raw, raw_rows)
    _write_jsonl(private, private_rows)

    report = audit_hotpot_semantic_swap(raw, private, output)

    assert report["passed"] is True
    assert report["aggregate"]["mean_perturbation_doc_overlap"] == 1.0
    assert report["aggregate"]["answer_mentions_reduced_rate"] == 1.0


def test_audit_hotpot_semantic_swap_reports_candidate_answer_change(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    output = tmp_path / "audit.json"
    stable = _raw("g:stable", "g", "Paris")
    swapped = _raw("g:semantic_swap", "g", "Berlin")
    swapped["candidate_answer"] = "Berlin"
    _write_jsonl(raw, [stable, swapped])
    _write_jsonl(
        private,
        [
            _private("g:stable", "g", True, "stable"),
            _private("g:semantic_swap", "g", False, "semantic_swap"),
        ],
    )

    report = audit_hotpot_semantic_swap(raw, private, output)

    assert report["passed"] is False
    assert "raw candidate_answer differs between stable and semantic_swap" in report["failure_examples"][0]["issues"]


def _raw(orbit_id, group_id, perturbation_city):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "hotpot-unit",
        "query": "Which city hosts the festival?",
        "candidate_answer": "Paris",
        "clean_evidence": [_doc("d1", "The festival is hosted in Paris.")],
        "perturbations": [
            {
                "query": "Which city hosts the festival?",
                "candidate_answer": "Paris",
                "evidence": [_doc("d1", f"The festival is hosted in {perturbation_city}.")],
            }
        ],
        "retrieval_scores": [0.5, 0.5],
    }


def _doc(doc_id, text):
    return {"doc_id": doc_id, "title": doc_id, "text": text, "rank": 0, "retrieval_score": 0.5}


def _private(orbit_id, group_id, label, construction_type):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "label_answerable": label,
        "construction_type": construction_type,
    }


def _write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
