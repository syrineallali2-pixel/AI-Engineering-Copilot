"""
Deprecated LangGraph entry. Orchestration now lives in agents/coordinator.py.
"""

from agents.coordinator import run_copilot_workflow


def build_graph():
    """Kept for import compatibility; returns the sequential workflow callable."""
    return run_copilot_workflow
