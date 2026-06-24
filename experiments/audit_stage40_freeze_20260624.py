#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_CONFIG = Path("configs/frozen_stage40.yaml")
DEFAULT_DATA_MANIFEST = Path("results/stage40_data_manifest.json")
DEFAULT_SPLIT_HASHES = Path("results/stage40_split_hashes.json")
DEFAULT_BASELINE_REGISTRY = Path("results/stage40_baseline_registry.json")
DEFAULT_CURRENT_REPRODUCTION = Path("results/stage40_current_reproduction.json")
DEFAULT_SUMMARY_MD = Path("results/stage40_freeze_audit_summary.md")

CANONICAL_ARTIFACTS: dict[str, Path] = {
    "stage40_config": DEFAULT_CONFIG,
    "public_manifest": Path("results/public_source_orbits_v4_n1000_manifest.json"),
    "public_integrity_audit": Path("results/public_source_n1000_integrity_audit_20260601.json"),
    "public_paired_bootstrap": Path("results/public_source_n1000_paired_bootstrap_csrm_cal_gbdt_20260606.json"),
    "public_ci_summary": Path("results/public_source_p1_paired_bootstrap_ci_summary_20260611.json"),
    "source_item_split": Path("configs/splits/source_item_group_split_20260611.json"),
    "accepted_baseline_registry": Path("results/accepted_baseline_registry_final_20260618.json"),
    "human_final": Path("results/human_public_source_final_20260609_eval/csrm_cal_gbdt_human_locked_eval_20260610.json"),
    "human_real_v2": Path(
        "results/human_public_source_real_human_v2_20260610_eval/"
        "csrm_cal_gbdt_human_locked_eval_v2_20260610.json"
    ),
    "p0_6_hybrid": Path("results/csrm_hybrid_orbitrank_p0_5seed3fold_20260618.json"),
    "p0_6_selection_rules": Path("results/p0_6_public_selection_rule_audit_20260618.json"),
    "p0_6_negative_closure": Path("results/stage33_p0_6_negative_closure_20260619.json"),
    "p1_real_generator_bottleneck": Path("results/p1_real_generator_negative_bottleneck_audit_20260619.json"),
    "strict_completion_blockers": Path("results/stage33_strict_completion_blockers_20260619.json"),
}

SPLIT_ARTIFACT_PATTERNS = (
    "results/public_source_orbits_v4_n1000.raw.jsonl",
    "results/public_source_orbits_v4_n1000.private_eval.jsonl",
    "results/public_source_orbits_v4_n1000.textonly_scored.jsonl",
    "results/public_source_end2end_splits_n1000/*.raw.jsonl",
    "results/public_source_end2end_splits_n1000/*.private_eval.jsonl",
    "results/public_source_end2end_splits_n1000/*.textonly_scored.jsonl",
)


