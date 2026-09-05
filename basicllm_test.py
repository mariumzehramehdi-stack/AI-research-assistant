import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)


def summarize_text(text):
    prompt = f"""
    Summarize the following text in 3 concise bullet pointsopjl:

    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


sample_text = """
Artificial intelligence is changing the way software is developed.
Large language models can understand text, generate code, summarize
information, and assist developers with many programming tasks.
"""

print(summarize_text(sample_text))