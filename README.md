# Multimodal AI Agent

An enterprise-grade, **multimodal** AI backend built with **FastAPI**, **LangGraph**, and **Hybrid Retrieval-Augmented Generation (Hybrid RAG)**. The system accepts text, images, audio, video, and realtime voice, intelligently routes each request to the appropriate execution engine—Knowledge Retrieval, SQL Database, or Calculator—and produces grounded, validated, and cited responses.

The project is designed using a modular architecture where every major component is independently replaceable, making it suitable for enterprise deployments and large-scale AI systems.

---

# Table of Contents

* Overview
* Features
* System Architecture
* End-to-End Workflow
* LangGraph Workflow
* Hybrid RAG Workflow
* Document Indexing Workflow
* Project Structure
* Technology Stack
* Installation
* Environment Variables
* Running the Application

---

# Overview

Multimodal AI Agent provides a unified interface for answering enterprise questions from text, images, audio, video, and voice, using multiple information sources.

Input can arrive as text, an image, an audio clip, a video, or a realtime voice stream — a multimodal preprocessing layer (`app/multimodal/`) converts every non-text input into plain text before anything else happens, so the rest of the pipeline stays modality-agnostic.

Depending on the incoming request, the system automatically selects one of three execution paths:

* Hybrid RAG for enterprise documents
* Read-only SQL database querying
* Secure mathematical calculations

Instead of relying on a single LLM prompt, the application orchestrates multiple independent components using **LangGraph**, ensuring predictable execution, modularity, and maintainability.

The project focuses on:

* Grounded responses
* Citation generation
* Confidence scoring
* Safe SQL execution
* Hybrid retrieval
* Enterprise-ready architecture

---

# Features

## Multimodal Input

* Image understanding (captioning + OCR) via a vision model
* Audio transcription (speech-to-text) via Whisper
* Video understanding (sampled frames + audio transcript) via ffmpeg
* Realtime push-to-talk voice chat (STT → agent → TTS) over WebSocket
* Every modality converts to plain text before hitting the shared agent graph

## AI Agent

* LangGraph-based workflow orchestration
* Planner-driven tool routing
* Multi-tool execution
* Modular node architecture
* State-based execution

## Hybrid RAG

* Dense vector retrieval
* BM25 keyword retrieval
* Hybrid score merging
* Cross-Encoder reranking
* Source citations
* Metadata-aware retrieval

## SQL Engine

* Read-only database access
* Automatic SQL generation
* Query validation
* Safe execution
* SQLAlchemy integration

## Calculator

* Secure AST-based expression evaluation
* Natural language expression extraction
* No usage of `eval()` or `exec()`

## Response Engine

* Context construction
* LLM answer generation
* Citation generation
* Confidence scoring
* Response validation

---

# System Architecture

```text
                           Client
                              │
                              │ HTTP
                              ▼
                     FastAPI REST API
                              │
                              ▼
                  Dependency Injection Layer
                              │
                              ▼
                  Enterprise LangGraph Agent
                              │
                    Planner / Router Node
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
  Knowledge Tool         SQL Tool          Calculator Tool
         │                    │                    │
         ▼                    ▼                    ▼
 Enterprise Retriever     SQL Database      Safe AST Evaluator
         │
         ▼
 ┌─────────────────────────────────────────────┐
 │ Hybrid Retrieval Engine                     │
 │                                             │
 │  Dense Search (Qdrant)                      │
 │  BM25 Search                                │
 │  Hybrid Merge                               │
 │  Cross Encoder Reranker                     │
 └─────────────────────────────────────────────┘
                     │
                     ▼
               Response Engine
                     │
     ┌───────────────────────────────────┐
     │ Context Builder                   │
     │ Response Generator                │
     │ Citation Builder                  │
     │ Confidence Scorer                 │
     │ Response Validator                │
     └───────────────────────────────────┘
                     │
                     ▼
               JSON API Response
```

---

# End-to-End Workflow

```text
User Request
      │
      ▼
POST /chat
      │
      ▼
Planner Node
      │
      ├──────────────► Knowledge Tool
      │                    │
      │                    ▼
      │             Hybrid Retrieval
      │
      ├──────────────► SQL Tool
      │                    │
      │                    ▼
      │              SQL Execution
      │
      └──────────────► Calculator
                           │
                           ▼
                    Mathematical Result
                           │
                           ▼
                   Response Construction
                           │
                           ▼
                  Citation Generation
                           │
                           ▼
                 Confidence Calculation
                           │
                           ▼
                  Response Validation
                           │
                           ▼
                    HTTP JSON Response
```

---

