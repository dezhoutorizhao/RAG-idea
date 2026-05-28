# RAG-idea 改进方案：CSRM-RAG 冲刺 NeurIPS Main Track / Spotlight

> 文件名：`RAG-idea改进.md`  
> 目标：把当前 CSRM-RAG / RAG-idea 从“强 bridge evidence”推进到“NeurIPS main track 级证据闭环”，并具备冲刺 spotlight 的展示强度。  
> 当前判断：方向有潜力，但现阶段不能以 near-perfect Hotpot/FEVER bridge 结果直接主张稳拿 NeurIPS。最大风险不是数值不够，而是审稿人可能质疑存在 oracle feature、label leakage、heuristic label shortcut，以及缺少 human-audited + end-to-end selective RAG 证据。

---

## 0. 一句话总策略

当前工作不要继续堆叠 oracle-structured bridge AUROC，而应把主线切换为：

> **leakage-free counterfactual orbit selective RAG**：在不使用 gold-derived 构造标签、不使用 support-key / is-support 等 oracle 特征的前提下，用 text-only verifier + human-audited labels + end-to-end RAG accepted-error risk 证明 CSRM 能在相同 verifier-call budget 下显著降低选择性 RAG 风险。

核心论文口号建议：

> **Single-set sufficiency is not orbit sufficiency.**

或者：

> **A query can look sufficient under the clean evidence set, yet be fragile over its counterfactual evidence-set orbit.**

---

## 1. 当前状态复盘

### 1.1 当前 idea

当前方向是 **CSRM-RAG: Counterfactual Set Risk Minimization for Selective RAG**。

核心假设：

> 单个 evidence set 的 sufficiency / relevance 高，并不意味着该 query 在 counterfactual perturbation orbit 下稳定可靠。稳健 RAG 需要评估一个 query 在多个反事实证据集合上的 sufficiency stability、answer consistency 和 orbit alignment，而不是只看 clean query 或单一证据集合。

当前不是完整复现并超越 CoRM-RAG，而是先基于 released CoRM critic 构建 counterfactual orbit bridge evaluation，验证 CSRM 是否比 clean-only、single-set sufficiency、naive orbit aggregation 更能识别 fragile RAG cases。

### 1.2 当前可以支持的 claim

当前可以谨慎主张：

1. CSRM 在 HotpotQA-derived counterfactual orbits 上显著优于 clean-only CoRM critic、SURE-style single-set sufficiency 和 naive orbit average。
2. CSRM 在 FEVER v3 near-miss counterfactual stress split 上也有 secondary bridge evidence。
3. shuffled perturbation ablation 崩掉，说明提升依赖正确的 orbit alignment，而不是简单增加 verifier 调用次数。
4. NLI cross-scorer probe 中 CSRM 仍保持方向性优势，说明信号不完全依赖原始 CoRM-derived features。
5. Hotpot-only conservative Clopper-Pearson risk-control pressure test 有正面 empirical signal，但不能推出 general formal guarantee。

### 1.3 当前不能支持的 claim

当前绝对不要主张：

1. 已完整复现 CoRM-RAG end-to-end retrieval-generation。
2. 已有 general formal risk-control guarantee。
3. 结果已经 human-audited。
4. robust RAG 被普遍解决。
5. 所有实验 all win。
6. 当前 bridge 结果本身已经足够稳拿 NeurIPS main track。

---

## 2. 当前实验结果与风险解释

### 2.1 HotpotQA Bridge 当前结果

| Method | AUROC | Risk@30 | AURC | 解释 |
|---|---:|---:|---:|---|
| CSRM | 0.9976 | 0.1669 | 0.4049 | 数值非常强，但存在 oracle/heuristic leakage 被质疑风险 |
| naive orbit average | 0.8321 | 0.5119 | 0.5829 | 多看 perturbations 有帮助，但简单平均不够 |
| clean-only CoRM | 0.5000 | 0.7497 | 0.7444 | clean-only 无法识别 orbit fragility |
| SURE-style single-set | 0.5000 | 0.7497 | 0.7375 | single-set sufficiency 不足 |
| shuffled perturbations | 0.0001 | 1.0000 | 0.9633 | orbit alignment 是必要机制 |

### 2.2 FEVER v3 Near-Miss Bridge 当前结果

| Method | AUROC | Risk@30 | AURC | 解释 |
|---|---:|---:|---:|---|
| CSRM | 1.0000 | 0.4444 | 0.5301 | 第二域 bridge 很强，但仍是 heuristic near-miss construction |
| naive orbit average | 0.7764 | 0.6407 | 0.7719 | 多 perturbation 平均不够 |
| clean-only CoRM | 0.5000 | 0.8333 | 0.8306 | clean-only 难以区分 |
| SURE-style single-set | 0.5000 | 0.8333 | 0.8264 | single-set 不够 |
| shuffled perturbations | 0.0327 | 1.0000 | 0.9778 | alignment 非常关键 |

### 2.3 NLI Cross-Scorer Probe 当前结果

| Method | AUROC | Risk@30 | AURC | 解释 |
|---|---:|---:|---:|---|
| CSRM | 0.7353 | 0.6267 | 0.6676 | 方向仍最好，但绝对强度中等 |
| naive orbit average | 0.4880 | 0.8600 | 0.7959 | 不稳定 |
| clean-only CoRM | 0.5244 | 0.7800 | 0.7838 | 较弱 |
| SURE-style single-set | 0.4818 | 0.8700 | 0.8202 | 较弱 |
| shuffled perturbations | 0.3281 | 0.9367 | 0.8921 | alignment 被破坏后明显下降 |

### 2.4 Paired bootstrap 当前证据

| 比较 | AUROC improvement 95% lower bound | Risk@30 reduction 95% lower bound | 解释 |
|---|---:|---:|---|
| Hotpot CSRM vs naive orbit average | 0.1379 | 0.2500 | bridge domain 上显著优于 naive aggregation |
| FEVER v3 CSRM vs naive orbit average | 0.1996 | 0.1056 | 第二域上也显著优于 naive aggregation |

### 2.5 Calibration / risk-control 当前负面证据

| Split | Empirical transfer | Formal guarantee | Target miss count | 结论 |
|---|---:|---:|---:|---|
| Hotpot CP | True | False | 0 | 只能作为 empirical pressure test |
| FEVER v3 CP | False | False | 2 | 不能写 general risk-control guarantee |

---

## 3. 审稿人最可能攻击的问题

### 3.1 致命风险：oracle feature / label leakage

当前 bridge 构造中可能存在以下被审稿人质疑的路径：

1. Hotpot orbit builder 从 `supporting_facts` 构造 support docs。
2. 文档内可能带有 `is_support`、`has_answer`、`support_key` 等 gold-derived metadata。
3. CSRM critic 可能使用 support、conflict、missing、answer consistency、support signature 等特征。
4. 如果这些特征间接或直接来自 gold supporting facts / construction metadata，则 near-perfect AUROC 会被质疑为 shortcut。

