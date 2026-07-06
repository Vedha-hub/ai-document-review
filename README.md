# AI Document Review System — Infotact Internship Project 2

## Overview
Agentic AI system that converts rough notes into approved PRDs using 
a multi-agent LangGraph pipeline.

## Architecture
[User Input] → [Writer Agent] → [Critic Agent] → (score<75? loop) → [Approved PRD]

## Tech Stack
Python 3.11 | LangGraph | Google Gemini API | FastAPI | Pydantic

## What Works
- Writer Agent generates complete 10-section PRDs
- Critic Agent reviews and scores PRDs (achieved 95/100)
- LangGraph state machine with automatic revision loop
- Tested with multiple inputs successfully

## Setup
1. git clone https://github.com/Vedha-hub/ai-document-review
2. python -m venv venv && venv\Scripts\activate
3. pip install -r requirements.txt
4. Create .env with GEMINI_API_KEY=...
5. python graph/workflow.py

## Team
Vedha — Writer Agent, LangGraph workflow, DocumentState
Sirisha — Critic Agent, JSON parsing, prompt engineering
