"""Trajectory evaluation tests — verify agent behavior for all 4 scenarios."""

import json

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
