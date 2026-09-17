 ![AI Research Assistant Demo](screenshots/research-demo.png)

 AI Research Assistant (Sift)

Most "AI research assistant" projects generate a confident-sounding answer whether or not they actually found good evidence for it. This one doesn't — it checks its own sources before writing anything, and it goes back to search again if what it found isn't good enough.

Overview

Sift is an agentic research system that combines live web search with an LLM to automate the research workflow end to end. You give it a query, it retrieves sources through the Tavily Search API, evaluates whether those sources are actually sufficient to answer the question, searches again on its own if they're not, and then uses Google Gemini to synthesize the findings into a structured, citation-grounded report.

Results

I didn't just assume this works — I manually checked it.

What I checked	Result
Reports manually reviewed for citation accuracy	8
Unsupported or miscited claims found	0
Sources manually confirmed as genuinely relevant	16 / 16
Topics where the follow-up search actually triggered	67%
Average end-to-end response time	18–19 seconds

The follow-up search rate matters most here — on two out of three tested topics, the first search round wasn't good enough on its own, and the agent caught that instead of answering anyway.

Features
Web Research — retrieves relevant, up-to-date information from the web using Tavily
Self-Evaluation — checks whether retrieved sources are sufficient before generating an answer, and triggers a targeted follow-up search if they aren't
LLM-Powered Analysis — uses Google Gemini to analyze and synthesize retrieved information
Source-Grounded Responses — constrains generated claims to what was actually retrieved, verified by hand across 8 full reports
Automated Reports — generates structured research reports from collected sources
FastAPI Backend — provides an API layer for running the research pipeline
Web Interface — simple browser-based interface for submitting research queries
Dockerized Deployment — containerized for consistent, reproducible execution
Architecture
User Query
    ↓
FastAPI
    ↓
Agent Loop
    ↓
Tavily Web Search
    ↓
Source Sufficiency Check ──[insufficient]──▶ Follow-up Search
    │
  [sufficient]
    ↓
Source Summarization
    ↓
Google Gemini
    ↓
Research Synthesis
    ↓
Citation-Grounded Report
Tech Stack
Technology	Purpose
Python	Core application and research pipeline
FastAPI	Backend API
Google Gemini	LLM-powered analysis and synthesis
Tavily Search API	Web search and source retrieval
HTML/CSS/JavaScript	Web interface
Docker	Application containerization
Project Structure
AI-research-assistant/
│
├── agent_loop.py
├── basicllm_test.py
├── build_report.py
├── main.py
├── search.py
├── summarize_sources.py
├── index.html
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
Setup
1. Clone the repository
git clone https://github.com/mariumzehramehdi-stack/AI-research-assistant.git
cd AI-research-assistant
2. Create a virtual environment
python -m venv venv
3. Activate the environment

Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Configure environment variables

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key

Never commit API keys or .env files to the repository.

6. Run locally
uvicorn main:app --reload

The application will be available at http://localhost:8000.

Docker
Build the image
docker build -t ai-research-assistant .
Run the container
docker run --env-file .env -p 8000:8000 ai-research-assistant

The application will then be available at http://localhost:8000.

Research Workflow
User submits a research query.
The agent initiates a web search through Tavily.
Relevant sources are collected and processed.
The agent checks whether the sources are actually sufficient — if not, it runs a targeted follow-up search.
Source content is summarized.
Google Gemini analyzes the retrieved information.
The findings are synthesized into a structured, citation-grounded report.
What I'd Improve Next
Swap keyword-based retrieval for a real vector store (Pinecone or pgvector) with proper embeddings — turning this into a full RAG pipeline
Add streaming responses to cut perceived latency below the current 18–19s
Add automated citation-accuracy testing instead of manual spot checks
Add conversation memory across queries
Deploy the containerized app to a cloud platform
Security
API keys are stored in environment variables
.env is excluded from version control
Local cache files are excluded from the Docker build context
Secrets are never hardcoded or committed to the repository
Author

Mariam Zehra — Computer Science Student | AI/ML | Python
 

 
 

   