审稿人会问：

> CSRM 到底是在识别真实 RAG fragility，还是在读取由构造过程泄漏出来的 oracle structure？

因此，**leakage-free v4 pipeline 是最高优先级**。

### 3.2 Human audit 为空

当前 audit pack 已准备，但人工标注未完成：

- audit_sample_100_v3 labeled = 0
- completion_rate = 0.0

这意味着：

1. 不能说 human-audited。
2. 不能把 heuristic labels 当最终 semantic ground truth。
3. 当前结果只能叫 structural / bridge evidence。

### 3.3 End-to-end RAG 证据缺失

当前 full CoRM-RAG reproduction 未完成，缺失：

- `wiki.faiss`
- `wiki_passages.jsonl`
- `biased_nq_test.jsonl`
- local `faiss`
- local `vllm`

这使得论文不能强 claim：

> CSRM improves real end-to-end RAG generation.

必须补 end-to-end selective RAG 证据，或者诚实地将论文定位为 human-audited orbit benchmark + selective risk detector。

### 3.4 Baseline 强度不足

当前 baseline 中 clean-only CoRM、SURE-style single-set、naive orbit average 对机制有帮助，但不足以说服 NeurIPS reviewer。

需要补充：

1. faithful / official CoRM-RAG baseline。
2. faithful SURE-style multi-evidence sufficiency baseline。
3. sufficient-context classifier baseline。
4. RC-RAG / conformal / risk-control abstention baseline。
5. LLM-as-judge / self-consistency baseline。
6. equal-budget orbit ensemble baseline。
7. retrieval-order / stability baseline。

### 3.5 Formal risk-control claim 当前不成立

FEVER v3 CP 失败，formal guarantee 两域都不成立。因此：

- 不能把 calibration/risk guarantee 当主贡献。
- 应改写为 empirical selective-risk ranking / coverage-risk reduction。
- 若要写理论，只能在明确 exchangeability assumptions 下给 conditional result。

---

## 4. 总体改进路线图

### 4.1 主线优先级

| 优先级 | 改进项 | 目标 | 是否必须 |
|---:|---|---|---|
| P0 | leakage-free v4 pipeline | 排除 oracle/label leakage | 必须 |
| P0 | feature firewall + anti-shortcut tests | 证明不是 metadata shortcut | 必须 |
| P0 | human audit | 把 heuristic label 转为 human-audited semantic evidence | 必须 |
| P0 | strong baselines | 避免只赢弱 baseline | 必须 |
| P1 | end-to-end selective RAG | 证明对真实 RAG answer quality 有用 | 强烈建议 |
| P1 | calibrated orbit risk model | 从 fixed rule 提升为 calibrated risk estimator | 强烈建议 |
| P1 | theory module | 提升 novelty 与可解释性 | 强烈建议 |
| P2 | case study gallery | 冲 spotlight 的直观证据 | 建议 |
| P2 | artifact-grade packaging | 提高 reproducibility 分数 | 必须但可后置 |

### 4.2 重新定义 paper 主 claim

建议主 claim：

> We identify counterfactual sufficiency instability as a distinct selective RAG failure mode. We propose CSRM, an aligned orbit-level risk scoring method that estimates whether a query remains answerable and semantically stable over counterfactual evidence-set orbits. On leakage-free, human-audited orbits and end-to-end selective RAG, CSRM reduces accepted-answer risk under equal verifier-call budget compared with CoRM/SURE/context-sufficiency/LLM baselines.

不要写：

- We solve robust RAG.
- We provide general formal risk control.
- We fully reproduce and outperform CoRM-RAG end-to-end, unless full reproduction is actually完成。
- Our labels are human-audited, unless audit 完成。

---

## 5. 应该新增的模块

## 5.1 新增模块 A：Leakage-Free Orbit Pipeline v4

### 5.1.1 目的

消除所有 oracle / gold-derived feature 泄漏，让 CSRM 的输入只来自模型实际可见的信息。

### 5.1.2 新增数据结构

建议新增两个严格分离的数据结构：

```text
OrbitRaw:
  orbit_id
  source_item_group_id
  query
  candidate_answer
  retrieved_passages
  retrieval_scores
  perturbation_texts
  generator_outputs
  verifier_outputs

OrbitPrivateEvalOnly:
  orbit_id
  source_item_group_id
  gold_answer
  gold_supporting_facts
  gold_evidence_ids
  construction_type
  perturbation_type
  heuristic_label
  human_label
  adjudicated_label
  support_key
  is_support
  has_answer
```

规则：

1. `OrbitRaw` 可以进入 CSRM、baseline、calibration、threshold selection。
2. `OrbitPrivateEvalOnly` 只能进入 evaluator，不能进入任何 scorer。
3. scorer 输入中出现以下字段必须直接报错：
   - `gold`
   - `support_key`
   - `is_support`
   - `has_answer`
   - `label`
   - `heuristic_label`
   - `human_label`
   - `perturbation_type`
   - `construction_type`
   - `source_split`
   - `near_miss_type`

### 5.1.3 新增代码建议

新增文件：

```text
src/csrm_rag/data_schema.py
src/csrm_rag/feature_firewall.py
src/csrm_rag/orbit_v4.py
experiments/build_hotpot_orbits_v4.py
experiments/build_fever_orbits_v4.py
experiments/validate_leakage_free_orbits.py
tests/test_feature_firewall.py
tests/test_orbit_private_fields_never_seen_by_scorer.py
```

### 5.1.4 Feature firewall 伪代码

```python
FORBIDDEN_KEYS = {
    "gold", "gold_answer", "gold_supporting_facts", "gold_evidence_ids",
    "support_key", "is_support", "has_answer", "label",
    "heuristic_label", "human_label", "adjudicated_label",
    "perturbation_type", "construction_type", "near_miss_type",
}


def assert_no_forbidden_features(obj, path="root"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in FORBIDDEN_KEYS:
                raise ValueError(f"Forbidden oracle feature at {path}.{k}")
            assert_no_forbidden_features(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            assert_no_forbidden_features(v, f"{path}[{i}]")
```

### 5.1.5 成功标准

| 检查项 | 成功标准 |
|---|---|
| scorer 输入检查 | 任何 oracle field 出现即 fail |
| train/calibration/test split | 按 `source_item_group_id` group split |
| metadata-only classifier | AUROC 接近随机，不能显著高于 0.55 |
| oracle-feature ablation | 移除 oracle 后 CSRM 仍优于 strongest baseline |
| shuffled alignment | 仍明显崩掉，证明 alignment 必要 |

---

## 5.2 新增模块 B：Text-Only Verifier / Independent Semantic Scorer

### 5.2.1 目的

让 support、conflict、missing、sufficiency 等信号来自文本判断，而不是来自 gold construction metadata。

### 5.2.2 Verifier 类型

