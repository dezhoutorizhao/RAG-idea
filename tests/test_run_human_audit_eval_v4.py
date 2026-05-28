import json

import pytest

from experiments.run_human_audit_eval_v4 import (
    infer_scored_path,
    load_adjudicated_labels,
    materialize_human_labeled_inputs,
    render_markdown,
)


def test_materialize_human_labeled_inputs_replaces_private_labels(tmp_path):
    raw = tmp_path / "pack.raw.jsonl"
    private = tmp_path / "pack.private_eval.jsonl"
    scored = tmp_path / "pack.textonly_scored.jsonl"
    _write_jsonl(raw, [{"orbit_id": "o1"}, {"orbit_id": "o2"}])
    _write_jsonl(private, [{"orbit_id": "o1", "label_answerable": True}, {"orbit_id": "o2", "label_answerable": False}])
    _write_jsonl(scored, [{"orbit_id": "o1"}, {"orbit_id": "o2"}])
    manifest = {
        "audit_items": [
            {"audit_id": "a1", "orbit_id": "o1"},
            {"audit_id": "a2", "orbit_id": "o2"},
        ]
    }

    outputs = materialize_human_labeled_inputs(
        manifest=manifest,
        labels={"a1": False, "a2": True},
        raw_path=raw,
        private_path=private,
        scored_path=scored,
        output_dir=tmp_path / "out",
        pack_name="pack",
        allow_partial=False,
    )

    rows = _read_jsonl(outputs["private_output"])
    assert [row["orbit_id"] for row in rows] == ["o1", "o2"]
    assert [row["label_answerable"] for row in rows] == [False, True]
    assert [row["heuristic_label_answerable"] for row in rows] == [True, False]
    assert all(row["label_source"] == "human_adjudicated_v4" for row in rows)


def test_materialize_human_labeled_inputs_requires_complete_labels(tmp_path):
    raw = tmp_path / "pack.raw.jsonl"
    private = tmp_path / "pack.private_eval.jsonl"
    scored = tmp_path / "pack.textonly_scored.jsonl"
    _write_jsonl(raw, [{"orbit_id": "o1"}, {"orbit_id": "o2"}])
    _write_jsonl(private, [{"orbit_id": "o1", "label_answerable": True}, {"orbit_id": "o2", "label_answerable": False}])
    _write_jsonl(scored, [{"orbit_id": "o1"}, {"orbit_id": "o2"}])
    manifest = {"audit_items": [{"audit_id": "a1", "orbit_id": "o1"}, {"audit_id": "a2", "orbit_id": "o2"}]}

    with pytest.raises(ValueError, match="without human labels"):
        materialize_human_labeled_inputs(
            manifest=manifest,
            labels={"a1": False},
            raw_path=raw,
            private_path=private,
            scored_path=scored,
            output_dir=tmp_path / "out",
            pack_name="pack",
            allow_partial=False,
        )


def test_load_adjudicated_labels_and_infer_scored_path(tmp_path):
    labels = tmp_path / "labels.jsonl"
    labels.write_text(
        "\n".join(
            [
                json.dumps({"audit_id": "a1", "adjudicated_label_answerable": "answerable"}),
                json.dumps({"audit_id": "a2", "adjudicated_label_answerable": "fragile"}),
                json.dumps({"audit_id": "a3", "adjudicated_label_answerable": ""}),
            ]
        ),
        encoding="utf-8",
    )

    assert load_adjudicated_labels(labels) == {"a1": True, "a2": False, "a3": None}
    assert infer_scored_path(tmp_path / "x.raw.jsonl") == tmp_path / "x.textonly_scored.jsonl"


def test_render_markdown_lists_failed_gates():
    text = render_markdown(
        {
            "ready": False,
            "pack_count": 1,
            "evaluated_pack_count": 0,
            "allow_partial": False,
            "claim_policy": "No claim.",
            "packs": [
                {
                    "pack_name": "pack",
                    "selected_items": 2,
                    "labeled": 0,
                    "pending": 2,
                    "evaluation_ready": False,
                    "evaluated": False,
                    "failed_gates": [{"gate": "non_empty_human_labels", "actual": 0}],
                }
            ],
        }
    )

    assert "non_empty_human_labels" in text
    assert "No claim." in text


def _write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")


def _read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
