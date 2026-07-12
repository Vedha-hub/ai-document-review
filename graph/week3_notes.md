# Week 3 — Structured Output via Function Calling

## What is Function Calling?
Instead of telling the model "return JSON", we define a function 
schema. The model MUST call the function with valid structured data.
This guarantees perfectly structured output every time.

## Why is this better than JSON prompting?
- No more json.loads() failures
- Model is forced to follow the exact schema
- No markdown code blocks to strip
- Data comes back as clean Python dict automatically

## How it works in Gemini:
1. Define a function schema with name, description, parameters
2. Pass it to generate_content() as tools
3. Response contains function_call with args dict
4. Extract args directly — no parsing needed