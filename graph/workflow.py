import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    if state["iteration_count"] == 0:
        prompt = state["raw_input"]
    else:
        fb = state["critic_feedback"]
        issues = "\n".join(fb.get("feedback", []))
        missing = ", ".join(fb.get("missing_sections", []))

        prompt = f"""Original idea: {state['raw_input']}

Previous draft was rejected. Fix these issues:

Missing sections: {missing}

Feedback:
{issues}

Generate a complete improved PRD with ALL 10 sections.
"""

    draft = run_writer_agent(prompt)

    return {
        **state,
        "current_draft": draft,
        "iteration_count": state["iteration_count"] + 1,
        "status": "reviewing",
    }


def critic_node(state: DocumentState) -> DocumentState:
    feedback = run_critic_agent(state["current_draft"])

    return {
        **state,
        "critic_feedback": feedback,
        "status": feedback.get("status", "needs_revision"),
    }


def finalize_node(state: DocumentState) -> DocumentState:
    return {
        **state,
        "final_document": state["current_draft"],
        "status": "approved",
    }


def should_revise(state: DocumentState) -> str:
    fb = state.get("critic_feedback", {})
    score = fb.get("score", 0)
    iterations = state.get("iteration_count", 0)

    if fb.get("status") == "approved" and score >= 75:
        return "approved"
    elif iterations >= MAX_ITERATIONS:
        return "approved"

    return "revise"


def build_graph():
    from langgraph.graph import StateGraph, END

    workflow = StateGraph(DocumentState)

    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("finalize", finalize_node)

    workflow.set_entry_point("writer")

    workflow.add_edge("writer", "critic")
    workflow.add_edge("finalize", END)

    workflow.add_conditional_edges(
        "critic",
        should_revise,
        {
            "approved": "finalize",
            "revise": "writer",
        },
    )

    return workflow.compile()


if __name__ == "__main__":
    print("Building graph...")
    graph = build_graph()

    test_inputs = [
        "Build a food delivery app for students.",
        "Build an e-commerce app for handmade crafts.",
        "Build a fitness tracking app for gym members.",
    ]

    for idea in test_inputs:
        print("\n" + "=" * 60)
        print(f"Testing: {idea}")
        print("=" * 60)

        result = graph.invoke(
            {
                "raw_input": idea,
                "current_draft": "",
                "critic_feedback": {},
                "iteration_count": 0,
                "status": "drafting",
                "final_document": None,
            }
        )

        print(f"Score: {result['critic_feedback'].get('score')}")
        print(f"Status: {result['status']}")
        print(f"Iterations: {result['iteration_count']}")
        print(f"Approved: {result['status'] == 'approved'}")