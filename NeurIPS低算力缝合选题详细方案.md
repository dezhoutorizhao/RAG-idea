# 2×4090 条件下冲 NeurIPS Main Track 的两条缝合选题详细方案

> 版本：2026-05-19  
> 目标：基于两篇当前较强且开源的论文，设计可在 **2 张 RTX 4090** 内完成的改进路线，形成具有 NeurIPS main track 潜力的研究 proposal / 开题文档。  
> 核心原则：不是“把模块堆起来”，而是用已有论文中的机制去解决一个被清楚诊断过的瓶颈，并用公平 baseline、瓶颈子集、ablation、机制验证证明贡献。

---

## 0. 一页结论

### 推荐推进顺序

| 优先级 | Topic | 主基底论文 / 代码 | 建议论文雏形 | 2×4090 可行性 | NeurIPS 潜力 |
|---:|---|---|---|---|---|
| 1 | **Counterfactual / Evidence-Calibrated RAG** | **CoRM-RAG**：*Beyond Semantic Relevance: Counterfactual Risk Minimization for Robust RAG* | **From Robust Retrieval to Sufficient Evidence: Counterfactual Calibration for Selective RAG** | 中等：RAG 工程链路较长，但可用 released checkpoint + 小 verifier | 高：可靠性、幻觉、证据充分性是核心问题 |
| 2 | **Negation & Calibration for CLIP/VLM TTA** | **A-TPT**：*Angular Diversity Calibration Properties for Test-Time Prompt Tuning of VLMs* | **When Angular Diversity Fails: Negation-Aware Calibration for Test-Time Prompt Tuning** | 高：CLIP 级实验，计算很轻 | 中高：低算力、可快速 pilot，但需要避免变成小 trick |

### 我的最终建议

如果你想最快看到结果，**先做 Topic 2：A-TPT + NegBench**，因为 CLIP/VLM-TTA 实验轻、复现快、失败模式容易可视化。  
如果你想冲更高上限，**并行打通 Topic 1：CoRM-RAG released checkpoint 的 evaluation**，一旦 set-level evidence sufficiency critic 显著改善 risk-coverage，就优先转向 RAG。

### 判断是否值得继续的硬标准

一个 topic 只有在 48 小时到 1 周内满足下列条件，才值得投入完整论文周期：

```text
[ ] 能复现原论文主趋势或至少跑通官方 checkpoint / evaluation。
[ ] 能构造一个原方法明显失败的瓶颈子集。
[ ] 你的最小改动能在瓶颈子集显著改善，而不是只涨平均值。
[ ] 参数量、FLOPs、额外推理次数、额外数据成本可控。
[ ] 至少能写出 H1/H2/H3 三条可证伪假设。
```

---

## 1. 当前核对过的关键来源

> 注：这里的“当前 SOTA 基底”不是保证所有 leaderboard 的绝对第一，而是指：论文近期、代码公开、主张强、和你的低算力缝合方向高度匹配，适合作为改进基础。

### 1.1 Topic 1 主基底：CoRM-RAG

- 论文：**Beyond Semantic Relevance: Counterfactual Risk Minimization for Robust Retrieval-Augmented Generation**
- 方法：**CoRM-RAG**
- 链接：<https://arxiv.org/html/2605.01302v1>
- 代码：<https://github.com/PeiYangLiu/CoRM-RAG>
- 关键信息：
  - 提出 **Relevance-Robustness Gap**。
  - 认为 RAG 不能只按 semantic relevance 检索，因为 false premise / confirmation bias 下，最相关文档可能强化错误答案。
  - 使用 **Cognitive Perturbation Protocol** 生成偏置扰动。
  - 将 teacher 评估 distill 成轻量 **Evidence Critic**。
  - 官方 repo 包含 Wikipedia indexing、perturbation generation、teacher evaluation、Evidence Critic 训练、end-to-end evaluation。
  - released checkpoint 位于 Hugging Face：`PeiyangLiu/CoRM-RAG`。

### 1.2 Topic 1 关键 baseline：FaithfulRAG

- 论文：**FaithfulRAG: Fact-Level Conflict Modeling for Context-Faithful Retrieval-Augmented Generation**
- 会议：ACL 2025 Long Paper
- 链接：<https://aclanthology.org/2025.acl-long.1062/>
- 代码：<https://github.com/DeepLearnXMU/Faithful-RAG>
- 作用：作为“context conflict / fact-level conflict”方向最接近 baseline。
- 你的方法必须和它区分：

```text
FaithfulRAG: 关注 parametric knowledge 与 retrieved context 的 fact-level conflict。
CoRM-RAG: 关注 biased query 下 semantic relevance 与 decision robustness 的错配。
你的方法: 关注 document-level robustness 之后，evidence set 是否足够支持生成与拒答。
```

### 1.3 Topic 2 主基底：A-TPT

- 论文：**A-TPT: Angular Diversity Calibration Properties for Test-Time Prompt Tuning of Vision-Language Models**
- 状态：ICLR 2026 paper / 官方代码仓库
- 论文：<https://arxiv.org/abs/2510.26441>
- OpenReview：<https://openreview.net/forum?id=VhlSBZebEw>
- 代码：<https://github.com/MB-Shihab-Aaqil-Ahamed/A-TPT>
- 关键信息：
  - 面向 VLM test-time prompt tuning 的 calibration。
  - 通过最大化 normalized text features 之间的 minimum pairwise angular distance，提高 textual feature dispersion。
  - 官方代码支持 CLIP baseline、TPT、A-TPT，并覆盖 fine-grained classification 与 natural distribution shift datasets。

### 1.4 Topic 2 关键 baseline：NEAT 与 NegBench

- NEAT 论文：**Negation-Aware Test-Time Adaptation for Vision-Language Models**
- NEAT 代码：<https://github.com/hhc1997/NEAT>
- NEAT 论文：<https://arxiv.org/abs/2507.19064>
- 作用：negation-aware TTA 的最接近 baseline。

- NegBench 项目页：<https://negbench.github.io/>
- NegBench 代码：<https://github.com/m1k2zoo/negbench>
- 作用：negation understanding 的核心 stress test。
- 关键信息：
  - 18 个 task variations。
  - 约 79k examples。
  - 覆盖 image、video、medical。
  - 两类核心任务：Retrieval with Negation 与 Multiple Choice Questions with Negated Captions。

---

## 2. 统一研究标准：把“超过 SOTA”升级为“发现新瓶颈”

### 2.1 不能只写“我们超过了原论文”

