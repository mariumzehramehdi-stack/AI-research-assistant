 
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_topic(topic: str, max_results: int = 5) -> list[dict]:
    """
    Searches the web for a topic and returns a list of sources.

    Each source:
    {"title": str, "url": str, "content": str}

    'content' is a short snippet Tavily extracts.
    Phase 4 will have the LLM properly summarize it.
    """

    response = tavily_client.search(
        query=topic,
        max_results=max_results,
        search_depth="advanced"
    )

    sources = []

    for result in response["results"]:
        sources.append({
            "title": result["title"],
            "url": result["url"],
            "content": result["content"],
        })

    return sources


if __name__ == "__main__":
    results = search_topic("impact of AI on software engineering jobs")

    for i, source in enumerate(results):
        print(f"\n--- Source {i + 1}: {source['title']} ---")
        print(f"URL: {source['url']}")
        print(f"Snippet: {source['content'][:200]}")
 