| Verifier | 用途 | 是否进入主方法 | 注意事项 |
|---|---|---:|---|
| NLI cross-encoder | 自动语义 entailment / contradiction / neutral | 是 | 主线之一，便宜可复现 |
| LLM judge | 强语义评估 / audit 辅助 | 可作为 baseline 或评估 | 避免用同一个 LLM 同时生成和评估 |
| Learned sufficiency verifier | 最终方法组件 | 是 | 必须在 disjoint data 上训练 |
| Human adjudication | 最终 label | 否，评估专用 | 不进入模型输入 |

### 5.2.3 新增特征

在 leakage-free 条件下，CSRM 可使用：

```text
clean_sufficiency
min_sufficiency_over_orbit
mean_sufficiency_over_orbit
sufficiency_variance
max_conflict_over_orbit
answer_consistency_over_orbit
support_signature_consistency_from_text_only_verifier
retrieval_overlap
verifier_entropy
generator_answer_entropy
claim_entailment_score
claim_contradiction_score
```

不可使用：

```text
gold support id
support_key
is_support
has_answer
constructed fragile/stable label
near-miss type
source split label
```

### 5.2.4 新增代码建议

```text
src/csrm_rag/verifiers/base.py
src/csrm_rag/verifiers/nli.py
src/csrm_rag/verifiers/llm_judge.py
src/csrm_rag/verifiers/sufficiency.py
experiments/score_orbits_textonly_v4.py
experiments/compare_verifier_sources_v4.py
tests/test_verifier_outputs_are_text_only.py
```

### 5.2.5 成功标准

1. NLI/text-only scorer 下 CSRM 仍优于 naive orbit average、single-set sufficiency、clean-only CoRM。
2. LLM judge 与 NLI 的 ranking 有中等以上相关性，但不要求完全一致。
3. Human labels 上，text-only CSRM 的 Risk@30 / Risk@50 显著优于 strongest baseline。
4. 不追求 AUROC 接近 1.0；human-audited AUROC 0.78–0.86 且跨域稳定，比 heuristic AUROC 0.99 更有说服力。

---

## 5.3 新增模块 C：Human Audit v4

### 5.3.1 目的

把当前 structural / heuristic labels 转换为 human-audited semantic ground truth。

### 5.3.2 标注任务定义

每个 orbit 给标注者展示：

1. query；
2. candidate answer；
3. clean evidence set；
4. counterfactual evidence sets；
5. model-generated answers；
6. 不展示 construction type、gold support id、heuristic label、CSRM score。

标注者给出 orbit-level label：

| Label | 含义 |
|---|---|
| stable_answerable | 在 orbit 内证据变化下仍足以支持同一正确答案 |
| fragile | clean set 看似足够，但 perturbation 后答案不稳定、证据缺失或冲突 |
| unanswerable | 原始证据整体不足以回答 |
| ambiguous | 问题或证据本身存在多义性，无法确定 |
| annotation_error | 数据构造或展示存在明显错误 |

### 5.3.3 标注规模

| 目标 | 最低 main-track 规格 | Spotlight 冲刺规格 |
|---|---:|---:|
| pilot | 100 orbits | 200 orbits |
| final | 1000 orbits | 2000–3000 orbits |
| annotators | 2 blind annotators + adjudicator | 3 annotators + adjudicator |
| agreement | Cohen’s κ / Gwet AC1 ≥ 0.65 | ≥ 0.75 |
| ambiguous rate | < 15% | < 10% |

### 5.3.4 新增代码建议

```text
annotation/README.md
annotation/guidelines_v4.md
annotation/label_schema_v4.json
annotation/export_blind_audit_pack_v4.py
annotation/merge_audit_labels_v4.py
annotation/adjudicate_labels_v4.py
annotation/compute_agreement_v4.py
annotation/audit_card_template.md
results/human_audit_v4/
```

### 5.3.5 Human audit 主表

| Dataset | Label source | Methods | Metrics |
|---|---|---|---|
| Hotpot-orbit-v4 | adjudicated human labels | CSRM, CoRM, SURE, context-sufficiency, LLM judge, equal-budget ensemble | AUROC, AUPRC, AURC, Risk@30/50/70 |
| FEVER-orbit-v4 | adjudicated human labels | 同上 | 同上 |
| NQ/Biased-NQ or TruthfulQA | human/trusted labels | 同上 | 同上 |

### 5.3.6 成功标准

1. Human-audited labels 上 CSRM 显著优于 strongest baseline。
2. Paired / cluster bootstrap 的 95% lower bound > 0。
3. 公开 disagreement taxonomy。
4. 报告 heuristic label 与 human label 的 mismatch rate。
5. 如果 heuristic mismatch > 15–20%，必须把当前 bridge 结果降级到 appendix。

---

## 5.4 新增模块 D：End-to-End Selective RAG Evaluation

### 5.4.1 目的

证明 CSRM 不只是 offline detector，而是真的能降低真实 RAG accepted-answer error。

### 5.4.2 Pipeline

```text
query
  -> retriever retrieves top-k passages
  -> generator produces answer
  -> verifier computes clean + orbit features
  -> CSRM scores risk
  -> selective policy accepts or abstains
  -> evaluator computes accepted-answer error / coverage-risk curve
```

### 5.4.3 数据集建议

| Dataset | 用途 | 备注 |
|---|---|---|
| HotpotQA | 多跳 QA / bridge reasoning | 保留，但必须 v4 leakage-free |
| FEVER | factual verification / evidence grounding | 保留，但 human audit 必须补 |
| NQ / Biased-NQ | 与 CoRM-RAG 对齐 | full reproduction 若做成则很强 |
| TruthfulQA | hallucination / truthfulness pressure | 可作为第三域 |

### 5.4.4 Retriever / Generator 组合

| 类型 | 最低配置 | 冲刺配置 |
|---|---|---|
| Retriever | BM25 + dense retriever | BM25 + dense + hybrid |
| Dense model | Contriever / BGE / E5 任一 | 至少两个 dense retriever |
| Generator | 2 个开源 LLM | 2–3 个开源 LLM + 一个 closed judge 只评估 |
| Inference | greedy 或固定 sampling | 报告 temperature / seed / prompt |

### 5.4.5 Metrics

必须报告：

```text
accepted-answer error
coverage
risk@coverage
AURC
selective accuracy
answer EM/F1/accuracy
calibration ECE / Brier
abstention rate
verifier-call budget
latency / cost
```

### 5.4.6 主图建议

1. Risk–coverage curve：相同 coverage 下 CSRM risk 更低。
2. Coverage at target risk：相同 risk target 下 CSRM coverage 更高。
3. Accepted-answer error bar chart：CSRM 显著降低被接受答案中的错误率。

### 5.4.7 新增代码建议

```text
src/csrm_rag/end2end/
  retrievers.py
  generators.py
  selective_policy.py
  evaluator.py
experiments/run_end2end_selective_rag.py
experiments/evaluate_coverage_risk.py
experiments/plot_risk_coverage_curves.py
configs/end2end_hotpot.yaml
configs/end2end_fever.yaml
configs/end2end_nq.yaml
```

