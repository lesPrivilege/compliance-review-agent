"""Score node — assign risk level based on analysis."""

import time

from src.state import (
    AuditEntry,
    ComplianceReport,
    ComplianceState,
    ReviewStatus,
    RiskLevel,
    RiskScore,
)
from src.tools import check_data_isolation, check_related_party


def score_node(state: ComplianceState) -> dict:
    """Score compliance risk based on analysis results."""
    start = time.perf_counter()
    material = state.material
    steps = state.analysis_steps

    # Determine risk level
    risk_factors = []

    # High risk conditions
    if material.条款标记.get("担保") and material.金额 > 5000000:
        risk_factors.append("大额对外担保")
    if material.涉及数据共享 and material.涉及受监管业务:
        risk_factors.append("受监管业务数据流向竞争性业务")

    # Medium risk conditions
    if material.关联方标记:
        risk_factors.append("关联交易需独立评估")
    if material.金额 > 5000000:
        risk_factors.append("大额交易")
    if material.条款标记.get("不可逆"):
        risk_factors.append("不可撤销条款")
    if "反垄断" in material.内容摘要 and material.金额 > 3000000:
        risk_factors.append("达到反垄断申报阈值")

    # Merge LLM-discovered risk factors (complementary, not replacement)
    for factor in state.llm_risk_factors:
        if factor not in risk_factors:
            risk_factors.append(factor)

    # Merge LLM-discovered regulations
    all_regulations = [d.source for d in state.retrieved_docs]
    for reg in state.llm_regulations:
        if reg not in all_regulations and reg != "未找到直接依据":
            all_regulations.append(reg)

    # Determine level
    if len(risk_factors) >= 2 or any("受监管" in r for r in risk_factors):
        level = RiskLevel.HIGH
    elif len(risk_factors) >= 1:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW

    # Build report
    report = ComplianceReport(
        summary=f"材料 {material.id} 审查完成：{level.value} 风险",
        risk_factors=risk_factors,
        recommendations=["建议人工审查"] if level != RiskLevel.LOW else ["可自动通过"],
        regulations_checked=all_regulations,
    )

    duration = max(1, int((time.perf_counter() - start) * 1000))

    audit = AuditEntry(
        node="score",
        action="risk_scoring",
        input_summary=f"风险因素: {len(risk_factors)}",
        output_summary=f"风险等级: {level.value}",
        decision=level.value,
        duration_ms=duration,
    )

    return {
        "risk_score": RiskScore(
            level=level,
            factors=risk_factors,
            reasoning=f"基于 {len(risk_factors)} 个风险因素评估",
        ),
        "report": report,
        "current_step": "scored",
        "status": ReviewStatus.SCORED,
        "audit_log": state.audit_log + [audit],
    }
