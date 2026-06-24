#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from csrm_rag import (
    area_under_risk_coverage,
    corm_max_score,
    corm_mean_score,
    risk_coverage_curve,
    roc_auc,
    selective_risk_at_coverage,
    single_set_sufficiency,
)
from csrm_rag.baselines.v4_baselines import _orbit_features
from csrm_rag.calibration import split_groups
from csrm_rag.feature_firewall import assert_no_forbidden_features
from experiments.evaluate_orbits import load_orbits


DEFAULT_RAW = Path("results/public_source_orbits_v4_n1000.raw.jsonl")
DEFAULT_PRIVATE = Path("results/public_source_orbits_v4_n1000.private_eval.jsonl")
DEFAULT_SCORED = Path("results/public_source_orbits_v4_n1000.textonly_scored.jsonl")
DEFAULT_OUTPUT_JSON = Path("results/stage40_residualset_pilot_20260624.json")
DEFAULT_OUTPUT_MD = Path("results/stage40_residualset_pilot_20260624.md")
DEFAULT_DATASETS = (
    "hotpot_qa/distractor",
    "copenlu/fever_gold_evidence",
    "bdsaglam/musique",
)
CANDIDATES = (
    "deep_sets_residual",
    "set_transformer_residual",
    "set_transformer_full",
    "mlp_parameter_matched",
)


@dataclass(frozen=True)
class PilotData:
    raw_rows: list[dict[str, Any]]
    private_rows: list[dict[str, Any]]
    orbits: list[Any]
    labels: list[bool]
    groups: list[str]
    datasets: list[str]
    construction_types: list[str]


@dataclass(frozen=True)
class FeaturePack:
    flat: np.ndarray
    sets: np.ndarray
    mask: np.ndarray


def run_stage40_residualset_pilot(
    *,
    raw_path: Path,
    private_path: Path,
    scored_path: Path,
    output_json: Path,
    output_md: Path,
    datasets: Sequence[str],
    seeds: Sequence[int],
    train_frac: float,
    cal_frac: float,
    epochs: int,
    batch_size: int,
    hidden_dim: int,
    learning_rate: float,
    weight_decay: float,
    bootstrap_samples: int,
    smoke_limit_groups: int | None,
    min_source_item_groups: int,
    device_name: str,
) -> dict[str, Any]:
    data = load_pilot_data(raw_path, private_path, scored_path)
    dataset_rows = []
    for dataset in datasets:
        dataset_rows.append(
            run_dataset(
                data,
                dataset=dataset,
                seeds=seeds,
                train_frac=train_frac,
                cal_frac=cal_frac,
                epochs=epochs,
                batch_size=batch_size,
                hidden_dim=hidden_dim,
                learning_rate=learning_rate,
                weight_decay=weight_decay,
                bootstrap_samples=bootstrap_samples,
                smoke_limit_groups=smoke_limit_groups,
                min_source_item_groups=min_source_item_groups,
                device_name=device_name,
            )
        )

    aggregate = aggregate_results(dataset_rows)
    result = {
        "artifact_type": "stage40_residualset_pilot_20260624",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_input": str(raw_path),
        "private_input": str(private_path),
        "scored_input": str(scored_path),
        "datasets": list(datasets),
        "seeds": [int(seed) for seed in seeds],
        "config": {
            "train_frac": train_frac,
            "cal_frac": cal_frac,
            "epochs": epochs,
            "batch_size": batch_size,
            "hidden_dim": hidden_dim,
            "learning_rate": learning_rate,
            "weight_decay": weight_decay,
            "bootstrap_samples": bootstrap_samples,
            "smoke_limit_groups": smoke_limit_groups,
            "min_source_item_groups": min_source_item_groups,
            "device": device_name,
        },
        "baseline": "calibrated_logistic_orbit",
        "candidates": list(CANDIDATES),
        "dataset_results": dataset_rows,
        "aggregate": aggregate,
        "claim_boundary": (
            "This is a Stage40 Phase 1 pilot over the existing public-source n1000 artifacts. "
            "It tests ResidualSet-style architectures against calibrated_logistic_orbit under "
            "source-item-group splits. It is not a human-final or independent-stream claim."
        ),
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(result), encoding="utf-8")
    return result