### 5.4.8 成功标准

1. 至少 2 个 dataset、2 个 generator 上成立。
2. 相同 coverage 下，accepted-error risk 显著低于 strongest baseline。
3. 相同 risk target 下，coverage 高于 strongest baseline。
4. equal verifier-call budget 下比较，不允许 CSRM 靠更多 API / verifier calls 取胜。

---

## 5.5 新增模块 E：Strong Baselines

### 5.5.1 目的

避免 reviewer 认为 CSRM 只赢了弱 baseline。

### 5.5.2 必须新增或强化的 baseline

| Baseline | 目标 | 实现要求 |
|---|---|---|
| faithful CoRM-RAG | 与参考工作正面对齐 | 不只是 clean-only score；尽量复现 risk-aware inference |
| faithful SURE-style | 与 sufficiency 方法正面对齐 | multi-evidence sufficiency、missing、conflict aggregation |
| context sufficiency classifier | 判断 context 是否足够回答 | 作为强 single-set / set-level baseline |
| LLM judge | 强语义判断 baseline | 同等输入，同等预算 |
| self-consistency | 检查是否只是 answer consistency | 多采样生成答案再聚合 |
| equal-budget orbit ensemble | 检查是否只是多看 perturbations | min/mean/quantile/logistic aggregation |
| retrieval stability baseline | 检查是否只是 retrieval-order robustness | 对 retrieval order / top-k perturbation 稳定性建模 |
| calibrated logistic baseline | 检查 fixed CSRM formula 是否必要 | 同特征 + 简单校准模型 |

### 5.5.3 新增代码建议

```text
src/csrm_rag/baselines/
  corm_faithful.py
  sure_faithful.py
  context_sufficiency.py
  llm_judge.py
  self_consistency.py
  equal_budget_ensemble.py
  retrieval_stability.py
  calibrated_logistic.py
experiments/run_all_baselines_v4.py
experiments/compare_equal_budget_v4.py
```

### 5.5.4 Baseline 公平性要求

1. 输入相同：不得给 CSRM 更多 gold-free 信息。
2. budget 相同：verifier-call 数、LLM judge call 数、retrieved passages 数一致。
3. split 相同：source item group split。
4. threshold selection 相同：统一在 calibration split 上选阈值。
5. 报告失败 baseline，不删除负面结果。

---

## 5.6 新增模块 F：Calibrated Orbit Risk Model

### 5.6.1 目的

当前 CSRM 更像 fixed weighted rule。NeurIPS reviewer 可能质疑：为什么这些权重？为什么不是 logistic regression / isotonic / gradient boosting？

建议把方法分为三层：

1. **CSRM-Rule**：当前可解释 fixed rule。
2. **CSRM-Calibrated**：在 calibration split 上学习 monotonic calibrated risk。
3. **CSRM-Minimax**：理论解释版本，用 worst-case orbit risk 表达。

### 5.6.2 CSRM-Calibrated 特征

```text
clean_sufficiency
min_sufficiency
mean_sufficiency
sufficiency_variance
max_conflict
answer_consistency
support_signature_consistency
retrieval_overlap
verifier_entropy
generator_answer_entropy
clean_to_worst_gap
orbit_answer_flip_rate
```

### 5.6.3 模型选择

| 模型 | 优点 | 风险 |
|---|---|---|
| Logistic regression | 简洁，可解释 | 非线性不足 |
| Isotonic regression | calibration 强 | 维度高时不稳定 |
| Monotonic GBM | 表达力强，可加单调约束 | 需要严格防过拟合 |
| Conformal wrapper | 可做 empirical risk pressure test | 不能乱写 general guarantee |

### 5.6.4 新增代码建议

```text
src/csrm_rag/calibration/orbit_risk_model.py
src/csrm_rag/calibration/monotonic_constraints.py
src/csrm_rag/calibration/isotonic.py
experiments/train_csrm_calibrated_v4.py
experiments/evaluate_calibration_v4.py
```

### 5.6.5 成功标准

1. CSRM-Calibrated 不明显过拟合，跨 seed / cross-domain 稳定。
2. CSRM-Rule 仍作为可解释版本存在。
3. Calibration 指标 ECE / Brier 优于 uncalibrated baselines。
4. 不把 calibration 写成 formal guarantee，除非理论假设和 empirical validation 都闭合。

---

## 5.7 新增模块 G：Shortcut / Anti-Leakage Probe

### 5.7.1 目的

主动证明结果不是 shortcut。

### 5.7.2 必做 probes

| Probe | 输入 | 目的 | 预期 |
|---|---|---|---|
| metadata-only classifier | doc count、passage length、retrieval score、position | 检查浅层统计 shortcut | 接近随机 |
| forbidden-feature classifier | oracle fields | sanity upper bound | 高，但只作为泄漏示范 |
| source-item group split | 按原问题分组 | 防止同一问题泄漏 | 主结果仍成立 |
| hard negative matching | 匹配长度、doc 数、answer overlap | 防止长度/overlap shortcut | 主结果仍成立 |
| shuffled orbit alignment | 打乱 orbit 对齐 | 检查 alignment 必要 | 性能明显崩掉 |
| random perturbation labels | 随机标签 | 检查 pipeline 是否过拟合 | 接近随机 |

### 5.7.3 新增代码建议

```text
experiments/probe_metadata_shortcuts_v4.py
experiments/probe_oracle_feature_upper_bound.py
experiments/probe_group_split_robustness.py
experiments/probe_hard_negative_matching.py
experiments/probe_random_label_sanity.py
```

### 5.7.4 成功标准

1. metadata-only AUROC 不应显著高于 0.55。
2. group split 后 CSRM 仍优于 strongest baseline。
3. hard-negative matched set 上仍有显著 improvement。
4. shuffled orbit 明显下降，证明 alignment 不是装饰。

---

## 5.8 新增模块 H：Theory / Formalization

### 5.8.1 目的

把 novelty 从“工程组合”提升为“明确 failure mode + 必要信号”。

### 5.8.2 建议理论命题

#### Proposition 1：Clean sufficiency does not imply orbit sufficiency

存在两个 query-orbit：

```text
(q1, O1), (q2, O2)
```

它们在 clean evidence set 上具有相同 sufficiency score：

```text
s(q1, S_clean1) = s(q2, S_clean2)
```

但 orbit risk 不同：

```text
R_orbit(q1, O1) != R_orbit(q2, O2)
```

因此任何只依赖 clean set 的 scorer 都无法区分二者。

#### Proposition 2：Single-set sufficiency is insufficient under counterfactual instability

存在两个 orbits，其任一单集合 sufficiency 分布均值相近，但 answer-consistency / worst-case sufficiency 不同，从而 selective risk 不同。naive average 无法稳定区分，CSRM 的 worst-case + consistency 结构提供额外信息。