NeurIPS main track 审稿人不会只看“表格第一”。尤其是在已有强开源论文基础上改进时，必须回答：

```text
1. 原论文解决了什么瓶颈？
2. 原论文没有解决什么新瓶颈？
3. 你的方法为什么不是简单加模块？
4. 你的提升是否来自新机制，而不是更多参数、更多模板、更多推理次数、更多调参？
5. 你的发现是否能改变社区对该问题的理解？
```

### 2.2 两个 topic 的共同论文叙事

这两个 topic 都适合采用同一个 NeurIPS 叙事模板：

```text
Existing methods improve average performance under standard evaluation,
but we identify a reliability bottleneck that is hidden by the average metric.

We construct a stress split / diagnostic metric that isolates this bottleneck.
We show that the current strong open-source method fails systematically.
We propose a minimal mechanism-level extension that directly targets the bottleneck.
Controlled ablations show the gain is not from parameter count, templates, or compute.
```

### 2.3 novelty 目标

按照“缝合方法论”的 novelty 分级，目标应至少是：

```text
N3: 提出新组合机制，证明互补性和泛化。
N4: 发现新瓶颈并提出机制级解决方案，影响多个任务。
```

你的两条路线都应该冲 N4：

| Topic | 原方法瓶颈 | 你的新瓶颈 | NeurIPS 贡献句 |
|---|---|---|---|
| CoRM-RAG | semantic relevance 不等于 decision robustness | document-level robustness 不等于 set-level evidence sufficiency | RAG 可靠性需要从 relevance → robustness → sufficiency 三层建模 |
| A-TPT | text feature dispersion 不足导致 calibration 差 | affirmative calibration 不等于 negation calibration | VLM-TTA 的校准必须区分 affirmative、negative、contradictory prompt manifolds |

---

# Part A：Topic 1 详细方案

# Counterfactual / Evidence-Calibrated RAG

## A1. 主基底：CoRM-RAG

### A1.1 为什么选 CoRM-RAG

CoRM-RAG 非常贴合你的第一个 topic，因为它已经把 RAG 从“相关性检索”推进到“反事实鲁棒证据检索”：

```text
传统 RAG 假设：semantic relevance ≈ evidence utility。
CoRM-RAG 诊断：false premise / confirmation bias 下，semantic relevance 可能强化错误答案。
CoRM-RAG 方法：使用 cognitive perturbation + teacher evaluation 训练 Evidence Critic。
```

这比从普通 DPR / Contriever / BM25-RAG 开始更好，因为你能站在一个更近的强基线之上继续推进：

```text
CoRM-RAG 解决了“相关但误导”的问题。
你的方法解决“鲁棒但不充分 / 多证据冲突 / 证据缺失”的问题。
```

### A1.2 官方代码可复用部分

CoRM-RAG repo 已经给出较完整 pipeline：

```text
src/encode_wikipedia.py               # Encode Wikipedia passages with Contriever; build FAISS index
src/gen_perturbations_api.py           # Generate cognitive perturbations via OpenAI-compatible API
src/gen_perturbations_distributed.py   # Multi-GPU perturbation generation with vLLM
src/retrieve_perturbed_distributed.py  # Retrieve top-K passages for each query / perturbation pair
src/teacher_evaluation.py              # Teacher LLM evaluation over query-doc-perturbation triples
src/train_critic.py                    # Train Evidence Critic with DeBERTa backbone and listwise loss
src/run_evaluation.py                  # End-to-end retrieve -> rerank -> answer
src/run_*.sh                           # Driver scripts
```

官方 pipeline：

```bash
# 1. Index Wikipedia
python src/encode_wikipedia.py

# 2. Generate perturbations
bash src/run_distributed.sh
# or use API-based generation
python src/gen_perturbations_api.py

# 3. Retrieve perturbed
bash src/run_retrieve_perturbed.sh

# 4. Teacher evaluation
python scripts/build_teacher_pool.py
RETRIEVAL_FILE_NAME=retrieval_teacher_pool.jsonl bash src/run_teacher.sh

# 5. Build training data
python scripts/build_train_expanded.py
python scripts/preprocess_training_data.py
python scripts/pretokenize_critic.py

# 6. Train critic
bash src/run_train_critic.sh

# 7. Evaluate with released checkpoint
huggingface-cli download PeiyangLiu/CoRM-RAG \
  critic-v12-mixed/checkpoint-latest/state.pt \
  --local-dir checkpoints/hf

CRITIC_PATH=checkpoints/hf/critic-v12-mixed/checkpoint-latest/state.pt bash src/run_eval.sh
```

### A1.3 2×4090 的算力策略

不要从完整 teacher pipeline 开始。建议分三层：

| 阶段 | 目标 | 是否需要训练 | 算力压力 | 备注 |
|---|---|---:|---|---|
| A | 跑通 released checkpoint evaluation | 否 | 低 | 确认 repo、数据、输出格式 |
| B | 训练一个 set-level sufficiency critic | 是，小模型 | 中低 | DeBERTa-base/large + LoRA 可行 |
| C | 小规模重训 / 复现 Evidence Critic | 是 | 中 | 只在小数据子集，不跑完整 Wikipedia |

你真正的论文方法不应该依赖全量重训 CoRM-RAG，而应依赖：

```text
CoRM-RAG released critic + 你的 set-level critic + 可控证据 stress split
```

---

## A2. 原论文仍未解决的关键缺口

### A2.1 CoRM-RAG 的核心单位是 document-level robustness

CoRM-RAG 的 Evidence Critic 主要判断某个 document 对某个 query / perturbation 是否有 robust evidential strength。这个设计很强，但 RAG 生成答案时真正依赖的是一个 evidence set，而不是单篇文档。

### A2.2 新瓶颈：document-level robustness ≠ set-level sufficiency

你可以提出如下失败模式：

| 失败类型 | 描述 | 为什么 CoRM-RAG 可能不够 |
|---|---|---|
| Missing Evidence | top-k 中有相关证据，但缺关键事实链 | 单文档 robust score 高，不代表完整证据链存在 |
| Conflicting Evidence | 多篇文档互相矛盾 | 单篇文档可能各自 robust，但集合层面冲突 |
| Distractor Evidence | 文档相关但不能支持答案 | 文档能抗 biased query，但仍不是 sufficient support |
| Partial Support | 支持答案一部分，但不能支持完整生成 | document rerank 无法评估答案级 coverage |
| Citation-Answer Mismatch | 答案正确但引用不支持 | 检索强，不代表生成的 citation faithful |

### A2.3 你的核心研究问题

