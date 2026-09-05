 
from google import genai
import os
from dotenv import load_dotenv
from summarize_sources import summarize_all_sources
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def build_structured_report(topic: str, max_results: int = 2) -> dict:
    """
    Full pipeline: search -> summarize each source -> combine into one
    structured report with key takeaways, each citing its source number.
    """

    summarized_sources = summarize_all_sources(
        topic,
        max_results=max_results
    )

    # Build a numbered reference list the LLM can cite by number
    numbered_sources = "\n".join(
        f"[{i + 1}] {s['title']}: {s['summary']}"
        for i, s in enumerate(summarized_sources)
    )

    prompt = f"""
    You are a research assistant. Based ONLY on the numbered
    source summaries below, write a structured research report
    on the topic:

    "{topic}"

    Sources:
    {numbered_sources}

    Write the report with this structure:

    1. A 2-3 sentence overview of the topic

    2. 4-6 key takeaways as bullet points, each ending with a
       citation like [1] or [2] referring to which source it came from

    3. Note any disagreement or conflicting information between
       sources, if present

    Only use information from the sources above.
    If sources don't cover something, don't invent it.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return {
        "topic": topic,
        "report": response.text,
        "sources": summarized_sources
    }


if __name__ == "__main__":
    topic = "The Impact of AI on Engineering Jobs"  # change this per test run

    start = time.time()
    result = build_structured_report(topic)
    elapsed = time.time() - start

    print(f"=== Report: {result['topic']} ===\n")
    print(result["report"])
    print("\n=== Sources ===")
    for i, s in enumerate(result["sources"]):
        print(f"[{i+1}] {s['title']} — {s['url']}")
    print(f"\n⏱ Response time: {elapsed:.2f} seconds")