def run_dataset(
    data: PilotData,
    *,
    dataset: str,
    seeds: Sequence[int],
    train_frac: float,
    cal_frac: float,
    epochs: int,
    batch_size: int,
    hidden_dim: int,
    learning_rate: float,
    weight_decay: float,
    bootstrap_samples: int,
    smoke_limit_groups: int | None,
    min_source_item_groups: int,
    device_name: str,
) -> dict[str, Any]:
    indices = [index for index, value in enumerate(data.datasets) if value == dataset]
    if smoke_limit_groups is not None:
        indices = limit_groups(indices, data.groups, smoke_limit_groups, seed=60624)

    dataset_groups = sorted({data.groups[index] for index in indices})
    labels = [data.labels[index] for index in indices]
    source_scope_pass = len(dataset_groups) >= min_source_item_groups
    if len(indices) < 4 or len(set(labels)) < 2:
        return {
            "dataset": dataset,
            "status": "skipped",
            "reason": "dataset has too few rows or lacks both labels",
            "n": len(indices),
            "source_item_groups": len(dataset_groups),
            "source_scope_pass": source_scope_pass,
            "seed_results": [],
            "candidate_summary": {},
            "dataset_gate": False,
        }

    seed_results = []
    for seed in seeds:
        try:
            seed_results.append(
                run_seed(
                    data,
                    indices=indices,
                    dataset=dataset,
                    seed=seed,
                    train_frac=train_frac,
                    cal_frac=cal_frac,
                    epochs=epochs,
                    batch_size=batch_size,
                    hidden_dim=hidden_dim,
                    learning_rate=learning_rate,
                    weight_decay=weight_decay,
                    bootstrap_samples=bootstrap_samples,
                    device_name=device_name,
                )
            )
        except Exception as exc:  # noqa: BLE001 - experiment output should record failed cells.
            seed_results.append(
                {
                    "dataset": dataset,
                    "seed": int(seed),
                    "status": "failed",
                    "error": str(exc),
                }
            )

    candidate_summary = summarize_dataset_candidates(seed_results)
    dataset_gate = any(row.get("dataset_candidate_gate") for row in candidate_summary.values())
    return {
        "dataset": dataset,
        "status": "ok" if any(row.get("status") == "ok" for row in seed_results) else "failed",
        "n": len(indices),
        "positive": int(sum(labels)),
        "negative": int(len(labels) - sum(labels)),
        "source_item_groups": len(dataset_groups),
        "source_scope_pass": source_scope_pass,
        "min_source_item_groups": min_source_item_groups,
        "seed_results": seed_results,
        "candidate_summary": candidate_summary,
        "dataset_gate": dataset_gate,
    }


def run_seed(
    data: PilotData,
    *,
    indices: Sequence[int],
    dataset: str,
    seed: int,
    train_frac: float,
    cal_frac: float,
    epochs: int,
    batch_size: int,
    hidden_dim: int,
    learning_rate: float,
    weight_decay: float,
    bootstrap_samples: int,
    device_name: str,
) -> dict[str, Any]:
    local_groups = [data.groups[index] for index in indices]
    local_labels = [data.labels[index] for index in indices]
    split = split_groups(local_groups, local_labels, train_frac=train_frac, cal_frac=cal_frac, seed=seed)
    train_idx = [indices[index] for index in split.train]
    cal_idx = [indices[index] for index in split.calibration]
    test_idx = [indices[index] for index in split.test]
    train_labels = np.asarray([data.labels[index] for index in train_idx], dtype=np.float32)
    test_labels = np.asarray([data.labels[index] for index in test_idx], dtype=np.float32)
    test_groups = [data.groups[index] for index in test_idx]
    test_slices = [data.construction_types[index] for index in test_idx]

    train_pack_raw = build_feature_pack([data.orbits[index] for index in train_idx])
    cal_pack_raw = build_feature_pack([data.orbits[index] for index in cal_idx])
    test_pack_raw = build_feature_pack([data.orbits[index] for index in test_idx])
    train_pack, cal_pack, test_pack = standardize_packs(train_pack_raw, cal_pack_raw, test_pack_raw)

    base_model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, class_weight="balanced", random_state=seed),
    )
    base_model.fit(train_pack_raw.flat, train_labels.astype(bool))
    base_scores = base_model.predict_proba(test_pack_raw.flat)[:, 1].astype(float)
    train_base_scores = base_model.predict_proba(train_pack_raw.flat)[:, 1].astype(float)
    base_metrics = score_metrics(base_scores, test_labels)

    device = select_device(device_name)
    candidate_results = {}
    for candidate in CANDIDATES:
        model = make_model(candidate, train_pack.flat.shape[1], train_pack.sets.shape[2], hidden_dim)
        model_result = fit_candidate(
            model,
            candidate=candidate,
            train_pack=train_pack,
            train_labels=train_labels,
            train_base_scores=train_base_scores,
            test_pack=test_pack,
            base_scores=base_scores,
            test_labels=test_labels,
            test_groups=test_groups,
            test_slices=test_slices,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
            weight_decay=weight_decay,
            bootstrap_samples=bootstrap_samples,
            bootstrap_seed=seed + 60624,
            device=device,
        )
        candidate_results[candidate] = model_result

    return {
        "dataset": dataset,
        "seed": int(seed),
        "status": "ok",
        "split_sizes": {
            "train": len(train_idx),
            "calibration_unused": len(cal_idx),
            "test": len(test_idx),
            "train_groups": len(split.train_groups),
            "calibration_groups_unused": len(split.calibration_groups),
            "test_groups": len(split.test_groups),
        },
        "baseline": {
            "method": "calibrated_logistic_orbit",
            "metrics": base_metrics,
        },
        "candidates": candidate_results,
    }