def audit_stage40_freeze(
    *,
    config_path: Path,
    output_data_manifest: Path,
    output_split_hashes: Path,
    output_baseline_registry: Path,
    output_current_reproduction: Path,
    output_summary_md: Path,
) -> dict[str, Any]:
    generated_at = datetime.now(timezone.utc).isoformat()
    artifacts = dict(CANONICAL_ARTIFACTS)
    artifacts["stage40_config"] = config_path

    artifact_records = {name: file_record(path) for name, path in artifacts.items()}
    required_artifacts_exist = all(record["exists"] for record in artifact_records.values())

    loaded = {name: load_json(path) for name, path in artifacts.items() if path.suffix == ".json"}
    public_manifest = loaded.get("public_manifest", {})
    public_integrity = loaded.get("public_integrity_audit", {})
    public_paired = loaded.get("public_paired_bootstrap", {})
    public_ci = loaded.get("public_ci_summary", {})
    split = loaded.get("source_item_split", {})
    registry = loaded.get("accepted_baseline_registry", {})
    human_final = loaded.get("human_final", {})
    human_real_v2 = loaded.get("human_real_v2", {})
    p0_6_hybrid = loaded.get("p0_6_hybrid", {})
    p0_6_rules = loaded.get("p0_6_selection_rules", {})
    p0_6_negative = loaded.get("p0_6_negative_closure", {})
    p1_bottleneck = loaded.get("p1_real_generator_bottleneck", {})
    strict_blockers = loaded.get("strict_completion_blockers", {})

    public_checks = public_source_checks(public_manifest, public_integrity, public_paired, public_ci)
    split_checks = split_overlap_checks(split)
    registry_checks = baseline_registry_checks(registry)
    human_checks = human_final_checks(human_final)
    negative_checks = negative_evidence_checks(p0_6_hybrid, p0_6_rules, p0_6_negative, p1_bottleneck, strict_blockers)

    gates = {
        "required_artifacts_exist": required_artifacts_exist,
        **public_checks["gates"],
        **split_checks["gates"],
        **registry_checks["gates"],
        **human_checks["gates"],
        **negative_checks["gates"],
    }
    freeze_gate_keys = (
        "required_artifacts_exist",
        "public_manifest_ready",
        "public_integrity_passed",
        "feature_firewall_passed",
        "public_source_main_reproduced",
        "learned_baseline_boundary_reproduced",
        "source_item_split_no_overlap",
        "accepted_baseline_registry_passed",
        "human_final_reproduced",
        "p0_6_negative_reproduced",
        "p1_real_generator_negative_reproduced",
        "strict_blocker_ledger_present",
    )
    phase0_freeze_ready = all(bool(gates.get(key)) for key in freeze_gate_keys)

    split_artifact_records = [file_record(path) for path in expand_patterns(SPLIT_ARTIFACT_PATTERNS)]
    split_hashes = {
        "artifact_type": "stage40_split_hashes",
        "generated_at_utc": generated_at,
        "source_item_split": artifact_records["source_item_split"],
        "split_summary": split_checks["summary"],
        "split_artifacts": split_artifact_records,
        "gates": split_checks["gates"],
        "claim_boundary": (
            "Split hashes freeze the public-source n1000 source-item-group split and the materialized "
            "raw/private/scored files used by the current evidence. They do not certify future streams."
        ),
    }

    baseline_output = {
        "artifact_type": "stage40_baseline_registry",
        "generated_at_utc": generated_at,
        "source_artifact": artifact_records["accepted_baseline_registry"],
        "accepted_baseline_registry": registry_checks["summary"],
        "internal_controls": {
            "strongest_current_internal_control": "calibrated_logistic_orbit",
            "equal_budget_controls": [
                "equal_budget_ensemble_logistic",
                "equal_budget_min",
                "equal_budget_q25",
                "equal_budget_mean",
            ],
            "naive_or_proxy_controls": [
                "calibrated_logistic_context",
                "context_sufficiency_clean",
                "retrieval_stability",
                "faithful_sure_multi",
            ],
        },
        "budget_policy": (
            "External official-code baselines are comparison baselines only after adaptation to the same "
            "public dataset, retriever/generator context, top-k, token budget, and verifier-call budget. "
            "Each row must keep its reproduction level explicit."
        ),
        "gates": registry_checks["gates"],
    }

    current_reproduction = {
        "artifact_type": "stage40_current_reproduction",
        "generated_at_utc": generated_at,
        "public_source_main": public_checks["summary"],
        "human_final": human_checks["summary"],
        "human_real_v2_auxiliary": summarize_human(human_real_v2),
        "p0_6": negative_checks["p0_6_summary"],
        "p1_real_generator": negative_checks["p1_summary"],
        "strict_completion_blockers": negative_checks["strict_summary"],
        "gates": {
            **public_checks["gates"],
            **human_checks["gates"],
            **negative_checks["gates"],
        },
        "claim_boundary": (
            "The current materialized evidence supports public-source/proxy robustness and a frozen negative "
            "boundary against the strongest learned internal control. It does not support an all-win or "
            "strict submission-ready claim."
        ),
    }

    data_manifest = {
        "artifact_type": "stage40_data_manifest",
        "generated_at_utc": generated_at,
        "config": artifact_records["stage40_config"],
        "canonical_artifacts": artifact_records,
        "public_source": public_checks["summary"],
        "source_item_split": split_checks["summary"],
        "baseline_registry": registry_checks["summary"],
        "human_final": human_checks["summary"],
        "negative_evidence": {
            "p0_6": negative_checks["p0_6_summary"],
            "p1_real_generator": negative_checks["p1_summary"],
            "strict_completion_blockers": negative_checks["strict_summary"],
        },
        "gates": gates,
        "phase0_freeze_ready": phase0_freeze_ready,
        "strict_submission_ready": bool((strict_blockers.get("gates") or {}).get("strict_completion_ready")),
        "claim_boundary": (
            "Stage40 freezes the already materialized evidence and confirms that Phase 0 inputs are "
            "machine-auditable. It intentionally preserves the strict completion blockers instead of "
            "counting them as solved."
        ),
    }

    write_json(output_data_manifest, data_manifest)
    write_json(output_split_hashes, split_hashes)
    write_json(output_baseline_registry, baseline_output)
    write_json(output_current_reproduction, current_reproduction)
    output_summary_md.parent.mkdir(parents=True, exist_ok=True)
    output_summary_md.write_text(render_markdown(data_manifest, current_reproduction), encoding="utf-8")

    return {
        "phase0_freeze_ready": phase0_freeze_ready,
        "strict_submission_ready": data_manifest["strict_submission_ready"],
        "gates": gates,
        "outputs": {
            "data_manifest": str(output_data_manifest),
            "split_hashes": str(output_split_hashes),
            "baseline_registry": str(output_baseline_registry),
            "current_reproduction": str(output_current_reproduction),
            "summary_md": str(output_summary_md),
        },
    }


