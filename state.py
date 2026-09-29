"""
Shared workflow state for the AI Engineering Copilot.

Agents read and write this Pydantic model as they move through
research, ML analysis, and architecture phases.
"""

from typing import Literal

from pydantic import BaseModel, Field

ApprovalStatus = Literal["pending", "approved", "rejected"]


class ProjectState(BaseModel):
    """Canonical state passed between LangChain agents."""

    # User input
    project_idea: str = Field(default="", description="High-level description of the AI project.")
    problem: str = Field(default="", description="Core problem the project aims to solve.")
    requirements: str = Field(default="", description="Constraints, non-goals, or specific requirements.")

    # Agent outputs
    research_findings: str = Field(default="", description="Summary of web research / landscape scan.")
    ml_analysis: str = Field(default="", description="Recommended ML approach and modeling notes.")
    architecture: str = Field(default="", description="System design / architecture outline.")

    # Workflow metadata
    status: str = Field(default="", description="Current phase of the copilot workflow.")
    approval_status: ApprovalStatus = Field(
        default="pending",
        description="Human-in-the-loop status for the current agent step.",
    )
    refined_prompt: str = Field(
        default="",
        description="Optional user feedback used when re-running an agent.",
    )