# LangGraph Workflow

The application is orchestrated using a directed execution graph.

```text
START
  │
  ▼
Planner
  │
  ├────────► Knowledge Node
  │
  ├────────► SQL Node
  │
  └────────► Calculator Node
               │
               ▼
          Response Node
               │
               ▼
        Validation Node
               │
               ▼
              END
```

Each node has a single responsibility.

| Node       | Responsibility                     |
| ---------- | ---------------------------------- |
| Planner    | Select execution tool              |
| Knowledge  | Hybrid document retrieval          |
| SQL        | Generate and execute read-only SQL |
| Calculator | Evaluate mathematical expressions  |
| Response   | Build context and generate answer  |
| Validation | Validate final response            |

---

# Hybrid RAG Workflow

The retrieval engine combines semantic search with keyword search.

```text
Question
   │
   ▼
Embedding Generation
   │
   ├────────────► Dense Retrieval (Qdrant)
   │
   └────────────► BM25 Retrieval
                     │
                     ▼
               Hybrid Merge
                     │
                     ▼
          Cross Encoder Reranker
                     │
                     ▼
               Top-k Chunks
                     │
                     ▼
             Context Builder
```

This hybrid approach improves retrieval quality by combining semantic similarity with exact keyword matching.

---

# Document Indexing Workflow

Documents are processed before becoming searchable.

```text
Documents
    │
    ▼
Document Loader
    │
    ▼
Document Cleaner
    │
    ▼
Metadata Builder
    │
    ▼
Chunk Splitter
    │
    ▼
Embedding Generation
    │
    ▼
Qdrant Vector Store
    │
    ▼
BM25 Corpus Snapshot
```

Supported document formats include:

* PDF
* DOCX
* TXT
* Markdown
* CSV
* HTML

---

# Project Structure

```text
app/
│
├── agent/
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
│
├── api/
│   ├── router.py
│   ├── schemas.py
│   └── dependencies.py
│
├── core/
│   └── config.py
│
├── llm/
│   ├── base.py
│   ├── factory.py
│   └── openai_client.py
│
├── multimodal/
│   ├── image_handler.py      # vision captioning + OCR
│   ├── audio_handler.py      # Whisper STT + TTS
│   ├── video_handler.py      # ffmpeg frame/audio extraction
│   └── voice_realtime.py     # WebSocket push-to-talk voice loop
│
├── planner/
│
├── prompts/
│
├── rag/
│   ├── ingestion/
│   ├── indexing/
│   └── retrieval/
│
├── response/
│
├── services/
│
├── tools/
│
└── main.py

tests/
scripts/
requirements.txt
README.md
```

---

# Technology Stack

| Layer           | Technology             |
| --------------- | ---------------------- |
| API             | FastAPI                |
| AI Workflow     | LangGraph              |
| LLM             | OpenAI                 |
| Embeddings      | BAAI/bge-m3            |
| Reranker        | BAAI/bge-reranker-base |
| Vector Database | Qdrant                 |
| Keyword Search  | BM25                   |
| Vision          | OpenAI vision model (captioning + OCR) |
| Speech-to-text  | OpenAI Whisper         |
| Text-to-speech  | OpenAI TTS             |
| Video frame/audio extraction | ffmpeg    |
| ORM             | SQLAlchemy             |
| Validation      | Pydantic               |
| Testing         | Pytest                 |
| Language        | Python 3.12            |

---

# Installation

Clone the repository.

```bash
git clone <repository-url>

cd multimodal-ai-agent
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
OPENAI_API_KEY=

OPENAI_MODEL=gpt-4o-mini

QDRANT_URL=http://localhost:6333

QDRANT_COLLECTION=enterprise_knowledge

DATABASE_URL=sqlite:///enterprise.db

EMBEDDING_MODEL=BAAI/bge-m3

RERANKER_MODEL=BAAI/bge-reranker-base
```

---

# Running the Application

Start the FastAPI server.

```bash
uvicorn app.main:app --reload
```

Once started, the API is available at:

```text
http://localhost:8000
```

Available endpoints:

| Method | Endpoint | Description           |
| ------ | ------------ | ------------------------------------- |
| GET    | /health      | Health check                          |
| POST   | /chat        | Text chat endpoint                    |
| POST   | /chat/image  | Chat with an image (caption + OCR)    |
| POST   | /chat/audio  | Chat with an audio clip (speech-to-text) |
| POST   | /chat/video  | Chat with a video (frames + audio)    |
| WS     | /ws/voice    | Realtime push-to-talk voice chat      |
| GET    | /docs        | Swagger documentation                 |

# API Usage

