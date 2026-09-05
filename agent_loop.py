from google import genai
import os
import json
from dotenv import load_dotenv
from search import search_topic
from summarize_sources import summarize_source
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def evaluate_sufficiency(topic: str, summaries: list[dict]) -> dict:
    """
    Ask Gemini whether the gathered sources are sufficient
    to answer the topic well, or whether another search is needed.
    """

    summary_text = "\n".join(
        f"- {s['summary']}" for s in summaries
    )

    prompt = f"""
Topic: "{topic}"

Gathered information so far:
{summary_text}

Is this enough information to write a well-rounded report
on the topic?

Reply in this exact JSON format, nothing else:

{{
    "sufficient": true or false,
    "follow_up_query": "a more specific search query if not sufficient, else empty string"
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    # Remove markdown code fences if Gemini adds them
    cleaned = (
        response.text
        .strip()
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        # If JSON parsing fails, stop safely
        return {
            "sufficient": True,
            "follow_up_query": ""
        }


def research_with_agent_loop(
    topic: str,
    max_iterations: int = 2
) -> list[dict]:
    """
    Searches, evaluates sufficiency, and performs a follow-up
    search if needed.

    max_iterations prevents the loop from running forever
    or making excessive API calls.
    """

    all_summaries = []
    current_query = topic

    for iteration in range(max_iterations):

        print(
            f"Iteration {iteration + 1}: "
            f"searching '{current_query}'"
        )

        # Search the web
        sources = search_topic(
            current_query,
            max_results=3
        )

        # Summarize the new sources
        new_summaries = [
            summarize_source(source)
            for source in sources
        ]

        # Add them to everything gathered so far
        all_summaries.extend(new_summaries)

        # Ask Gemini whether we have enough information
        decision = evaluate_sufficiency(
            topic,
            all_summaries
        )

        print(f"Sufficient: {decision['sufficient']}")

        # Stop if enough information was found
        if (
            decision["sufficient"]
            or not decision.get("follow_up_query")
        ):
            break

        # Otherwise, Gemini's refined query becomes
        # the query for the next iteration
        current_query = decision["follow_up_query"]

    return all_summaries

 

if __name__ == "__main__":
    topic ="What are the emerging risks of AI agents in cybersecurity"  # change this per test run

    start = time.time()
    results = research_with_agent_loop(topic)
    elapsed = time.time() - start

    print(f"\nTotal sources gathered: {len(results)}")
    print(f"⏱ Response time: {elapsed:.2f} seconds")