def fit_candidate(
    model: nn.Module,
    *,
    candidate: str,
    train_pack: FeaturePack,
    train_labels: np.ndarray,
    train_base_scores: np.ndarray,
    test_pack: FeaturePack,
    base_scores: np.ndarray,
    test_labels: np.ndarray,
    test_groups: Sequence[str],
    test_slices: Sequence[str],
    epochs: int,
    batch_size: int,
    learning_rate: float,
    weight_decay: float,
    bootstrap_samples: int,
    bootstrap_seed: int,
    device: torch.device,
) -> dict[str, Any]:
    torch.manual_seed(bootstrap_seed)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    pos_weight_value = class_pos_weight(train_labels)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight_value], dtype=torch.float32, device=device))

    dataset = TensorDataset(
        torch.as_tensor(train_pack.flat, dtype=torch.float32),
        torch.as_tensor(train_pack.sets, dtype=torch.float32),
        torch.as_tensor(train_pack.mask, dtype=torch.bool),
        torch.as_tensor(logit(train_base_scores), dtype=torch.float32),
        torch.as_tensor(train_labels, dtype=torch.float32),
    )
    generator = torch.Generator()
    generator.manual_seed(bootstrap_seed)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, generator=generator)
    for _ in range(epochs):
        model.train()
        for flat, sets, mask, base_logit, labels in loader:
            flat = flat.to(device)
            sets = sets.to(device)
            mask = mask.to(device)
            base_logit = base_logit.to(device)
            labels = labels.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits, _ = model(flat, sets, mask, base_logit)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        test_flat = torch.as_tensor(test_pack.flat, dtype=torch.float32, device=device)
        test_sets = torch.as_tensor(test_pack.sets, dtype=torch.float32, device=device)
        test_mask = torch.as_tensor(test_pack.mask, dtype=torch.bool, device=device)
        base_logit = torch.as_tensor(logit(base_scores), dtype=torch.float32, device=device)
        logits, diagnostics = model(test_flat, test_sets, test_mask, base_logit)
        scores = torch.sigmoid(logits).detach().cpu().numpy().astype(float)

    metrics = score_metrics(scores, test_labels)
    baseline_metrics = score_metrics(base_scores, test_labels)
    comparison = compare_metrics(metrics, baseline_metrics)
    ci = paired_group_bootstrap_ci(
        scores,
        base_scores,
        test_labels,
        test_groups,
        samples=bootstrap_samples,
        seed=bootstrap_seed,
    )
    slice_deltas = slice_auroc_deltas(scores, base_scores, test_labels, test_slices)
    max_source_auroc_drop = min((row["auroc_delta"] for row in slice_deltas if row["auroc_delta"] is not None), default=None)
    residual = diagnostics_to_json(diagnostics)
    residual_ok = residual_diagnostics_pass(candidate, residual)
    candidate_gate = (
        (comparison["aurc_reduction"] >= 0.015 or comparison["risk_at_30_reduction"] >= 0.02)
        and ci_positive_for_observed_gate(comparison, ci)
        and (max_source_auroc_drop is None or max_source_auroc_drop >= -0.02)
        and residual_ok
    )
    return {
        "metrics": metrics,
        "comparison_vs_calibrated_logistic_orbit": comparison,
        "paired_group_bootstrap_ci": ci,
        "slice_auroc_deltas": slice_deltas,
        "max_source_auroc_drop": max_source_auroc_drop,
        "residual_diagnostics": residual,
        "residual_diagnostics_pass": residual_ok,
        "seed_candidate_gate": candidate_gate,
    }


class MLPFull(nn.Module):
    def __init__(self, flat_dim: int, hidden_dim: int) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(flat_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.05),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, flat: torch.Tensor, sets: torch.Tensor, mask: torch.Tensor, base_logit: torch.Tensor):
        del sets, mask, base_logit
        return self.net(flat).squeeze(-1), {}