## Health Check

Verify that the service is running.

```http
GET /health
```

### Response

```json
{
  "status": "ok"
}
```

---

## Chat Endpoint

Submit a question to the Multimodal AI Agent.

```http
POST /chat
```

### Request

```json
{
  "question": "What is the employee leave policy?"
}
```

### Example Response

```json
{
  "answer": "Employees are entitled to 20 annual leave days.",
  "sources": [
    {
      "document": "HR_Policy.pdf",
      "page": 12,
      "section": "Leave Policy"
    }
  ],
  "confidence": 0.96
}
```

---

## Multimodal Endpoints

The agent accepts more than text. Every non-text input is converted to
plain text by a handler in `app/multimodal/`, then run through the
**exact same** LangGraph pipeline (planner → knowledge/SQL/calculator
→ response engine) that `/chat` uses — so citations, confidence
scoring, and validation all work identically regardless of modality.

| Modality | Endpoint      | How it's converted to text                                  |
| -------- | ------------- | ------------------------------------------------------------ |
| Image    | `POST /chat/image` | Vision model captions the image and transcribes any visible text (OCR) |
| Audio    | `POST /chat/audio` | Whisper transcribes the clip to text                         |
| Video    | `POST /chat/video` | `ffmpeg` samples frames (described by the vision model) + extracts and transcribes the audio track |
| Voice (realtime) | `WS /ws/voice` | Push-to-talk loop: Whisper STT → agent → TTS spoken reply |

All three upload endpoints accept the same form fields and return the
same response shape:

### Request (multipart/form-data)

| Field      | Required | Notes                                              |
| ---------- | -------- | --------------------------------------------------- |
| `file`     | yes      | The image / audio / video file                      |
| `question` | no       | Optional text question to pair with the attachment. If omitted, the extracted content itself is used as the question. |

```http
POST /chat/image
Content-Type: multipart/form-data

file=@invoice.png
question=Does the total on this invoice match our SQL records?
```

### Example Response

```json
{
  "answer": "The invoice total ($4,820) matches the amount on file for PO-1042.",
  "sources": [],
  "confidence": 0.9,
  "modality": "image",
  "extracted_text": "An invoice from Acme Supplies dated ... Total: $4,820.00 ..."
}
```

`extracted_text` is exactly what the vision/STT model produced before
the question was answered — useful for debugging and for showing the
user what the agent actually "saw" or "heard".

### Realtime Voice (`/ws/voice`)

Push-to-talk over a WebSocket, one full utterance per turn:

1. Client sends **one binary message** containing a complete recorded
   utterance (e.g. a `.wav`/`.webm` clip).
2. Server replies with:
   - a **text** message: `{"type": "answer", "transcript": "...", "text": "...", "confidence": 0.9}`
   - a **binary** message containing the synthesized speech (MP3) for that answer.
3. Repeat for the next utterance, or close the connection.

```js
const ws = new WebSocket("ws://localhost:8000/ws/voice");
ws.binaryType = "arraybuffer";
ws.onmessage = (event) => {
  if (typeof event.data === "string") {
    console.log(JSON.parse(event.data)); // transcript + answer
  } else {
    playAudio(event.data); // MP3 bytes -> speaker
  }
};
// later: ws.send(recordedAudioBlobBytes)
```

This is turn-based (not token-level streaming) by design — it keeps
the endpoint simple and reliable. True continuous/interruptible
streaming is listed in the roadmap below.

### Requirements for multimodal features

- `OPENAI_API_KEY` must be set — image, audio, and video handlers all
  call OpenAI's vision, Whisper, and TTS APIs.
- Video processing additionally requires the **`ffmpeg`** binary to be
  installed and on `PATH` (e.g. `apt install ffmpeg` / `brew install ffmpeg`).
  If it's missing, `/chat/video` returns `503` with a clear message
  instead of a stack trace.
- Uploads are capped at `MAX_UPLOAD_SIZE_MB` (default 25MB, see `.env.example`).

---

# Document Indexing

Before documents become searchable they must be indexed.

Run the indexing script:

```bash
python scripts/index_documents.py ./documents
```

The indexing pipeline performs the following operations:

```text
Load Documents
      │
      ▼
Clean Text
      │
      ▼
Extract Metadata
      │
      ▼
Chunk Documents
      │
      ▼
Generate Embeddings
      │
      ▼
Store Vectors in Qdrant
      │
      ▼
Create BM25 Snapshot
```

Indexed chunks are stored in:

* Qdrant Vector Database
* BM25 Corpus Snapshot

Both are used together during retrieval.

---

# Retrieval Pipeline