def public_source_checks(
    manifest: dict[str, Any],
    integrity: dict[str, Any],
    paired: dict[str, Any],
    ci_summary: dict[str, Any],
) -> dict[str, Any]:
    manifest_reports = manifest.get("dataset_reports") or []
    manifest_ready = (
        manifest.get("dataset_count_requested") == 6
        and manifest.get("dataset_count_successful") == 6
        and manifest.get("records", 0) > 0
        and manifest.get("source_item_groups", 0) >= 5000
        and all((row.get("status") == "ok") for row in manifest_reports)
    )
    integrity_checks = integrity.get("checks") or {}
    feature_firewall_passed = (
        integrity.get("passed") is True
        and integrity_checks.get("raw_oracle_firewall_passed") is True
        and integrity_checks.get("textonly_scorer_declares_no_private_fields") is True
    )
    id_alignment_passed = integrity_checks.get("id_alignment_passed") is True
    public_integrity_passed = integrity.get("passed") is True and integrity.get("error_count") == 0

    orbit_comparison = ((paired.get("aggregate") or {}).get("comparisons") or {}).get("calibrated_logistic_orbit") or {}
    primary_metrics = (paired.get("aggregate") or {}).get("primary_metrics") or {}
    public_source_main_reproduced = (
        paired.get("primary_method") == "csrm_calibrated_gbdt"
        and paired.get("n", 0) > 0
        and metric_mean(primary_metrics, "auroc") is not None
        and bool(orbit_comparison)
    )
    claim_assessment = ci_summary.get("claim_assessment") or {}
    learned_boundary_reproduced = (
        bool(orbit_comparison)
        and claim_assessment.get("learned_baseline_dominance_supported") is False
        and claim_assessment.get("learned_baseline_has_ci_boundary") is True
    )

    summary = {
        "manifest": {
            "records": manifest.get("records"),
            "positive": manifest.get("positive"),
            "negative": manifest.get("negative"),
            "source_item_groups": manifest.get("source_item_groups"),
            "dataset_count_requested": manifest.get("dataset_count_requested"),
            "dataset_count_successful": manifest.get("dataset_count_successful"),
        },
        "integrity": {
            "passed": integrity.get("passed"),
            "error_count": integrity.get("error_count"),
            "checks": integrity_checks,
        },
        "primary_method": paired.get("primary_method"),
        "n": paired.get("n"),
        "seeds": paired.get("seeds"),
        "primary_metrics": primary_metrics,
        "comparison_vs_calibrated_logistic_orbit": orbit_comparison,
        "claim_assessment": claim_assessment,
    }
    return {
        "summary": summary,
        "gates": {
            "public_manifest_ready": manifest_ready,
            "public_integrity_passed": public_integrity_passed,
            "feature_firewall_passed": feature_firewall_passed,
            "id_alignment_passed": id_alignment_passed,
            "public_source_main_reproduced": public_source_main_reproduced,
            "learned_baseline_boundary_reproduced": learned_boundary_reproduced,
        },
    }


