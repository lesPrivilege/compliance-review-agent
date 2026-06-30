"""Retrieve node — RAG search for relevant regulations."""

import time

from src.state import AuditEntry, ComplianceState, RetrievedDoc, ReviewStatus
from src.tools import search_regulations


def retrieve_node(state: ComplianceState) -> dict:
    """Search regulations relevant to this material."""
    start = time.time()
    material = state.material

    # Build search queries from material
    queries = [material.材料类型, material.内容摘要[:50]]
    if material.关联方标记:
        queries.append("关联交易")
    if material.涉及数据共享:
        queries.append("数据隐私")
    if material.条款标记.get("担保"):
        queries.append("担保")

    # Search regulations
    all_docs = []
    seen_sources = set()
    for q in queries:
        results = search_regulations(q)
        for r in results:
            if r["source"] not in seen_sources:
                seen_sources.add(r["source"])
                all_docs.append(RetrievedDoc(
                    source=r["source"],
                    content=r["excerpt"],
                    relevance=1.0,
                ))

    duration = int((time.time() - start) * 1000)

    audit = AuditEntry(
        node="retrieve",
        action="search_regulations",
        input_summary=f"查询: {', '.join(queries[:3])}",
        output_summary=f"检索到 {len(all_docs)} 条法规",
        decision="found" if all_docs else "missing",
        duration_ms=duration,
    )

    return {
        "retrieved_docs": all_docs,
        "current_step": "retrieved",
        "status": ReviewStatus.RETRIEVED,
        "audit_log": state.audit_log + [audit],
    }
