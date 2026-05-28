import csv
import json

import pytest

from experiments.export_audit_pack import export_audit_pack
from experiments.merge_audit_annotations import merge_audit_annotations


def _audit_item():
    return {
        "orbit_id": "orbit-1",
        "source": "unit",
        "split": "split-a",
        "expected_label_answerable": True,
        "auditor_label_answerable": None,
        "auditor_failure_type": None,
        "auditor_notes": None,
        "answer": "answer",
        "clean": {
            "query": "clean <query>",
            "label_answerable": True,
            "support_key": "gold",
            "perturbation_type": "clean",
            "docs": [
                {
                    "doc_id": "d1",
                    "title": "Title",
                    "rank": 0,
                    "corm_score": 0.9,
                    "support": 0.8,
                    "conflict": 0.0,
                    "missing": 0.1,
                    "text": "Evidence <must escape>",
                }
            ],
        },
        "perturbations": [],
    }


def test_export_audit_pack_writes_csv_and_html(tmp_path):
    source = tmp_path / "audit.jsonl"
    source.write_text(json.dumps(_audit_item()), encoding="utf-8")
    manifest = export_audit_pack(source, tmp_path / "audit_pack")

    labels_csv = tmp_path / "audit_pack.labels.csv"
    review_html = tmp_path / "audit_pack.review.html"
    assert manifest["items"] == 1
    assert labels_csv.exists()
    assert review_html.exists()

    rows = list(csv.DictReader(labels_csv.open(encoding="utf-8-sig")))
    assert rows[0]["orbit_id"] == "orbit-1"
    assert rows[0]["expected_label_answerable"] == "true"
    assert "adjudicated_label_answerable" in rows[0]
    assert "Evidence &lt;must escape&gt;" in review_html.read_text(encoding="utf-8")


def test_export_blind_audit_pack_hides_labels_and_scores(tmp_path):
    source = tmp_path / "audit.jsonl"
    items = [_audit_item(), _audit_item() | {"orbit_id": "orbit-2", "split": "split-b"}]
    source.write_text(
        "\n".join(json.dumps(item) for item in items),
        encoding="utf-8",
    )

    manifest = export_audit_pack(
        source,
        tmp_path / "audit_pack_a2",
        blind=True,
        shuffle_seed=11,
        annotator="auditor2",
    )

    labels_csv = tmp_path / "audit_pack_a2.blind.labels.csv"
    review_html = tmp_path / "audit_pack_a2.blind.review.html"
    rows = list(csv.DictReader(labels_csv.open(encoding="utf-8-sig")))
    assert manifest["blind"] is True
    assert manifest["annotator"] == "auditor2"
    assert set(rows[0]) == {
        "orbit_id",
        "split",
        "auditor2_label_answerable",
        "auditor2_failure_type",
        "auditor2_notes",
    }
    assert "expected_label_answerable" not in rows[0]

    html_text = review_html.read_text(encoding="utf-8")
    assert "Expected answerable" not in html_text
    assert "Original label_answerable" not in html_text
    assert "corm=" not in html_text
    assert "conflict=" not in html_text
    assert sorted(manifest["review_order"]) == ["orbit-1", "orbit-2"]


def test_merge_audit_annotations_updates_editable_fields(tmp_path):
    source = tmp_path / "audit.jsonl"
    source.write_text(json.dumps(_audit_item()), encoding="utf-8")
    labels_csv = tmp_path / "labels.csv"
    labels_csv.write_text(
        "\n".join(
            [
                "orbit_id,split,expected_label_answerable,auditor_label_answerable,auditor_failure_type,auditor_notes,auditor2_label_answerable,auditor2_failure_type,auditor2_notes,adjudicated_label_answerable,adjudication_notes",
                "orbit-1,split-a,true,false,missing_evidence,missing one hop,true,,,false,adjudicated missing",
            ]
        ),
        encoding="utf-8",
    )
    output = tmp_path / "merged.jsonl"

    result = merge_audit_annotations(source, labels_csv, output)

    merged = json.loads(output.read_text(encoding="utf-8"))
    assert result["updated"] == 1
    assert merged["auditor_label_answerable"] is False
    assert merged["auditor_failure_type"] == "missing_evidence"
    assert merged["auditor_notes"] == "missing one hop"
    assert merged["auditor2_label_answerable"] is True
    assert merged["adjudicated_label_answerable"] is False
    assert merged["adjudication_notes"] == "adjudicated missing"


def test_merge_audit_annotations_accepts_partial_blind_csv(tmp_path):
    source = tmp_path / "audit.jsonl"
    source.write_text(json.dumps(_audit_item()), encoding="utf-8")
    labels_csv = tmp_path / "labels.csv"
    labels_csv.write_text(
        "\n".join(
            [
                "orbit_id,split,auditor2_label_answerable,auditor2_failure_type,auditor2_notes",
                "orbit-1,split-a,false,conflicting_evidence,second pass",
            ]
        ),
        encoding="utf-8",
    )
    output = tmp_path / "merged.jsonl"

    result = merge_audit_annotations(source, labels_csv, output)

    merged = json.loads(output.read_text(encoding="utf-8"))
    assert result["updated"] == 1
    assert merged["auditor_label_answerable"] is None
    assert merged["auditor2_label_answerable"] is False
    assert merged["auditor2_failure_type"] == "conflicting_evidence"
    assert merged["auditor2_notes"] == "second pass"


def test_merge_audit_annotations_rejects_same_input_output(tmp_path):
    source = tmp_path / "audit.jsonl"
    source.write_text(json.dumps(_audit_item()), encoding="utf-8")
    labels_csv = tmp_path / "labels.csv"
    labels_csv.write_text(
        "\n".join(
            [
                "orbit_id,split,expected_label_answerable,auditor_label_answerable,auditor_failure_type,auditor_notes,auditor2_label_answerable,auditor2_failure_type,auditor2_notes,adjudicated_label_answerable,adjudication_notes",
                "orbit-1,split-a,true,true,,,,,,true,",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="must differ"):
        merge_audit_annotations(source, labels_csv, source)
