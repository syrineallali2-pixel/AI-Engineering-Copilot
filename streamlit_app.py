"""
AI Engineering Copilot — Streamlit UI with per-agent approval.
"""

from __future__ import annotations

import asyncio

import streamlit as st

from agents.coordinator import (
    create_coordinator,
    run_architecture_step,
    run_ml_step,
    run_research_step,
)
from output import generate_markdown
from state import ProjectState

STEPS = ("research", "ml", "architecture")
STEP_LABELS = {
    "research": "Research",
    "ml": "ML Engineer",
    "architecture": "Architecture",
}


def _init_session() -> None:
    defaults = {
        "project_state": None,
        "current_step": None,
        "approval_status": "pending",
        "refined_prompt": "",
        "show_refine": False,
        "workflow_complete": False,
        "error": "",
        "running": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _load_state() -> ProjectState | None:
    raw = st.session_state.project_state
    if raw is None:
        return None
    return ProjectState.model_validate(raw)


def _save_state(state: ProjectState) -> None:
    st.session_state.project_state = state.model_dump()
    st.session_state.approval_status = state.approval_status
    st.session_state.refined_prompt = state.refined_prompt


def _run_current_step(state: ProjectState, refinement: str = "") -> ProjectState:
    state.refined_prompt = refinement
    step = st.session_state.current_step
    if step == "research":
        return asyncio.run(run_research_step(state))
    if step == "ml":
        return run_ml_step(state)
    if step == "architecture":
        return run_architecture_step(state)
    return state


def _progress_value() -> float:
    step = st.session_state.current_step
    if st.session_state.workflow_complete:
        return 1.0
    if step == "research":
        return 0.33
    if step == "ml":
        return 0.66
    if step == "architecture":
        return 1.0
    return 0.0


def _render_card(title: str, body: str, active: bool) -> None:
    with st.container(border=True):
        heading = f"**{title}**"
        if active and not st.session_state.workflow_complete:
            heading += " · awaiting approval"
        st.markdown(heading)
        if body:
            st.markdown(body)
        else:
            st.caption("Not generated yet.")


st.set_page_config(page_title="AI Engineering Copilot", layout="wide")
_init_session()

st.title("AI Engineering Copilot")
st.caption("Gemini + LangChain agents · Tavily research · approve each step")

with st.sidebar:
    st.header("Project inputs")
    with st.form("project_form", clear_on_submit=False):
        project_idea = st.text_area("Describe your AI project", height=100)
        problem = st.text_area("What's the core problem?", height=80)
        requirements = st.text_area(
            "Any specific requirements or constraints?", height=80
        )
        submitted = st.form_submit_button(
            "Start workflow", type="primary", use_container_width=True
        )

    if submitted:
        if not project_idea.strip() or not problem.strip():
            st.error("Project idea and core problem are required.")
        else:
            state = ProjectState(
                project_idea=project_idea.strip(),
                problem=problem.strip(),
                requirements=requirements.strip(),
                status="initialized",
                approval_status="pending",
            )
            state = create_coordinator().invoke(state)
            st.session_state.current_step = "research"
            st.session_state.workflow_complete = False
            st.session_state.show_refine = False
            st.session_state.error = ""
            with st.spinner("Research agent is running…"):
                try:
                    state = _run_current_step(state)
                    _save_state(state)
                except Exception as exc:
                    st.session_state.error = str(exc)
                    _save_state(state)
            st.rerun()

    if st.session_state.project_state:
        if st.button("Reset session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

state = _load_state()

if st.session_state.error:
    st.error(st.session_state.error)

if state is None:
    st.info("Fill in the sidebar and start the workflow to generate a blueprint.")
else:
    st.progress(
        _progress_value(),
        text=f"Step: {STEP_LABELS.get(st.session_state.current_step, '—')}",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        _render_card(
            "1. Research",
            state.research_findings,
            st.session_state.current_step == "research",
        )
    with col2:
        _render_card(
            "2. ML Approach",
            state.ml_analysis,
            st.session_state.current_step == "ml",
        )
    with col3:
        _render_card(
            "3. Architecture",
            state.architecture,
            st.session_state.current_step == "architecture",
        )

    if (
        not st.session_state.workflow_complete
        and st.session_state.current_step in STEP_LABELS
    ):
        st.subheader("Review this step")
        st.caption(
            f"Current agent: **{STEP_LABELS[st.session_state.current_step]}** · "
            f"approval: `{st.session_state.approval_status}`"
        )

        a, b, c = st.columns(3)
        with a:
            approve = st.button("✅ Approve", type="primary", use_container_width=True)
        with b:
            reject = st.button("❌ Reject", use_container_width=True)
        with c:
            refine = st.button("🔧 Refine", use_container_width=True)

        if st.session_state.show_refine:
            feedback = st.text_area(
                "What should this agent change?",
                value=st.session_state.refined_prompt,
                key="refine_box",
            )
            if st.button("Re-run with feedback", type="primary"):
                st.session_state.approval_status = "pending"
                with st.spinner("Re-running agent with your feedback…"):
                    try:
                        updated = _run_current_step(state, refinement=feedback.strip())
                        _save_state(updated)
                        st.session_state.show_refine = False
                        st.session_state.error = ""
                    except Exception as exc:
                        st.session_state.error = str(exc)
                st.rerun()

        if approve:
            idx = STEPS.index(st.session_state.current_step)
            state.approval_status = "approved"
            if idx == len(STEPS) - 1:
                st.session_state.workflow_complete = True
                _save_state(state)
                st.rerun()
            next_step = STEPS[idx + 1]
            st.session_state.current_step = next_step
            st.session_state.show_refine = False
            label = STEP_LABELS[next_step]
            with st.spinner(f"{label} agent is running…"):
                try:
                    updated = _run_current_step(state)
                    updated.approval_status = "pending"
                    _save_state(updated)
                    st.session_state.error = ""
                except Exception as exc:
                    st.session_state.error = str(exc)
                    _save_state(state)
            st.rerun()

        if reject:
            state.approval_status = "rejected"
            st.session_state.show_refine = False
            with st.spinner("Re-running this agent…"):
                try:
                    updated = _run_current_step(
                        state,
                        refinement=(
                            "The previous answer was rejected. "
                            "Produce a substantially different, higher-quality version."
                        ),
                    )
                    _save_state(updated)
                    st.session_state.error = ""
                except Exception as exc:
                    st.session_state.error = str(exc)
            st.rerun()

        if refine:
            st.session_state.show_refine = True
            st.rerun()

    if state.research_findings and state.ml_analysis and state.architecture:
        markdown = generate_markdown(state)
        with st.expander(
            "Final markdown blueprint", expanded=st.session_state.workflow_complete
        ):
            st.markdown(markdown)
            st.download_button(
                "Download blueprint.md",
                data=markdown.encode("utf-8"),
                file_name="blueprint.md",
                mime="text/markdown",
                use_container_width=True,
            )
