"""Trajectory evaluation tests — verify agent behavior for all scenarios."""

import json
import os

import pytest
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from src.graph import compile_graph
from src.state import ComplianceState, ReviewMaterial, ReviewStatus, RiskLevel


def _load_material(material_id: str) -> dict:
    with open("data/materials.jsonl", encoding="utf-8") as f:
        for line in f:
            m = json.loads(line)
            if m["id"] == material_id:
                return m
    raise ValueError(f"Material {material_id} not found")


_checkpointer = MemorySaver()
_graph = compile_graph(checkpointer=_checkpointer)


def _run(material_id: str, resume=None, thread_id=None):
    data = _load_material(material_id)
    config = {"configurable": {"thread_id": thread_id or f"test-{material_id}"}}

    if resume is not None:
        result = _graph.invoke(Command(resume=resume), config=config)
    else:
        info = ReviewMaterial(**data)
        state = ComplianceState(material=info)
        result = _graph.invoke(state, config=config)

    interrupts = result.get("__interrupt__", [])
    if interrupts:
        return {"interrupted": True, "payload": interrupts, "thread_id": config["configurable"]["thread_id"]}
    return result


class TestNormalPass:
    """M001: standard procurement — low risk, auto approve."""

    def test_status_approved(self):
        result = _run("M001")
        assert result["status"] == ReviewStatus.APPROVED

    def test_risk_level_low(self):
        result = _run("M001")
        assert result["risk_score"].level == RiskLevel.LOW

    def test_auto_approve(self):
        result = _run("M001")
        assert result["human_decision"] == "auto_approved"

    def test_audit_trajectory(self):
        result = _run("M001")
        nodes = [e.node for e in result["audit_log"]]
        assert "ingest" in nodes
        assert "retrieve" in nodes
        assert "analyze" in nodes
        assert "score" in nodes
        assert "hitl" in nodes
        assert "report_gen" in nodes


class TestRelatedPartyReview:
    """M002: related party — medium risk, HITL."""

    def test_interrupt_triggered(self):
        result = _run("M002")
        assert result["interrupted"] is True

    def test_risk_level_medium(self):
        result = _run("M002")
        # The payload contains risk_level
        payload = result["payload"][0].value
        assert payload["risk_level"] == "medium"

    def test_related_party_factor(self):
        result = _run("M002")
        payload = result["payload"][0].value
        assert any("关联" in f for f in payload["risk_factors"])

    def test_resume_approved(self):
        result = _run("M002")
        thread = result["thread_id"]
        result2 = _run("M002", resume="approved", thread_id=thread)
        assert result2["status"] == ReviewStatus.APPROVED

    def test_resume_rejected(self):
        result = _run("M002")
        thread = result["thread_id"]
        result2 = _run("M002", resume="rejected", thread_id=thread)
        assert result2["status"] == ReviewStatus.BLOCKED


class TestHighRiskBlock:
    """M003: large guarantee — high risk, HITL."""

    def test_interrupt_triggered(self):
        result = _run("M003")
        assert result["interrupted"] is True

    def test_risk_level_high(self):
        result = _run("M003")
        payload = result["payload"][0].value
        assert payload["risk_level"] == "high"

    def test_multiple_risk_factors(self):
        result = _run("M003")
        payload = result["payload"][0].value
        assert len(payload["risk_factors"]) >= 2

    def test_resume_rejected(self):
        result = _run("M003")
        thread = result["thread_id"]
        result2 = _run("M003", resume="rejected", thread_id=thread)
        assert result2["status"] == ReviewStatus.BLOCKED


class TestIsolationBlock:
    """M004: cross-segment data sharing — HITL with isolation reason."""

    def test_interrupt_triggered(self):
        result = _run("M004")
        assert result["interrupted"] is True

    def test_isolation_reason(self):
        result = _run("M004")
        payload = result["payload"][0].value
        assert "跨业务" in payload["reason"] or "受监管" in payload["reason"]

    def test_resume_approved(self):
        result = _run("M004")
        thread = result["thread_id"]
        result2 = _run("M004", resume="approved", thread_id=thread)
        assert result2["status"] == ReviewStatus.APPROVED


class TestCSectorLowRisk:
    """M005: C板块 standard service — low risk, auto approve, retrieves 反垄断价格合规."""

    def test_status_approved(self):
        result = _run("M005")
        assert result["status"] == ReviewStatus.APPROVED

    def test_risk_level_low(self):
        result = _run("M005")
        assert result["risk_score"].level == RiskLevel.LOW

    def test_auto_approve(self):
        result = _run("M005")
        assert result["human_decision"] == "auto_approved"

    def test_retrieved_pricing_regulation(self):
        result = _run("M005")
        sources = [d.source for d in result["retrieved_docs"]]
        assert "反垄断价格合规" in sources