```text
RQ1: 在 counterfactual / biased query 场景下，document-level robustness 能否充分代表 answer-level evidence sufficiency？
RQ2: 如果不能，哪些错误来自 evidence missing、evidence conflict、partial support 或 citation mismatch？
RQ3: 是否可以用一个轻量 set-level critic，在不训练大模型的情况下改善 selective RAG 的 risk-coverage 与 faithfulness？
```

---

## A3. 拟议方法：Set-Calibrated CoRM-RAG

### A3.1 方法名称

建议名称：

```text
Set-Calibrated CoRM-RAG
或
SufCal-RAG: Evidence Sufficiency Calibration for Counterfactual RAG
```

### A3.2 一句话方法

> 在 CoRM-RAG 的 document-level Evidence Critic 之上，增加一个轻量 set-level Evidence Sufficiency Critic，显式建模 top-k 证据集合对候选答案的 support、coverage、conflict 与 missingness，并通过 selective prediction / conformal calibration 决定回答或拒答。

### A3.3 方法结构

```text
User Query q
   ↓
Base Retriever: BM25 / Contriever / E5 / DPR
   ↓
CoRM-RAG Evidence Critic: document-level robustness score r_i
   ↓
Top-k evidence set D = {d_1, ..., d_k}
   ↓
Candidate Answer a generated by frozen LLM
   ↓
Set-Level Sufficiency Critic g(q, a, D, r)
   ↓
Outputs:
   - answerability score s_ans
   - support score s_sup
   - conflict score s_con
   - missing evidence score s_miss
   - calibrated abstention decision
   ↓
Final response:
   - answer with citations
   - or abstain / request more evidence
```

### A3.4 输入特征设计

Set-level critic 的输入可以分成四组：

#### 1. Query-answer pair

```text
[CLS] query [SEP] candidate_answer [SEP]
```

作用：判断候选答案是否具体、是否与 query 类型匹配。

#### 2. Evidence snippets

```text
document title + passage text + CoRM score
```

作用：判断证据是否支持答案。

#### 3. Inter-document relation features

可用轻量 NLI / cross-encoder 估计：

```text
support(d_i, a)
contradict(d_i, a)
support(d_i, d_j)
contradict(d_i, d_j)
```

作用：建模集合层面的冲突。

#### 4. Coverage features

```text
coverage = fraction of answer atomic facts supported by at least one document
max_support = max_i support(d_i, answer)
mean_support = mean_i support(d_i, answer)
conflict_rate = #contradictory_pairs / #pairs
robustness_entropy = entropy(normalize(CoRM scores))
```

作用：把“证据是否足够”从黑盒判断变成可解释信号。

### A3.5 模型选择

从低到高三档：

| 档位 | 模型 | 优点 | 风险 |
|---|---|---|---|
| V1 | DeBERTa-v3-base cross-encoder | 轻、稳定、2×4090 足够 | 上限有限 |
| V2 | DeBERTa-v3-large + listwise pooling | 表达力强，和 CoRM-RAG 兼容 | 显存稍高 |
| V3 | 7B LLM LoRA verifier | 更强推理能力 | 工程复杂、推理成本高 |

建议先做 V1/V2，不要一开始用 7B verifier，否则 reviewer 会质疑算力、成本和可复现性。

### A3.6 训练目标

建议把训练目标分成四部分：

```text
L = L_answerability
  + λ1 L_support
  + λ2 L_conflict
  + λ3 L_missing
  + λ4 L_calibration
```

其中：

```text
L_answerability: 判断证据集合是否足以回答。
L_support: 判断 answer atomic facts 是否被证据支持。
L_conflict: 识别证据间或证据-答案间冲突。
L_missing: 识别缺关键证据时的拒答场景。
L_calibration: 让 answerability score 与真实风险对齐。
```

### A3.7 推理时决策

```python
if sufficiency_score >= tau_answer and conflict_score <= tau_conflict:
    return answer_with_citations
else:
    return abstain_or_request_more_evidence
```

阈值不要手调，可以使用 calibration split：

```text
- 在 calibration set 上选择 tau，使 selective risk 不超过预设风险水平。
- 报告不同 coverage 下的 risk-coverage curve。
```

---

## A4. 数据与 stress split 设计

### A4.1 不要只跑标准 QA

标准 QA 的平均 EM/F1 很难证明你的贡献。你需要设计 evidence sufficiency stress split。

### A4.2 四类核心 evidence split

| Split | 构造方式 | 期望行为 | 主要指标 |
|---|---|---|---|
| Supporting | top-k 包含完整支持证据 | 回答 + 正确引用 | EM/F1、citation precision |
| Distracting | top-k 相关但不支持答案 | 降权或拒答 | distractor rejection |
| Conflicting | top-k 含相互矛盾证据 | 检测冲突 / 谨慎回答 | conflict AUROC |
| Missing | top-k 缺关键证据 | 拒答 | missing-evidence AUROC |

### A4.3 候选数据集

| 数据集 | 用途 | 备注 |
|---|---|---|
| Natural Questions | 单跳开放域 QA | 构造 false premise / missing evidence |
| HotpotQA | 多跳 QA | 适合测试 evidence chain sufficiency |
| FEVER | claim verification | 适合 support/refute/NEI 标签 |
| TruthfulQA | 反常识/误导性问题 | 适合 biased query stress |
| RGB / RAGTruth / ASQA | RAG faithfulness 方向 | 视代码可用性选择 |

### A4.4 自动构造流程

```text
For each original QA example (q, y):
  1. Retrieve top-k documents with baseline retriever.
  2. Use CoRM-RAG critic to score document-level robustness.
  3. Build four evidence sets:
     a. Support set: contains gold/supporting docs.
     b. Distractor set: replace supporting docs with semantically related but non-supporting docs.
     c. Conflict set: inject documents supporting alternative answer.
     d. Missing set: remove one or more required evidence hops.
  4. Generate candidate answer with frozen LLM.
  5. Label set-level sufficiency by:
     - existing dataset annotation when available,
     - NLI / entailment model,
     - LLM-as-judge for bootstrapping,
     - manual verification on small dev/test subset.
```

### A4.5 最重要的人工核验

NeurIPS reviewer 很可能质疑自动标签。你需要人工核验一个小而高质量的 test slice：

```text
- 200~500 examples。
- 每类 split 均衡。
- 标注：support / partial support / conflict / missing / irrelevant。
- 至少两个 annotator 或二次人工检查。
- 用于最终 case study 与 label noise 分析。
```

---

## A5. Baseline 设计

