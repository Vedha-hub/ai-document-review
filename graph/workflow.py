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
def should_revise(state: DocumentState) -> str:
    fb = state.get('critic_feedback', {})
    score = fb.get('score', 0)
    iters = state.get('iteration_count', 0)
    if fb.get('status') == 'approved' and score >= 75:
        return 'approved'
    elif iters >= MAX_ITERATIONS:
        return 'approved'
    return 'revise'


def build_graph():
    from langgraph.graph import StateGraph, END
    
    wf = StateGraph(DocumentState)
    
    wf.add_node('writer', writer_node)
    wf.add_node('critic', critic_node)
    wf.add_node('finalize', finalize_node)
    
    wf.set_entry_point('writer')
    wf.add_edge('writer', 'critic')
    wf.add_edge('finalize', END)
    wf.add_conditional_edges('critic', should_revise, {
        'approved': 'finalize',
        'revise': 'writer'
    })
    
    return wf.compile()


if __name__ == '__main__':
    print("Building graph...")
    graph = build_graph()
    
    print("Running workflow...")
    result = graph.invoke({
        'raw_input': 'Build a food delivery app for students.',
        'current_draft': '',
        'critic_feedback': {},
        'iteration_count': 0,
        'status': 'drafting',
        'final_document': None
    })
    
    print("\n=== WORKFLOW COMPLETE ===")
    print(f"Total iterations: {result['iteration_count']}")
    print(f"Final score: {result['critic_feedback'].get('score')}")
    print(f"Status: {result['status']}")
    print("\n=== FINAL DOCUMENT ===")
    print(result['final_document'])