class DeepSetsResidual(nn.Module):
    def __init__(self, set_dim: int, hidden_dim: int) -> None:
        super().__init__()
        self.phi = nn.Sequential(nn.Linear(set_dim, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, hidden_dim), nn.ReLU())
        self.rho = nn.Sequential(nn.Linear(hidden_dim, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, 1))
        self.gate_logit = nn.Parameter(torch.zeros(()))

    def forward(self, flat: torch.Tensor, sets: torch.Tensor, mask: torch.Tensor, base_logit: torch.Tensor):
        del flat
        encoded = self.phi(sets)
        pooled = masked_mean(encoded, mask)
        raw_residual = self.rho(pooled).squeeze(-1)
        gate = torch.sigmoid(self.gate_logit)
        residual = gate * raw_residual
        return base_logit + residual, {"gate": gate, "residual": residual}


class SetTransformerModel(nn.Module):
    def __init__(self, set_dim: int, hidden_dim: int, *, residual: bool) -> None:
        super().__init__()
        heads = 4 if hidden_dim % 4 == 0 else 1
        self.residual = residual
        self.embed = nn.Linear(set_dim, hidden_dim)
        self.attn = nn.MultiheadAttention(hidden_dim, num_heads=heads, batch_first=True)
        self.ff = nn.Sequential(nn.LayerNorm(hidden_dim), nn.Linear(hidden_dim, hidden_dim), nn.ReLU())
        self.head = nn.Sequential(nn.Linear(hidden_dim, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, 1))
        if residual:
            self.gate_logit = nn.Parameter(torch.zeros(()))
        else:
            self.gate_logit = None

    def forward(self, flat: torch.Tensor, sets: torch.Tensor, mask: torch.Tensor, base_logit: torch.Tensor):
        del flat
        embedded = self.embed(sets)
        key_padding_mask = ~mask
        attended, _ = self.attn(embedded, embedded, embedded, key_padding_mask=key_padding_mask)
        encoded = self.ff(attended + embedded)
        pooled = masked_mean(encoded, mask)
        raw = self.head(pooled).squeeze(-1)
        if not self.residual:
            return raw, {}
        gate = torch.sigmoid(self.gate_logit)
        residual = gate * raw
        return base_logit + residual, {"gate": gate, "residual": residual}


def make_model(candidate: str, flat_dim: int, set_dim: int, hidden_dim: int) -> nn.Module:
    if candidate == "deep_sets_residual":
        return DeepSetsResidual(set_dim, hidden_dim)
    if candidate == "set_transformer_residual":
        return SetTransformerModel(set_dim, hidden_dim, residual=True)
    if candidate == "set_transformer_full":
        return SetTransformerModel(set_dim, hidden_dim, residual=False)
    if candidate == "mlp_parameter_matched":
        return MLPFull(flat_dim, hidden_dim)
    raise ValueError(f"unknown candidate: {candidate}")


def load_pilot_data(raw_path: Path, private_path: Path, scored_path: Path) -> PilotData:
    raw_rows = read_jsonl(raw_path)
    private_rows = read_jsonl(private_path)
    orbits = load_orbits(scored_path)
    if not (len(raw_rows) == len(private_rows) == len(orbits)):
        raise ValueError("raw, private, and scored files must have the same row count")
    for index, (raw, private, orbit) in enumerate(zip(raw_rows, private_rows, orbits)):
        assert_no_forbidden_features(raw)
        if raw["orbit_id"] != private["orbit_id"] or raw["orbit_id"] != orbit.orbit_id:
            raise ValueError(f"row {index} has misaligned orbit_id values")
    return PilotData(
        raw_rows=raw_rows,
        private_rows=private_rows,
        orbits=list(orbits),
        labels=[bool(row["label_answerable"]) for row in private_rows],
        groups=[str(row.get("source_item_group_id") or row["orbit_id"]) for row in raw_rows],
        datasets=[str(row.get("dataset") or "unknown") for row in private_rows],
        construction_types=[str(row.get("construction_type") or "unknown") for row in private_rows],
    )


def build_feature_pack(orbits: Sequence[Any]) -> FeaturePack:
    flat = np.asarray([_orbit_features(orbit) for orbit in orbits], dtype=np.float32)
    max_sets = max((len(orbit.all_sets) for orbit in orbits), default=1)
    sample_features = set_features(orbits[0].all_sets[0], is_clean=True) if orbits else [0.0]
    sets = np.zeros((len(orbits), max_sets, len(sample_features)), dtype=np.float32)
    mask = np.zeros((len(orbits), max_sets), dtype=bool)
    for row, orbit in enumerate(orbits):
        for col, evidence_set in enumerate(orbit.all_sets[:max_sets]):
            sets[row, col, :] = np.asarray(set_features(evidence_set, is_clean=(col == 0)), dtype=np.float32)
            mask[row, col] = True
    return FeaturePack(flat=flat, sets=sets, mask=mask)