#### Proposition 3：Orbit alignment is necessary

如果 perturbation 与 evidence-set alignment 被随机打乱，则 answer/support consistency 的估计变成有偏或无效，risk ranking 退化。

### 5.8.3 公式建议

Orbit risk：

```text
R_orbit(q) = E_{S ~ O(q)}[loss(f(q, S), y)] + lambda * max_{S in O(q)} loss(f(q, S), y)
```

CSRM score：

```text
CSRM(q, O) =
  alpha * min_i suff(q, S_i)
  + beta * consistency(a_1, ..., a_k)
  - gamma * max_i conflict(q, S_i)
  + delta * alignment(q, O)
```

Selective policy：

```text
accept(q) = 1[CSRM(q, O) >= tau]
```

### 5.8.4 新增内容位置

```text
paper/sections/formalization.tex
paper/sections/theory.tex
appendix/proofs.tex
```

---

## 5.9 新增模块 I：Case Study Gallery / Failure Taxonomy

### 5.9.1 目的

冲 spotlight 需要不只是表格，还要让 reviewer 直观看到 failure mode 很真实、很重要。

### 5.9.2 核心图

建议 Figure 1：

```text
Clean sufficiency is misleading.
```

横轴：clean / single-set sufficiency score  
纵轴：human-audited orbit failure rate  
颜色：CSRM risk score

预期图像：

1. 很多 clean sufficiency 高分样本在 orbit 上仍 fragile。
2. CSRM 能把这些 high-clean / high-risk 的点挑出来。
3. SURE / clean-only / naive average 对这些点不敏感。

### 5.9.3 Case study 格式

每个 case 展示：

```text
Query
Candidate answer
Clean evidence
Counterfactual evidence set 1
Counterfactual evidence set 2
Generator answer under each evidence set
Clean-only score
SURE/context score
Naive orbit average
CSRM score
Human label
Why fragile
```

### 5.9.4 Failure taxonomy

| Failure type | 含义 |
|---|---|
| missing-hop fragility | 一个 hop 在 perturbation 中缺失导致答案不稳定 |
| distractor-supported answer | distractor 看似支持错误答案 |
| answer alias flip | 语义等价或别名导致模型误判 |
| evidence conflict | 反事实证据与 clean evidence 冲突 |
| retrieval-order instability | 检索顺序变化导致 answer flip |
| bridge-entity ambiguity | 多跳 bridge entity 不唯一 |
| overconfident unsupported answer | 生成器给出自信但证据不足答案 |

### 5.9.5 新增代码建议

```text
experiments/export_case_studies_v4.py
experiments/build_failure_taxonomy_report.py
paper/figures/clean_sufficiency_misleading.py
paper/case_studies/
```

---

## 5.10 新增模块 J：Artifact-Grade Reproducibility

### 5.10.1 目的

提升 NeurIPS checklist / artifact reviewer 信任度。

### 5.10.2 建议仓库结构

```text
RAG-idea/
  README.md
  LICENSE
  CITATION.cff
  environment.yml
  Dockerfile
  pyproject.toml
  configs/
    hotpot_v4.yaml
    fever_v4.yaml
    nq_v4.yaml
    end2end_hotpot.yaml
    end2end_fever.yaml
  src/csrm_rag/
    data_schema.py
    feature_firewall.py
    orbit_v4.py
    verifiers/
    baselines/
    calibration/
    end2end/
  experiments/
    run_main_hotpot_v4.py
    run_main_fever_v4.py
    run_human_audit_eval_v4.py
    run_end2end_selective_rag.py
    run_all_baselines_v4.py
  annotation/
    guidelines_v4.md
    label_schema_v4.json
  scripts/
    run_smoke.sh
    run_main_tables.sh
    run_end2end.sh
    run_all_ablations.sh
  results/
    main/
    ablations/
    human_audit/
    end2end/
  data_cards/
  audit_cards/
  reproducibility/
    checksums.json
    seeds.json
    hardware.md
    artifact_manifest.md
  tests/
```

### 5.10.3 必须具备

1. one-command smoke test。
2. one-command main table reproduction。
3. fixed seeds。
4. exact checkpoint hashes。
5. dataset construction hash。
6. no hidden local path。
7. no unavailable artifact silently required。
8. CI 跑 unit tests + smoke tests。
9. `results/README.md` 说明每个表来自哪个脚本。
10. `CLAIMS_LEDGER.md` 逐条列出 claim 与 supporting evidence。

---

## 6. 应该删除、降级或移出主线的模块 / 方法

## 6.1 从主 claim 删除：general formal risk-control guarantee

### 当前问题

- Hotpot CP formal guarantee = False。
- FEVER v3 empirical transfer = False。
- FEVER v3 target_miss_count = 2。
- general formal guarantee 当前不成立。

### 处理方式

| 当前写法 | 修改后写法 |
|---|---|
| CSRM provides formal risk control | CSRM improves empirical selective-risk ranking under audited evaluation |
| distribution-free guarantee | empirical pressure test under stated assumptions |
| calibrated risk guarantee | calibrated score / selective thresholding |

### 模块处置

- calibration / CP scripts 保留。
- 从主贡献降级为 appendix / limitation / pressure test。
- 只在明确 exchangeability assumption 和验证 split 成立时写 conditional result。

---

## 6.2 从 scorer 输入中删除：oracle / gold-derived fields

### 必须删除或隔离的字段

```text
support_key
is_support
has_answer
gold_supporting_facts
gold_evidence_ids
heuristic_label
construction_type
perturbation_type
near_miss_type
source_split
```

### 处理方式

1. 这些字段可以保留在 `OrbitPrivateEvalOnly`。
2. 不能进入 CSRM scorer、baseline、calibration、threshold selection。
3. 所有 scorer 前调用 `assert_no_forbidden_features()`。
4. tests 中构造含 forbidden field 的假输入，确认 scorer 报错。

---

## 6.3 将当前 Hotpot / FEVER near-perfect 结果从主表降级

### 当前问题

Hotpot AUROC=0.9976、FEVER AUROC=1.0000 很强，但容易被怀疑 shortcut。

### 处理方式

主文中改为：

> Oracle-structured bridge sanity check.

放在 appendix 或 preliminary evidence 中。

主表改用：

1. leakage-free v4 text-only features；
2. human-audited labels；
3. end-to-end selective RAG accepted-error risk。

---

## 6.4 删除或替换弱化的 SURE-style single-set baseline

### 当前问题

当前 SURE-style single-set baseline 接近随机，但 reviewer 可能认为这是弱化版，不代表真实 SURE-RAG。

### 处理方式

| 当前模块 | 处理 |
|---|---|
| SURE-style single-set weak baseline | 保留为 ablation/control |
| faithful SURE-style multi-evidence baseline | 新增，作为主 baseline |

论文中不要写：

> CSRM beats SURE-RAG.

除非实现足够忠实并在相同 budget 下比较。

