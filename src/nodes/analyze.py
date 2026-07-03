"""Analyze node — real LLM ReAct loop when API key available, deterministic fallback otherwise."""

import os
import time

from src.state import (
    AnalysisStep,
    AuditEntry,
    ComplianceAnalysis,
    ComplianceState,
    ReviewStatus,
)
from src.tools import search_regulations_tool

_MAX_ITERATIONS = 2
_has_api_key = bool(os.getenv("OPENAI_API_KEY"))


def _usage_from_response(response) -> dict:
    """Extract token counts from LangChain response metadata."""
    usage = getattr(response, "usage_metadata", None) or {}
    if not usage:
        response_metadata = getattr(response, "response_metadata", {}) or {}
        usage = response_metadata.get("token_usage", {}) or {}
    return {
        "tokens_in": usage.get("input_tokens") or usage.get("prompt_tokens"),
        "tokens_out": usage.get("output_tokens") or usage.get("completion_tokens"),
    }


def _deterministic_analyze(state: ComplianceState) -> dict:
    """Original hardcoded analysis — used when no API key is available."""
    start = time.perf_counter()
    material = state.material
    docs = state.retrieved_docs

    steps = []

    risk_factors = []
    if material.关联方标记:
        risk_factors.append("关联交易：需审查定价公允性和审批程序")
    if material.涉及数据共享 and material.涉及受监管业务:
        risk_factors.append("跨业务数据共享：受监管业务数据可能流向竞争性业务")
    if material.条款标记.get("担保"):
        risk_factors.append("对外担保：高风险财务承诺")
    if material.条款标记.get("不可逆"):
        risk_factors.append("不可撤销条款：无法单方面撤回")
    if material.金额 > 5000000:
        risk_factors.append(f"大额交易（{material.金额:,}元）：需高层审批")
    if "反垄断" in material.内容摘要 and material.金额 > 3000000:
        risk_factors.append("达到反垄断申报阈值，需审查申报义务履行情况")

    steps.append(AnalysisStep(
        thought="识别材料中的风险因素",
        action="check_risk_factors",
        observation=f"发现 {len(risk_factors)} 个风险因素",
    ))

    reg_findings = []
    for doc in docs:
        if "关联方" in doc.content and material.关联方标记:
            reg_findings.append(f"[{doc.source}] 关联交易需独立评估定价")
        if "数据隔离" in doc.content or "反垄断" in doc.content:
            if material.涉及数据共享:
                reg_findings.append(f"[{doc.source}] 跨业务数据需隔离审查")
        if "担保" in doc.content and material.条款标记.get("担保"):
            reg_findings.append(f"[{doc.source}] 对外担保需高层审批")

    steps.append(AnalysisStep(
        thought="将风险因素与检索到的法规交叉比对",
        action="cross_reference",
        observation=f"找到 {len(reg_findings)} 条相关法规依据",
    ))

    if len(risk_factors) == 0:
        assessment = "无明显合规风险"
    elif any("跨业务" in r or "受监管" in r for r in risk_factors):
        assessment = "存在跨业务合规风险，需隔离审查"
    elif any("担保" in r or "不可逆" in r for r in risk_factors):
        assessment = "存在高风险条款，需人工确认"
    elif material.关联方标记:
        assessment = "关联交易，定价需独立评估"
    else:
        assessment = "存在中等风险，建议审查"

    steps.append(AnalysisStep(
        thought="综合评估合规风险",
        action="overall_assessment",
        observation=assessment,
    ))

    duration = max(1, int((time.perf_counter() - start) * 1000))

    audit = AuditEntry(
        node="analyze",
        action="multi_step_analysis",
        input_summary=f"{len(docs)} 条法规, {len(risk_factors)} 个风险因素",
        output_summary=assessment,
        decision="analyzed",
        duration_ms=duration,
    )

    return {
        "analysis_steps": steps,
        "current_step": "analyzed",
        "status": ReviewStatus.ANALYZED,
        "audit_log": state.audit_log + [audit],
        "llm_risk_factors": [],
        "llm_regulations": [],
    }