def set_features(evidence_set: Any, *, is_clean: bool) -> list[float]:
    docs = list(evidence_set.docs)
    supports = [float(doc.support) for doc in docs] or [0.0]
    conflicts = [float(doc.conflict) for doc in docs] or [0.0]
    missings = [float(doc.missing) for doc in docs] or [1.0]
    corm_scores = [float(doc.corm_score) for doc in docs] or [0.0]
    return [
        float(single_set_sufficiency(evidence_set)),
        float(corm_max_score(evidence_set)),
        float(corm_mean_score(evidence_set)),
        max(supports),
        float(np.mean(supports)),
        max(conflicts),
        float(np.mean(conflicts)),
        max(missings),
        float(np.mean(missings)),
        max(corm_scores),
        float(np.mean(corm_scores)),
        float(len(docs)),
        1.0 if is_clean else 0.0,
    ]


def standardize_packs(train: FeaturePack, cal: FeaturePack, test: FeaturePack) -> tuple[FeaturePack, FeaturePack, FeaturePack]:
    flat_mean = train.flat.mean(axis=0, keepdims=True)
    flat_std = train.flat.std(axis=0, keepdims=True)
    flat_std[flat_std < 1e-6] = 1.0
    valid_sets = train.sets[train.mask]
    set_mean = valid_sets.mean(axis=0, keepdims=True).reshape(1, 1, -1)
    set_std = valid_sets.std(axis=0, keepdims=True).reshape(1, 1, -1)
    set_std[set_std < 1e-6] = 1.0

    def transform(pack: FeaturePack) -> FeaturePack:
        flat = (pack.flat - flat_mean) / flat_std
        sets = (pack.sets - set_mean) / set_std
        sets = np.where(pack.mask[:, :, None], sets, 0.0)
        return FeaturePack(flat=flat.astype(np.float32), sets=sets.astype(np.float32), mask=pack.mask)

    return transform(train), transform(cal), transform(test)


def score_metrics(scores: Sequence[float], labels: Sequence[float | bool]) -> dict[str, Any]:
    labels_bool = [bool(value) for value in labels]
    return {
        "n": len(labels_bool),
        "positive": int(sum(labels_bool)),
        "negative": int(len(labels_bool) - sum(labels_bool)),
        "auroc": safe_auc(scores, labels_bool),
        "aurc": area_under_risk_coverage(risk_coverage_curve(scores, labels_bool)),
        "risk_at_30": selective_risk_at_coverage(scores, labels_bool, 0.30)["risk"],
        "risk_at_50": selective_risk_at_coverage(scores, labels_bool, 0.50)["risk"],
        "risk_at_70": selective_risk_at_coverage(scores, labels_bool, 0.70)["risk"],
    }


def compare_metrics(candidate: dict[str, Any], baseline: dict[str, Any]) -> dict[str, float | None]:
    return {
        "auroc_delta": none_delta(candidate["auroc"], baseline["auroc"]),
        "aurc_reduction": float(baseline["aurc"] - candidate["aurc"]),
        "risk_at_30_reduction": float(baseline["risk_at_30"] - candidate["risk_at_30"]),
        "risk_at_50_reduction": float(baseline["risk_at_50"] - candidate["risk_at_50"]),
        "risk_at_70_reduction": float(baseline["risk_at_70"] - candidate["risk_at_70"]),
    }


def paired_group_bootstrap_ci(
    candidate_scores: Sequence[float],
    baseline_scores: Sequence[float],
    labels: Sequence[float | bool],
    groups: Sequence[str],
    *,
    samples: int,
    seed: int,
) -> dict[str, Any]:
    if samples <= 0:
        return {
            "samples": 0,
            "aurc_reduction": None,
            "risk_at_30_reduction": None,
            "auroc_delta": None,
        }
    group_to_indices: dict[str, list[int]] = {}
    for index, group in enumerate(groups):
        group_to_indices.setdefault(str(group), []).append(index)
    group_ids = sorted(group_to_indices)
    rng = random.Random(seed)
    rows = {"aurc_reduction": [], "risk_at_30_reduction": [], "auroc_delta": []}
    labels_array = np.asarray(labels, dtype=bool)
    cand = np.asarray(candidate_scores, dtype=float)
    base = np.asarray(baseline_scores, dtype=float)
    for _ in range(samples):
        sampled = []
        for group in (rng.choice(group_ids) for _ in group_ids):
            sampled.extend(group_to_indices[group])
        if len(set(labels_array[sampled].tolist())) < 2:
            continue
        cand_metrics = score_metrics(cand[sampled], labels_array[sampled])
        base_metrics = score_metrics(base[sampled], labels_array[sampled])
        diff = compare_metrics(cand_metrics, base_metrics)
        for key in rows:
            if diff[key] is not None:
                rows[key].append(float(diff[key]))
    return {
        "samples": samples,
        "unit": "source_item_group_id",
        **{key: percentile_ci(values) for key, values in rows.items()},
    }