---

## 6.5 降级 clean-only CoRM critic

### 当前问题

clean-only CoRM AUROC=0.5，但这不能说明 CoRM-RAG 本身无效，只说明 clean-only 使用方式不足。

### 处理方式

1. clean-only CoRM 保留为 control baseline。
2. 新增 faithful CoRM / released CoRM critic + risk-aware inference。
3. 论文措辞改为：

> Clean-only use of the CoRM critic cannot detect counterfactual orbit fragility in our bridge setting.

不要写：

> CoRM-RAG fails.

---

## 6.6 删除“full CoRM reproduction 已完成”的任何暗示

### 当前问题

full reproduction 缺关键 artifact 与工程环境。

### 处理方式

论文和 README 中必须明确：

```text
We do not claim full CoRM-RAG end-to-end reproduction unless the missing Wikipedia FAISS / passages / Biased-NQ / vLLM / FAISS environment is completed.
```

如果继续推进 full reproduction，需要：

1. reliable ext4/XFS storage ≥ 180GB，最好 250GB+；
2. 修复 `/mnt/ntfs-disk` 写入失败；
3. 完成 sharded `wiki_passages` 和 FAISS index；
4. materialize `biased_nq_test.jsonl`；
5. 跑 full retrieval-generation evaluation。

---

## 6.7 删除“human-audited”表述直到标注完成

### 当前问题

audit_sample_100_v3 labeled = 0。

### 处理方式

| 当前可能表述 | 修改后 |
|---|---|
| human-audited results | audit pack prepared; labels pending |
| semantic ground truth | heuristic structural labels |
| human evaluation confirms | human evaluation planned / pending |

---

## 6.8 删除“all-win / solve robust RAG”式语言

### 当前问题

存在负面证据：

1. FEVER risk-control 不支持 empirical transfer。
2. NLI cross-scorer AUROC 只有 0.7353。
3. human audit 未完成。
4. full end-to-end reproduction 未完成。

### 处理方式

改为边界清晰的 claim：

> CSRM identifies a distinct failure mode and empirically reduces selective risk in leakage-free, human-audited orbit evaluation and end-to-end selective RAG experiments.

---

## 7. 应该保留但重新定位的模块

### 7.1 保留 CSRM core scoring

保留原因：

1. 当前 bridge 结果强。
2. shuffled perturbation 崩掉支持 orbit alignment 必要性。
3. no answer consistency 消融显示 answer/support consistency 有作用。

重新定位：

- 作为 **CSRM-Rule** 的可解释版本。
- 不作为唯一最终模型。
- 与 **CSRM-Calibrated** 并列。

### 7.2 保留 naive orbit average

保留原因：

- 它是最重要的 “多看 perturbation 是否足够” 对照。

定位：

- internal ablation / equal-budget naive aggregation baseline。

### 7.3 保留 shuffled perturbations

保留原因：

- 当前最强机制证据之一。
- 证明 orbit alignment 不是装饰。

定位：

- 必须在 leakage-free + human-audited v4 下重跑。

### 7.4 保留 NLI cross-scorer

保留原因：

- 能证明信号不完全依赖 CoRM-derived scorer。

重新定位：

- 从 probe 升级为 text-only verifier 主线之一。
- 但不能替代 human audit。

### 7.5 保留 structural audits

保留原因：

- 证明构造没有明显 schema/provenance 错误。

重新定位：

- artifact / reproducibility evidence。
- 不能替代 human semantic label。

---

## 8. 具体文件级改造建议

### 8.1 `experiments/build_hotpot_orbits.py`

当前问题：可能把 support facts 构造信息与模型可见信息混在一起。

建议：

1. 改为 `build_hotpot_orbits_v4.py`。
2. 输出两个文件：

```text
hotpot_orbits_v4.raw.jsonl
hotpot_orbits_v4.private_eval.jsonl
```

3. raw 文件只含 query、passages、retrieval scores、candidate answer。
4. private 文件才含 gold/support/heuristic label。
5. 所有后续 scorer 只读 raw 文件。

### 8.2 `experiments/build_fever_orbits.py`

建议同 Hotpot：

```text
fever_orbits_v4.raw.jsonl
fever_orbits_v4.private_eval.jsonl
```

额外建议：

1. 对 near-miss construction 加 human audit。
2. 明确 FEVER label 是 claim verification label，不要偷换成 QA answerability。
3. 对 SUPPORTS / REFUTES / NOT ENOUGH INFO 分别报告。

### 8.3 `src/csrm_rag/critic.py`

建议拆分：

```text
src/csrm_rag/critic_rule.py
src/csrm_rag/critic_calibrated.py
src/csrm_rag/features.py
src/csrm_rag/feature_firewall.py
```

必须修改：

1. scorer 开始处调用 feature firewall。
2. 不读取任何 private eval fields。
3. 明确每个 feature 的来源：retriever / generator / verifier / aggregation。
4. 输出 feature attribution，便于 audit。

### 8.4 `experiments/score_orbits_nli.py`

建议升级为：

```text
experiments/score_orbits_textonly_v4.py
```

新增功能：

1. 支持多个 NLI/verifier 模型。
2. 输出 verifier entropy。
3. 输出 support/conflict/missing 的 text-only estimates。
4. 记录模型 checkpoint hash。
5. 记录 prompt / preprocessing / max length。

### 8.5 `experiments/score_orbits_corm.py`

建议保留，但降级为：

1. bridge scoring module；
2. CoRM-derived control；
3. 不作为唯一主 scorer。

如果要主表使用 CoRM，需要实现 faithful CoRM-RAG risk-aware baseline。

### 8.6 `results/claims_verification.json` 与 `CLAIMS_LEDGER.json`

建议新增 claim 分级：

```text
SUPPORTED_MAIN
SUPPORTED_APPENDIX
SUPPORTED_BRIDGE_ONLY
PENDING_HUMAN_AUDIT
PENDING_END2END
UNSUPPORTED_DO_NOT_CLAIM
```

把当前 claim 改为：

| Claim | 状态 |
|---|---|
| CSRM improves bridge orbit ranking under CoRM-derived scoring | SUPPORTED_APPENDIX |
| CSRM improves text-only NLI probe directionally | SUPPORTED_BRIDGE_ONLY |
| CSRM has human-audited semantic advantage | PENDING_HUMAN_AUDIT |
| CSRM improves end-to-end selective RAG | PENDING_END2END |
| CSRM gives general risk-control guarantee | UNSUPPORTED_DO_NOT_CLAIM |
| Full CoRM-RAG reproduction completed | UNSUPPORTED_DO_NOT_CLAIM |

---

## 9. 新的主实验矩阵

## 9.1 Main Table 1：Leakage-free human-audited orbit fragility detection

