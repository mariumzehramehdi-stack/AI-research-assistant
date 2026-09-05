# AI Research Assistant

An agentic AI research assistant that searches the web, retrieves relevant sources, summarizes findings, and generates citation-grounded research reports.

## Overview

**AI Research Assistant** automates the research workflow by combining web search, source processing, and large language models.

The system retrieves live information from the web using **Tavily Search API**, processes the retrieved sources, and uses **Google Gemini** to generate structured research findings and reports grounded in the collected sources.

## Features

* Web Research — Retrieves relevant and up-to-date sources using Tavily.
* LLM-Powered Analysis — Uses Google Gemini to analyze and synthesize information.
* Source-Grounded Responses — Connects generated findings to retrieved sources.
* Automated Reports — Generates structured research reports from collected information.
* Agentic Workflow — Coordinates search, analysis, summarization, and report generation.
* FastAPI Backend — Provides an API for running the research workflow.
* Web Interface — Simple frontend for submitting research queries.
* Docker Support — Containerized setup for consistent deployment.

## Architecture

```text
User Query
    |
    v
FastAPI Application
    |
    v
Agent Loop
    |
    +----> Tavily Web Search
    |          |
    |          v
    |     Relevant Sources
    |
    v
Source Summarization
    |
    v
Google Gemini
    |
    v
Research Synthesis
    |
    v
Citation-Grounded Report
```

## Tech Stack

| Technology          | Purpose                            |
| ------------------- | ---------------------------------- |
| Python              | Core application                   |
| FastAPI             | Backend API                        |
| Google Gemini       | LLM-powered research and synthesis |
| Tavily Search API   | Web search and source retrieval    |
| Docker              | Containerization                   |
| HTML/CSS/JavaScript | Frontend                           |

## Project Structure

```text
AI-research-assistant/
|
├── agent_loop.py
├── basicllm_test.py
├── build_report.py
├── main.py
├── search.py
├── summarize_sources.py
├── index (1).html
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mariumzehramehdi-stack/AI-research-assistant.git
cd AI-research-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**Never commit your `.env` file or expose API keys publicly.**

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available locally through the FastAPI server.

## Research Workflow

1. User submits a research question.
2. The agent determines the required research steps.
3. Tavily searches the web for relevant sources.
4. Retrieved sources are processed and summarized.
5. Gemini synthesizes the information.
6. Findings are grounded in the retrieved sources.
7. A structured research report is generated.

## Use Cases

* Academic research
* Technology research
* Market research
* Topic exploration
* Source comparison
* Rapid information gathering

## Security

API credentials are stored locally using environment variables and are excluded from Git using `.gitignore`.

## Future Improvements

* Add multi-agent research planning
* Improve source ranking and relevance
* Add persistent research history
* Add streaming responses
* Deploy the application publicly
* Add automated evaluation of research quality

## Author

**Mariam Zehra **

Computer Science Student | AI/ML | Python
