from fastapi import FastAPI
from .rag import generate_answer


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Financial LLM RAG API running"}

@app.post("/analyze")
def analyze(question: str):
    answer = generate_answer(question)
    return {"question": question, "answer": answer}

