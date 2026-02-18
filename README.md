# QuantumLeap AI — Private Knowledge Workspace

QuantumLeap AI is a production-oriented knowledge management system designed for grounded document intelligence. It utilizes Retrieval-Augmented Generation (RAG) to allow users to interact with uploaded datasets while maintaining strict data provenance and verifiable evidence.

---

## Technical Features

* **Multi-Format Ingestion:** Support for PDF, DOCX, TXT, MD, and XLSX.
* **Workspace Management:** Isolated document storage and retrieval per workspace.
* **Grounded QA:** RAG-based query engine ensuring answers are derived strictly from provided context.
* **Citation Engine:** Direct mapping of LLM responses to specific document segments.
* **System Diagnostics:** Integrated health monitoring for API, Database, and LLM provider status.
* **Safe Deletion:** Synchronized removal of files and corresponding vector embeddings to maintain index integrity.

---

## Architecture Overview

### System Flow

1. **Ingestion:** Documents are parsed and decomposed into semantic chunks.
2. **Vectorization:** Text chunks are transformed into high-dimensional vectors using `all-MiniLM-L6-v2`.
3. **Indexing:** Vectors are stored in a local FAISS index for low-latency similarity search.
4. **Retrieval:** User queries are embedded to find the top  relevant context blocks.
5. **Augmentation:** The LLM (`llama-3.1-8b-instant`) processes the query alongside retrieved context to generate a grounded response.

### Technical Stack

| Layer | Technology |
| --- | --- |
| **Frontend** | React, TailwindCSS |
| **Backend** | FastAPI (Asynchronous API Layer) |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **Embeddings** | SentenceTransformers (Local Inference) |
| **Inference** | Groq Cloud API (Llama 3.1) |

---

## Engineering Decisions & Tradeoffs

### 1. Retrieval-Augmented Generation (RAG) vs. Fine-Tuning

Fine-tuning models on private data is computationally expensive and suffers from data obsolescence. RAG was chosen to provide:

* **Real-time Updates:** New documents are queryable immediately after indexing.
* **Zero Hallucination Focus:** The model is constrained by system prompting to only use provided context.
* **Auditability:** Every answer can be traced back to a specific document chunk.

### 2. Local FAISS vs. Managed Vector Databases

**Decision:** Local FAISS Index.

* **Reasoning:** For the current scope, FAISS offers sub-millisecond search latency without the overhead of network calls to external providers like Pinecone.
* **Tradeoff:** Vertical scaling is limited. For production environments with millions of documents, a transition to a distributed vector database (e.g., Qdrant or Weaviate) would be required.

### 3. Embedding Model: `all-MiniLM-L6-v2`

**Decision:** Small-footprint local encoder.

* **Reasoning:** This model strikes an optimal balance between semantic accuracy and CPU-bound inference speed. It allows the backend to remain performant without requiring dedicated GPU resources for the embedding step.

### 4. Semantic Chunking Strategy

Text is split into medium-sized overlapping chunks.

* **Small Chunks:** High precision but lose surrounding context (coherence).
* **Large Chunks:** Better context but introduce "noise" and increase token costs.
* **Our Approach:** Balanced chunking with a 10-15% overlap to ensure semantic continuity across boundaries.

---

## Scalability & Future Roadmap

### Current Bottlenecks

* **Synchronous Processing:** Heavy document uploads can block the API event loop.
* **Memory Persistence:** FAISS indices are currently stored on the local filesystem, which is incompatible with ephemeral container deployments (e.g., Heroku, AWS Fargate).

### Proposed Enhancements

1. **Asynchronous Task Queue:** Implement Celery or Redis Streams for background document processing.
2. **Hybrid Search:** Combine FAISS semantic search with BM25 keyword matching to improve retrieval for technical jargon and acronyms.
3. **Streaming Responses:** Implement Server-Sent Events (SSE) for real-time LLM token streaming to improve perceived UX latency.
4. **Persistent Storage:** Migrate file storage to AWS S3 and vector storage to a managed cloud provider.

---

## Safety & Reliability

* **Boundary Constraints:** System prompts explicitly forbid the LLM from using internal "world knowledge" when answering.
* **Input Sanitization:** Strict file extension validation and size limits (10MB) to prevent DoS attacks via resource exhaustion.
* **Environment Security:** No hardcoded credentials; all API keys and model configurations are managed via environment variables.

---

## Local Development Setup

### Backend Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

```

### Frontend Environment

```bash
cd frontend
npm install
npm run dev

```

### Required Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_actual_key_here
MODEL_NAME=llama-3.1-8b-instant
EMBEDDING_MODEL=all-MiniLM-L6-v2

```

---

**Author:** Korivi Chetan Kumar

**Role:** AI/ML Engineer

**Contact:** korivichetan5@gmail.com

**License:** MIT

---