import json

from experiments.build_corm_biased_nq_test import build_biased_nq_test
from experiments.build_corm_template_perturbations import build_template_perturbations


def test_template_perturbations_are_biased_nq_compatible(tmp_path):
    rows = [
        {"question": "who wrote hamlet", "answer": ["William Shakespeare"], "query_idx": 0},
        {"question": "what language is spoken in brazil", "answer": ["Portuguese"], "query_idx": 1},
        {"question": "who painted the mona lisa", "answer": ["Leonardo da Vinci"], "query_idx": 2},
    ]
    perturbations = tmp_path / "perturbations.jsonl"
    manifest = tmp_path / "perturbations_manifest.json"

    report = build_template_perturbations(rows, output=perturbations, manifest=manifest)

    assert report["status"] == "built"
    assert report["rows"] == 3
    assert report["type_counts"] == {"1": 5, "2": 5, "3": 5}
    lines = [json.loads(line) for line in perturbations.read_text(encoding="utf-8").splitlines()]
    assert all({1, 2, 3}.issubset({p["perturbation_type"] for p in row["perturbations"]}) for row in lines)
    assert all(p["generator"] == "template_fallback" for row in lines for p in row["perturbations"])

    biased_nq = tmp_path / "biased_nq_test.jsonl"
    biased_manifest = tmp_path / "biased_manifest.json"
    biased_report = build_biased_nq_test(perturbations, biased_nq, manifest=biased_manifest)

    assert biased_report["status"] == "built"
    assert biased_report["rows"] == 3
    assert biased_nq.exists()
