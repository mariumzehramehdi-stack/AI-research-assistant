from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from build_report import build_structured_report
from agent_loop import research_with_agent_loop


app = FastAPI(title="AI Research Assistant")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vite dev server default
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic: str
    use_agent_loop: bool = False


@app.post("/research")
async def research(request: ResearchRequest):
    """
    Main endpoint: takes a topic, runs the research pipeline, and returns a
    structured report. use_agent_loop=True enables the Phase 6 follow-up
    search behavior.
    """

    if request.use_agent_loop:
        summaries = research_with_agent_loop(request.topic)

        return {
            "topic": request.topic,
            "sources": summaries
        }

    else:
        result = build_structured_report(request.topic)
        return result


@app.get("/")
async def health_check():
    return {
        "status": "AI Research Assistant backend running"
    }