def split_overlap_checks(split: dict[str, Any]) -> dict[str, Any]:
    overlap = split.get("overlap") or {}
    counts = split.get("counts") or {}
    no_overlap = (
        split.get("split_unit") in {"source_item_group", "source_item_group_id"}
        and split.get("no_group_overlap") is True
        and overlap.get("train_vs_calibration") == 0
        and overlap.get("train_vs_test") == 0
        and overlap.get("calibration_vs_test") == 0
    )
    has_counts = all(int(counts.get(key, 0) or 0) > 0 for key in ("train", "calibration", "test"))
    summary = {
        "split_unit": split.get("split_unit"),
        "split_hash": split.get("split_hash"),
        "seed": split.get("seed"),
        "counts": counts,
        "dataset_counts": split.get("dataset_counts"),
        "overlap": overlap,
        "no_group_overlap": split.get("no_group_overlap"),
    }
    return {
        "summary": summary,
        "gates": {
            "source_item_split_no_overlap": no_overlap,
            "source_item_split_counts_present": has_counts,
        },
    }


def baseline_registry_checks(registry: dict[str, Any]) -> dict[str, Any]:
    gates = registry.get("gates") or {}
    counted_rows = [row for row in registry.get("rows", []) if row.get("counted_as_accepted_baseline")]
    summary = {
        "artifact_type": registry.get("artifact_type"),
        "policy": registry.get("policy"),
        "gates": gates,
        "counted_rows": [
            {
                "id": row.get("id"),
                "venue": row.get("venue"),
                "strict_counting_tier": row.get("strict_counting_tier"),
                "reproduction_level": row.get("reproduction_level"),
                "official_resource": row.get("official_resource"),
            }
            for row in counted_rows
        ],
        "claim_policy": registry.get("claim_policy"),
    }
    return {
        "summary": summary,
        "gates": {
            "accepted_baseline_registry_passed": gates.get("registry_gate_pass") is True,
            "accepted_baseline_count_passed": gates.get("accepted_baseline_count_pass") is True,
            "official_code_or_model_count_passed": gates.get("official_code_or_model_count_pass") is True,
        },
    }


def human_final_checks(human_final: dict[str, Any]) -> dict[str, Any]:
    summary = summarize_human(human_final)
    orbit_auroc_mean = get_nested(
        human_final,
        "aggregate",
        "calibrated_logistic_orbit",
        "auroc",
        "mean",
    )
    csrm_auroc_mean = get_nested(human_final, "aggregate", "csrm_calibrated_gbdt", "auroc", "mean")
    human_final_reproduced = (
        human_final.get("n", 0) > 0
        and orbit_auroc_mean is not None
        and 0.74 <= float(orbit_auroc_mean) <= 0.75
        and csrm_auroc_mean is not None
    )
    return {
        "summary": summary,
        "gates": {
            "human_final_reproduced": human_final_reproduced,
            "human_overlap_exclusion_recorded": human_final.get("excluded_public_rows_due_to_human_overlap") is not None,
        },
    }


