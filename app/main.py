from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import generate_answer


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Financial LLM RAG API running"}


class AnalyzeRequest(BaseModel):
    question: str


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    answer = generate_answer(request.question)
    return {"question": request.question, "answer": answer}

