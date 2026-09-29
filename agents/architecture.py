"""
Architecture agent — LangChain agent (LLM only, no tools).
"""

from langchain.agents import create_agent

from config import get_llm, last_ai_text
from state import ProjectState

SYSTEM_PROMPT = """You are a software architect specializing in ML systems. Given ML analysis, design:
1. Backend services and APIs
2. Frontend requirements
3. Database and data pipeline design
4. ML service deployment
5. Integration points
6. Scalability and performance considerations

Format: clear architectural components and their interactions."""


class ArchitectureAgent:
    """LangChain architecture agent that updates ProjectState.architecture."""

    def __init__(self) -> None:
        self._agent = create_agent(
            model=get_llm(),
            tools=[],
            system_prompt=SYSTEM_PROMPT,
            name="architecture_agent",
        )

    def invoke(self, state: ProjectState) -> ProjectState:
        user_prompt = f"""Project Idea: {state.project_idea}

ML Approach:
{state.ml_analysis}

Design the complete system architecture:
- What backend services are needed?
- What APIs should the ML model expose?
- How should data flow through the system?
- What database/storage would you use?
- How would you deploy and scale the ML model?
- What frontend or client would use this?
- Any third-party integrations needed?"""

        if state.refined_prompt:
            user_prompt += (
                f"\n\nThe previous architecture was not accepted. "
                f"Revise with this feedback:\n{state.refined_prompt}"
            )

        result = self._agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
        state.architecture = last_ai_text(result.get("messages", []))
        state.status = "blueprint_complete"
        state.approval_status = "pending"
        state.refined_prompt = ""
        return state


def create_architecture_agent() -> ArchitectureAgent:
    """Return a LangChain architecture agent (no tools)."""
    return ArchitectureAgent()