### A5.1 必须正面对比的 baseline

```text
Retrieval baselines:
- BM25
- DPR / Contriever
- E5 / BGE retriever
- Cross-encoder reranker
- LLM reranker

RAG reliability baselines:
- Standard RAG
- Self-RAG / self-check style methods
- CalibRAG / uncertainty-based abstention, if reproducible
- FaithfulRAG
- CoRM-RAG

Your controlled baselines:
- CoRM-RAG + threshold on max document score
- CoRM-RAG + average document score
- CoRM-RAG + naive verifier
- CoRM-RAG + LLM-as-judge verifier
- Your set-level critic without conflict features
- Your set-level critic without coverage features
```

### A5.2 最关键的公平性控制

```text
[ ] Same retriever candidate pool。
[ ] Same generator LLM。
[ ] Same top-k。
[ ] Same context length budget。
[ ] Same number of LLM calls。
[ ] Same calibration split。
[ ] Same answer extraction / citation format。
```

---

## A6. 指标体系

### A6.1 平均任务指标

```text
- EM / F1
- answer accuracy
- exact citation support accuracy
```

### A6.2 可靠性指标

```text
- hallucination rate
- unsupported answer rate
- citation precision / recall
- conflict detection AUROC
- missing evidence AUROC
- answerability ECE
```

### A6.3 selective prediction 指标

```text
- risk-coverage curve
- AURC: area under risk-coverage curve
- selective accuracy at fixed coverage
- coverage at fixed risk
```

### A6.4 你最应该主打的指标

主表不要只放 EM/F1，建议主表结构：

| Method | EM/F1 | Unsupported Answer ↓ | Conflict AUROC ↑ | Missing AUROC ↑ | Risk@80%Cov ↓ | Citation Prec ↑ |
|---|---:|---:|---:|---:|---:|---:|
| Standard RAG | | | | | | |
| FaithfulRAG | | | | | | |
| CoRM-RAG | | | | | | |
| Ours | | | | | | |

这样能把你的论文从“RAG 涨点”变成“selective reliable RAG”。

---

## A7. Ablation 与机制验证

### A7.1 必做 ablation

```text
[ ] Remove CoRM document scores。
[ ] Remove set-level critic。
[ ] Remove conflict features。
[ ] Remove coverage features。
[ ] Replace set-level critic with mean / max document score。
[ ] Replace DeBERTa critic with same-parameter random MLP over scores。
[ ] Change top-k: 3 / 5 / 10 / 20。
[ ] Change generator LLM: Qwen / Llama / Mistral small variants。
[ ] Change retriever: Contriever / E5 / BM25。
[ ] Calibration with vs without conformal threshold。
```

### A7.2 机制验证图

建议做四张图：

1. **Relevance vs Robustness vs Sufficiency scatter**  
   证明 semantic relevance、CoRM robustness、set-level sufficiency 不是同一信号。

2. **Risk-Coverage Curve**  
   证明你的 score 更适合做 selective RAG。

3. **Error decomposition bar chart**  
   把错误分为 unsupported、conflict、missing、wrong citation、wrong answer。

4. **Case study table**  
   展示 CoRM-RAG 选择了高 robust 文档但仍然 evidence insufficient，而你的方法拒答或纠正。

### A7.3 Reviewer 最可能的质疑与反驳

| 质疑 | 反驳实验 |
|---|---|
| 只是多加了 verifier | 对比 naive verifier、LLM-as-judge verifier、same-parameter critic |
| 只是 threshold 更好 | 对比 max/mean CoRM score + threshold |
| 标签是 LLM 造的，不可靠 | 人工核验 test slice + label noise sensitivity |
| 只在一个数据集成立 | NQ + HotpotQA + FEVER/TruthfulQA 至少两个 domain |
| 推理太贵 | 报告 latency、额外参数、LLM call 数，显示 critic 是小模型 |

---

## A8. 48 小时到 2 周 pilot

### 48 小时 pilot

```text
Day 1:
- clone CoRM-RAG repo。
- 下载 released Evidence Critic checkpoint。
- 跑通 run_eval.sh 或最小 evaluation。
- 抽取 top-k docs、CoRM score、answer、是否正确。

Day 2:
- 构造 100~300 个 mini stress examples：support / distractor / conflict / missing。
- 先不用训练模型，用 rule-based set sufficiency score：
  score = max_support - alpha * conflict - beta * missing
- 画 risk-coverage curve，比较 max CoRM score vs set score。
```

通过条件：

```text
[ ] CoRM-RAG 在某些 set-level stress split 上明显失败。
[ ] 简单 set-level signal 就能改善 abstention 或 conflict/missing detection。
[ ] 有 5 个以上清楚 case study。
```

### 2 周 pilot

```text
Week 1:
- 训练 DeBERTa-base set-level critic。
- 完成一个数据集上的 support/conflict/missing/distractor split。
- 对比 CoRM-RAG + naive threshold。

Week 2:
- 扩展到第二个数据集。
- 加 citation precision 与 risk-coverage。
- 完成 ablation：no conflict / no coverage / no CoRM score。
```

---

## A9. 成功标准与投稿边界

### A9.1 值得冲 NeurIPS 的成功标准

```text
[ ] 在 conflict / missing / false-premise split 上显著优于 CoRM-RAG。
[ ] 在标准 QA 上不明显掉点，最好略有提升。
[ ] Risk-coverage curve 明显优于 document-score baseline。
[ ] Set-level sufficiency score 与人类标注高度相关。
[ ] 至少两个数据集、两个 retriever 或两个 generator 上趋势稳定。
[ ] ablation 能证明 conflict/coverage/set-level modeling 必要。
```

### A9.2 不值得硬冲的情况

```text
[ ] 只在平均 EM/F1 上涨 0.5~1%。
[ ] 主要提升来自更多 LLM calls。
[ ] 无法构造可靠 stress split。
[ ] 人工核验发现自动标签噪声很大。
[ ] FaithfulRAG / CoRM-RAG + simple threshold 已经接近你的方法。
```

---

# Part B：Topic 2 详细方案

# Negation & Calibration for CLIP/VLM Test-Time Adaptation

## B1. 主基底：A-TPT

### B1.1 为什么选 A-TPT

A-TPT 是很适合你算力条件的主基底：

```text
- 任务是 CLIP/VLM test-time prompt tuning，不需要训练大模型。
- 代码公开，实验脚本覆盖常见 fine-grained 与 distribution shift 数据集。
- 方法主张是 calibration，非常贴合你的“Negation & Calibration”主题。
- 现有方法主打 affirmative classification calibration，没有系统解决 negation calibration。
```

