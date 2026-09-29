"""
Application configuration.

Loads API keys from `.env` and builds the Gemini chat model used by agents.
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp.shared.exceptions import McpError
from mcp.types import CallToolResult, TextContent


load_dotenv()

GITHUB_PAT = os.getenv("GITHUB_PAT")


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

MODEL_NAME = "gemini-3.1-flash-lite-preview"
TEMPERATURE = 0.7
MAX_TOKENS = 2000


def get_llm() -> ChatGoogleGenerativeAI:
    """Return a configured Gemini chat model."""
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY or None,
        temperature=TEMPERATURE,
        max_output_tokens=MAX_TOKENS,
    )


def message_text(content: object) -> str:
    """Normalize LangChain / Gemini message content to a plain string."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content") or ""
                if text:
                    parts.append(str(text))
            elif hasattr(item, "text"):
                parts.append(str(item.text))
        return "\n".join(parts).strip()
    return str(content).strip()


def last_ai_text(messages: list[BaseMessage] | list[object]) -> str:
    """Extract the last AI message text from an agent result message list."""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) or getattr(msg, "type", None) == "ai":
            return message_text(getattr(msg, "content", msg))
        if isinstance(msg, dict) and msg.get("role") in {"ai", "assistant"}:
            return message_text(msg.get("content", ""))
    if not messages:
        return ""
    last = messages[-1]
    return message_text(getattr(last, "content", last))


# github_mcp adaptation


async def setup_github_mcp():
    """Setup GitHub MCP server for tool use."""

    client = MultiServerMCPClient(
        {
            "github": {
                "transport": "streamable_http",
                "url": "https://api.githubcopilot.com/mcp/",
                "headers": {
                    "Authorization": f"Bearer {GITHUB_PAT}",
                },
            }
        }
    )

    return client


# Create a sync wrapper for tools
def get_github_tools():
    """Get GitHub MCP tools synchronously."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        mcp_client = loop.run_until_complete(setup_github_mcp())
        tools = loop.run_until_complete(mcp_client.get_tools())
        return tools
    except Exception as e:
        import traceback

        print("⚠️ GitHub MCP setup failed:")
        print(f"{type(e).__name__}: {e}")
        traceback.print_exc()

        if hasattr(e, "exceptions"):
            print("\nUnderlying exceptions:")
            for sub_error in e.exceptions:
                print(f"  - {type(sub_error).__name__}: {sub_error}")
                traceback.print_exception(
                    type(sub_error),
                    sub_error,
                    sub_error.__traceback__,
                )

        return []
