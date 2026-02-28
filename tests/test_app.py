from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_analyze():
    response = client.post("/analyze", json={"question": "What is revenue?"})
    assert response.status_code == 200
    assert "answer" in response.json()

