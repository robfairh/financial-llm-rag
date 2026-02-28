# financial-llm-rag
Hosts a RAG LLM pipeline for analyzing earnings reports, 10-Ks, and other financial documents.


# DEMO output

## BUILD DEMO

```
(base) roberto ~/Documents/financial-llm-rag (main) $ PYTHONPATH=. python scripts/demo.py 
2026-02-28 15:00:33.166159: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2026-02-28 15:00:46.410214: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:38] TF-TRT Warning: Could not find TensorRT
/home/roberto/miniconda3/lib/python3.9/site-packages/huggingface_hub/file_download.py:942: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
Token indices sequence length is longer than the specified maximum sequence length for this model (1205 > 512). Running this sequence through the model will result in indexing errors
Q: What was total revenue in 2025?
A: $132.4 billion
------------------------------------------------------------
Q: What was net income in 2025?
A: Net income $ 112,010 $ 93,736 $ 96,995 Earnings per share: Basic $ 7.49 $ 6.11 $ 6.16 Diluted $ ves/edgar/data/320193/000032019325000079/aapl-20250927.htm 34/78 1/17/26, 11:13 AM aapl-20250927
------------------------------------------------------------
Q: What are key risk factors?
A: The Company’s net sales and gross margins are subject to volatility and downward pres ect on the Company’s business, reputation, results of operations, financial condition and stock price
------------------------------------------------------------
```

## Run API locally

uvicorn app.main:app --reload

```
(base) roberto ~/Documents/financial-llm-rag (main) $ curl -X POST "http://127.0.0.1:8000/analyze" \
>   -H "Content-Type: application/json" \
>   -d '{"question":"What was net income in 2025?"}'
{"question":"What was net income in 2025?","answer":"No documents ingested yet."}(base) roberto ~/Documents/financial-llm-rag (main) $ curl -X POST "http://127.0.0.1:8000/ingest" \
>   -F "file=@20250927-aapl-10K.pdf"
{"filename":"20250927-aapl-10K.pdf","status":"ingested"}(base) roberto ~/Documents/financial-llm-rag (main) $ curl -X POST "http://127.0.0.1:8000/ingest"   -F "fileanalyze"   -H "Content-Type: application/json"   -d '{"question":"What was net income in 2025?"}'
{"question":"What was net income in 2025?","answer":"Net income $ 112,010 $ 93,736 $ 96,995 Earnings per share: Basic $ 7.49 $ 6.11 $ 6.16 Diluted $ ves/edgar/data/320193/000032019325000079/aapl-20250927.htm 34/78 1/17/26, 11:13 AM aapl-20250927"}(base) roberto ~/Documents/financial-llm-rag (main) $ 
```

