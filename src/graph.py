"""Graph assembly — LangGraph StateGraph."""

from langgraph.graph import END, START, StateGraph

from src.nodes.analyze import analyze_node
from src.nodes.hitl import hitl_node
from src.nodes.ingest import ingest_node
from src.nodes.report_gen import report_gen_node
from src.nodes.retrieve import retrieve_node
from src.nodes.score import score_node
from src.state import ComplianceState


def build_graph() -> StateGraph:
    """Build the compliance review graph."""
    graph = StateGraph(ComplianceState)

    # Add nodes
    graph.add_node("ingest", ingest_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("score", score_node)
    graph.add_node("hitl", hitl_node)
    graph.add_node("report_gen", report_gen_node)

    # Edges
    graph.add_edge(START, "ingest")
    graph.add_edge("ingest", "retrieve")
    graph.add_edge("retrieve", "analyze")
    graph.add_edge("analyze", "score")
    graph.add_edge("score", "hitl")
    graph.add_edge("hitl", "report_gen")
    graph.add_edge("report_gen", END)

    return graph


def compile_graph(checkpointer=None):
    """Compile the graph, optionally with a checkpointer for HITL."""
    graph = build_graph()
    return graph.compile(checkpointer=checkpointer)
