"""Ingest node — parse material and extract key clauses."""

import time

from src.state import AuditEntry, ComplianceState, ReviewStatus


def ingest_node(state: ComplianceState) -> dict:
    """Parse material, extract key information for downstream analysis."""
    start = time.time()
    material = state.material

    # Extract key clauses from material summary
    clauses = []
    summary = material.内容摘要

    # Check for risk indicators
    if material.关联方标记:
        clauses.append("关联交易")
    if material.涉及数据共享:
        clauses.append("数据共享")
    if material.涉及受监管业务:
        clauses.append("涉及受监管业务")
    if material.条款标记.get("担保"):
        clauses.append("对外担保")
    if material.条款标记.get("不可逆"):
        clauses.append("不可撤销条款")
    if material.金额 > 5000000:
        clauses.append("大额交易")

    # Build search queries for RAG
    search_queries = [material.材料类型]
    search_queries.extend(clauses)

    duration = int((time.time() - start) * 1000)

    audit = AuditEntry(
        node="ingest",
        action="parse_material",
        input_summary=f"材料 {material.id}: {material.材料类型}",
        output_summary=f"提取 {len(clauses)} 个关键条款: {', '.join(clauses) if clauses else '无'}",
        decision="parsed",
        duration_ms=duration,
    )

    return {
        "current_step": "ingested",
        "status": ReviewStatus.INGESTED,
        "audit_log": state.audit_log + [audit],
    }