| Dataset | Label | Methods | Metrics |
|---|---|---|---|
| Hotpot-orbit-v4 | adjudicated human | CSRM-Rule, CSRM-Calibrated, faithful CoRM, faithful SURE, context sufficiency, LLM judge, self-consistency, equal-budget ensemble | AUROC, AUPRC, AURC, Risk@30/50/70 |
| FEVER-orbit-v4 | adjudicated human | 同上 | 同上 |
| NQ/Biased-NQ or TruthfulQA | human/trusted | 同上 | 同上 |

成功门槛：

1. CSRM-Calibrated 或 CSRM-Rule 至少一个显著优于 strongest non-CSRM baseline。
2. paired / cluster bootstrap 95% lower bound > 0。
3. 至少两个数据域成立。

## 9.2 Main Table 2：End-to-end selective RAG

| Dataset | Retriever | Generator | Methods | Metrics |
|---|---|---|---|---|
| HotpotQA | BM25 | LLM-1 | vanilla RAG, CoRM, SURE, context-suff, LLM judge, CSRM | accepted-error, coverage, AURC, EM/F1 |
| HotpotQA | Dense | LLM-1 | 同上 | 同上 |
| FEVER | BM25/Dense | LLM-1 | 同上 | accuracy/error/coverage |
| NQ/TruthfulQA | Dense | LLM-2 | 同上 | accepted-error/coverage |

成功门槛：

1. 相同 coverage 下 CSRM accepted-error risk 更低。
2. 相同 risk target 下 CSRM coverage 更高。
3. 不依赖单一 retriever 或 generator。

## 9.3 Main Table 3：Mechanism ablation

| Ablation | 目的 | 预期 |
|---|---|---|
| no answer consistency | 检验 answer/support consistency | 性能下降 |
| no worst-case sufficiency | 检验 worst-case 组件 | 性能下降 |
| no conflict term | 检验 conflict signal | 部分数据下降 |
| no alignment | 检验 orbit alignment | 明显崩掉 |
| first perturbation only | 检查是否需要 full orbit | 不如 full orbit |
| random/shuffled perturbations | 检查 alignment | 崩掉 |
| equal-call naive ensemble | 检查是否只是多调用 | 不如 CSRM |
| no oracle features | 检查 leakage | 仍保留核心提升 |

## 9.4 Main Table 4：Anti-shortcut probes

| Probe | Metric | 通过标准 |
|---|---|---|
| metadata-only classifier | AUROC | ≤ 0.55 或不显著 |
| length/doc-count matched set | CSRM improvement | lower bound > 0 |
| group split | CSRM improvement | lower bound > 0 |
| random label sanity | AUROC | 接近 0.5 |
| oracle-feature upper bound | AUROC | 可高，但标为 leakage upper bound |

---

## 10. Spotlight 冲刺增强项

### 10.1 必须有一个杀手级图

Figure 1：Clean sufficiency is misleading。

图中展示：

1. clean/single-set sufficiency 高不等于 orbit stable。
2. human-audited orbit failure rate 随 CSRM risk 明显变化。
3. CSRM 能识别 clean-only / SURE 接收但实际 fragile 的样本。

### 10.2 必须有高质量 case studies

至少 6–8 个 case：

1. clean evidence 看起来足够；
2. SURE/context sufficiency 接收；
3. generator 给出自信答案；
4. counterfactual evidence replacement 后答案 flip 或支持链断裂；
5. CSRM 拒绝；
6. human audit 判为 fragile。

### 10.3 必须有清晰 failure taxonomy

把 CSRM 捕捉的 failure mode 变成论文贡献，而不是只有数值。

建议 taxonomy：

1. missing-hop fragility；
2. distractor-supported wrong answer；
3. evidence conflict；
4. answer alias flip；
5. bridge entity ambiguity；
6. retrieval-order instability；
7. overconfident unsupported answer。

---

## 11. 论文结构建议

### 11.1 主文结构

```text
1. Introduction
   - RAG selective risk problem
   - clean sufficiency is misleading
   - single-set sufficiency is not orbit sufficiency

2. Problem Setup
   - evidence-set orbit
   - orbit fragility
   - selective RAG risk

3. Method: CSRM
   - orbit construction without oracle features
   - text-only verifier features
   - CSRM-Rule
   - CSRM-Calibrated
   - selective decision policy

4. Theory / Analysis
   - clean sufficiency does not imply orbit sufficiency
   - alignment necessity

5. Experimental Setup
   - leakage-free v4 pipeline
   - human audit protocol
   - baselines
   - metrics

6. Results
   - human-audited orbit detection
   - end-to-end selective RAG
   - ablations
   - anti-shortcut probes

7. Case Studies
   - clean sufficiency misleading examples
   - failure taxonomy

8. Limitations
   - no general distribution-free guarantee unless assumptions hold
   - audit cost
   - verifier dependence

9. Conclusion
```

### 11.2 Appendix 内容

```text
A. Oracle-structured bridge sanity checks
B. Full current Hotpot/FEVER bridge tables
C. NLI probe details
D. Calibration pressure tests
E. Annotation guidelines
F. Reproducibility checklist
G. Extra case studies
H. Negative results
```

---

## 12. 论文措辞替换表

| 不建议写法 | 建议写法 |
|---|---|
| CSRM solves robust RAG | CSRM targets counterfactual sufficiency instability in selective RAG |
| We provide formal risk control | We empirically reduce selective risk; formal guarantees require stated assumptions |
| We outperform CoRM-RAG | We compare against CoRM-derived and faithful CoRM baselines under equal budget |
| Human-audited results | Human audit pending / completed only after labels are done |
| SURE-RAG fails | Single-set sufficiency baselines do not capture orbit-level fragility in our setting |
| Near-perfect AUROC proves semantic robustness | Bridge results motivate the method; human-audited leakage-free results are the main evidence |
| Generalizable robust RAG solution | Orbit-level selective risk estimator evaluated across multiple datasets/retrievers/generators |

---

## 13. NeurIPS main-track readiness checklist

### 13.1 必须完成

| 项目 | 当前状态 | 目标状态 |
|---|---|---|
| leakage-free v4 | 未完成 | scorer 完全不见 oracle fields |
| human audit | labeled=0 | ≥1000 adjudicated labels |
| strong baselines | 不足 | faithful CoRM/SURE/context/LLM/equal-budget 全部完成 |
| end-to-end RAG | 未完成 | 至少 2 datasets × 2 generators |
| anti-shortcut probes | 不完整 | metadata-only / group split / hard negative 全部完成 |
| claim ledger | 已有基础 | claim 分级并与 evidence 对齐 |
| artifact packaging | workspace 级 | artifact-grade repo |

### 13.2 Main-track 最低通过门槛

1. Human-audited orbit labels 上，CSRM 显著优于 strongest baseline。
2. End-to-end selective RAG 上，accepted-error risk 显著下降。
3. Anti-shortcut probes 排除 metadata / oracle leakage。
4. Baseline 公平，equal budget。
5. 代码和数据构造可复现。
6. 负面结果和 claim boundary 清楚。

