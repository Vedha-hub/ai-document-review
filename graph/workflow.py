from typing import TypedDict, Optional

class DocumentState(TypedDict):
    raw_input: str
    current_draft: str
    critic_feedback: dict
    iteration_count: int
    status: str
    final_document: Optional[str]