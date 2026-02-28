# import faiss
# import torch
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from transformers import AutoModelForCausalLM, AutoTokenizer
# 
# 
# # 1. Load embeddings
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# 
# # 2. Dummy vector DB
# dimension = 384
# index = faiss.IndexFlatL2(dimension)
# texts = [
#     "Company revenue increased by 10%",
#     "R&D expenses grew by 5%"
# ]
# embeddings = embedding_model.encode(texts)
# index.add(np.array(embeddings).astype("float32"))
# 
# # 3. Load LLM
# model_name = "tiiuae/falcon-7b-instruct"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
# # model = AutoModelForCausalLM.from_pretrained(model_name)
# 
# def retrieve(query, k=1):
#     q_emb = embedding_model.encode([query])
#     D, I = index.search(np.array(q_emb).astype("float32"), k)
#     return [texts[i] for i in I[0]]
# 
# def generate_answer(query):
#     context = retrieve(query)[0]
#     input_text = f"Context: {context}\nQuestion: {query}\nAnswer:"
#     inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
#     outputs = model.generate(**inputs, max_new_tokens=150)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)
# 
# rag.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


_model = None
_tokenizer = None


def get_model():
    global _model, _tokenizer

    if _model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

        model_name = "tiiuae/falcon-7b-instruct"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

    return _model, _tokenizer


def generate_answer(query):
    model, tokenizer = get_model()

    inputs = tokenizer(query, return_tensors="pt")
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    outputs = model.generate(**inputs, max_new_tokens=100)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

