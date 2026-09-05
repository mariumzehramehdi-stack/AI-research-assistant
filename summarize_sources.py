 
from google import genai
import os
import time
import json
from dotenv import load_dotenv
from search import search_topic

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CACHE_FILE = "cache.json"


def load_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def summarize_source(source: dict) -> dict:
    """
    Takes one search result and asks the LLM to extract the key points
    relevant to research in 1-2 sentences, staying strictly grounded
    in the provided content.

    Results are cached locally to avoid repeated Gemini API calls.
    """

    cache = load_cache()

    # Use the source URL as a unique cache key
    cache_key = source["url"]

    # Return cached result if we already summarized this source
    if cache_key in cache:
        print("Using cached summary...")
        return cache[cache_key]

    prompt = f"""
    Summarize the key point of the following source in 1-2 sentences.
    Only use information from the text below.
    Do not add outside knowledge.

    Title: {source['title']}

    Content: {source['content']}

    Summary:
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            result = {
                "title": source["title"],
                "url": source["url"],
                "summary": response.text.strip()
            }

            # Save the successful result
            cache[cache_key] = result
            save_cache(cache)

            return result

        except Exception as e:
            if attempt < 2:
                print(
                    "Gemini request failed. Retrying in 5 seconds..."
                )
                time.sleep(5)
            else:
                raise e


def summarize_all_sources(
    topic: str,
    max_results: int = 2
) -> list[dict]:

    sources = search_topic(
        topic,
        max_results=max_results
    )

    summarized = [
        summarize_source(s)
        for s in sources
    ]

    return summarized


if __name__ == "__main__":

    results = summarize_all_sources(
        "impact of AI on software engineering jobs"
    )

    for i, r in enumerate(results):
        print(f"\n[{i + 1}] {r['title']}")
        print(f"Summary: {r['summary']}")
        print(f"Source: {r['url']}")