def slice_auroc_deltas(
    candidate_scores: Sequence[float],
    baseline_scores: Sequence[float],
    labels: Sequence[float | bool],
    slices: Sequence[str],
) -> list[dict[str, Any]]:
    rows = []
    for item in sorted(set(slices)):
        indices = [index for index, value in enumerate(slices) if value == item]
        slice_labels = [bool(labels[index]) for index in indices]
        if len(set(slice_labels)) < 2:
            rows.append({"slice": item, "n": len(indices), "auroc_delta": None})
            continue
        candidate_auc = safe_auc([candidate_scores[index] for index in indices], slice_labels)
        baseline_auc = safe_auc([baseline_scores[index] for index in indices], slice_labels)
        rows.append(
            {
                "slice": item,
                "n": len(indices),
                "candidate_auroc": candidate_auc,
                "baseline_auroc": baseline_auc,
                "auroc_delta": none_delta(candidate_auc, baseline_auc),
            }
        )
    return rows


def summarize_dataset_candidates(seed_results: Sequence[dict[str, Any]]) -> dict[str, Any]:
    ok_rows = [row for row in seed_results if row.get("status") == "ok"]
    output = {}
    for candidate in CANDIDATES:
        rows = [row["candidates"][candidate] for row in ok_rows if candidate in row.get("candidates", {})]
        if not rows:
            output[candidate] = {"status": "missing", "dataset_candidate_gate": False}
            continue
        aurc_values = [row["comparison_vs_calibrated_logistic_orbit"]["aurc_reduction"] for row in rows]
        risk30_values = [row["comparison_vs_calibrated_logistic_orbit"]["risk_at_30_reduction"] for row in rows]
        auroc_values = [
            row["comparison_vs_calibrated_logistic_orbit"]["auroc_delta"]
            for row in rows
            if row["comparison_vs_calibrated_logistic_orbit"]["auroc_delta"] is not None
        ]
        source_drops = [
            row["max_source_auroc_drop"]
            for row in rows
            if row.get("max_source_auroc_drop") is not None
        ]
        residual_pass = all(row["residual_diagnostics_pass"] for row in rows)
        ci_aurc_lower = [
            row["paired_group_bootstrap_ci"]["aurc_reduction"]["p2_5"]
            for row in rows
            if row["paired_group_bootstrap_ci"].get("aurc_reduction")
        ]
        ci_risk30_lower = [
            row["paired_group_bootstrap_ci"]["risk_at_30_reduction"]["p2_5"]
            for row in rows
            if row["paired_group_bootstrap_ci"].get("risk_at_30_reduction")
        ]
        mean_aurc = float(np.mean(aurc_values))
        mean_risk30 = float(np.mean(risk30_values))
        positive_metric = mean_aurc >= 0.015 or mean_risk30 >= 0.02
        ci_positive = (
            (mean_aurc >= 0.015 and bool(ci_aurc_lower) and min(ci_aurc_lower) > 0.0)
            or (mean_risk30 >= 0.02 and bool(ci_risk30_lower) and min(ci_risk30_lower) > 0.0)
        )
        no_source_drop = not source_drops or min(source_drops) >= -0.02
        output[candidate] = {
            "status": "ok",
            "seed_count": len(rows),
            "mean_aurc_reduction": mean_aurc,
            "mean_risk_at_30_reduction": mean_risk30,
            "mean_auroc_delta": float(np.mean(auroc_values)) if auroc_values else None,
            "min_source_auroc_delta": min(source_drops) if source_drops else None,
            "min_aurc_ci_lower": min(ci_aurc_lower) if ci_aurc_lower else None,
            "min_risk30_ci_lower": min(ci_risk30_lower) if ci_risk30_lower else None,
            "positive_metric_gate": positive_metric,
            "paired_ci_gate": ci_positive,
            "no_source_auroc_drop_gt_0_02": no_source_drop,
            "residual_diagnostics_pass": residual_pass,
            "dataset_candidate_gate": positive_metric and ci_positive and no_source_drop and residual_pass,
        }
    return output


