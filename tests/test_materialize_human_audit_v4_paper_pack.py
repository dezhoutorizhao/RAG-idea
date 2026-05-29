import json

from experiments.materialize_human_audit_v4_paper_pack import (
    materialize_human_audit_v4_paper_pack,
)


def test_materialize_human_audit_v4_paper_pack_builds_pending_pack(tmp_path):
    _write_source(
        tmp_path,
        "results/hotpot_orbits_v4_n100.constant.raw.jsonl",
        "results/hotpot_orbits_v4_n100.private_eval.jsonl",
        "results/hotpot_orbits_v4_n100.constant.textonly_scored.jsonl",
        "hotpot",
        2,
    )
    _write_source(
        tmp_path,
        "results/fever_orbits_v4_n100.constant.raw.jsonl",
        "results/fever_orbits_v4_n100.private_eval.jsonl",
        "results/fever_orbits_v4_n100.constant.textonly_scored.jsonl",
        "fever",
        2,
    )

    summary = materialize_human_audit_v4_paper_pack(
        tmp_path,
        tmp_path / "results" / "human_audit_v4",
        pack_name="unit_paper_pack",
        seed=7,
    )

    assert summary["selected_items"] == 4
    assert summary["paper_pack_ready_for_labeling"] is True
    assert summary["human_labels_complete"] is False
    assert summary["pending_adjudicated_labels"] == 4
    assert summary["merge_summary"]["rows"] == 8
    assert summary["adjudication_summary"]["pending"] == 4
    assert (tmp_path / "results" / "human_audit_v4" / "unit_paper_pack.review.html").exists()
    public_items = (
        tmp_path / "results" / "human_audit_v4" / "unit_paper_pack.items.jsonl"
    ).read_text(encoding="utf-8")
    assert "label_answerable" not in public_items
    assert "support_key" not in public_items


def _write_source(root, raw_rel, private_rel, scored_rel, prefix, count):
    raw_rows = []
    private_rows = []
    scored_rows = []
    for index in range(count):
        orbit_id = f"{prefix}:{index}"
        raw_rows.append(
            {
                "orbit_id": orbit_id,
                "source_item_group_id": f"{prefix}:group:{index}",
                "dataset": prefix,
                "query": f"{prefix} query {index}",
                "candidate_answer": "answer",
                "clean_evidence": [{"doc_id": f"{orbit_id}:doc", "text": "clean"}],
                "perturbations": [
                    {
                        "query": f"{prefix} query {index}",
                        "candidate_answer": "answer",
                        "evidence": [{"doc_id": f"{orbit_id}:pert", "text": "perturbed"}],
                    }
                ],
            }
        )
        private_rows.append(
            {
                "orbit_id": orbit_id,
                "source_item_group_id": f"{prefix}:group:{index}",
                "dataset": prefix,
                "label_answerable": index % 2 == 0,
                "construction_type": "unit",
                "label_source": "unit",
                "heuristic_label": "unit",
                "support_key": f"{orbit_id}:doc",
                "gold_answer": "answer",
            }
        )
        scored_rows.append({"orbit_id": orbit_id, "csrm_score": 0.1 * index})
    _write_jsonl(root / raw_rel, raw_rows)
    _write_jsonl(root / private_rel, private_rows)
    _write_jsonl(root / scored_rel, scored_rows)


def _write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
