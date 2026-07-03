"""Report generation node — produce structured compliance report."""

import json
import time
from pathlib import Path

from src.state import AuditEntry, ComplianceReport, ComplianceState, ReviewStatus

AUDIT_LOG_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "audit_log.jsonl"
TRACE_LOG_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "trace_log.jsonl"


def report_gen_node(state: ComplianceState) -> dict:
    """Generate final compliance report and write audit log."""
    start = time.perf_counter()
    material = state.material
    risk_score = state.risk_score
    analysis = state.analysis_steps

    # Build final report
    report = state.report or ComplianceReport()

    # Enrich report with analysis details
    if analysis:
        report.summary = (
            f"材料 {material.id}（{material.材料类型}）合规审查完成。"
            f"风险等级：{risk_score.level.value if risk_score else '未评估'}。"
        )
        if risk_score and risk_score.factors:
            report.risk_factors = risk_score.factors

    # Write audit log
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        for entry in state.audit_log:
            record = entry.model_dump()
            record["timestamp"] = record["timestamp"].isoformat()
            record["material_id"] = state.material.id
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Write trace log
    if state.trace_steps:
        with open(TRACE_LOG_PATH, "a", encoding="utf-8") as f:
            for step in state.trace_steps:
                f.write(json.dumps(step, ensure_ascii=False) + "\n")

    duration = max(1, int((time.perf_counter() - start) * 1000))

    audit = AuditEntry(
        node="report_gen",
        action="generate_report",
        input_summary=f"材料 {material.id}, 风险 {risk_score.level.value if risk_score else 'N/A'}",
        output_summary="报告已生成",
        decision="completed",
        duration_ms=duration,
    )

    return {
        "report": report,
        "current_step": "completed",
        "audit_log": state.audit_log + [audit],
    }
