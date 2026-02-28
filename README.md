# financial-llm-rag
Hosts a RAG LLM pipeline for analyzing earnings reports, 10-Ks, and other financial documents.


# DEMO output

## Run locally

uvicorn app.main:app --reload

(base) roberto ~/Documents/financial-llm-rag (main) $ curl -X POST "http://127.0.0.1:8000/analyze" \
>   -H "Content-Type: application/json" \
>   -d '{"question":"What was net income in 2025?"}'
{"question":"What was net income in 2025?","answer":"No documents ingested yet."}(base) roberto ~/Documents/financial-llm-rag (main) $ curl -X POST "http://127.0.0.1:8000/ingest" \
>   -F "file=@20250927-aapl-10K.pdf"
{"filename":"20250927-aapl-10K.pdf","status":"ingested"}(base) roberto ~/Documents/financial-llm-rag (main) $ curl -X POST "http://127.0.0.1:8000/ingest"   -F "fileanalyze"   -H "Content-Type: application/json"   -d '{"question":"What was net income in 2025?"}'
{"question":"What was net income in 2025?","answer":"Net income $ 112,010 $ 93,736 $ 96,995 Earnings per share: Basic $ 7.49 $ 6.11 $ 6.16 Diluted $ ves/edgar/data/320193/000032019325000079/aapl-20250927.htm 34/78 1/17/26, 11:13 AM aapl-20250927"}(base) roberto ~/Documents/financial-llm-rag (main) $ 


