import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from api.schemas import DocumentRequest, DocumentResponse, CriticFeedback
from graph.workflow import build_graph

router = APIRouter(prefix='/api/v1')

# In-memory store for pending approvals
pending = {}

@router.post('/generate-document')
def generate_document(req: DocumentRequest):
    graph = build_graph()
    result = graph.invoke({
        'raw_input': req.raw_input,
        'current_draft': '',
        'critic_feedback': {},
        'iteration_count': 0,
        'status': 'drafting',
        'final_document': None
    })
    
    doc_id = f'doc_{len(pending) + 1}'
    pending[doc_id] = result
    
    return {
        'doc_id': doc_id,
        'draft': result['current_draft'],
        'score': result['critic_feedback'].get('score'),
        'status': result['status'],
        'iterations': result['iteration_count']
    }

@router.post('/approve-document/{doc_id}')
def approve(doc_id: str):
    if doc_id not in pending:
        raise HTTPException(status_code=404, detail='Document not found')
    doc = pending[doc_id]
    return {
        'message': 'Document approved!',
        'doc_id': doc_id,
        'final_document': doc['current_draft']
    }

@router.post('/reject-document/{doc_id}')
def reject(doc_id: str, reason: str = ''):
    if doc_id not in pending:
        raise HTTPException(status_code=404, detail='Document not found')
    pending.pop(doc_id)
    return {
        'message': 'Document rejected. Please resubmit with revised input.',
        'doc_id': doc_id,
        'reason': reason
    }

@router.get('/pending-approvals')
def pending_list():
    return {
        'pending': list(pending.keys()),
        'count': len(pending)
    }