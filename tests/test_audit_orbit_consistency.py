import json

from experiments.audit_orbit_consistency import audit_orbit_consistency


def test_audit_orbit_consistency_passes_structural_hotpot_record(tmp_path):
    path = tmp_path / "orbits.jsonl"
    path.write_text(
        json.dumps(
            {
                "orbit_id": "hotpot:1:missing_hop",
                "source": "hotpot_qa/distractor",
                "clean": _set(
                    split="hotpot_missing_hop",
                    support_key="A|B",
                    perturbation_type="clean",
                    label=True,
                    docs=["A", "B", "C"],
                ),
                "perturbations": [
                    _set(
                        split="hotpot_missing_hop",
                        support_key="A|B",
                        perturbation_type="missing_hop_framing",
                        label=False,
                        docs=["A", "C"],
                    )
                ],
            }
        ),
        encoding="utf-8",
    )

    report = audit_orbit_consistency(path)

    assert report["passed"] is True
    assert report["error_count"] == 0
    assert report["splits"]["hotpot_missing_hop"]["negative"] == 1


def test_audit_orbit_consistency_flags_inconsistent_positive_support(tmp_path):
    path = tmp_path / "orbits.jsonl"
    path.write_text(
        json.dumps(
            {
                "orbit_id": "hotpot:1:stable",
                "source": "hotpot_qa/distractor",
                "clean": _set(
                    split="hotpot_stable_support",
                    support_key="A|B",
                    perturbation_type="clean",
                    label=True,
                    docs=["A", "B"],
                ),
                "perturbations": [
                    _set(
                        split="hotpot_stable_support",
                        support_key="A|B",
                        perturbation_type="answer_preserving",
                        label=True,
                        docs=["A"],
                    )
                ],
            }
        ),
        encoding="utf-8",
    )

    report = audit_orbit_consistency(path)

    assert report["passed"] is False
    assert any(error["code"] == "positive_support_incomplete" for error in report["errors"])


def test_audit_orbit_consistency_rejects_vacuous_feature_values(tmp_path):
    path = tmp_path / "orbits.jsonl"
    record = {
        "orbit_id": "hotpot:1:distractor",
        "source": "hotpot_qa/distractor",
        "clean": _set(
            split="hotpot_distractor",
            support_key="A",
            perturbation_type="clean",
            label=True,
            docs=["A"],
        ),
        "perturbations": [
            _set(
                split="hotpot_distractor",
                support_key="distractor_only",
                perturbation_type="distractor_only",
                label=False,
                docs=["C"],
            )
        ],
    }
    record["perturbations"][0]["docs"][0]["support"] = 1.5
    path.write_text(json.dumps(record), encoding="utf-8")

    report = audit_orbit_consistency(path)

    assert report["passed"] is False
    assert any(error["code"] == "feature_out_of_range" for error in report["errors"])


def test_audit_orbit_consistency_flags_fever_missing_full_support(tmp_path):
    path = tmp_path / "orbits.jsonl"
    path.write_text(
        json.dumps(
            {
                "orbit_id": "fever:1:missing",
                "source": "copenlu/fever_gold_evidence",
                "clean": _set(
                    split="fever_missing_evidence",
                    support_key="Gold:1",
                    perturbation_type="clean",
                    label=True,
                    docs=["Gold:1"],
                ),
                "perturbations": [
                    _set(
                        split="fever_missing_evidence",
                        support_key="Gold:1:partial",
                        perturbation_type="missing_evidence",
                        label=False,
                        docs=["Gold:1", "Distractor:1"],
                    )
                ],
            }
        ),
        encoding="utf-8",
    )

    report = audit_orbit_consistency(path)

    assert report["passed"] is False
    assert any(error["code"] == "missing_split_has_full_support" for error in report["errors"])


