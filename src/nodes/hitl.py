"""HITL node — pause for human confirmation on medium/high risk."""

import time

from langgraph.types import interrupt

from src.state import AuditEntry, ComplianceState, RiskLevel, ReviewStatus


def hitl_node(state: ComplianceState) -> dict:
    """Check if HITL is needed; if so, pause and wait for human decision."""
    start = time.perf_counter()
    material = state.material
    risk_score = state.risk_score

    # Check if human review is needed
    needs_hitl = False
    reason = ""

    if risk_score and risk_score.level in (RiskLevel.MEDIUM, RiskLevel.HIGH):
        needs_hitl = True
        reason = f"风险等级 {risk_score.level.value}，需人工确认"

    # Also check for isolation violation
    if material.涉及数据共享 and material.涉及受监管业务:
        needs_hitl = True
        reason = "跨业务数据共享，需合规审查"

    if needs_hitl:
        payload = {
            "material_id": material.id,
            "material_type": material.材料类型,
            "amount": material.金额,
            "risk_level": risk_score.level.value if risk_score else "unknown",
            "risk_factors": risk_score.factors if risk_score else [],
            "reason": reason,
            "question": "请确认此材料的合规审查结果",
        }

        decision = interrupt(payload)

        duration = max(1, int((time.perf_counter() - start) * 1000))

        audit = AuditEntry(
            node="hitl",
            action="human_review",
            input_summary=f"需人工确认: {reason}",
            output_summary=f"人工决策: {decision}",
            decision=str(decision),
            duration_ms=duration,
        )

        if decision in ("approved", "approve", True, "pass"):
            return {
                "human_decision": "approved",
                "status": ReviewStatus.APPROVED,
                "current_step": "approved",
                "audit_log": state.audit_log + [audit],
            }
        else:
            return {
                "human_decision": "rejected",
                "status": ReviewStatus.BLOCKED,
                "block_reason": "人工驳回",
                "current_step": "blocked",
                "audit_log": state.audit_log + [audit],
            }
    else:
        # Low risk — auto approve
        duration = max(1, int((time.perf_counter() - start) * 1000))

        audit = AuditEntry(
            node="hitl",
            action="auto_approve",
            input_summary="低风险，无需人工确认",
            output_summary="自动通过",
            decision="auto_approved",
            duration_ms=duration,
        )

        return {
            "human_decision": "auto_approved",
            "status": ReviewStatus.APPROVED,
            "current_step": "approved",
            "audit_log": state.audit_log + [audit],
        }
