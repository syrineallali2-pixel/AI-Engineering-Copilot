"""
CLI entry point (optional). Prefer: streamlit run streamlit_app.py
"""

import asyncio

from agents.coordinator import run_copilot_workflow
from output import generate_markdown
from state import ProjectState


def prompt_user() -> ProjectState:
    print("AI Engineering Copilot")
    print("-" * 40)

    project_idea = input("Describe your AI project: ").strip()
    problem = input("What's the core problem? ").strip()
    requirements = input("Any specific requirements or constraints? ").strip()

    return ProjectState(
        project_idea=project_idea,
        problem=problem,
        requirements=requirements,
        status="initialized",
        approval_status="pending",
    )


def main() -> None:
    state = prompt_user()
    print("\nRunning sequential LangChain agents (no approval UI)…\n")
    final_state = asyncio.run(run_copilot_workflow(state))
    markdown = generate_markdown(final_state)
    print(markdown)
    with open("project_blueprint.md", "w", encoding="utf-8") as f:
        f.write(markdown)
    print("\nBlueprint saved to: project_blueprint.md")
    print("For human-in-the-loop review, run: streamlit run streamlit_app.py")


if __name__ == "__main__":
    main()
