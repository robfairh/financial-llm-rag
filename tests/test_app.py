from fastapi.testclient import TestClient
from app.main import app
import app.rag as rag


def fake_answer(question):
    return "mocked answer"

rag.generate_answer = fake_answer
client = TestClient(app)


def test_analyze():
    response = client.post("/analyze", json={"question": "test"})
    assert response.status_code == 200
    assert response.json()["answer"] == "mocked answer"

