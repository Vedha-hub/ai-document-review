import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# API endpoint tests
# Run server first: uvicorn api.main:app --reload --port 8000
# Then test via http://localhost:8000/docs

def test_endpoints_exist():
    from api.routes import router
    routes = [r.path for r in router.routes]
    assert '/api/v1/generate-document' in routes
    assert '/api/v1/pending-approvals' in routes
    print("✅ All API endpoints exist — PASSED")

if __name__ == '__main__':
    test_endpoints_exist()
    print("✅ API tests passed!")