def summarize_human(human: dict[str, Any]) -> dict[str, Any]:
    return {
        "n": human.get("n"),
        "positive": human.get("positive"),
        "negative": human.get("negative"),
        "seeds": human.get("seeds"),
        "public_rows": human.get("public_rows"),
        "human_source_item_groups": human.get("human_source_item_groups"),
        "public_source_item_groups": human.get("public_source_item_groups"),
        "excluded_public_rows_due_to_human_overlap": human.get("excluded_public_rows_due_to_human_overlap"),
        "excluded_public_groups_due_to_human_overlap": human.get("excluded_public_groups_due_to_human_overlap"),
        "calibrated_logistic_orbit": get_nested(human, "aggregate", "calibrated_logistic_orbit"),
        "csrm_calibrated_gbdt": get_nested(human, "aggregate", "csrm_calibrated_gbdt"),
        "primary_vs_public_trained_baselines": get_nested(
            human,
            "aggregate",
            "primary_vs_public_trained_baselines",
        ),
        "claim_guardrails": human.get("claim_guardrails"),
    }


def negative_evidence_checks(
    p0_6_hybrid: dict[str, Any],
    p0_6_rules: dict[str, Any],
    p0_6_negative: dict[str, Any],
    p1_bottleneck: dict[str, Any],
    strict_blockers: dict[str, Any],
) -> dict[str, Any]:
    hybrid_gate = p0_6_hybrid.get("p0_6_gate") or {}
    p0_6_reproduced = (
        p0_6_negative.get("negative_closure_gate") is True
        and p0_6_negative.get("reference_method") == "calibrated_logistic_orbit"
        and (p0_6_negative.get("current_gate") or {}).get("p0_6_gate_cleared") is False
        and hybrid_gate.get("p0_6_gate_cleared") is False
        and p0_6_rules.get("any_public_rule_clears_p0_6") is False
    )

    p1_main = p1_bottleneck.get("main_matrix") or {}
    requirements = p1_bottleneck.get("requirements") or {}
    threshold = requirements.get("mean_task_aware_accuracy_min", 0.2)
    p1_reproduced = (
        p1_bottleneck.get("negative_bottleneck_gate") is True
        and p1_main.get("main_p1_real_generator_rag_complete") is False
        and p1_main.get("mean_task_aware_accuracy") is not None
        and float(p1_main["mean_task_aware_accuracy"]) < float(threshold)
    )

    strict_gates = strict_blockers.get("gates") or {}
    strict_ledger_present = (
        strict_gates.get("all_blockers_have_authoritative_evidence") is True
        and strict_gates.get("strict_completion_blocker_count", 0) >= 1
        and strict_gates.get("strict_completion_ready") is False
    )

    return {
        "p0_6_summary": {
            "selected_by_public_test": p0_6_hybrid.get("selected_by_public_test"),
            "strongest_reference_by_human_aurc": p0_6_hybrid.get("strongest_reference_by_human_aurc"),
            "hybrid_gate": hybrid_gate,
            "public_rule_status": {
                "rules_evaluated": p0_6_rules.get("rules_evaluated"),
                "any_public_rule_clears_p0_6": p0_6_rules.get("any_public_rule_clears_p0_6"),
                "status": p0_6_rules.get("status"),
            },
            "negative_closure": {
                "status": p0_6_negative.get("status"),
                "negative_closure_gate": p0_6_negative.get("negative_closure_gate"),
                "reference_method": p0_6_negative.get("reference_method"),
                "selected_candidate": p0_6_negative.get("selected_candidate"),
                "current_gate": p0_6_negative.get("current_gate"),
            },
        },
        "p1_summary": {
            "status": p1_bottleneck.get("status"),
            "negative_bottleneck_gate": p1_bottleneck.get("negative_bottleneck_gate"),
            "main_matrix": p1_main,
            "requirements": requirements,
            "diagnostics": p1_bottleneck.get("diagnostics"),
        },
        "strict_summary": {
            "gates": strict_gates,
            "rows": strict_blockers.get("rows"),
            "claim_boundary": strict_blockers.get("claim_boundary"),
        },
        "gates": {
            "p0_6_negative_reproduced": p0_6_reproduced,
            "p1_real_generator_negative_reproduced": p1_reproduced,
            "strict_blocker_ledger_present": strict_ledger_present,
            "strict_submission_ready": strict_gates.get("strict_completion_ready") is True,
        },
    }


