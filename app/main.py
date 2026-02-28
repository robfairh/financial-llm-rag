# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import tempfile
from app import rag

app = FastAPI(title="Financial RAG API")

# --------------------------
# Request models
# --------------------------
class AnalyzeRequest(BaseModel):
    question: str

# --------------------------
# Endpoints
# --------------------------

@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF to ingest its content into the RAG index.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp.flush()
        rag.ingest_pdf(tmp.name)
    
    return {"filename": file.filename, "status": "ingested"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    """
    Ask a question. Returns an answer based on ingested PDFs.
    """
    answer = rag.rag_query(request.question)
    return {"question": request.question, "answer": answer}

