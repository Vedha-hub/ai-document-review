from typing import TypedDict, Optional
from agents.writer_agent import run_writer_agent
from agents.critic_agent import run_critic_agent

MAX_ITERATIONS = 3

class DocumentState(TypedDict):
    raw_input: str
    current_draft: str
    critic_feedback: dict
    iteration_count: int
    status: str
    final_document: Optional[str]


def writer_node(state: DocumentState) -> DocumentState:
    if state['iteration_count'] == 0:
        prompt = state['raw_input']
    else:
        fb = state['critic_feedback']
        issues = '\n'.join(fb.get('feedback', []))
        missing = ', '.join(fb.get('missing_sections', []))
        prompt = f"""Original idea: {state['raw_input']}
        
Previous draft was rejected. Fix these issues:
Missing sections: {missing}
Feedback: {issues}

Generate a complete improved PRD with ALL 10 sections."""

    draft = run_writer_agent(prompt)
    
    return {
        **state,
        'current_draft': draft,
        'iteration_count': state['iteration_count'] + 1,
        'status': 'reviewing'
    }


def critic_node(state: DocumentState) -> DocumentState:
    feedback = run_critic_agent(state['current_draft'])
    return {
        **state,
        'critic_feedback': feedback,
        'status': feedback.get('status', 'needs_revision')
    }


def finalize_node(state: DocumentState) -> DocumentState:
    return {
        **state,
        'final_document': state['current_draft'],
        'status': 'approved'
    }