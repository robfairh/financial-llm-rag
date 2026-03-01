# financial-llm-rag
This repo hosts a RAG LLM pipeline for analyzing earnings reports, 10-Ks, and other financial documents.

The pipeline runs locally and uses an Apple 10-K for its capability
demonstration. <br />
The response model is based on the `google/flan-t5-small` which is an
instruction-tuned version of T5 (Text-to-Text Transfer Transformer). <br />
This is a lightweight version of the model which makes faster to run either
locally or to deploy on SAAS free tiers. <br />
And that could be the natural next step for a real life production-ready
project, to deploy the package as-is or dockerized on a SAAS platform. <br />


# DEMO output

## Run demo

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

## Run tests locally

```
(base) roberto ~/Documents/financial-llm-rag (main) $ PYTHONPATH=. pytest
========================== test session starts ===========================
platform linux -- Python 3.9.18, pytest-8.4.2, pluggy-1.6.0
rootdir: /home/roberto/Documents/financial-llm-rag
configfile: pytest.ini
plugins: hydra-core-1.3.2, anyio-4.2.0, typeguard-4.5.1, time-machine-2.13.0
collected 2 items                                                        

tests/test_app.py ..                                               [100%]

============================ warnings summary ============================
../../miniconda3/lib/python3.9/site-packages/huggingface_hub/file_download.py:942
  /home/roberto/miniconda3/lib/python3.9/site-packages/huggingface_hub/file_download.py:942: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
    warnings.warn(

../../miniconda3/lib/python3.9/site-packages/httpx/_client.py:680
  /home/roberto/miniconda3/lib/python3.9/site-packages/httpx/_client.py:680: DeprecationWarning: The 'app' shortcut is now deprecated. Use the explicit style 'transport=WSGITransport(app=...)' instead.
    warnings.warn(message, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============== 2 passed, 2 warnings in 157.79s (0:02:37) ================
```

## Run tests using GitHub Actions

Tests passing [link](
https://github.com/robfairh/financial-llm-rag/actions/runs/22529226301/job/65266033919)


