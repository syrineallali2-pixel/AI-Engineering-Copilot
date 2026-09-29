"""
Turn a completed ProjectState into a markdown blueprint.
"""

from state import ProjectState


def generate_markdown(state: ProjectState) -> str:
    """Render the final project blueprint from workflow state."""
    overview = state.project_idea or "_Not provided._"
    problem = state.problem or "_Not provided._"
    requirements = state.requirements or "_Not provided._"
    research = state.research_findings or "_Not generated yet._"
    ml_approach = state.ml_analysis or "_Not generated yet._"
    architecture = state.architecture or "_Not generated yet._"

    # Implementation / risks are not dedicated state fields yet — stub from existing values.
    implementation_plan = (
        f"1. Confirm problem framing and requirements.\n"
        f"2. Validate research findings and data availability.\n"
        f"3. Implement the outlined ML approach.\n"
        f"4. Build the system architecture and iterate.\n\n"
        f"_Status: {state.status or 'unknown'}_"
    )
    risks = (
        "Assumes API keys, data access, and evaluation labels will be available. "
        "Research and design sections are stubs until LLM prompts are added; "
        "treat architecture and ML notes as a starting point, not a spec."
    )

    return f"""# AI Project Blueprint

## 1. Project Overview
{overview}

## 2. Problem Definition
{problem}

## 3. Requirements
{requirements}

## 4. Research Findings
{research}

## 5. ML Approach
{ml_approach}

## 6. System Architecture
{architecture}

## 7. Implementation Plan
{implementation_plan}

## 8. Risks & Assumptions
{risks}
"""
