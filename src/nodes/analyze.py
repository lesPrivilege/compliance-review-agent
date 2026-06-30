"""Analyze node — multi-step reasoning to evaluate compliance."""

import time

from src.state import AnalysisStep, AuditEntry, ComplianceState, ReviewStatus


def analyze_node(state: ComplianceState) -> dict:
    """Analyze material against retrieved regulations using structured reasoning."""
    start = time.time()
    material = state.material
    docs = state.retrieved_docs

    # Build analysis context
    reg_context = "\n".join([f"[{d.source}] {d.content[:200]}" for d in docs[:3]])

    # Structured analysis steps (simulating ReAct reasoning)
    steps = []

    # Step 1: Identify risk factors
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

    steps.append(AnalysisStep(
        thought="识别材料中的风险因素",
        action="check_risk_factors",
        observation=f"发现 {len(risk_factors)} 个风险因素",
    ))

    # Step 2: Cross-reference with regulations
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

    # Step 3: Overall assessment
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

    duration = int((time.time() - start) * 1000)

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
    }
