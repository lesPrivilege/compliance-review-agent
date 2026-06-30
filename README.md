# Compliance Review Agent

合规审查 Agent —— 基于 LangGraph 的多步推理 + RAG 检索 + 风险评分 + HITL 确认。

## 这是什么

一个演示项目，展示如何用 Agent 技术处理**知识密集型**的合规审查任务。与 `contract-approval-agent`（路由+HITL）互补——本项目的核心是 **RAG 检索 + 多步推理 + 风险评估**，不是路由。

**核心论点**：合规审查的难点不是「走哪条审批链」（那是路由问题），而是「这份材料是否合规」——需要检索法规、比对政策、评估风险、生成报告。这是 RAG + 推理的典型场景。

**诚实口径**：场景设计参考了多行业合规审查的通用模式，数据全部虚构，Agent 实现是为学习范式自己搭建的。

## 与 contract-approval-agent 的对比

| 维度 | contract-approval-agent | compliance-review-agent |
|------|------------------------|------------------------|
| 核心能力 | 路由 + HITL | RAG + 推理 + 评估 |
| 决策类型 | 「走哪条路」（结构化） | 「是否合规」（知识密集） |
| 工具使用 | 查表（审批矩阵） | 检索（法规/政策/案例） |
| 输出 | 审批路径 + 决策 | 合规报告 + 风险评分 |
| 推理模式 | 规则优先 + LLM 兜底 | LLM 多步推理 + 规则校验 |

## 架构

```
材料提交
   │
   ▼
┌──────────────────────────────────────────────────┐
│                LangGraph 图                       │
│                                                  │
│  ┌──────────┐    ┌──────────┐    ┌────────────┐ │
│  │ Ingest   │───▶│ Retrieve │───▶│  Analyze   │ │
│  │(解析材料) │    │(RAG检索)  │    │(多步推理)   │ │
│  └──────────┘    └──────────┘    └────────────┘ │
│                                       │          │
│                              ┌────────▼────────┐ │
│                              │    Score        │ │
│                              │ (风险评分)       │ │
│                              └────────┬────────┘ │
│                                       │          │
│                              ┌────────▼────────┐ │
│                              │     HITL       │ │
│                              │ (高风险→人工)    │ │
│                              └────────┬────────┘ │
│                                       │          │
│                              ┌────────▼────────┐ │
│                              │  Report Gen    │ │
│                              │ (生成审查报告)   │ │
│                              └────────────────┘ │
└──────────────────────────────────────────────────┘
```

### 每个节点的实现方式

| 节点 | 方式 | 为什么 |
|------|------|--------|
| **Ingest** | 解析输入材料（文本/表格/条款） | 结构化为可检索的片段 |
| **Retrieve** | RAG 检索法规、政策、先例 | 合规判断需要参考外部知识 |
| **Analyze** | LLM 多步推理（ReAct） | 需要综合多个信息源做判断 |
| **Score** | 纯代码 + LLM 辅助 | 风险评分需要可解释 |
| **HITL** | `interrupt()` + `Command(resume=...)` | 高风险审查必须人工确认 |
| **Report Gen** | LLM 生成结构化报告 | 输出需要可读、可审计 |

## 数据设计

所有数据虚构，覆盖多个行业的通用合规场景。

### 法规库 (`data/regulations/`)

```markdown
# 反垄断合规指引
## 适用范围
- 关联交易
- 市场支配地位滥用
- 竞争性业务与受监管业务的数据隔离
## 审查要点
1. 交易是否涉及关联方
2. 定价是否符合市场公允原则
3. 是否存在强制搭售
...
```

### 审查材料样本 (`data/materials.jsonl`)

```json
{
  "id": "M001",
  "test_case": "normal_pass",
  "材料类型": "采购合同",
  "内容摘要": "标准设备采购，非关联方，市场价格",
  "关联方标记": false,
  "金额": 200000,
  "说明": "标准采购，无合规风险"
}
```

### 四个测试场景

| ID | 场景 | 材料特征 | 预期行为 |
|----|------|----------|----------|
| M001 | 正常通过 | 标准采购，非关联方 | RAG 检索 → 分析 → 低风险 → 通过 |
| M002 | 关联方审查 | 关联方交易，需定价审查 | RAG 检索 → 分析 → 中风险 → HITL |
| M003 | 高风险阻断 | 大额担保，不可撤销条款 | RAG 检索 → 分析 → 高风险 → 阻断 |
| M004 | 跨业务隔离 | 涉及受监管业务数据 | Guardrail 直接阻断 |

## 运行

```bash
cd compliance-review-agent
uv sync
uv run python main.py --list
uv run python main.py --material M001
uv run pytest tests/ -v
```

## 8 个「为什么」

### 为什么是合规审查？

合规审查是**知识密集型**任务——需要检索法规、比对政策、评估风险。这与 contract-approval-agent（路由型任务）形成互补，展示不同类型的 agent 能力。

### 为什么需要 RAG？

合规判断需要参考外部知识（法规、政策、先例）。LLM 的训练数据不包含企业内部的合规政策，必须通过 RAG 注入。

### 为什么多步推理？

合规审查不是单一判断，而是多步骤的推理链：
1. 识别材料中的关键条款
2. 检索相关法规和政策
3. 逐条比对是否合规
4. 综合评估风险等级
5. 生成审查报告

这需要 ReAct 或 Plan-and-Execute 模式。

### 为什么 HITL？

高风险的合规审查（关联交易、大额担保）必须人工确认。合规审查的错误代价远高于审批路由——漏审一个条款可能导致法律风险。

### 为什么风险评分？

纯「通过/不通过」的二元判断不够。风险评分（低/中/高）让人工审查者可以优先处理高风险项，提高效率。

### 为什么独立报告生成？

合规审查的输出不是简单的「通过」，而是需要可审计的报告——审查了哪些条款、参考了哪些法规、发现了什么风险、给出什么建议。这需要独立的报告生成节点。

### 为什么与 contract-approval-agent 分开？

两个项目展示不同的 agent 能力：
- contract-approval-agent：路由 + HITL（结构化决策）
- compliance-review-agent：RAG + 推理（知识密集决策）

分开比合并更能证明「我理解不同场景需要不同架构」。

### 为什么用 LangGraph？

同 contract-approval-agent——图结构可审计、`interrupt()` 支持 HITL、Checkpointing 支持跨天暂停。合规审查流程比审批更复杂（多步推理），图结构的可视化和调试优势更明显。

## 项目结构

```
compliance-review-agent/
├── README.md
├── TODO.md
├── pyproject.toml
├── .env.example
├── main.py
├── src/
│   ├── state.py
│   ├── graph.py
│   ├── config.py
│   ├── tools.py
│   └── nodes/
│       ├── ingest.py
│       ├── retrieve.py
│       ├── analyze.py
│       ├── score.py
│       ├── hitl.py
│       └── report_gen.py
├── data/
│   ├── regulations/
│   ├── materials.jsonl
│   └── templates/
├── tests/
│   └── test_trajectories.py
└── scripts/
    └── generate_data.py
```

## 参考信源

| 信源 | 用途 |
|------|------|
| Anthropic「Building Effective Agents」 | 架构哲学：从简单开始 |
| LangGraph docs | 图结构 + HITL + checkpointing |
| OpenAI Agents SDK | RAG + multi-step reasoning 模式 |
| ReAct 论文 (Yao et al., ICLR 2023) | 多步推理范式 |
