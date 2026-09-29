# AI Engineering Copilot

A production-ready multi-agent system that transforms AI project ideas into detailed, actionable engineering blueprints in minutes.

**Input:** A one-liner AI idea
**Output:** Research findings → ML strategy → System architecture → Implementation plan

---

## Features

- **Multi-Agent Architecture** — Coordinator, Research, ML Engineer, and Architecture agents working in harmony
- **GitHub + Web Search** — Research Agent searches GitHub for similar projects and the web for papers and datasets
- **Human-in-the-Loop** — Approve, reject, or refine each agent's output before proceeding
- **Web UI** — Streamlit interface with real-time progress tracking
- **Production Blueprints** — Generates professional markdown engineering documents
- **MCP Integration** — Demonstrates modern AI infrastructure (Model Context Protocol)
- **Persistent Storage** — Save and resume projects
- **Error Handling and Logging** — Production-grade reliability

---

## Architecture

```
User Input (Web UI)
        |
   Coordinator Agent
        |
   Research Agent (Tavily + GitHub MCP)
        |
   Human Approval
        |
   ML Engineer Agent
        |
   Human Approval
        |
   Architecture Agent
        |
   Human Approval
        |
Markdown Blueprint (downloadable)
```

**Tech Stack:**

| Component | Technology |
|---|---|
| LLM | gemini-3.1-flash-lite-preview (`langchain-google-genai`) |
| Agent Framework | LangChain |
| Orchestration | LangChain Agent Executor |
| Web Search | Tavily API |
| Repository Search | GitHub MCP (Model Context Protocol) |
| UI | Streamlit |
| State Management | Pydantic BaseModel |
| Language | Python 3.10+ |

---

## Quick Start

### Prerequisites

- Python 3.10+
- API Keys:
  - `GOOGLE_API_KEY` — Get one free from [AI Studio](https://aistudio.google.com/apikey)
  - `TAVILY_API_KEY` — Get one free from [Tavily](https://tavily.com)
  - `GITHUB_TOKEN` — Generate one from [GitHub Settings](https://github.com/settings/tokens)

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-engineering-copilot.git
cd ai-engineering-copilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env
echo "TAVILY_API_KEY=your_key_here" >> .env
echo "GITHUB_TOKEN=your_token_here" >> .env
```

### Run

```bash
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How It Works

1. Enter your AI project idea (e.g., "Build a fraud detection system")

2. **Research Agent** searches GitHub and the web for:
   - Similar projects
   - Relevant papers and datasets
   - Existing solutions

3. You approve, reject, or refine the research findings

4. **ML Engineer Agent** designs:
   - ML task definition
   - Model architectures
   - Data preprocessing strategy
   - Evaluation metrics

5. You approve or refine the ML approach

6. **Architecture Agent** designs:
   - Backend services (FastAPI)
   - Frontend requirements (React/Streamlit)
   - Database schema
   - Deployment strategy
   - Scalability considerations

7. You approve the architecture

8. Download your blueprint as a professional markdown document

---

## Example

**Input:**

```
Project: Stroke risk prediction system
Problem: Predict stroke risk from patient data
Requirements: Real-time predictions, interpretability
```

**Output (in ~10 seconds):**

```markdown
# AI Project Blueprint

## Research Findings
- Found 12 stroke prediction papers
- Top GitHub projects: stroke-prediction-ml, clinical-risk-models
- Recommended datasets: Kaggle Stroke Dataset, UCI ML datasets

## ML Approach
- Task: Binary classification
- Models: XGBoost, Neural Networks, SHAP interpretability
- Metrics: AUC-ROC, Precision, Recall
- Data: 5,000 patient records needed

## System Architecture
- Backend: FastAPI + Python
- ML Service: scikit-learn + XGBoost
- Database: PostgreSQL
- Frontend: Streamlit or React
- Deployment: Docker + AWS/GCP
```

---

## Project Structure

```
ai-engineering-copilot/
├── streamlit_app.py          # Web UI (main entry point)
├── config.py                 # Gemini + Tavily + GitHub MCP setup
├── state.py                  # ProjectState schema
├── output.py                 # Markdown blueprint generation
├── agents/
│   ├── research.py           # Research Agent (GitHub + Tavily)
│   ├── ml_engineer.py        # ML Engineer Agent
│   ├── architecture.py       # Architecture Agent
│   └── coordinator.py        # Coordinator Agent
├── tools/
│   └── tavily_search.py      # Web search wrapper
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Key Technologies Demonstrated

- **Multi-Agent Systems** — LangChain agents with sequential orchestration
- **State Management** — Pydantic BaseModel for workflow state
- **Tool Integration** — Tavily API and GitHub MCP for external data
- **Human-in-the-Loop** — Approval gates between agent steps
- **LLM Integration** — Google Gemini via `langchain-google-genai`
- **MCP (Model Context Protocol)** — GitHub MCP for repository search
- **Error Handling** — Try-catch blocks with graceful degradation
- **Web UI** — Streamlit for interactive interface

---

## Production Features

- **Logging and Monitoring** — Request tracking, error logs
- **Error Handling** — Graceful failures, retry logic
- **Input Validation** — Pydantic schemas
- **Extensibility** — Easy to add new agents or tools
- **Code Quality** — Clean, modular, documented

---



## Future Enhancements

- **Dynamic Agent Loading** — Create agents based on project type
- **Long Conversation Management** — Refine blueprints iteratively
- **Database Persistence** — Save projects to PostgreSQL
- **Monitoring Dashboard** — Prometheus + Grafana
- **CI/CD Pipeline** — GitHub Actions for testing
- **API Endpoint** — FastAPI wrapper for programmatic access

---

## License

MIT License — feel free to use and modify for personal and educational purposes.

---

## About

Built as a portfolio project to demonstrate:

- Multi-agent system architecture
- Production-ready AI applications
- Modern AI infrastructure (MCP, LLMs, APIs)



---

## Contact

- **GitHub:** [syrine allali](https://github.com/syrineallali2-pixel)
- **LinkedIn:** [ALLALI SYRINE](https://www.linkedin.com/in/allali-syrine-02311a369/)

---

## Show Some Love

If this project helped you, please star it on GitHub!

```bash
git clone https://github.com/syrineallali2-pixel/AI-Engineering-Copilot.git
```

Made with care for AI engineers everywhere :)
