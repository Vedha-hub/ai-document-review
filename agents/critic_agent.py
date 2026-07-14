# Week 4 - Day 16: Verified FastAPI server runs successfully
# critic_agent with Function Calling integrated into FastAPI backend
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

load_dotenv()

def load_prompt(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
    with open(path, encoding='utf-8') as f:
        return f.read()

# Define Function Calling schema
review_function = types.FunctionDeclaration(
    name='submit_prd_review',
    description='Submit a structured review of a PRD document',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'status': types.Schema(
                type=types.Type.STRING,
                description='approved or needs_revision'
            ),
            'score': types.Schema(
                type=types.Type.INTEGER,
                description='Score between 0 and 100'
            ),
            'missing_sections': types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description='List of missing section names'
            ),
            'feedback': types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description='List of specific issues found'
            ),
            'approval_message': types.Schema(
                type=types.Type.STRING,
                description='Brief summary of the review decision'
            )
        },
        required=['status', 'score', 'missing_sections', 
                  'feedback', 'approval_message']
    )
)

def run_critic_agent(prd_text: str) -> dict:
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    
    prompt = load_prompt('critic_system_prompt.txt')
    
    tool = types.Tool(function_declarations=[review_function])
    
    response = client.models.generate_content(
        model='gemini-flash-lite-latest',
        contents=f"{prompt}\n\nReview this PRD:\n{prd_text}",
        config=types.GenerateContentConfig(
            tools=[tool],
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(
                    mode='ANY',
                    allowed_function_names=['submit_prd_review']
                )
            )
        )
    )
    
    # Extract function call result directly
    for part in response.candidates[0].content.parts:
        if part.function_call:
            # Returns clean dict — no JSON parsing needed!
            return dict(part.function_call.args)
    
    # Fallback if function call not found
    return {
        "status": "needs_revision",
        "score": 0,
        "missing_sections": ["Unable to get structured response"],
        "feedback": ["Function calling failed"],
        "approval_message": "Error in critic response"
    }


if __name__ == '__main__':
    sample = "This is a sample PRD about a food delivery app for students."
    result = run_critic_agent(sample)
    print(json.dumps(result, indent=2))