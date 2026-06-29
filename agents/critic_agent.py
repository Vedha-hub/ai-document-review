from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()

def load_prompt(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
    with open(path, encoding='utf-8') as f:
        return f.read()

def run_critic_agent(prd_text: str) -> dict:
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    
    prompt = load_prompt('critic_system_prompt.txt')
    
    response = client.models.generate_content(
        model='gemini-flash-lite-latest',
        contents=f"{prompt}\n\nReview this PRD:\n{prd_text}"
    )
    
    raw = response.text.strip()
    
    if raw.startswith('```'):
        raw = raw.split('```')[1]
        if raw.startswith('json'):
            raw = raw[4:]
    
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "status": "needs_revision",
            "score": 0,
            "missing_sections": ["Unable to parse critic response"],
            "feedback": ["Critic returned invalid JSON"],
            "approval_message": "Error in critic response"
        }


if __name__ == '__main__':
    sample = "This is a sample PRD about a food delivery app."
    result = run_critic_agent(sample)
    print(json.dumps(result, indent=2))