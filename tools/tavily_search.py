"""
Thin wrapper around Tavily web search, plus a LangChain tool.

Returns a short string summary of results. On any failure, returns
"No results found" so agent nodes can keep running.
"""

from langchain_core.tools import StructuredTool
from tavily import TavilyClient

from config import TAVILY_API_KEY


def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web with Tavily and return a concatenated summary string.

    Args:
        query: Search query.
        max_results: Maximum number of results to include.

    Returns:
        A human-readable summary of titles/snippets, or "No results found".
    """
    if not query or not query.strip():
        return "No results found"

    if not TAVILY_API_KEY or TAVILY_API_KEY.startswith("tvly_your_key"):
        return "No results found"

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY.strip())
        response = client.search(query=query.strip(), max_results=max_results)
        results = response.get("results") or []
        if not results:
            return "No results found"

        lines = []
        for item in results:
            title = (item.get("title") or "").strip()
            content = (item.get("content") or item.get("snippet") or "").strip()
            url = (item.get("url") or "").strip()
            piece = " — ".join(part for part in (title, content) if part)
            if url:
                piece = f"{piece} ({url})" if piece else url
            if piece:
                lines.append(f"- {piece}")

        return "\n".join(lines) if lines else "No results found"
    except Exception:
        return "No results found"


def tavily_search_tool() -> StructuredTool:
    """LangChain tool the research agent can call."""
    return StructuredTool.from_function(
        name="tavily_search",
        description=(
            "Search the public web for current information about technologies, "
            "datasets, products, papers, and best practices. Pass a focused query."
        ),
        func=search_web,
    )