### B1.2 官方代码可复用部分

A-TPT 官方 repo 提供：

```bash
# Clone

git clone https://github.com/MB-Shihab-Aaqil-Ahamed/A-TPT.git
cd A-TPT

# Create env
conda env create -f environment.yml
conda activate atpt

# Baseline CLIP
bash scripts/test_baseline.sh {dataset}

# TPT / A-TPT style experiments
bash scripts/test_tpt_fg.sh {dataset}
```

官方支持的实验包括：

```text
Fine-grained classification:
- ImageNet
- Flower102
- OxfordPets
- SUN397
- DTD
- Food101
- StanfordCars
- Aircraft
- UCF101
- EuroSAT
- Caltech101

Natural distribution shift:
- ImageNet-V2
- ImageNet-A
- ImageNet-R
- ImageNet-Sketch
```

### B1.3 为什么 NEAT 不作为主基底

NEAT 本身就是 negation-aware TTA。直接在 NEAT 上加 calibration，容易被 reviewer 认为是“NEAT + ECE loss”。

更强的叙事是：

```text
A-TPT: calibration strong, but not designed for negation。
NEAT: negation-aware, but calibration story不够系统。
Your method: negation-aware calibration，证明 affirmative calibration 与 negation calibration 可分离。
```

---

## B2. 原论文仍未解决的关键缺口

### B2.1 A-TPT 的核心假设

A-TPT 的核心思想是：class-wise textual features 的 angular diversity / dispersion 对 calibration 很重要。

这在普通分类中合理：

```text
class prompt 1: a photo of a dog
class prompt 2: a photo of a cat
class prompt 3: a photo of a car
```

这些类别通常互斥，文本特征分散能改善 calibration。

### B2.2 新瓶颈：affirmative calibration ≠ negation calibration

在 negation 场景中，prompt 不再是简单互斥类别：

```text
Affirmative: a photo of a dog
Negated: a photo without a dog
Contradictory: a photo of a dog without a dog
Relational negation: a person not holding a cup
Absence query: find images that do not contain pneumonia
```

此时，text feature dispersion 本身可能不足，因为 negated prompt 仍然包含目标词，例如 “dog”，CLIP 可能仍被关键词激活。

### B2.3 你的核心研究问题

```text
RQ1: A-TPT 在 standard ECE 上表现好时，是否仍然在 negated prompts 上过度自信？
RQ2: 普通 angular diversity 是否会把 affirmative prompts 分散得很好，但无法分离 affirmative / negative / contradictory prompt manifolds？
RQ3: 是否可以在 test-time 无标签条件下，引入 negation-pair angular calibration，改善 NegBench，同时不破坏 standard distribution shift calibration？
```

---

## B3. 拟议方法：Neg-Calibrated A-TPT

### B3.1 方法名称

建议名称：

```text
Neg-Calibrated A-TPT
或
NAC-TPT: Negation-Aware Calibration for Test-Time Prompt Tuning
```

### B3.2 一句话方法

> 在 A-TPT 的 angular diversity calibration 基础上，引入 affirmation-negation paired prompt manifolds 与 contradiction-aware calibration loss，使 VLM test-time prompt tuning 同时保持普通分类 calibration 与 negation-specific reliability。

### B3.3 方法结构

```text
Input image x
   ↓
CLIP image encoder, frozen
   ↓
Prompt set construction:
   - affirmative prompts P_aff
   - negative prompts P_neg
   - contradiction prompts P_contra
   - reversed negation prompts P_rev
   ↓
Test-time prompt tuning:
   - TPT entropy / confidence objective
   - A-TPT angular diversity objective
   - negation-pair angular separation
   - contradiction consistency calibration
   ↓
Output:
   - standard class prediction
   - negation-aware score
   - calibrated confidence / selective decision
```

### B3.4 Prompt templates

#### Affirmative templates

```text
a photo of a {class}
a clear image of a {class}
a close-up photo of a {class}
```

#### Negative templates

```text
a photo without a {class}
a photo that does not contain a {class}
an image where no {class} is present
```

#### Relational negative templates

```text
a {subject} not holding a {object}
a {subject} not next to a {object}
a {object} is not on the {surface}
```

#### Contradiction templates

```text
a photo of a {class} without a {class}
a scene containing {class} and not containing {class}
```

这些 contradiction templates 不一定用于最终 prediction，而是作为 calibration regularizer 的 stress anchors。

---

## B4. 方法版本设计

不要一开始做复杂系统。建议分四个版本递进。

### B4.1 V0：A-TPT + negated prompt evaluation

目标：证明 A-TPT 在 standard calibration 与 negation calibration 上存在 gap。

```text
不改训练。
只把 A-TPT 输出用于 NegBench evaluation。
报告：standard ECE vs Neg-ECE。
```

如果 V0 无法发现明显 gap，这个 topic 就有风险。

### B4.2 V1：Negated Prompt Ensemble

目标：简单增强 prompt set，作为弱 baseline。

```text
score(c) = sim(image, positive_prompt_c) - gamma * sim(image, negative_prompt_c)
```

这不是最终方法，但可以证明简单模板是否已经足够。

### B4.3 V2：Negation-Pair Angular Diversity

目标：在 A-TPT 的 angular diversity 上加入 negation pair 约束。

设：

```text
z_aff_c = text feature of affirmative prompt for class c
z_neg_c = text feature of negative prompt for class c
z_con_c = text feature of contradiction prompt for class c
```

新增约束：

```text
1. Affirmative class features should remain diverse:
   L_aff_ang = A-TPT angular diversity objective

2. Affirmative and negated prompts should not collapse:
   L_pair = max(0, m_pair - angle(z_aff_c, z_neg_c))

3. Contradiction prompts should have low confidence:
   L_contra = confidence_penalty(z_con_c)

4. Negative prompts should not be treated as another positive class:
   L_neg_cal = consistency / entropy regularization on negation scores
```

总目标：

```text
L = L_TPT
  + λ1 L_A-TPT
  + λ2 L_pair
  + λ3 L_contra
  + λ4 L_neg_cal
```

### B4.4 V3：Selective Negation Calibration

目标：当模型无法判断 negation 时拒答或降低置信度。

```text
neg_conflict_score = max_c p_aff(c|x) * p_neg(c|x)

if neg_conflict_score > threshold:
    abstain / low confidence
else:
    output calibrated prediction
```

阈值在 calibration split 上选择，最终报告 risk-coverage curve。

---

