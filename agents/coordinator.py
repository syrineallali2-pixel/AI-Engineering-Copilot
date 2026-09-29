"""
Coordinator — sequential orchestrator for LangChain agents (no tools).
"""

from state import ProjectState

from .architecture import create_architecture_agent
from .ml_engineer import create_ml_engineer_agent
from .research import create_research_agent


class Coordinator:
    """Lightweight orchestrator: set workflow status, then hand off to agents."""

    def invoke(self, state: ProjectState) -> ProjectState:
        print("Coordinator: Starting workflow")
        state.status = "research_phase"
        state.approval_status = "pending"
        return state


def create_coordinator() -> Coordinator:
    """Return a simple sequential orchestrator (no tools)."""
    return Coordinator()


async def run_research_step(state: ProjectState) -> ProjectState:
    """Run only the research agent."""
    return await create_research_agent().invoke(state)


def run_ml_step(state: ProjectState) -> ProjectState:
    """Run only the ML engineer agent."""
    return create_ml_engineer_agent().invoke(state)


def run_architecture_step(state: ProjectState) -> ProjectState:
    """Run only the architecture agent."""
    return create_architecture_agent().invoke(state)


async def run_copilot_workflow(state: ProjectState) -> ProjectState:
    """Run research → ML engineer → architecture without human-in-the-loop."""
    coordinator = create_coordinator()
    research_agent = create_research_agent()
    ml_agent = create_ml_engineer_agent()
    arch_agent = create_architecture_agent()

    state = coordinator.invoke(state)
    state = await research_agent.invoke(state)
    state = ml_agent.invoke(state)
    state = arch_agent.invoke(state)
    return state