def _llm_react_analyze(state: ComplianceState) -> dict:
    """Real LLM ReAct loop — used when API key is available."""
    from src.config import get_llm

    start = time.perf_counter()
    material = state.material
    docs = state.retrieved_docs

    reg_context = "\n".join([f"[{d.source}] {d.content[:300]}" for d in docs[:3]])

    material_info = (
        f"材料ID: {material.id}\n"
        f"类型: {material.材料类型}\n"
        f"板块: {material.板块}\n"
        f"金额: {material.金额:,}元\n"
        f"摘要: {material.内容摘要}\n"
        f"关联方: {material.关联方标记}\n"
        f"数据共享: {material.涉及数据共享}\n"
        f"受监管业务: {material.涉及受监管业务}\n"
        f"条款标记: {material.条款标记}"
    )

    llm = get_llm().bind_tools([search_regulations_tool])
    steps = []
    all_regulations = [d.source for d in docs]
    total_tokens_in = 0
    total_tokens_out = 0

    messages = [
        {"role": "system", "content": (
            "你是合规审查分析师。根据提供的材料和法规，分析合规风险。"
            "如果现有信息足够下结论，直接给出结论。"
            "如果需要更多法规依据，使用 search_regulations_tool 搜索。"
            "最多搜索2轮。"
        )},
        {"role": "user", "content": (
            f"## 待审材料\n{material_info}\n\n"
            f"## 已检索法规\n{reg_context if reg_context else '（无初始检索结果）'}\n\n"
            f"请分析此材料的合规风险。如果需要更多法规，调用搜索工具。"
        )},
    ]

    for iteration in range(_MAX_ITERATIONS):
        response = llm.invoke(messages)
        messages.append(response)

        usage = _usage_from_response(response)
        total_tokens_in += usage["tokens_in"] or 0
        total_tokens_out += usage["tokens_out"] or 0

        steps.append(AnalysisStep(
            thought=f"ReAct 第{iteration + 1}轮: LLM 分析",
            action="llm_analyze",
            observation=f"tool_calls={len(response.tool_calls)}",
        ))

        if not response.tool_calls:
            break

        for tc in response.tool_calls:
            tool_result = search_regulations_tool.invoke(tc["args"])
            messages.append({"role": "tool", "content": tool_result, "tool_call_id": tc["id"]})
            query = tc["args"].get("query", "")
            steps.append(AnalysisStep(
                thought=f"需要更多法规依据: {query}",
                action="search_regulations",
                observation=tool_result[:200],
            ))

    structured_llm = get_llm().with_structured_output(ComplianceAnalysis)
    final_messages = messages + [
        {"role": "user", "content": (
            "请基于以上分析，输出结构化的合规审查结论。"
            "confidence 表示你的结论有多少法规依据支撑（1=有明确法规明文支持，0=完全没有法规覆盖、只能凭常识判断）——"
            "不是你对'风险高低'这个判断本身有多大把握。法规库查不到东西时，即使你倾向于认为风险不高，confidence 也应该低。"
            "如果法规库中没有直接依据，在 regulations_cited 中注明'未找到直接依据'。"
        )}
    ]
    analysis = structured_llm.invoke(final_messages)

    for reg in analysis.regulations_cited:
        if reg not in all_regulations and reg != "未找到直接依据":
            all_regulations.append(reg)

    steps.append(AnalysisStep(
        thought="结构化输出",
        action="compliance_analysis",
        observation=f"置信度={analysis.confidence:.2f}, 风险因素={len(analysis.risk_factors)}",
    ))

    duration = max(1, int((time.perf_counter() - start) * 1000))

    audit = AuditEntry(
        node="analyze",
        action="react_loop",
        input_summary=f"{len(docs)} 条初始法规, {len(steps)} 步推理",
        output_summary=analysis.overall_assessment[:80],
        decision="analyzed",
        duration_ms=duration,
        tokens_in=total_tokens_in or None,
        tokens_out=total_tokens_out or None,
    )

    return {
        "analysis_steps": steps,
        "current_step": "analyzed",
        "status": ReviewStatus.ANALYZED,
        "audit_log": state.audit_log + [audit],
        "llm_risk_factors": analysis.risk_factors,
        "llm_regulations": analysis.regulations_cited,
    }


def analyze_node(state: ComplianceState) -> dict:
    """Analyze material — LLM ReAct when key available, deterministic fallback otherwise."""
    if _has_api_key:
        return _llm_react_analyze(state)
    return _deterministic_analyze(state)
