# scripts/demo.py
from app import rag

# Ingest a PDF (replace with a small local PDF for demo)
rag.ingest_pdf("20250927-aapl-10K.pdf")

# Ask some questions
questions = [
    "What was total revenue in 2025?",
    "What was net income in 2025?",
    "What are key risk factors?"
]

for q in questions:
    answer = rag.rag_query(q)
    print(f"Q: {q}\nA: {answer}\n{'-'*60}")

