import csv
import json

from annotation.adjudicate_labels_v4 import adjudicate_labels_v4
from annotation.compute_agreement_v4 import compute_agreement_v4
from annotation.export_blind_audit_pack_v4 import export_blind_audit_pack_v4
from annotation.merge_audit_labels_v4 import merge_audit_labels_v4


def _raw_item(orbit_id, answer="SUPPORTS"):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": orbit_id.rsplit(":", 1)[0],
        "dataset": "unit-fever",
        "query": "Determine whether this claim is supported or refuted: A < B.",
        "candidate_answer": answer,
        "clean_evidence": [
            {
                "doc_id": "doc-1",
                "title": "Title",
                "text": "Evidence <must escape>.",
                "rank": 0,
                "retrieval_score": 0.99,
            }
        ],
        "perturbations": [
            {
                "query": "Using only evidence, fact-check: A < B.",
                "candidate_answer": answer,
                "evidence": [
                    {
                        "doc_id": "doc-2",
                        "title": "Perturbed",
                        "text": "Perturbed evidence.",
                        "rank": 0,
                        "retrieval_score": 0.12,
                    }
                ],
            }
        ],
        "retrieval_scores": [0.99, 0.12],
        "generator_outputs": [{"score": 1.0}],
        "verifier_outputs": {"nli": 1.0},
    }


def _private_item(orbit_id, label, construction_type):
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": orbit_id.rsplit(":", 1)[0],
        "label_answerable": label,
        "construction_type": construction_type,
        "label_source": "unit",
        "heuristic_label": construction_type,
        "support_key": "doc-1",
        "gold_answer": "SUPPORTS",
    }


def _write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")


def test_export_v4_pack_is_blind_and_balanced(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    orbit_ids = [
        "fever:a:stable",
        "fever:b:missing",
        "fever:c:stable",
        "fever:d:conflict",
    ]
    _write_jsonl(raw, [_raw_item(orbit_id) for orbit_id in orbit_ids])
    _write_jsonl(
        private,
        [
            _private_item("fever:a:stable", True, "stable"),
            _private_item("fever:b:missing", False, "missing"),
            _private_item("fever:c:stable", True, "stable"),
            _private_item("fever:d:conflict", False, "conflict"),
        ],
    )

    manifest = export_blind_audit_pack_v4(
        raw,
        private,
        tmp_path / "audit",
        pack_name="unit_pack",
        max_items=2,
        seed=7,
        annotator_ids=["ann1", "ann2"],
        audit_id_prefix="unit",
    )

    assert manifest["selected_items"] == 2
    assert manifest["selected_label_counts"] == {"false": 1, "true": 1, "unknown": 0}
    labels = list(
        csv.DictReader((tmp_path / "audit" / "unit_pack.ann1.labels.csv").open(encoding="utf-8-sig"))
    )
    assert set(labels[0]) == {
        "audit_id",
        "dataset",
        "auditor_id",
        "label_answerable",
        "failure_type",
        "confidence",
        "notes",
    }
    assert labels[0]["audit_id"].startswith("unit-")
    assert "orbit_id" not in labels[0]

    html_text = (tmp_path / "audit" / "unit_pack.review.html").read_text(encoding="utf-8")
    public_text = (tmp_path / "audit" / "unit_pack.items.jsonl").read_text(encoding="utf-8")
    assert "Evidence &lt;must escape&gt;" in html_text
    assert "retrieval_score" not in html_text
    assert "generator_outputs" not in public_text
    assert "fever:a:stable" not in html_text
    assert "construction_type" not in public_text
    assert manifest["audit_items"][0]["orbit_id"].startswith("fever:")


def test_merge_agreement_and_adjudication_v4(tmp_path):
    raw = tmp_path / "raw.jsonl"
    private = tmp_path / "private.jsonl"
    orbit_ids = ["fever:a:stable", "fever:b:missing"]
    _write_jsonl(raw, [_raw_item(orbit_id) for orbit_id in orbit_ids])
    _write_jsonl(
        private,
        [
            _private_item("fever:a:stable", True, "stable"),
            _private_item("fever:b:missing", False, "missing"),
        ],
    )
    export_blind_audit_pack_v4(
        raw,
        private,
        tmp_path / "audit",
        pack_name="unit_pack",
        seed=3,
        annotator_ids=["ann1", "ann2"],
        audit_id_prefix="unit",
    )

    labels1 = tmp_path / "audit" / "unit_pack.ann1.labels.csv"
    labels2 = tmp_path / "audit" / "unit_pack.ann2.labels.csv"
    rows1 = list(csv.DictReader(labels1.open(encoding="utf-8-sig")))
    rows2 = list(csv.DictReader(labels2.open(encoding="utf-8-sig")))
    rows1[0]["label_answerable"] = "answerable"
    rows1[1]["label_answerable"] = "fragile"
    rows2[0]["label_answerable"] = "answerable"
    rows2[1]["label_answerable"] = "answerable"
    _write_csv(labels1, rows1)
    _write_csv(labels2, rows2)

    merged = tmp_path / "audit" / "merged.jsonl"
    merge_result = merge_audit_labels_v4(
        tmp_path / "audit" / "unit_pack.manifest.json",
        [labels1, labels2],
        merged,
    )
    assert merge_result["rows"] == 4
    merged_text = merged.read_text(encoding="utf-8")
    assert "fever:" in merged_text

    agreement = compute_agreement_v4(merged)
    assert agreement["pairwise"][0]["compared"] == 2
    assert agreement["pairwise"][0]["agreements"] == 1
    assert len(agreement["conflicts"]) == 1

    adjudicated = tmp_path / "audit" / "adjudicated.jsonl"
    template = tmp_path / "audit" / "adjudication_template.csv"
    summary = adjudicate_labels_v4(merged, adjudicated, template_csv=template)
    assert summary["auto_agree"] == 1
    assert summary["pending"] == 1
    assert len(list(csv.DictReader(template.open(encoding="utf-8-sig")))) == 1


def _write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
