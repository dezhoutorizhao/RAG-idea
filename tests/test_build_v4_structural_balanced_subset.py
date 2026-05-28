import json

from experiments.build_v4_structural_balanced_subset import build_v4_structural_balanced_subset
from experiments.score_orbits_textonly_v4 import score_orbits_textonly_v4


def test_build_v4_structural_balanced_subset_minimizes_shortcut_auc(tmp_path):
    raw_path = tmp_path / "raw.jsonl"
    private_path = tmp_path / "private.jsonl"
    scored_path = tmp_path / "scored.jsonl"
    prefix = tmp_path / "balanced"
    raw_rows = [
        _raw("g1:stable", "g1", 10, True),
        _raw("g2:stable", "g2", 20, True),
        _raw("g3:bad_short", "g3", 1, False),
        _raw("g4:bad_long", "g4", 80, False),
        _raw("g5:good_10", "g5", 10, False),
        _raw("g6:good_20", "g6", 20, False),
    ]
    private_rows = [_private(row["orbit_id"], row["source_item_group_id"], row["orbit_id"].endswith("stable")) for row in raw_rows]
    raw_path.write_text("\n".join(json.dumps(row) for row in raw_rows), encoding="utf-8")
    private_path.write_text("\n".join(json.dumps(row) for row in private_rows), encoding="utf-8")
    score_orbits_textonly_v4(raw_path, private_path, scored_path)

    report = build_v4_structural_balanced_subset(raw_path, private_path, scored_path, prefix)

    assert report["selected_positive"] == 2
    assert report["selected_negative"] == 2
    assert report["structural_only_probe"]["max_single_feature_auroc"] == 0.5
    assert report["selected_negative_orbit_ids"] == ["g5:good_10", "g6:good_20"]
    raw_out = [json.loads(line) for line in (tmp_path / "balanced.raw.jsonl").read_text(encoding="utf-8").splitlines()]
    private_out = [json.loads(line) for line in (tmp_path / "balanced.private_eval.jsonl").read_text(encoding="utf-8").splitlines()]
    scored_out = [json.loads(line) for line in (tmp_path / "balanced.textonly_scored.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [row["orbit_id"] for row in raw_out] == [row["orbit_id"] for row in private_out]
    assert [row["orbit_id"] for row in raw_out] == [row["orbit_id"] for row in scored_out]


def _raw(orbit_id: str, group_id: str, length: int, label: bool) -> dict:
    text = "x" * length
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "query": "Where is Paris?",
        "candidate_answer": "France",
        "clean_evidence": [{"doc_id": f"{orbit_id}:clean", "text": text, "retrieval_score": 0.5}],
        "perturbations": [
            {
                "query": "Where is Paris?",
                "candidate_answer": "France",
                "evidence": [{"doc_id": f"{orbit_id}:perturb", "text": text, "retrieval_score": 0.5}],
            }
        ],
        "retrieval_scores": [0.5, 0.5],
        "generator_outputs": [],
        "verifier_outputs": {},
        "metadata": {"demo_answerable_marker": "yes" if label else "no"},
    }


def _private(orbit_id: str, group_id: str, label: bool) -> dict:
    return {
        "orbit_id": orbit_id,
        "source_item_group_id": group_id,
        "dataset": "demo",
        "label_answerable": label,
        "construction_type": "stable" if label else "fragile",
    }
