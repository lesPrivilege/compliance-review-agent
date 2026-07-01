"""Graph State — Pydantic model shared across all nodes."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    INGESTED = "ingested"
    RETRIEVED = "retrieved"
    ANALYZED = "analyzed"
    SCORED = "scored"
    WAITING_HITL = "waiting_hitl"
    APPROVED = "approved"
    BLOCKED = "blocked"


class RetrievedDoc(BaseModel):
    source: str
    content: str
    relevance: float = 0.0


class AnalysisStep(BaseModel):
    thought: str
    action: str
    observation: str
    timestamp: datetime = Field(default_factory=datetime.now)


class RiskScore(BaseModel):
    level: RiskLevel
    factors: list[str] = Field(default_factory=list)
    reasoning: str = ""


class ComplianceReport(BaseModel):
    summary: str = ""
    risk_factors: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    regulations_checked: list[str] = Field(default_factory=list)


class ComplianceAnalysis(BaseModel):
    """LLM structured output for ReAct analysis loop."""
    risk_factors: list[str]
    overall_assessment: str
    confidence: float
    regulations_cited: list[str]


class AuditEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    node: str
    action: str
    input_summary: str
    output_summary: str
    decision: str
    duration_ms: int = 0


class ReviewMaterial(BaseModel):
    id: str
    材料类型: str
    板块: str
    内容摘要: str
    关联方标记: bool = False
    金额: int = 0
    涉及数据共享: bool = False
    涉及受监管业务: bool = False
    条款标记: dict[str, bool] = Field(default_factory=dict)
    说明: str = ""


class ComplianceState(BaseModel):
    # Core data
    material: ReviewMaterial
    retrieved_docs: list[RetrievedDoc] = Field(default_factory=list)
    analysis_steps: list[AnalysisStep] = Field(default_factory=list)

    # Results
    risk_score: RiskScore | None = None
    report: ComplianceReport | None = None
    llm_risk_factors: list[str] = Field(default_factory=list)
    llm_regulations: list[str] = Field(default_factory=list)

    # Flow control
    current_step: str = "pending"
    status: ReviewStatus = ReviewStatus.PENDING
    block_reason: str | None = None

    # HITL
    interrupt_reason: str | None = None
    human_decision: str | None = None

    # Audit
    audit_log: list[AuditEntry] = Field(default_factory=list)
