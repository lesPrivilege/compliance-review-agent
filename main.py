"""Compliance Review Agent — Entry point."""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("compliance-agent")

DATA_DIR = Path(__file__).parent / "data"

_checkpointer = None
_graph = None


def _get_graph():
    global _checkpointer, _graph
    if _graph is None:
        from langgraph.checkpoint.memory import MemorySaver
        from src.graph import compile_graph
        _checkpointer = MemorySaver()
        _graph = compile_graph(checkpointer=_checkpointer)
    return _graph


def load_material(material_id: str) -> dict | None:
    with open(DATA_DIR / "materials.jsonl", encoding="utf-8") as f:
        for line in f:
            m = json.loads(line)
            if m["id"] == material_id:
                return m
    return None


def list_materials():
    with open(DATA_DIR / "materials.jsonl", encoding="utf-8") as f:
        for line in f:
            m = json.loads(line)
            print(f"  {m['id']} | {m['test_case']:25s} | {m['材料类型']:6s} | {m['说明']}")


def run_material(material_data: dict, resume_value=None, thread_id=None):
    from src.state import ComplianceState, ReviewMaterial

    material_info = ReviewMaterial(**material_data)
    state = ComplianceState(material=material_info)
    graph = _get_graph()
    config = {"configurable": {"thread_id": thread_id or f"review-{material_info.id}"}}

    logger.info(f"Reviewing material {material_info.id}: {material_info.材料类型}, ¥{material_info.金额:,}")

    if resume_value is not None:
        from langgraph.types import Command
        result = graph.invoke(Command(resume=resume_value), config=config)
    else:
        result = graph.invoke(state, config=config)

    interrupts = result.get("__interrupt__", [])
    if interrupts:
        return {
            "interrupted": True,
            "interrupt_payload": interrupts,
            "thread_id": config["configurable"]["thread_id"],
            "partial_state": result,
        }

    return result


def print_result(result):
    print("\n" + "=" * 60)

    if result.get("interrupted"):
        print("⏸  HITL 中断 — 等待人工确认")
        for interrupt in result.get("interrupt_payload", []):
            payload = interrupt.value
            if isinstance(payload, dict):
                print(f"\n审查请求:")
                for k, v in payload.items():
                    print(f"  {k}: {v}")
            else:
                print(f"  {payload}")
        print(f"\n恢复命令:")
        print(f"  python main.py --material <ID> --resume approved --thread {result.get('thread_id', 'review')}")
        print("=" * 60)
        return

    material = result["material"]
    print(f"材料 ID: {material.id}")
    print(f"状态: {result['status'].value}")
    print(f"当前步骤: {result['current_step']}")

    if result.get("risk_score"):
        rs = result["risk_score"]
        print(f"风险等级: {rs.level.value}")
        if rs.factors:
            print(f"风险因素: {', '.join(rs.factors)}")

    if result.get("report"):
        report = result["report"]
        print(f"报告摘要: {report.summary}")

    if result.get("block_reason"):
        print(f"阻断原因: {result['block_reason']}")

    if result.get("human_decision"):
        print(f"人工决策: {result['human_decision']}")

    print(f"\n审计日志 ({len(result.get('audit_log', []))} 条):")
    for entry in result.get("audit_log", []):
        print(f"  [{entry.node:12s}] {entry.action:20s} | {entry.decision:15s} | {entry.output_summary}")

    print("=" * 60)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Compliance Review Agent")
    parser.add_argument("--list", action="store_true", help="List available materials")
    parser.add_argument("--material", type=str, help="Material ID to review")
    parser.add_argument("--resume", type=str, help="Resume value for HITL (approved/rejected)")
    parser.add_argument("--thread", type=str, default=None, help="Thread ID for resume")
    args = parser.parse_args()

    if args.list:
        print("Available materials:")
        list_materials()
        return

    if not args.material:
        print("Usage: python main.py --material <ID> | --list")
        return

    material_data = load_material(args.material)
    if material_data is None:
        print(f"Material {args.material} not found.")
        return

    result = run_material(material_data, resume_value=args.resume, thread_id=args.thread)
    print_result(result)


if __name__ == "__main__":
    main()