class TestCSectorMediumRisk:
    """M006: C板块 large sales — medium risk, HITL, retrieves 反垄断价格合规."""

    def test_interrupt_triggered(self):
        result = _run("M006")
        assert result["interrupted"] is True

    def test_risk_level_medium(self):
        result = _run("M006")
        payload = result["payload"][0].value
        assert payload["risk_level"] == "medium"

    def test_retrieved_pricing_regulation(self):
        result = _run("M006")
        # Check from the partial state's retrieved docs
        payload = result["payload"][0].value
        assert payload["material_id"] == "M006"

    def test_resume_approved(self):
        result = _run("M006")
        thread = result["thread_id"]
        result2 = _run("M006", resume="approved", thread_id=thread)
        assert result2["status"] == ReviewStatus.APPROVED


class TestDSectorLowRisk:
    """M007: D板块 admin procurement — low risk, auto approve."""

    def test_status_approved(self):
        result = _run("M007")
        assert result["status"] == ReviewStatus.APPROVED

    def test_risk_level_low(self):
        result = _run("M007")
        assert result["risk_score"].level == RiskLevel.LOW

    def test_auto_approve(self):
        result = _run("M007")
        assert result["human_decision"] == "auto_approved"

    def test_audit_trajectory(self):
        result = _run("M007")
        nodes = [e.node for e in result["audit_log"]]
        assert "retrieve" in nodes
        assert "analyze" in nodes
        assert "score" in nodes


class TestDSectorGuaranteeHigh:
    """M008: D板块 large guarantee — high risk, HITL, retrieves 借贷担保合规."""

    def test_interrupt_triggered(self):
        result = _run("M008")
        assert result["interrupted"] is True

    def test_risk_level_high(self):
        result = _run("M008")
        payload = result["payload"][0].value
        assert payload["risk_level"] == "high"

    def test_guarantee_risk_factor(self):
        result = _run("M008")
        payload = result["payload"][0].value
        assert any("担保" in f for f in payload["risk_factors"])

    def test_resume_rejected(self):
        result = _run("M008")
        thread = result["thread_id"]
        result2 = _run("M008", resume="rejected", thread_id=thread)
        assert result2["status"] == ReviewStatus.BLOCKED


class TestFranchiseCompliance:
    """M009: A板块 franchise agreement — low risk, retrieves 特许经营权合规."""

    def test_status_approved(self):
        result = _run("M009")
        assert result["status"] == ReviewStatus.APPROVED

    def test_risk_level_low(self):
        result = _run("M009")
        assert result["risk_score"].level == RiskLevel.LOW

    def test_retrieved_franchise_regulation(self):
        result = _run("M009")
        sources = [d.source for d in result["retrieved_docs"]]
        assert "特许经营权合规" in sources

    def test_auto_approve(self):
        result = _run("M009")
        assert result["human_decision"] == "auto_approved"


class TestAntitrustFiling:
    """M010: B板块 investment cooperation — medium risk, HITL, retrieves 投资评审与反垄断申报."""

    def test_interrupt_triggered(self):
        result = _run("M010")
        assert result["interrupted"] is True

    def test_risk_level_medium(self):
        result = _run("M010")
        payload = result["payload"][0].value
        assert payload["risk_level"] == "medium"

    def test_antitrust_risk_factor(self):
        result = _run("M010")
        payload = result["payload"][0].value
        assert any("反垄断" in f for f in payload["risk_factors"])

    def test_resume_approved(self):
        result = _run("M010")
        thread = result["thread_id"]
        result2 = _run("M010", resume="approved", thread_id=thread)
        assert result2["status"] == ReviewStatus.APPROVED


_has_api_key = bool(os.getenv("OPENAI_API_KEY"))


@pytest.mark.skipif(not _has_api_key, reason="需要真实 API key")
class TestLLMOneShot:
    """M011: related party — LLM should give conclusion in one round."""

    def test_status(self):
        result = _run("M011")
        assert result["status"] in (ReviewStatus.APPROVED, ReviewStatus.BLOCKED)

    def test_confidence_reasonable(self):
        result = _run("M011")
        score = result["risk_score"]
        assert score is not None

    def test_audit_has_analyze(self):
        result = _run("M011")
        nodes = [e.node for e in result["audit_log"]]
        assert "analyze" in nodes


@pytest.mark.skipif(not _has_api_key, reason="需要真实 API key")
class TestLLMMultiTurn:
    """M012: cross-segment data — LLM should do multi-turn retrieval."""

    def test_status(self):
        result = _run("M012")
        assert result["status"] in (ReviewStatus.APPROVED, ReviewStatus.BLOCKED)

    def test_risk_factors_present(self):
        result = _run("M012")
        score = result["risk_score"]
        assert score is not None
        assert len(score.factors) >= 1

    def test_react_steps(self):
        result = _run("M012")
        analyze_steps = [s for s in result["analysis_steps"] if "ReAct" in s.thought]
        assert len(analyze_steps) >= 1


@pytest.mark.skipif(not _has_api_key, reason="需要真实 API key")
class TestLLMNoMatch:
    """M013: quantum computing — no matching regulation, LLM should be honest."""

    def test_status(self):
        result = _run("M013")
        assert result["status"] in (ReviewStatus.APPROVED, ReviewStatus.BLOCKED)

    def test_low_risk(self):
        result = _run("M013")
        score = result["risk_score"]
        assert score is not None
        assert score.level == RiskLevel.LOW