def test_audit_orbit_consistency_flags_provenance_and_lineage_errors(tmp_path):
    path = tmp_path / "orbits.jsonl"
    path.write_text(
        json.dumps(
            {
                "orbit_id": "fever:1:near_miss_dilution",
                "source": "hotpot_qa/distractor",
                "clean": _set(
                    split="fever_near_miss_dilution",
                    support_key="Gold:1",
                    perturbation_type="clean",
                    label=True,
                    docs=["Gold:1", "Distractor:1"],
                ),
                "perturbations": [
                    _set(
                        split="fever_missing_evidence",
                        support_key="Gold:1",
                        perturbation_type="near_miss_high_sufficiency",
                        label=False,
                        docs=["Near:1"],
                    )
                ],
            }
        ),
        encoding="utf-8",
    )

    report = audit_orbit_consistency(path)

    assert report["passed"] is False
    assert {error["code"] for error in report["errors"]} >= {
        "source_mismatch",
        "split_mismatch",
        "perturbation_count_mismatch",
        "support_key_lineage_mismatch",
    }


def test_audit_orbit_consistency_flags_duplicate_docs(tmp_path):
    path = tmp_path / "orbits.jsonl"
    path.write_text(
        json.dumps(
            {
                "orbit_id": "hotpot:1:stable",
                "source": "hotpot_qa/distractor",
                "clean": _set(
                    split="hotpot_stable_support",
                    support_key="A|B",
                    perturbation_type="clean",
                    label=True,
                    docs=["A", "B", "A"],
                ),
                "perturbations": [
                    _set(
                        split="hotpot_stable_support",
                        support_key="A|B",
                        perturbation_type="answer_preserving",
                        label=True,
                        docs=["A", "B"],
                    ),
                    _set(
                        split="hotpot_stable_support",
                        support_key="A|B",
                        perturbation_type="answer_preserving",
                        label=True,
                        docs=["B", "A"],
                    ),
                ],
            }
        ),
        encoding="utf-8",
    )

    report = audit_orbit_consistency(path)

    assert report["passed"] is False
    assert any(error["code"] == "duplicate_doc_id" for error in report["errors"])


def test_audit_orbit_consistency_flags_non_gold_high_support_feature(tmp_path):
    path = tmp_path / "orbits.jsonl"
    record = {
        "orbit_id": "hotpot:1:stable",
        "source": "hotpot_qa/distractor",
        "clean": _set(
            split="hotpot_stable_support",
            support_key="A|B",
            perturbation_type="clean",
            label=True,
            docs=["A", "B", "C"],
        ),
        "perturbations": [
            _set(
                split="hotpot_stable_support",
                support_key="A|B",
                perturbation_type="answer_preserving",
                label=True,
                docs=["A", "B"],
            ),
            _set(
                split="hotpot_stable_support",
                support_key="A|B",
                perturbation_type="answer_preserving",
                label=True,
                docs=["B", "A"],
            ),
        ],
    }
    record["clean"]["docs"][2]["support"] = 0.9
    path.write_text(json.dumps(record), encoding="utf-8")

    report = audit_orbit_consistency(path)

    assert report["passed"] is False
    assert any(error["code"] == "non_gold_doc_high_support_feature" for error in report["errors"])


def _set(split, support_key, perturbation_type, label, docs):
    label_source = (
        "fever_gold_evidence_heuristic"
        if split.startswith("fever_")
        else "hotpot_supporting_facts_heuristic"
    )
    support_ids = _support_ids(support_key)
    return {
        "query": "q",
        "answer": "a",
        "label_answerable": label,
        "split": split,
        "metadata": {
            "support_key": support_key,
            "perturbation_type": perturbation_type,
            "label_source": label_source,
        },
        "docs": [
            {
                "doc_id": doc_id,
                "title": doc_id,
                "text": "evidence",
                "corm_score": 0.5,
                "support": 0.9 if doc_id in support_ids else 0.1,
                "conflict": 0.0,
                "missing": 0.05 if doc_id in support_ids else 0.8,
            }
            for doc_id in docs
        ],
    }


def _support_ids(support_key):
    for prefix in ["opposite:", "near_miss:"]:
        if support_key.startswith(prefix):
            return set()
    if support_key == "distractor_only":
        return set()
    for suffix in [":partial", ":false_premise"]:
        if support_key.endswith(suffix):
            support_key = support_key[: -len(suffix)]
    return {part for part in support_key.split("|") if part}
