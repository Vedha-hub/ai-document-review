from pydantic import BaseModel
from typing import Optional, List

class DocumentRequest(BaseModel):
    raw_input: str
    max_iterations: Optional[int] = 3

class CriticFeedback(BaseModel):
    status: str
    score: int
    missing_sections: List[str]
    feedback: List[str]
    approval_message: str

class DocumentResponse(BaseModel):
    final_document: str
    critic_feedback: CriticFeedback
    iteration_count: int
    status: str