def aggregate_results(dataset_rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    ok_datasets = [row for row in dataset_rows if row.get("status") == "ok"]
    scope_ready = all(row.get("source_scope_pass") for row in ok_datasets) and len(ok_datasets) >= 3
    candidates = {}
    for candidate in CANDIDATES:
        candidate_rows = [
            row["candidate_summary"][candidate]
            for row in ok_datasets
            if candidate in row.get("candidate_summary", {}) and row["candidate_summary"][candidate].get("status") == "ok"
        ]
        dataset_positive = sum(1 for row in candidate_rows if row.get("dataset_candidate_gate"))
        dataset_auroc_deltas = [
            row.get("mean_auroc_delta")
            for row in candidate_rows
            if row.get("mean_auroc_delta") is not None
        ]
        min_dataset_auroc_delta = min(dataset_auroc_deltas) if dataset_auroc_deltas else None
        no_dataset_auroc_drop = min_dataset_auroc_delta is not None and min_dataset_auroc_delta >= -0.02
        candidates[candidate] = {
            "dataset_count": len(candidate_rows),
            "dataset_positive_count": dataset_positive,
            "two_of_three_positive": dataset_positive >= 2,
            "scope_ready": scope_ready,
            "no_dataset_auroc_drop_gt_0_02": no_dataset_auroc_drop,
            "phase1_candidate_gate": scope_ready and dataset_positive >= 2 and no_dataset_auroc_drop,
            "mean_aurc_reduction": mean_or_none([row.get("mean_aurc_reduction") for row in candidate_rows]),
            "mean_risk_at_30_reduction": mean_or_none([row.get("mean_risk_at_30_reduction") for row in candidate_rows]),
            "min_dataset_auroc_delta": min_dataset_auroc_delta,
            "min_source_auroc_delta": min_or_none([row.get("min_source_auroc_delta") for row in candidate_rows]),
        }
    return {
        "ok_dataset_count": len(ok_datasets),
        "scope_ready": scope_ready,
        "source_scope_failures": [
            {
                "dataset": row.get("dataset"),
                "source_item_groups": row.get("source_item_groups"),
                "min_source_item_groups": row.get("min_source_item_groups"),
            }
            for row in ok_datasets
            if not row.get("source_scope_pass")
        ],
        "candidates": candidates,
        "any_phase1_candidate_gate": any(row["phase1_candidate_gate"] for row in candidates.values()),
    }


def limit_groups(indices: Sequence[int], groups: Sequence[str], limit: int, *, seed: int) -> list[int]:
    group_ids = sorted({groups[index] for index in indices})
    rng = random.Random(seed)
    rng.shuffle(group_ids)
    keep = set(group_ids[: max(1, limit)])
    return [index for index in indices if groups[index] in keep]


def masked_mean(encoded: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    weights = mask.float().unsqueeze(-1)
    summed = (encoded * weights).sum(dim=1)
    denom = weights.sum(dim=1).clamp_min(1.0)
    return summed / denom


def class_pos_weight(labels: np.ndarray) -> float:
    positives = float(labels.sum())
    negatives = float(labels.shape[0] - labels.sum())
    if positives <= 0.0:
        return 1.0
    return max(0.1, negatives / positives)


def logit(scores: Sequence[float]) -> np.ndarray:
    arr = np.asarray(scores, dtype=np.float32)
    arr = np.clip(arr, 1e-5, 1.0 - 1e-5)
    return np.log(arr / (1.0 - arr)).astype(np.float32)


def safe_auc(scores: Sequence[float], labels: Sequence[bool]) -> float | None:
    try:
        return roc_auc(scores, labels)
    except ValueError:
        return None


def none_delta(value: float | None, reference: float | None) -> float | None:
    if value is None or reference is None:
        return None
    return float(value - reference)


def percentile_ci(values: Sequence[float]) -> dict[str, float] | None:
    if not values:
        return None
    ordered = sorted(float(value) for value in values)
    return {
        "p2_5": ordered[int(0.025 * (len(ordered) - 1))],
        "median": ordered[int(0.500 * (len(ordered) - 1))],
        "p97_5": ordered[int(0.975 * (len(ordered) - 1))],
    }


def ci_positive_for_observed_gate(comparison: dict[str, float | None], ci: dict[str, Any]) -> bool:
    aurc = comparison["aurc_reduction"]
    risk30 = comparison["risk_at_30_reduction"]
    aurc_ci = ci.get("aurc_reduction")
    risk30_ci = ci.get("risk_at_30_reduction")
    return (
        aurc is not None
        and aurc >= 0.015
        and aurc_ci is not None
        and aurc_ci["p2_5"] > 0.0
    ) or (
        risk30 is not None
        and risk30 >= 0.02
        and risk30_ci is not None
        and risk30_ci["p2_5"] > 0.0
    )


def diagnostics_to_json(diagnostics: dict[str, torch.Tensor]) -> dict[str, Any]:
    if not diagnostics:
        return {"applies": False}
    residual = diagnostics.get("residual")
    gate = diagnostics.get("gate")
    residual_abs_mean = float(residual.abs().mean().detach().cpu()) if residual is not None else None
    residual_std = float(residual.std(unbiased=False).detach().cpu()) if residual is not None else None
    gate_value = float(gate.detach().cpu()) if gate is not None else None
    return {
        "applies": True,
        "residual_abs_mean": residual_abs_mean,
        "residual_std": residual_std,
        "gate": gate_value,
        "gate_entropy": binary_entropy(gate_value) if gate_value is not None else None,
    }


def residual_diagnostics_pass(candidate: str, diagnostics: dict[str, Any]) -> bool:
    if candidate not in {"deep_sets_residual", "set_transformer_residual"}:
        return True
    return (
        diagnostics.get("applies") is True
        and (diagnostics.get("residual_abs_mean") or 0.0) > 1e-4
        and (diagnostics.get("residual_std") or 0.0) > 1e-5
        and (diagnostics.get("gate_entropy") or 0.0) > 0.10
    )


def binary_entropy(prob: float) -> float:
    p = min(1.0 - 1e-8, max(1e-8, float(prob)))
    return float(-(p * math.log(p) + (1.0 - p) * math.log(1.0 - p)))


def select_device(name: str) -> torch.device:
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if name == "cuda" and not torch.cuda.is_available():
        return torch.device("cpu")
    return torch.device(name)


def mean_or_none(values: Sequence[float | None]) -> float | None:
    numeric = [float(value) for value in values if value is not None]
    return float(np.mean(numeric)) if numeric else None


def min_or_none(values: Sequence[float | None]) -> float | None:
    numeric = [float(value) for value in values if value is not None]
    return min(numeric) if numeric else None


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no} is not valid JSON") from exc
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Stage40 ResidualSet Pilot",
        "",
        f"Generated: `{result['generated_at_utc']}`",
        f"Baseline: `{result['baseline']}`",
        f"Datasets: `{result['datasets']}`",
        f"Seeds: `{result['seeds']}`",
        f"Scope ready: `{result['aggregate']['scope_ready']}`",
        f"Any Phase1 candidate gate: `{result['aggregate']['any_phase1_candidate_gate']}`",
        "",
        "## Candidate Summary",
        "",
        "| Candidate | Positive datasets | Phase1 gate | Mean AURC reduction | Mean Risk@30 reduction | Min dataset AUROC delta | Min slice AUROC delta |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, row in result["aggregate"]["candidates"].items():
        lines.append(
            f"| `{name}` | {row['dataset_positive_count']}/{row['dataset_count']} | "
            f"{row['phase1_candidate_gate']} | {fmt(row['mean_aurc_reduction'])} | "
            f"{fmt(row['mean_risk_at_30_reduction'])} | {fmt(row['min_dataset_auroc_delta'])} | "
            f"{fmt(row['min_source_auroc_delta'])} |"
        )
    lines.extend(["", "## Dataset Scope", ""])
    for row in result["dataset_results"]:
        lines.append(
            f"- `{row['dataset']}`: status `{row['status']}`, groups `{row.get('source_item_groups')}`, "
            f"scope pass `{row.get('source_scope_pass')}`."
        )
    lines.extend(["", "## Claim Boundary", "", result["claim_boundary"], ""])
    return "\n".join(lines)


def fmt(value: float | None) -> str:
    if value is None:
        return "NA"
    return f"{value:.4f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--private", type=Path, default=DEFAULT_PRIVATE)
    parser.add_argument("--scored", type=Path, default=DEFAULT_SCORED)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--datasets", nargs="+", default=list(DEFAULT_DATASETS))
    parser.add_argument("--seeds", type=int, nargs="+", default=[17, 31, 47, 59, 71])
    parser.add_argument("--train-frac", type=float, default=0.60)
    parser.add_argument("--cal-frac", type=float, default=0.20)
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--hidden-dim", type=int, default=48)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--bootstrap-samples", type=int, default=200)
    parser.add_argument("--smoke-limit-groups", type=int, default=None)
    parser.add_argument("--min-source-item-groups", type=int, default=800)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_stage40_residualset_pilot(
        raw_path=args.raw,
        private_path=args.private,
        scored_path=args.scored,
        output_json=args.output_json,
        output_md=args.output_md,
        datasets=args.datasets,
        seeds=args.seeds,
        train_frac=args.train_frac,
        cal_frac=args.cal_frac,
        epochs=args.epochs,
        batch_size=args.batch_size,
        hidden_dim=args.hidden_dim,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        bootstrap_samples=args.bootstrap_samples,
        smoke_limit_groups=args.smoke_limit_groups,
        min_source_item_groups=args.min_source_item_groups,
        device_name=args.device,
    )
    print(
        json.dumps(
            {
                "aggregate": result["aggregate"],
                "output_json": str(args.output_json),
                "output_md": str(args.output_md),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
