import json

from experiments.run_v4_structural_balance_diagnostic import run_v4_structural_balance_diagnostic


def test_run_v4_structural_balance_diagnostic_writes_summary_and_artifacts(tmp_path):
    raw_path = tmp_path / "raw.jsonl"
    private_path = tmp_path / "private.jsonl"
    prefix = tmp_path / "demo"
    raw_rows = [
        _raw("g1:stable", "g1", "Paris is in France.", True),
        _raw("g2:stable", "g2", "Berlin is in Germany.", True),
        _raw("g3:fragile", "g3", "Paris is a city.", False),
        _raw("g4:fragile", "g4", "Berlin is a city.", False),
    ]
    private_rows = [
        _private(row["orbit_id"], row["source_item_group_id"], row["orbit_id"].endswith("stable"))
        for row in raw_rows
    ]
    raw_path.write_text("\n".join(json.dumps(row) for row in raw_rows), encoding="utf-8")
    private_path.write_text("\n".join(json.dumps(row) for row in private_rows), encoding="utf-8")

    summary = run_v4_structural_balance_diagnostic(
        raw_path,
        private_path,
        prefix,
        bootstrap_samples=5,
        random_trials=5,
    )

    assert summary["balance"]["selected_n"] == 4
    assert summary["anti_shortcut"]["structural_max_auc"] == 0.5
    assert summary["csrm"]["n"] == 4
    assert (tmp_path / "demo.constant.raw.jsonl").exists()
    assert (tmp_path / "demo.constant.structbalanced.summary.json").exists()
    saved = json.loads((tmp_path / "demo.constant.structbalanced.summary.json").read_text(encoding="utf-8"))
    assert saved["outputs"]["balanced_raw"].endswith("demo.constant.structbalanced.raw.jsonl")


def _raw(orbit_id: str, group_id: str, text: str, label: bool) -> dict:
    doc_text = "x" * 24
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "query": "Where is the city?",
        "candidate_answer": "France" if "Paris" in text else "Germany",
        "clean_evidence": [{"doc_id": f"{orbit_id}:clean", "text": doc_text, "retrieval_score": 0.9}],
        "perturbations": [
            {
                "query": "Where is the city?",
                "candidate_answer": "France" if "Paris" in text else "Germany",
                "evidence": [{"doc_id": f"{orbit_id}:perturb", "text": doc_text, "retrieval_score": 0.2}],
            }
        ],
        "retrieval_scores": [0.9, 0.2],
        "generator_outputs": [],
        "verifier_outputs": {},
        "metadata": {"demo_expected": "answerable" if label else "fragile"},
    }


def _private(orbit_id: str, group_id: str, label: bool) -> dict:
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "label_answerable": label,
        "construction_type": "stable" if label else "fragile",
    }
