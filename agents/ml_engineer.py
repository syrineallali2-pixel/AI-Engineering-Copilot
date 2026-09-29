"""
ML engineer agent — LangChain agent (LLM only, no tools).
"""

from langchain.agents import create_agent

from config import get_llm, last_ai_text
from state import ProjectState

SYSTEM_PROMPT = """You are an ML architect. Given a project idea and research findings, your job is to:
1. Define the ML task (classification, regression, generation, etc.)
2. Recommend model architectures and algorithms
3. Suggest data preprocessing and feature engineering
4. Define metrics and evaluation strategy
5. Highlight data challenges

Format: structured sections with concrete recommendations."""


class MLEngineerAgent:
    """LangChain ML engineer agent that updates ProjectState.ml_analysis."""

    def __init__(self) -> None:
        self._agent = create_agent(
            model=get_llm(),
            tools=[],
            system_prompt=SYSTEM_PROMPT,
            name="ml_engineer_agent",
        )

    def invoke(self, state: ProjectState) -> ProjectState:
        user_prompt = f"""Project Idea: {state.project_idea}
Problem: {state.problem}

Research Findings:
{state.research_findings}

Design the ML approach:
- What is the ML task? (classification, regression, NLP, computer vision, etc.)
- What models or architectures would work?
- How would you collect and preprocess data?
- What metrics would you use to evaluate success?
- What are the key challenges?"""

        if state.refined_prompt:
            user_prompt += (
                f"\n\nThe previous ML analysis was not accepted. "
                f"Revise with this feedback:\n{state.refined_prompt}"
            )

        result = self._agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
        state.ml_analysis = last_ai_text(result.get("messages", []))
        state.status = "architecture_phase"
        state.approval_status = "pending"
        state.refined_prompt = ""
        return state


def create_ml_engineer_agent() -> MLEngineerAgent:
    """Return a LangChain ML engineer agent (no tools)."""
    return MLEngineerAgent()