## B5. 数据与评估设计

### B5.1 Standard calibration datasets

用于证明你的方法没有破坏 A-TPT 的核心能力：

```text
- ImageNet
- ImageNet-V2
- ImageNet-A
- ImageNet-R
- ImageNet-Sketch
- OxfordPets
- Food101
- DTD
- EuroSAT
- Caltech101
```

### B5.2 Negation datasets

优先级：

| 优先级 | 数据 | 用途 |
|---:|---|---|
| 1 | NegBench image split | 最重要的 negation stress test |
| 2 | NegBench MCQ with negated captions | 测试选择题式 negation reasoning |
| 3 | NegBench retrieval with negation | 测试图文检索中的 absence semantics |
| 4 | medical split, if feasible | 增强 use-inspired 价值 |
| 5 | video split, optional | 算力与工程复杂度较高，后期再做 |

### B5.3 自建轻量 stress split

为了更好控制机制，可以从 ImageNet / COCO 类别构造：

```text
1. Present-object query:
   image contains dog; prompt asks dog.

2. Absent-object query:
   image does not contain dog; prompt asks without dog.

3. Hard negative query:
   image contains wolf; prompt asks not dog.

4. Co-occurrence trap:
   image contains person and cup; prompt asks person not holding cup.

5. Reversed negation:
   prompt A: dog without cat
   prompt B: cat without dog
```

这些 split 可以帮助你解释 NegBench 结果，而不是只报总分。

---

## B6. 指标体系

### B6.1 Standard metrics

```text
- top-1 accuracy
- ECE: Expected Calibration Error
- NLL: Negative Log-Likelihood
- Brier score
```

### B6.2 Negation-specific metrics

建议提出或系统使用：

```text
Neg-Accuracy:
  accuracy on negated prompts / MCQ / retrieval tasks

Neg-ECE:
  ECE computed only on negation queries

Aff-Neg Calibration Gap:
  |ECE_affirmative - ECE_negation|

Contradiction Confidence:
  average confidence assigned to contradictory prompts; lower is better

Absent Object AUROC:
  AUROC for deciding whether object is absent

Reversed Negation Consistency:
  whether prediction flips correctly when negation relation is reversed

Selective Risk under Negation:
  risk-coverage curve on negation examples
```

### B6.3 主表建议

| Method | Std Acc ↑ | Std ECE ↓ | NegBench Acc ↑ | Neg-ECE ↓ | Aff-Neg Gap ↓ | Contra Conf ↓ |
|---|---:|---:|---:|---:|---:|---:|
| CLIP zero-shot | | | | | | |
| TPT | | | | | | |
| C-TPT | | | | | | |
| O-TPT | | | | | | |
| A-TPT | | | | | | |
| NEAT | | | | | | |
| Ours | | | | | | |

这张表的目标是证明：

```text
A-TPT: standard calibration strong，但 negation-specific calibration 不够。
NEAT: negation performance strong，但 calibration / standard shift 未必最优。
Ours: 在 standard calibration 和 negation reliability 上形成 Pareto improvement。
```

---

## B7. Baseline 设计

### B7.1 必须包括的 baseline

```text
- Zero-shot CLIP
- TPT
- C-TPT
- O-TPT
- A-TPT
- NEAT
- NegCLIP / ConCLIP, if available
- A-TPT + simple negated template ensemble
- A-TPT + same number of random extra templates
- A-TPT + more prompts but no negation structure
```

### B7.2 最关键控制实验

```text
[ ] Same CLIP backbone: RN50 / ViT-B/16 / ViT-L/14。
[ ] Same test-time batch size。
[ ] Same number of prompt tokens。
[ ] Same number of templates。
[ ] Same number of optimization steps。
[ ] Same augmentations。
[ ] Same test data order for online TTA。
```

### B7.3 Reviewer 最可能的质疑与反驳

| 质疑 | 反驳实验 |
|---|---|
| 只是多加了 negation templates | 对比 random templates、more affirmative templates、template ensemble |
| 只是 NEAT 的变体 | 正面对比 NEAT，并展示 standard ECE / Neg-ECE Pareto |
| 会伤害普通分类 | ImageNet-shift + fine-grained datasets 证明不掉点 |
| metric 是你自己定义的 | 同时报告 NegBench 官方指标与你的 Neg-ECE |
| prompt engineering 不够算法 | 用 angular manifold analysis、ablation、risk-coverage 证明机制 |

---

## B8. 机制验证

### B8.1 Prompt embedding geometry

画图或统计：

```text
- affirmative prompt feature distance matrix
- negative prompt feature distance matrix
- affirmative-negative pair angle
- contradiction prompt confidence distribution
```

目标：证明 A-TPT 只改善 class-wise dispersion，但没有保证 affirmative / negated prompt manifolds 的正确关系。

### B8.2 Calibration decomposition

报告：

```text
ECE_affirmative
ECE_negation
ECE_absent_object
ECE_relation_negation
ECE_contradiction
```

目标：证明 average ECE 掩盖了 negation-specific miscalibration。

### B8.3 Pareto frontier

画二维图：

```text
x-axis: NegBench performance
 y-axis: Neg-ECE or selective risk
 bubble size: inference cost / number of tunable params
```

目标：证明你的方法不是只在一个指标上取巧，而是形成新的 accuracy-calibration Pareto frontier。

---

## B9. 48 小时到 2 周 pilot

### 48 小时 pilot

```text
Day 1:
- clone A-TPT。
- 跑通 CLIP baseline 与 A-TPT on ImageNet-V2 或一个小数据集。
- 记录 standard accuracy / ECE。

Day 2:
- 接入 NegBench image split 或小规模 negation subset。
- 跑 zero-shot CLIP、TPT、A-TPT。
- 计算 NegBench accuracy、Neg-ECE、Aff-Neg Calibration Gap。
```

通过条件：

```text
[ ] A-TPT standard ECE 有改善，但 Neg-ECE 仍然差。
[ ] 有明显 contradiction confidence 或 aff-neg gap。
[ ] 简单 negation-pair regularizer 有初步改善。
```

### 2 周 pilot

```text
Week 1:
- 实现 V1 / V2：negated template ensemble + negation-pair angular diversity。
- 在 NegBench image split + ImageNet-V2/R/Sketch 上跑。
- 对比 A-TPT 与 NEAT。

Week 2:
- 完成 ablation：no neg pair / no contradiction / random templates / more affirmative templates。
- 做 prompt geometry 分析。
- 做 50~100 个 case study。
```

---

## B10. 成功标准与投稿边界