### 13.3 Spotlight 冲刺门槛

1. Figure 1 非常直观地证明 clean sufficiency misleading。
2. 跨 3 个数据域、2 个 retriever、2 个 generator 稳定。
3. Human audit 样本 2000+，agreement 高。
4. failure taxonomy 清晰，case studies 有说服力。
5. 理论命题与实验闭环。
6. 论文叙事足够锋利：**single-set sufficiency is not orbit sufficiency**。

---

## 14. 推荐的实施顺序

### Phase 0：冻结当前结果

目标：避免继续在可能有 leakage 风险的主线上堆数值。

行动：

1. 当前 Hotpot/FEVER bridge 结果保留为 sanity check。
2. 在 README / claims ledger 中明确其 status 是 `SUPPORTED_BRIDGE_ONLY`。
3. 不再把 near-perfect AUROC 当最终主证据。

### Phase 1：Leakage-free v4

目标：建立可信主实验输入。

行动：

1. 新增 `OrbitRaw` / `OrbitPrivateEvalOnly`。
2. 所有 scorer 加 feature firewall。
3. 按 source item group split。
4. 重跑 Hotpot / FEVER v4。
5. 做 metadata-only / random label / shuffled alignment probes。

### Phase 2：Text-only verifier

目标：替代 gold-derived support/missing/conflict。

行动：

1. 升级 NLI scorer 为主线。
2. 增加 LLM judge baseline。
3. 增加 learned sufficiency verifier。
4. 对比 verifier sources。

### Phase 3：Human audit

目标：形成 semantic evidence。

行动：

1. 先做 100 pilot，修 guideline。
2. 再做 1000 final。
3. 双盲标注 + adjudication。
4. 计算 agreement、mismatch、risk metrics。

### Phase 4：Strong baselines

目标：避免 baseline 不够硬。

行动：

1. faithful CoRM。
2. faithful SURE-style。
3. context sufficiency classifier。
4. LLM judge / self-consistency。
5. equal-budget orbit ensemble。

### Phase 5：End-to-end selective RAG

目标：证明真实 RAG 有收益。

行动：

1. BM25 + dense retriever。
2. 至少两个 generator。
3. coverage-risk curves。
4. accepted-answer error。
5. equal budget。

### Phase 6：Theory + paper polish

目标：提升 novelty 和 spotlight 潜力。

行动：

1. 写 clean sufficiency not imply orbit sufficiency theorem。
2. 写 alignment necessity proposition。
3. 做 Figure 1。
4. 做 case gallery。
5. 完成 artifact package。

---

## 15. 红线与降级策略

如果出现以下情况，应主动降级 claim：

| 情况 | 降级策略 |
|---|---|
| leakage-free 后 AUROC < 0.70 且 Risk@30 不显著优于 baseline | 改为 benchmark / analysis paper |
| human audit 显示 heuristic label 错误率 > 20% | 当前 bridge 结果放 appendix，不作为主证据 |
| faithful SURE / equal-budget ensemble 与 CSRM 持平 | 强调 failure mode analysis，弱化 method superiority |
| end-to-end RAG 无 accepted-error improvement | 不 claim real RAG improvement，只 claim detector |
| 跨域不稳定 | 主张限定在 multi-hop / evidence-fragility setting |
| calibration 继续失败 | 不写 risk-control guarantee，只写 ranking/selective risk |

---

## 16. 最终建议的新增 / 删除清单

### 16.1 必须新增

```text
[新增] Leakage-free Orbit Pipeline v4
[新增] OrbitRaw / OrbitPrivateEvalOnly schema
[新增] Feature firewall
[新增] Source item group split
[新增] Text-only verifier module
[新增] Human audit v4 pipeline
[新增] Faithful CoRM baseline
[新增] Faithful SURE-style baseline
[新增] Context sufficiency baseline
[新增] LLM judge baseline
[新增] Self-consistency baseline
[新增] Equal-budget orbit ensemble baseline
[新增] Metadata-only shortcut probe
[新增] Hard-negative matched evaluation
[新增] End-to-end selective RAG evaluation
[新增] CSRM-Calibrated risk model
[新增] Theory / formalization section
[新增] Case study gallery
[新增] Artifact-grade reproducibility package
```

### 16.2 必须删除或隔离

```text
[删除/隔离] scorer 输入中的 support_key
[删除/隔离] scorer 输入中的 is_support
[删除/隔离] scorer 输入中的 has_answer
[删除/隔离] scorer 输入中的 gold_supporting_facts
[删除/隔离] scorer 输入中的 heuristic_label
[删除/隔离] scorer 输入中的 construction_type / perturbation_type
[删除/降级] general formal risk-control guarantee claim
[删除/降级] full CoRM-RAG reproduction completed claim
[删除/降级] human-audited claim until labels completed
[删除/降级] all-win / solve robust RAG language
[降级] current near-perfect Hotpot/FEVER bridge as appendix sanity check
[降级] clean-only CoRM as control, not proof CoRM fails
[降级] weak SURE-style single-set as control, not official SURE comparison
```

### 16.3 应该保留但重命名 / 重新定位

```text
[保留] CSRM core scoring -> CSRM-Rule
[保留] naive orbit average -> equal-budget naive aggregation baseline
[保留] shuffled perturbation -> alignment ablation
[保留] NLI probe -> text-only verifier mainline
[保留] structural audits -> reproducibility / construction validity evidence
[保留] CP calibration scripts -> empirical pressure test / appendix
[保留] CoRM critic scorer -> bridge scorer / CoRM-derived control
```

---

## 17. 最终结论

当前 CSRM-RAG 的核心 idea 是有潜力的，尤其是：

1. clean-only 和 single-set sufficiency 无法识别 counterfactual orbit fragility；
2. naive orbit average 不如显式建模 worst-case / consistency / alignment；
3. shuffled perturbation 崩掉说明 orbit alignment 是关键；
4. NLI cross-scorer 仍保留方向性优势。

但要达到 NeurIPS main track 强度，必须完成三件事：

1. **leakage-free**：证明 CSRM 不依赖 oracle / construction labels；
2. **human-audited**：证明 heuristic fragile/stable 与人类语义判断一致；
3. **end-to-end**：证明在真实 RAG 生成中降低 accepted-answer risk。

当前最安全、最强的论文定位是：

> CSRM identifies and mitigates counterfactual sufficiency instability in selective RAG. Unlike clean-only relevance or single-set sufficiency methods, CSRM evaluates answerability stability over aligned evidence-set orbits. After removing oracle features and validating with human-audited labels, CSRM reduces accepted-answer risk under equal verifier budget across multiple retrieval and generation settings.

冲刺 spotlight 的关键不是再把 heuristic AUROC 做到 1.0，而是用一个强图、强 audit、强 end-to-end 曲线证明：

> **看起来 sufficient 的 clean evidence，经常不是 robustly sufficient；CSRM 能系统性识别这种隐藏 fragility。**
