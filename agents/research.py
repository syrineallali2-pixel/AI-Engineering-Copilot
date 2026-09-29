from langchain.agents import create_agent

from config import get_llm, last_ai_text
from state import ProjectState
from langchain_tavily import TavilySearch


SYSTEM_PROMPT = """You are an AI research expert.

Your job is to:
1. Search the web via Tavily for relevant information.
2. Search GitHub via the GitHub MCP tools when useful.
3. Synthesize your findings into a comprehensive research summary.

When researching an AI project, investigate:
- Existing approaches and solutions
- Relevant technologies and frameworks
- Relevant papers and datasets
- Similar GitHub projects
- Potential risks and technical challenges

Always provide a final text answer after using tools.
Do not finish with only a tool call.
"""


class ResearchAgent:
    def __init__(self):
        tavily_tool = TavilySearch(max_results=3)

        # IMPORTANT:
        # This now uses your working GitHub MCP connection.
        from config import get_github_tools

        github_tools = get_github_tools()

        all_tools = [tavily_tool] + github_tools

        print(f"🔧 Research agent tools: {len(all_tools)}")
        for tool in all_tools:
            print(f"   - {getattr(tool, 'name', str(tool))}")

        self._agent = create_agent(
            model=get_llm(),
            tools=all_tools,
            system_prompt=SYSTEM_PROMPT,
            name="research_agent",
        )

    async def invoke(self, state: ProjectState) -> ProjectState:

        user_prompt = f"""
Research this AI project.

Project Idea:
{state.project_idea}

Problem:
{state.problem}

Requirements:
{state.requirements}

Provide a research summary covering:

- Existing approaches and solutions
- Relevant technologies
- Relevant datasets
- Similar GitHub projects
- Potential risks and technical challenges

Use the available search tools when appropriate.

IMPORTANT:
After using any tools, return a normal text research summary.
"""

        print("\n📨 Sending research request to Gemini...")

        try:
            result = await self._agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_prompt,
                        }
                    ]
                }
            )

            print("✅ Agent returned a result.")

            messages = result.get("messages", [])

            print(f"📨 Messages returned: {len(messages)}")

            for i, message in enumerate(messages):
                print(
                    f"   [{i}] "
                    f"type={getattr(message, 'type', None)} "
                    f"content_type={type(getattr(message, 'content', None)).__name__}"
                )

            research_findings = last_ai_text(messages)

            if not research_findings:
                research_findings = "Research agent returned no final text."

        except Exception as e:
            import traceback

            print("\n❌ RESEARCH AGENT ERROR:")
            print(str(e))
            traceback.print_exc()

            research_findings = f"Research failed: {str(e)}"

        state.research_findings = research_findings
        state.status = "ml_analysis_phase"

        print(f"\n✅ Research findings:\n{research_findings[:500]}...\n")

        return state


def create_research_agent():
    return ResearchAgent()
