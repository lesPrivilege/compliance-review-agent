# TODO · Compliance Review Agent MVP

## 设计决策速查

| 决策 | 选择 | 理由 |
|------|------|------|
| 核心范式 | RAG + ReAct 多步推理 | 合规审查是知识密集型任务 |
| 推理模式 | ReAct（Thought→Action→Observation） | 需要综合多个信息源做判断 |
| RAG 实现 | ChromaDB + 本地法规库 | MVP 用本地向量库，生产可换 |
| 风险评分 | 低/中/高 三级 | 让人工审查者可以优先处理高风险项 |
| HITL 触发 | 中风险及以上 | 低风险自动通过，中高风险人工确认 |
| 输出格式 | 结构化合规报告（JSON + 可读文本） | 可审计、可追溯 |

---

## Phase 0：项目初始化（P0）

- [x] 初始化 Python 项目（uv）
- [x] 配置 LangGraph + LangChain
- [x] 配置 LLM Provider（环境变量）
- [x] main.py 入口
- [x] README.md

验收：`uv run python main.py` 正常启动 ✓

---

## Phase 1：业务数据（P0）

- [x] 法规库（`data/regulations/`）：4 个通用合规领域
- [x] 审查材料（`data/materials.jsonl`）：4 种场景
- [x] 审查模板（隐含在 report_gen 节点）

验收：数据格式正确，覆盖四类分支 ✓

---

## Phase 2：Graph State（P0）

- [x] 定义 ComplianceState（Pydantic BaseModel）
- [x] 字段：material / retrieved_docs / analysis_steps / risk_score / report / status / audit_log
- [x] 状态流转：pending → ingested → retrieved → analyzed → scored → approved/blocked

验收：State 可序列化 ✓

---

## Phase 3：RAG 管线（P0）

- [x] 法规库 ingest（关键词匹配，MVP 简化）
- [x] 检索函数（search_regulations）
- [x] 检索失败兜底

验收：`search_regulations("关联交易")` 返回相关法规片段 ✓

---

## Phase 4：Graph（P0）

- [x] Ingest 节点
- [x] Retrieve 节点
- [x] Analyze 节点（多步推理）
- [x] Score 节点（风险评分）
- [x] HITL 节点（interrupt/resume）
- [x] Report Gen 节点
- [x] 条件边

验收：graph.compile() 成功 ✓

---

## Phase 5：Evaluation（P1）

- [x] Case 1：正常通过 → 低风险 → auto approve
- [x] Case 2：关联方审查 → 中风险 → HITL → resume
- [x] Case 3：高风险阻断 → 高风险 → HITL → resume
- [x] Case 4：跨业务隔离 → 高风险 → HITL → resume

验收：`uv run pytest tests/ -v` 全部通过 ✓（16/16）

---

## Phase 6：Audit（P1）

- [x] append-only JSONL 审计日志
- [x] 记录每步推理过程
- [x] 记录检索结果和风险评分依据

验收：完整 trace 可回放 ✓

---

## Phase 7：README 完善（P0）

- [ ] 架构图
- [ ] 状态图
- [ ] 运行方式
- [ ] 8 个「为什么」
- [ ] 90 秒讲解

---

## Don't Do

- 真实法规数据
- 数据库
- 用户系统
- 前端页面
- 真实 ERP 集成
- Docker / K8s