### B10.1 值得冲 NeurIPS 的成功标准

```text
[ ] 在 NegBench 上明显优于 A-TPT。
[ ] 在 Neg-ECE / Aff-Neg Gap 上显著优于 A-TPT 与 NEAT。
[ ] 在 standard distribution shift datasets 上不明显低于 A-TPT。
[ ] random template / more template baselines 不能解释提升。
[ ] prompt geometry 分析能证明 negation manifold 被更好分离。
[ ] 至少两个 CLIP backbone 上趋势一致。
```

### B10.2 不值得硬冲的情况

```text
[ ] 只靠 hand-crafted prompt ensemble 提升。
[ ] 只在一个 NegBench 子集有效。
[ ] 标准 ImageNet-shift calibration 明显下降。
[ ] NEAT 一跑就全面优于你的方法。
[ ] 没有机制图，只剩表格小涨点。
```

---

# Part C：两条路线的对比与决策

## C1. 风险-收益矩阵

| 维度 | CoRM-RAG 路线 | A-TPT 路线 |
|---|---|---|
| 复现难度 | 中高 | 低 |
| 工程复杂度 | 高，涉及 retrieval / generation / critic / calibration | 低到中，主要是 CLIP evaluation |
| 算力压力 | 中，主要是 retrieval + verifier 训练 + LLM inference | 低 |
| Novelty 上限 | 高 | 中高 |
| 竞争激烈度 | 高，但可靠 RAG 仍有空间 | 高，VLM-TTA 与 negation 都热门 |
| 最快 pilot | 2~4 天 | 1~2 天 |
| 最可能失败原因 | 数据构造和标签质量 | 被认为是 prompt engineering |
| 最适合投稿叙事 | selective reliable RAG / evidence sufficiency | calibration under semantic negation |

## C2. 推荐决策树

```text
Start
 ├─ 是否能在 48 小时内跑通 A-TPT + NegBench？
 │    ├─ 是：看 A-TPT 是否存在明显 Neg-ECE / Aff-Neg Gap
 │    │    ├─ 是：推进 Topic 2 两周 pilot
 │    │    └─ 否：降级为 baseline，不主推
 │    └─ 否：先修 A-TPT 环境，避免投入 RAG 长链路
 │
 └─ 是否能在 3~5 天内跑通 CoRM-RAG released checkpoint？
      ├─ 是：构造 set-level stress split
      │    ├─ 若 CoRM-RAG 明显失败且你的 set score 改善：转 Topic 1 冲高上限
      │    └─ 若失败不明显：只作为后备方向
      └─ 否：暂缓 RAG，避免工程泥潭
```

---

# Part D：完整实验时间线

## D1. 0~2 周：双线 pilot

### Topic 2 快速线

```text
Day 1-2:
- A-TPT 复现。
- NegBench 接入。
- 计算 standard ECE 与 Neg-ECE。

Day 3-5:
- V1 negated prompt ensemble。
- V2 negation-pair angular diversity。
- 初步 ablation。

Day 6-14:
- NEAT baseline。
- prompt geometry 分析。
- 两个 CLIP backbone。
```

### Topic 1 高上线

```text
Day 1-3:
- CoRM-RAG repo + checkpoint evaluation。
- 抽取 top-k docs / scores / answers。

Day 4-7:
- 小规模 stress split。
- rule-based set sufficiency score。
- risk-coverage curve。

Week 2:
- 训练 DeBERTa-base set-level critic。
- 与 CoRM-RAG threshold 比较。
```

## D2. 3~6 周：确定主线并扩大实验

如果 Topic 2 胜出：

```text
Week 3:
- 完成 NegBench image + MCQ。
- 完成 A-TPT / NEAT / TPT / CLIP 对比。

Week 4:
- ImageNet-V2/A/R/Sketch + fine-grained datasets。
- 完成 prompt geometry 与 calibration decomposition。

Week 5:
- 多 backbone、多 seed、超参敏感性。
- 失败案例与可视化。

Week 6:
- 写第一版论文 introduction / method / experiments。
```

如果 Topic 1 胜出：

```text
Week 3:
- 完成两个 QA 数据集的 stress split。
- 训练 set-level critic。

Week 4:
- FaithfulRAG / CoRM-RAG / naive verifier baseline。
- 完成 selective prediction 指标。

Week 5:
- 人工核验 test slice。
- 多 retriever / 多 generator。

Week 6:
- 写第一版论文 introduction / method / experiments。
```

## D3. 7~10 周：NeurIPS 级补强

```text
Week 7:
- 强 baseline 补齐。
- reviewer 反驳实验。

Week 8:
- 主表、ablation 表、机制图全部定稿。
- case study 与 failure analysis。

Week 9:
- 完成完整 paper draft。
- 找外部同学读 related work 与 novelty。

Week 10:
- 重跑关键实验、多 seed、置信区间。
- 开源 repo 整理。
```

---

# Part E：论文写作框架

## E1. Topic 1 论文大纲

### Title

```text
From Robust Retrieval to Sufficient Evidence:
Counterfactual Calibration for Selective Retrieval-Augmented Generation
```

### Abstract 草稿结构

```text
Retrieval-augmented generation systems increasingly rely on robust retrievers to mitigate hallucinations under biased or adversarial queries. However, we show that document-level retrieval robustness is not sufficient for answer-level reliability: a set of individually robust documents may still be incomplete, mutually conflicting, or insufficient to support the generated answer. We introduce evidence sufficiency calibration, a lightweight set-level critic that models support, coverage, conflict, and missingness over retrieved evidence. Built on top of CoRM-RAG, our method enables calibrated selective generation without retraining the generator. Across multiple QA and fact verification benchmarks, it improves risk-coverage trade-offs, conflict detection, and citation faithfulness under counterfactual evidence perturbations. Controlled ablations show that the gains come from set-level sufficiency modeling rather than additional retrieval scores or naive verification.
```

### Contributions

```text
1. We identify a new reliability bottleneck in robust RAG: document-level evidence robustness does not imply set-level evidence sufficiency.
2. We construct counterfactual evidence sufficiency stress splits covering supporting, distracting, conflicting, and missing evidence.
3. We propose a lightweight set-level sufficiency critic that calibrates selective generation using support, coverage, and conflict signals.
4. We show improved risk-coverage, citation faithfulness, and conflict/missing-evidence detection over CoRM-RAG, FaithfulRAG, and strong verifier baselines.
```

## E2. Topic 2 论文大纲

### Title

```text
When Angular Diversity Fails:
Negation-Aware Calibration for Test-Time Prompt Tuning
```

