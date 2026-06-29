from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

def load_prompt(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
    with open(path, encoding='utf-8') as f:
        return f.read()

def run_writer_agent(rough_input: str) -> str:
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    
    prompt = load_prompt('writer_system_prompt.txt')
    
    response = client.models.generate_content(
        model='gemini-flash-lite-latest',
        contents=f"""{prompt}

Generate a complete PRD with ALL 10 sections for this idea: {rough_input}

YOU MUST WRITE ALL 10 SECTIONS COMPLETELY. DO NOT STOP EARLY.

### 1. Executive Summary
Write at least 150 words here.

### 2. Problem Statement
Write at least 150 words here.

### 3. User Personas
Write at least 2 complete personas with name, age, occupation, goals, frustrations.

### 4. User Stories
Write exactly 5 user stories in format: As a [user] I want [goal] so that [benefit]

### 5. Functional Requirements
Write at least 8 specific functional requirements numbered FR-1 through FR-8.

### 6. Non-Functional Requirements
Write performance, security, scalability, and availability requirements.

### 7. Success Metrics / KPIs
Write at least 4 KPIs with specific measurable numbers.

### 8. Edge Cases and Risk Analysis
Write at least 4 risks each with description and mitigation strategy.

### 9. Technical Specifications
Write tech stack, architecture, APIs, and database requirements.

### 10. Timeline and Milestones
Write at least 4 milestones with dates and deliverables.

NOW WRITE THE COMPLETE PRD STARTING FROM SECTION 1:""",
        config={'max_output_tokens': 8192}
    )
    
    return response.text


if __name__ == '__main__':
    result = run_writer_agent('Build a food delivery app for students.')
    print(result)
    print("\nTotal length:", len(result))