def render_markdown(data_manifest: dict[str, Any], current_reproduction: dict[str, Any]) -> str:
    gates = data_manifest["gates"]
    p0_6 = current_reproduction["p0_6"]["negative_closure"]
    p1 = current_reproduction["p1_real_generator"]
    human_orbit = current_reproduction["human_final"]["calibrated_logistic_orbit"] or {}
    public = current_reproduction["public_source_main"]
    lines = [
        "# Stage40 Freeze Audit",
        "",
        f"Generated: `{data_manifest['generated_at_utc']}`",
        f"Phase 0 freeze ready: `{data_manifest['phase0_freeze_ready']}`",
        f"Strict submission ready: `{data_manifest['strict_submission_ready']}`",
        "",
        "## Gate Summary",
        "",
        "| Gate | Value |",
        "|---|---:|",
    ]
    for key in sorted(gates):
        lines.append(f"| `{key}` | `{gates[key]}` |")
    lines.extend(
        [
            "",
            "## Key Frozen Results",
            "",
            f"- Public source primary method: `{public.get('primary_method')}`.",
            f"- Public source AUROC mean: `{metric_mean(public.get('primary_metrics') or {}, 'auroc')}`.",
            f"- Public comparison vs calibrated_logistic_orbit AURC reduction mean: "
            f"`{metric_mean(public.get('comparison_vs_calibrated_logistic_orbit') or {}, 'aurc_reduction')}`.",
            f"- Human-final calibrated_logistic_orbit AUROC mean: `{metric_mean(human_orbit, 'auroc')}`.",
            f"- P0.6 selected candidate: `{p0_6.get('selected_candidate')}`.",
            f"- P0.6 negative closure gate: `{p0_6.get('negative_closure_gate')}`.",
            f"- P1 real-generator mean task-aware accuracy: "
            f"`{(p1.get('main_matrix') or {}).get('mean_task_aware_accuracy')}`.",
            "",
            "## Boundary",
            "",
            data_manifest["claim_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"_load_error": str(exc)}


def file_record(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(path),
            "exists": False,
            "bytes": None,
            "sha256": None,
            "mtime_utc": None,
        }
    stat = path.stat()
    return {
        "path": str(path),
        "exists": True,
        "bytes": stat.st_size,
        "sha256": sha256_file(path),
        "mtime_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expand_patterns(patterns: Iterable[str]) -> list[Path]:
    paths: set[Path] = set()
    for pattern in patterns:
        matches = sorted(Path(".").glob(pattern))
        paths.update(matches)
    return sorted(paths, key=lambda item: str(item))


def metric_mean(block: dict[str, Any], metric: str) -> float | None:
    value = block.get(metric)
    if isinstance(value, dict) and value.get("mean") is not None:
        return float(value["mean"])
    if metric in block and isinstance(block[metric], (int, float)):
        return float(block[metric])
    return None


def get_nested(payload: dict[str, Any], *keys: str) -> Any:
    cursor: Any = payload
    for key in keys:
        if not isinstance(cursor, dict) or key not in cursor:
            return None
        cursor = cursor[key]
    return cursor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-data-manifest", type=Path, default=DEFAULT_DATA_MANIFEST)
    parser.add_argument("--output-split-hashes", type=Path, default=DEFAULT_SPLIT_HASHES)
    parser.add_argument("--output-baseline-registry", type=Path, default=DEFAULT_BASELINE_REGISTRY)
    parser.add_argument("--output-current-reproduction", type=Path, default=DEFAULT_CURRENT_REPRODUCTION)
    parser.add_argument("--output-summary-md", type=Path, default=DEFAULT_SUMMARY_MD)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = audit_stage40_freeze(
        config_path=args.config,
        output_data_manifest=args.output_data_manifest,
        output_split_hashes=args.output_split_hashes,
        output_baseline_registry=args.output_baseline_registry,
        output_current_reproduction=args.output_current_reproduction,
        output_summary_md=args.output_summary_md,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