Every knowledge request follows the same retrieval pipeline.

```text
User Question
      │
      ▼
Embedding Generation
      │
      ├────────────► Dense Search
      │
      └────────────► BM25 Search
                          │
                          ▼
                 Hybrid Score Merge
                          │
                          ▼
             Cross Encoder Reranking
                          │
                          ▼
                  Top-k Relevant Chunks
                          │
                          ▼
                  Context Construction
```

This approach combines semantic understanding with exact keyword matching to improve retrieval accuracy.

---

# Response Generation Pipeline

After retrieval, the response engine constructs the final answer.

```text
Retrieved Context
        │
        ▼
Context Builder
        │
        ▼
LLM Response Generator
        │
        ▼
Citation Builder
        │
        ▼
Confidence Scorer
        │
        ▼
Response Validator
        │
        ▼
Final JSON Response
```

Every response contains:

* Answer
* Sources
* Confidence Score

---

# Configuration

All application configuration is centralized in `app/core/config.py`.

Configuration categories include:

* LLM Provider
* OpenAI Model
* Embedding Model
* Reranker Model
* Qdrant Connection
* SQL Database
* Chunk Size
* Chunk Overlap
* Retrieval Parameters

Using a centralized configuration layer simplifies deployment across multiple environments.

---

# Testing

Run the complete test suite.

```bash
pytest
```

Run a specific module.

```bash
pytest tests/agent
```

Run a single file.

```bash
pytest tests/tools/test_calculator.py
```

Generate coverage.

```bash
pytest --cov=app
```

---

# Security

The project includes multiple safeguards for production deployments.

## SQL Safety

* Only `SELECT` statements are executed.
* Destructive SQL operations are rejected.
* Queries are validated before execution.

Rejected statements include:

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* TRUNCATE

---

## Calculator Safety

The calculator does **not** use:

* `eval()`
* `exec()`

Instead, it evaluates expressions through Python's Abstract Syntax Tree (AST), preventing arbitrary code execution.

---

## Response Validation

Every generated response is validated using Pydantic before being returned to the client.

Validation includes:

* Answer
* Sources
* Confidence Score

---

## Grounded Generation

The language model is instructed to:

* Answer only from retrieved context
* Avoid hallucinations
* Return "Information not found" when evidence is unavailable
* Include citations whenever possible

---

# Performance Optimizations

Several optimizations improve throughput and reduce latency.

## Lazy Loading

Large ML models are initialized only when first required.

---

## Dependency Caching

Frequently used components are cached using `lru_cache()`.

Examples include:

* Embedding model
* Vector store
* Reranker
* SQL engine
* LLM client

---

## Hybrid Retrieval

Combining semantic retrieval with keyword search significantly improves recall compared to either approach alone.

---

## Cross Encoder Reranking

Retrieved candidates are reranked before context generation, improving answer quality by prioritizing the most relevant chunks.

---

# Design Decisions

## LangGraph

Chosen for deterministic workflow orchestration and explicit execution graphs.

---

## Hybrid Retrieval

Combines:

* Dense vector search
* BM25 keyword retrieval

This improves retrieval quality across both semantic and lexical queries.

---

## Modular Architecture

Every subsystem is independently replaceable.

Examples include:

* LLM Provider
* Embedding Model
* Reranker
* Vector Database
* SQL Database

No component is tightly coupled to another.

---

## Dependency Injection

The API layer does not instantiate services directly.

All dependencies are provided through a centralized dependency injection layer, improving maintainability and testability.

---

# Future Roadmap

Planned improvements include:

* True token-level realtime voice streaming (interruptible, partial transcripts) instead of the current turn-based push-to-talk loop
* Multimodal document ingestion (images/diagrams embedded in indexed PDFs, described and made retrievable)
* Multi-turn conversation memory
* Streaming responses
* Authentication and authorization
* Role-based document access
* Multi-agent workflows
* Async retrieval pipeline
* Redis caching
* Kubernetes deployment
* Docker Compose support
* Observability with Prometheus and Grafana
* OpenTelemetry tracing
* Multi-LLM provider support
* Evaluation framework
* Automatic document ingestion
* Continuous indexing
* Agent analytics dashboard

---

# Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

Please ensure all tests pass before submitting changes.

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for complete license information.

---

# Acknowledgements

This project is built using the following open-source technologies:

* FastAPI
* LangGraph
* OpenAI
* LangChain
* Qdrant
* SQLAlchemy
* Pydantic
* Hugging Face Transformers
* Sentence Transformers
* BM25
* Pytest

Each project contributes to the architecture and capabilities of this Multimodal AI Agent.