### Abstract 草稿结构

```text
Test-time prompt tuning improves the calibration of vision-language models by adapting textual prompts to unlabeled test data. Recent angular-diversity methods further improve calibration by dispersing class-wise text features. In this work, we show that such calibration can be misleading under semantic negation: a model may be well-calibrated over affirmative class names while remaining over-confident on absent objects and contradictory negated prompts. We introduce negation-aware calibration for test-time prompt tuning, which augments angular diversity with affirmation-negation pair constraints and contradiction-aware confidence regularization. On standard distribution-shift benchmarks and NegBench, our method improves negation-specific calibration and selective risk while preserving standard accuracy and ECE. Our analysis reveals that affirmative calibration and negation calibration are distinct reliability dimensions for VLM test-time adaptation.
```

### Contributions

```text
1. We show that standard calibration metrics can hide severe miscalibration under negated prompts in VLM test-time adaptation.
2. We introduce negation-specific metrics, including Neg-ECE, Aff-Neg Calibration Gap, and Contradiction Confidence.
3. We propose a negation-aware angular calibration objective that separates affirmative, negative, and contradictory prompt manifolds at test time.
4. We demonstrate improved performance on NegBench while preserving A-TPT-level calibration on standard distribution shift benchmarks.
```

---

# Part F：代码结构建议

## F1. Topic 1 repo structure

```text
sufcal-rag/
  README.md
  requirements.txt
  configs/
    corm_eval.yaml
    sufficiency_critic.yaml
  data/
    README.md
  src/
    build_stress_split.py
    extract_corm_outputs.py
    label_evidence_sets.py
    train_sufficiency_critic.py
    evaluate_selective_rag.py
    metrics.py
    visualization.py
  scripts/
    run_corm_eval.sh
    build_support_split.sh
    build_conflict_split.sh
    train_critic.sh
    eval_all.sh
  notebooks/
    risk_coverage.ipynb
    case_studies.ipynb
  results/
    tables/
    figures/
```

## F2. Topic 2 repo structure

```text
neg-calibrated-atpt/
  README.md
  environment.yml
  configs/
    atpt.yaml
    neg_calibration.yaml
  datasets/
    README.md
  src/
    prompt_templates.py
    negation_losses.py
    run_atpt_neg.py
    eval_negbench.py
    calibration_metrics.py
    geometry_analysis.py
  scripts/
    run_clip_baseline.sh
    run_atpt.sh
    run_neat.sh
    run_neg_cal_atpt.sh
    eval_all.sh
  notebooks/
    neg_ece_analysis.ipynb
    prompt_geometry.ipynb
  results/
    tables/
    figures/
```

---

# Part G：最终自审清单

## G1. 机制自审

```text
[ ] 我的 paper 不是“we combine A and B”。
[ ] 我能用一句话说出原 SOTA 没解决的新瓶颈。
[ ] 我有一个专门暴露该瓶颈的 stress split 或 metric。
[ ] 我的方法每个组件都能映射到瓶颈的一部分。
[ ] 我能证明提升不是来自更多参数 / 更多 prompts / 更多 LLM calls。
[ ] 我有失败案例分析，而不是只报平均指标。
```

## G2. 实验自审

```text
[ ] 至少 3 个强 baseline。
[ ] 至少 2 个数据集或 domain。
[ ] 至少 2 个 backbone / retriever / generator 设置。
[ ] 至少 3 个核心 ablation。
[ ] 至少 1 个机制图。
[ ] 至少 1 个风险-覆盖或校准图。
[ ] 报告参数、显存、额外推理时间。
```

## G3. 投稿前 red flag

```text
[ ] 结果只在一个数据集有效。
[ ] 只靠 prompt wording 或 threshold 调参。
[ ] baseline 没有跑最强开源方法。
[ ] 关键标签来自 LLM，但无人工核验。
[ ] 代码无法复现主表。
[ ] paper contribution 读起来像工程集成。
```

---

# Part H：最终推荐

## H1. 最优推进策略

```text
第一周：
  主攻 A-TPT + NegBench，因为它最容易快速验证。
  并行打通 CoRM-RAG released checkpoint，不做重训。

第二周：
  如果 A-TPT 有明显 Neg-ECE gap，推进 negation-aware calibration。
  如果 CoRM-RAG 有明显 set-level insufficiency failure，转向 RAG 高上限路线。

第三周：
  二选一作为主线，另一条作为备选或未来工作。
```

## H2. 我更看好的最终论文形态

如果 CoRM-RAG 方向 pilot 通过，我更看好它冲 NeurIPS main track，因为它的贡献可以自然写成：

```text
RAG reliability requires a three-level decomposition:
semantic relevance → counterfactual robustness → evidence sufficiency.
```

这个叙事比普通模块改进更接近“改变社区理解”。

如果 A-TPT 方向 pilot 通过，它的优势是速度快、算力低、实验干净。为了达到 NeurIPS 水平，必须把故事从“negation prompt tuning”提升到：

```text
Affirmative calibration and negation calibration are distinct reliability dimensions in VLM test-time adaptation.
```

---

# References

1. CoRM-RAG: *Beyond Semantic Relevance: Counterfactual Risk Minimization for Robust Retrieval-Augmented Generation*.  
   <https://arxiv.org/html/2605.01302v1>  
   Code: <https://github.com/PeiYangLiu/CoRM-RAG>

2. A-TPT: *Angular Diversity Calibration Properties for Test-Time Prompt Tuning of Vision-Language Models*.  
   <https://arxiv.org/abs/2510.26441>  
   OpenReview: <https://openreview.net/forum?id=VhlSBZebEw>  
   Code: <https://github.com/MB-Shihab-Aaqil-Ahamed/A-TPT>

3. NEAT: *Negation-Aware Test-Time Adaptation for Vision-Language Models*.  
   <https://arxiv.org/abs/2507.19064>  
   Code: <https://github.com/hhc1997/NEAT>

4. NegBench: *Vision-Language Models Do Not Understand Negation*.  
   Project: <https://negbench.github.io/>  
   Code: <https://github.com/m1k2zoo/negbench>

5. FaithfulRAG: *Fact-Level Conflict Modeling for Context-Faithful Retrieval-Augmented Generation*.  
   <https://aclanthology.org/2025.acl-long.1062/>  
   Code: <https://github.com/DeepLearnXMU/Faithful-RAG>

6. NeurIPS 2026 Reviewer Guidelines.  
   <https://neurips.cc/Conferences/2026/ReviewerGuidelines>
