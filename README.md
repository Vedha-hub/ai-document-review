# AI Document Review System
### Infotact Solutions — Internship Project 2

An Agentic AI pipeline that automatically converts rough ideas into 
complete, professional Product Requirements Documents (PRDs) using 
a multi-agent LangGraph workflow powered by Google Gemini API.

---

## Overview

The system uses two AI agents connected through a LangGraph state 
machine that automatically loops and self-corrects until the document 
meets quality standards (score >= 75/100).

## Architecture
[User Input] → [Writer Agent] → [Critic Agent] → (score<75? loop back) → [Human Approval] → [Final PRD]

## How It Works

1. User submits rough notes via API
2. Writer Agent generates complete 10-section PRD using Gemini API
3. Critic Agent reviews and scores the PRD using Function Calling
4. If score is below 75 → automatically loops back to Writer
5. If score is above 75 → sent for Human approval
6. Human approves or rejects via API endpoints
7. Final approved PRD is returned

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Core language |
| LangGraph | Multi-agent workflow state machine |
| Google Gemini API | Language model for Writer and Critic |
| FastAPI | REST API backend |
| Pydantic | Request/response validation |
| pytest | Testing framework |
| python-dotenv | Environment variable management |
| GitHub | Version control with feature branches |

## Project Structure
ai-document-review/
├── agents/
│   ├── writer_agent.py      # Writer Agent — generates PRDs
│   └── critic_agent.py      # Critic Agent — reviews with Function Calling
├── graph/
│   └── workflow.py          # LangGraph state machine
├── api/
│   ├── main.py              # FastAPI application
│   ├── routes.py            # API endpoints
│   └── schemas.py           # Pydantic models
├── prompts/
│   ├── writer_system_prompt.txt
│   └── critic_system_prompt.txt
├── notebooks/
│   └── week1_prompt_experiments.ipynb
├── tests/
│   ├── test_agents.py
│   └── test_api.py
├── .env                     # API keys — NEVER commit!
├── .gitignore
├── README.md
└── requirements.txt

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /api/v1/generate-document | Generate PRD from rough notes |
| POST | /api/v1/approve-document/{doc_id} | Approve a generated document |
| POST | /api/v1/reject-document/{doc_id} | Reject a generated document |
| GET | /api/v1/pending-approvals | List all pending documents |

## Setup Instructions

1. Clone the repository:
git clone https://github.com/Vedha-hub/ai-document-review
cd ai-document-review

2. Create virtual environment:
python -m venv venv
venv\Scripts\activate

3. Install dependencies:
python -m pip install -r requirements.txt

4. Create .env file:
GEMINI_API_KEY=your_gemini_api_key_here

5. Run the server:
uvicorn api.main:app --reload --port 8000

6. Open Swagger UI:
http://localhost:8000/docs

## Testing

Run all tests:
python -m pytest tests/ -v

Run workflow directly:
python graph/workflow.py

## Results

- Writer Agent generates complete 10-section PRDs
- Critic Agent scores PRDs using Gemini Function Calling
- Achieved scores of 95-100 out of 100 consistently
- All PRDs approved in single iteration
- 2/2 pytest tests passing

## Team

| Member | Role | Responsibilities |
|--------|------|-----------------|
| Vedha | Writer Agent + LangGraph | writer_agent.py, workflow.py, FastAPI backend, DocumentState, conditional edges |
| Sirisha | Critic Agent + Testing | critic_agent.py, Function Calling integration, Pydantic schemas, pytest tests |

## Weekly Progress

| Week | Focus | Status |
|------|-------|--------|
| Week 1 | Prompt Engineering + Agent files | ✅ Complete |
| Week 2 | LangGraph Multi-Agent Workflow | ✅ Complete |
| Week 3 | Function Calling + Pydantic + pytest | ✅ Complete |
| Week 4 | FastAPI Backend + Human in the Loop | ✅ Complete |

---

*Built during Infotact Solutions 2-Month Technical Internship Program*
*Stack: Python · LangGraph · Google Gemini · FastAPI · Pydantic*