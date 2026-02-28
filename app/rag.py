import torch
import faiss
import pdfplumber
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer


# -------------------
# config
# -------------------
# MODEL_NAME = "tiiuae/falcon-7b-instruct"
MODEL_NAME = "google/flan-t5-small"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_model, _tokenizer = None, None
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# FAISS index and storage
index = None
chunks = []

# -------------------
# Model lazy loader
# -------------------
def get_model():
    global _model, _tokenizer
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE)
    return _model, _tokenizer

# --------------------------
# PDF / document ingestion
# --------------------------
def ingest_pdf(path: str, chunk_size: int = 800):
    global index, chunks
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    new_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    embs = embedding_model.encode(new_chunks, convert_to_numpy=True).astype("float32")

    if index is None:
        index = faiss.IndexFlatL2(embs.shape[1])
    index.add(embs)
    chunks.extend(new_chunks)

# --------------------------
# Retrieval
# --------------------------
def retrieve(query, k=5):
    if not index or len(chunks) == 0:
        return []
    query_emb = embedding_model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_emb, k)
    return [chunks[i] for i in indices[0]]

# --------------------------
# Prompt builder
# --------------------------
def build_prompt(context_chunks, question):
    context = "\n\n".join(context_chunks)
    return f"""
You are a financial analyst.

Answer the question using ONLY the information below.
If the answer is not present, say: "Not found in the document."

Context:
{context}

Question:
{question}

Answer:
"""

# --------------------------
# Answer generator
# --------------------------
def generate_answer(prompt):
    model, tokenizer = get_model()
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
    outputs = model.generate(**inputs, max_new_tokens=200, do_sample=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# --------------------------
# RAG query helper
# --------------------------
def rag_query(question):
    docs_for_q = retrieve(question)
    if not docs_for_q:
        return "No documents ingested yet."
    prompt = build_prompt(docs_for_q, question)
    return generate_answer(prompt)

