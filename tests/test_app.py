# tests/test_app.py
from fastapi.testclient import TestClient
from app.main import app
import app.rag as rag

# Mock RAG functions to skip heavy model loading
rag.rag_query = lambda question: "mocked answer"
rag.ingest_pdf = lambda path: None

client = TestClient(app)

def test_analyze():
    response = client.post("/analyze", json={"question": "test"})
    assert response.status_code == 200
    assert response.json()["answer"] == "mocked answer"

def test_ingest():
    response = client.post("/ingest", files={"file": ("dummy.pdf", b"%PDF-1.4")})
    assert response.status_code == 200
    assert response.json()["status"] == "ingested"

