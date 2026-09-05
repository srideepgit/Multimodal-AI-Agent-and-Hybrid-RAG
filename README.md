<div align="center">

# 🤖 Multimodal AI Agent & Hybrid RAG

### Enterprise-Ready Multimodal AI • Agentic Routing • Hybrid Retrieval • Grounded Responses

<br>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2600&pause=900&center=true&vCenter=true&width=900&lines=Text+%7C+Image+%7C+Audio+%7C+Video+%7C+Voice;LangGraph+Agentic+Workflow;BM25+%2B+Dense+Vector+Search;Cross-Encoder+Reranking;SQL+%2B+Calculator+Tools;Citations+%2B+Confidence+%2B+Validation" alt="Typing animation" />

<br><br>

<a href="#-quick-start">
<img src="https://img.shields.io/badge/%F0%9F%9A%80%20Quick%20Start-111827?style=for-the-badge" alt="Quick Start" />
</a>
<a href="#-architecture">
<img src="https://img.shields.io/badge/%F0%9F%8F%97%EF%B8%8F%20Architecture-1F2937?style=for-the-badge" alt="Architecture" />
</a>
<a href="#-api">
<img src="https://img.shields.io/badge/%F0%9F%94%8C%20API-4F46E5?style=for-the-badge" alt="API" />
</a>
<a href="#-hybrid-rag">
<img src="https://img.shields.io/badge/%F0%9F%94%8E%20Hybrid%20RAG-7C3AED?style=for-the-badge" alt="Hybrid RAG" />
</a>

<br><br>

<img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/FastAPI-0F766E?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/LangGraph-Agentic%20Workflow-111827?style=for-the-badge" alt="LangGraph" />
<img src="https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" />

<br>

<img src="https://img.shields.io/badge/Qdrant-Vector%20Search-DC244C?style=for-the-badge" alt="Qdrant" />
<img src="https://img.shields.io/badge/BM25-Lexical%20Retrieval-6B7280?style=for-the-badge" alt="BM25" />
<img src="https://img.shields.io/badge/Cross--Encoder-Reranking-2563EB?style=for-the-badge" alt="Cross Encoder" />
<img src="https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
<img src="https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic" />

<br><br>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&height=90&section=header&text=One%20Agent.%20Multiple%20Reasoning%20Paths.&fontSize=28&fontAlignY=55&animation=fadeIn" width="100%" alt="Animated header" />

</div>

---

## ✨ Overview

**Multimodal AI Agent & Hybrid RAG** is a modular AI backend that combines **agentic orchestration, multimodal understanding, hybrid retrieval, SQL analytics, safe calculation, citations, confidence scoring, and final-response validation** behind a single FastAPI service.

Instead of routing every request directly to a language model, the system first determines **what kind of reasoning the request needs** and then executes the most appropriate path.

### What the system can handle

| Capability | What it does |
|---|---|
| 💬 Text | Standard natural-language interaction |
| 🖼️ Image | Vision analysis + OCR-style text extraction |
| 🎙️ Audio | Speech-to-text + text-to-speech |
| 🎬 Video | Sampled-frame vision analysis + audio transcription |
| 🗣️ Voice | Push-to-talk WebSocket speech interaction |
| 📚 Knowledge | Hybrid BM25 + dense retrieval |
| 🔁 Reranking | Cross-encoder refinement of retrieved candidates |
| 🗄️ SQL | Read-only database-oriented question answering |
| 🧮 Calculator | Controlled expression evaluation |
| 🔖 Citations | Source-aware answer generation |
| 📈 Confidence | Retrieval-based confidence scoring |
| ✅ Validation | Final answer validation before returning output |

The multimodal layer converts image, audio, and video inputs into text/context that can enter the **same downstream LangGraph pipeline**, so the agent logic remains modality-agnostic. The API exposes dedicated multimodal endpoints for this workflow. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/api/router.py

---

# 🖼️ Application Experience

The repository includes a browser-based frontend with:

- Chat history and new-chat flow
- File attachment support
- Image/audio/video uploads
- API-base configuration
- Suggestion prompts
- Voice interaction support through the backend WebSocket API

The frontend is served by FastAPI when the `frontend/` directory is present. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/main.py

> **Add your own screenshots here** if you later want the repository to show the running UI directly. The project already contains the frontend implementation, so the README does not invent demo images that are not in the repository.

---

# 🎯 Key Design Goals

### 1. Route before generating

The planner identifies whether a request belongs to:

```text
Knowledge  →  Retrieval pipeline
SQL       →  Database tool
Math      →  Calculator
```

### 2. Retrieve before answering

Knowledge questions use retrieval rather than relying only on the LLM's parametric memory.

### 3. Keep multimodal logic modular

Images, audio, video, and voice are handled by dedicated adapters rather than embedding modality-specific logic throughout the agent.

### 4. Validate before returning

The response engine assembles context, generates an answer, builds citations, calculates confidence, and validates the result before returning it to the API caller. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/agent/nodes.py

---

# 🏗️ Architecture

```text
                                  ┌──────────────────────┐
                                  │       User           │
                                  │ Text / Image / Audio │
                                  │ Video / Voice        │
                                  └──────────┬───────────┘
                                             │
                                             ▼
                              ┌───────────────────────────┐
                              │        FastAPI API        │
                              │                           │
                              │ /chat                    │
                              │ /chat/image              │
                              │ /chat/audio              │
                              │ /chat/video              │
                              │ /ws/voice                │
                              └─────────────┬─────────────┘
                                            │
                            ┌───────────────┴───────────────┐
                            │   Multimodal Normalization   │
                            │ image → text                 │
                            │ audio → transcript           │
                            │ video → frames + transcript  │
                            │ voice → transcript           │
                            └───────────────┬───────────────┘
                                            │
                                            ▼
                                  ┌──────────────────┐
                                  │    LangGraph     │
                                  │      Agent       │
                                  └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │     Planner      │
                                  └───────┬──────────┘
                                          │
                       ┌──────────────────┼──────────────────┐
                       ▼                  ▼                  ▼
                ┌────────────┐     ┌────────────┐     ┌────────────┐
                │ Knowledge  │     │    SQL     │     │ Calculator │
                └─────┬──────┘     └─────┬──────┘     └─────┬──────┘
                      │                  │                  │
                      ▼                  ▼                  ▼
               Hybrid RAG         Read-only DB       Safe Evaluation
                      │                  │                  │
                      └──────────────────┼──────────────────┘
                                         ▼
                                ┌───────────────────┐
                                │  Response Engine  │
                                │ Context + LLM      │
                                │ Citations          │
                                │ Confidence         │
                                │ Validation         │
                                └─────────┬─────────┘
                                          │
                                          ▼
                                  ┌─────────────────┐
                                  │ Final Response  │
                                  └─────────────────┘
```

The LangGraph implementation contains explicit `planner`, `knowledge`, `sql`, `calculator`, `response`, and `validation` nodes, with conditional routing from the planner and a final validation stage. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/agent/graph.py

---

# 🧠 Agentic Workflow

The core execution path is:

```text
START
  │
  ▼
PLANNER
  │
  ├───────────────┬────────────────┐
  ▼               ▼                ▼
KNOWLEDGE         SQL         CALCULATOR
  │               │                │
  └───────────────┼────────────────┘
                  ▼
              RESPONSE
                  │
                  ▼
              VALIDATION
                  │
                  ▼
                 END
```

The planner currently uses simple routing signals to distinguish calculation requests, database-oriented questions, and general knowledge requests. The design intentionally keeps routing separate from the downstream execution nodes. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/agent/nodes.py

---

# 🔎 Hybrid RAG

The retrieval stack is organized into separate **ingestion, indexing, retrieval, and reranking** layers.

```text
                 DOCUMENTS / KNOWLEDGE
                           │
                           ▼
                  ┌──────────────────┐
                  │    Ingestion     │
                  │ Load → Clean →   │
                  │ Metadata → Split │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │     Indexing     │
                  │ Embeddings +     │
                  │ Vector Store     │
                  └────────┬─────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │ BM25 Search  │          │ Dense Search │
       │ Lexical      │          │ Vector       │
       └──────┬───────┘          └──────┬───────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                   ┌───────────────┐
                   │ Hybrid Fusion │
                   └───────┬───────┘
                           ▼
                   ┌───────────────┐
                   │ Cross-Encoder │
                   │   Reranker    │
                   └───────┬───────┘
                           ▼
                     Top Results
                           │
                           ▼
                    Response Engine
```

The repository contains distinct modules for document ingestion/cleaning/splitting, embedding/index construction, BM25 retrieval, dense retrieval, hybrid retrieval, and reranking. citehttps://api.github.com/repos/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/git/trees/da99b6bdeb4fdf58928dbcb29d95481dd2340bb0?recursive=1

### Why hybrid retrieval?

| Retrieval method | Strength |
|---|---|
| **BM25** | Exact terms, keywords, identifiers, names |
| **Dense vectors** | Semantic similarity and paraphrases |
| **Hybrid fusion** | Combines lexical + semantic recall |
| **Cross-encoder** | Re-ranks candidates for higher relevance |

---

# 📚 Ingestion & Indexing

The project separates ingestion and indexing into explicit modules:

```text
ingestion/
├── loader.py
├── cleaner.py
├── metadata.py
├── splitter.py
├── schemas.py
└── pipeline.py

indexing/
├── embeddings.py
├── indexer.py
└── vectorstore.py
```

This separation makes the pipeline easier to test, replace, and extend as document sources grow. citehttps://api.github.com/repos/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/git/trees/da99b6bdeb4fdf58928dbcb29d95481dd2340bb0?recursive=1

---

# 🖼️ Multimodal Intelligence

## Image Understanding

The image handler converts image bytes into a detailed grounded description and extracts visible text. It explicitly instructs the vision model to avoid inventing information that is not visible. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/multimodal/image_handler.py

```text
Image
  │
  ▼
Vision Model
  │
  ├── Visual description
  └── Visible text / OCR
          │
          ▼
      Text context
          │
          ▼
      Agent pipeline
```

---

## 🎙️ Audio Understanding

The audio handler supports both:

- **Speech-to-text transcription**
- **Text-to-speech synthesis**

The implementation uses the OpenAI audio APIs and returns normalized text to the rest of the application. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/multimodal/audio_handler.py

---

## 🎬 Video Understanding

Video is processed by combining two signals:

```text
Video
 ├── Sample frames ──► Vision analysis
 │
 └── Extract audio ──► Speech transcription
            │
            ▼
     Combined text context
            │
            ▼
       Same agent graph
```

The current implementation samples frames at a fixed interval and combines visual descriptions with the extracted transcript. It requires `ffmpeg` to be available on `PATH`. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/multimodal/video_handler.py

---

## 🗣️ Voice Interaction

The voice service provides a **push-to-talk, turn-based WebSocket loop**:

```text
Audio Clip
   │
   ▼
Speech-to-Text
   │
   ▼
LangGraph Agent
   │
   ▼
Text Answer + Confidence
   │
   ▼
Text-to-Speech
   │
   ▼
Audio Reply
```

The implementation intentionally uses complete utterance clips instead of continuous duplex streaming. The code documents true low-latency streaming as a future enhancement. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/multimodal/voice_realtime.py

---

# 🗄️ SQL Reasoning

Database-oriented questions are routed through the SQL tool path.

The current agent distinguishes SQL-oriented questions using terms such as:

```text
employee
salary
department
count
database
```

The SQL node then asks the configured LLM to generate SQL and only proceeds with the generated statement when it passes a basic `SELECT` check. Otherwise, the implementation falls back to a safe default query. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/agent/nodes.py

> **Production hardening note:** before exposing arbitrary natural-language SQL generation in a production environment, add stronger AST-based validation, parameterization, role-based permissions, query timeouts, table/column allow-lists, and resource limits.

---

# 🧮 Safe Calculator Path

Mathematical requests are routed separately from knowledge retrieval.

```text
User Expression
      │
      ▼
Calculator Tool
      │
      ▼
Validated Result
      │
      ▼
Response Engine
```

This isolates deterministic arithmetic from free-form language generation.

---

# 🔖 Citations, Confidence & Validation

The response stage is more than simple text generation.

It performs:

```text
Retrieved Evidence
       │
       ▼
Context Builder
       │
       ▼
Answer Generator
       │
       ├──────────────► Citation Builder
       │
       ├──────────────► Confidence Scorer
       │
       └──────────────► Validator
                              │
                              ▼
                       Final Response
```

The implementation builds the response context, generates the answer, creates citations from retrieved chunks, calculates confidence, validates the assembled response, and stores the validated output back into agent state. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/agent/nodes.py

---

# 🔌 API

The FastAPI router exposes the following interfaces:

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | `GET` | Health check |
| `/chat` | `POST` | Standard text chat |
| `/chat/image` | `POST` | Image + optional question |
| `/chat/audio` | `POST` | Audio + optional question |
| `/chat/video` | `POST` | Video + optional question |
| `/ws/voice` | `WebSocket` | Push-to-talk voice interaction |

These routes are implemented in `app/api/router.py`. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/api/router.py

### Example: text request

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the capital of France?"}'
```

### Example response shape

```json
{
  "answer": "...",
  "sources": [],
  "confidence": 0.0
}
```

The API service returns answer text together with sources and confidence for the standard agent response. Multimodal endpoints additionally include the modality and extracted text. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/api/router.py

---

# 📂 Project Structure

```text
Multimodal-AI-Agent-and-Hybrid-RAG/
│
├── app/
│   ├── agent/
│   │   ├── graph.py              # LangGraph topology
│   │   ├── nodes.py              # Planner, tools, response, validation
│   │   └── state.py              # Agent state model
│   │
│   ├── api/
│   │   ├── router.py             # REST + WebSocket endpoints
│   │   ├── schemas.py             # Request/response contracts
│   │   └── dependencies.py       # Dependency wiring
│   │
│   ├── core/
│   │   └── config.py             # Application configuration
│   │
│   ├── llm/
│   │   ├── base.py
│   │   ├── factory.py
│   │   └── openai_client.py
│   │
│   ├── multimodal/
│   │   ├── image_handler.py      # Vision + OCR-style extraction
│   │   ├── audio_handler.py      # STT + TTS
│   │   ├── video_handler.py      # Frame + audio processing
│   │   └── voice_realtime.py     # WebSocket voice loop
│   │
│   ├── planner/
│   │   ├── planner.py
│   │   └── schema.py
│   │
│   ├── prompts/
│   │   ├── planner.py
│   │   ├── knowledge.py
│   │   ├── sql.py
│   │   ├── response.py
│   │   └── system.py
│   │
│   ├── rag/
│   │   ├── indexing/
│   │   ├── ingestion/
│   │   └── retrieval/
│   │
│   ├── services/
│   │   └── ai_service.py         # Graph invocation facade
│   │
│   └── main.py                   # FastAPI application
│
├── frontend/
│   ├── index.html                # Chat UI
│   ├── style.css
│   └── script.js
│
├── .env.example
├── requirements.txt
├── LICENSE
└── README.md
```

The repository currently follows this modular organization in the `dbs` branch. citehttps://api.github.com/repos/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/git/trees/dbs?recursive=1

---

# 🚀 Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG.git
cd Multimodal-AI-Agent-and-Hybrid-RAG
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

The repository pins versions for major dependencies including FastAPI, LangChain, LangGraph, OpenAI, Qdrant, rank-bm25, sentence-transformers, SQLAlchemy, and supporting multimodal/document-processing libraries. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/requirements.txt

## 4. Configure environment variables

Copy the example file:

```bash
cp .env.example .env
```

Then populate the required API keys, database settings, model configuration, and other values used by the application.

> Keep secrets out of Git. Do not commit real API keys or production database credentials.

## 5. Install `ffmpeg`

Required for the video pipeline.

Verify:

```bash
ffmpeg -version
```

## 6. Start the FastAPI app

The application uses FastAPI/Uvicorn. A typical development command is:

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://localhost:8000
```

The frontend is mounted at `/` when the `frontend/` directory exists. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/main.py

---

# ⚙️ Configuration

The repository includes `.env.example` to document the expected configuration surface.

Typical configuration categories include:

```text
OpenAI / LLM settings
Embedding model settings
Vector database settings
Database / SQL settings
Upload limits
Application settings
```

Use the project's configuration module in `app/core/config.py` as the source of truth when adding or changing environment variables.

---

# 🧪 Example Use Cases

### 💬 Knowledge question

```text
Explain our employee benefits policy.
```

→ Planner → Knowledge → Hybrid RAG → Reranking → Response

### 🗄️ SQL question

```text
How many employees are in the Engineering department?
```

→ Planner → SQL → Database → Response

### 🧮 Calculation

```text
Calculate 18% of 2450.
```

→ Planner → Calculator → Response

### 🖼️ Image analysis

Upload an image and ask:

```text
Summarize the information in this chart.
```

→ Image handler → Extracted context → Same agent graph

### 🎬 Video analysis

Upload a video and ask:

```text
What are the main points discussed in this video?
```

→ Frame analysis + transcription → Combined context → Same agent graph

### 🎙️ Voice

Send an utterance through `/ws/voice` and receive:

```text
Transcript + answer + confidence + synthesized speech
```

---

# 🛡️ Reliability & Safety Considerations

The architecture already contains several useful controls:

- Structured agent state
- Separate execution paths for knowledge, SQL, and calculation
- Upload size enforcement
- Empty-input validation
- Final response validation
- Source and confidence fields
- Explicit multimodal preprocessing
- Separation between application layers

The API also returns appropriate error responses for invalid uploads, oversized files, malformed input, and unavailable video processing dependencies. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/api/router.py

### Recommended production hardening

For production use, consider adding:

- Strict CORS origins instead of wildcard access
- Stronger SQL AST validation and allow-lists
- Authentication and authorization
- Rate limiting
- Request tracing and structured logging
- Persistent conversation/checkpoint storage
- Retrieval evaluation datasets
- Prompt-injection defenses
- PII redaction
- Model and retrieval observability
- Background processing for large files

The current FastAPI configuration allows all CORS origins, so this should be restricted before a public deployment. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/main.py

---

# 📦 Technology Stack

| Layer | Technology |
|---|---|
| API | FastAPI, Uvicorn |
| Agent orchestration | LangGraph |
| LLM | OpenAI API |
| Retrieval | BM25 + dense vectors + hybrid fusion |
| Reranking | Cross-encoder / sentence-transformers |
| Vector database | Qdrant |
| Database access | SQLAlchemy |
| Validation | Pydantic |
| Audio | OpenAI speech APIs |
| Image | OpenAI vision-capable model |
| Video | FFmpeg + image/audio handlers |
| Frontend | HTML / CSS / JavaScript |
| Document processing | PyMuPDF, pypdf, python-docx, unstructured |
| NLP / ML utilities | scikit-learn, spaCy, transformers |

These dependencies are reflected in the repository's pinned `requirements.txt`. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/requirements.txt

---

# 📈 Engineering Highlights

### Modular architecture

Each major responsibility has its own package, reducing coupling and making components easier to replace.

### Multimodal normalization

Different media types are converted into textual context before the core agent executes, allowing a common reasoning path.

### Retrieval specialization

Lexical and semantic retrieval are handled separately before hybrid fusion and reranking.

### Response governance

The system carries source and confidence metadata and validates the generated response before returning it.

### API-first design

The same agent graph can be used through text and multimodal routes without duplicating reasoning logic. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/api/router.pyhttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/services/ai_service.py

---

# 🗺️ Roadmap

```text
✅ Multimodal API layer
✅ LangGraph planner + routing
✅ Hybrid BM25 + dense retrieval
✅ Reranking layer
✅ SQL + calculator paths
✅ Citations + confidence + validation
✅ Image / audio / video handling
✅ Push-to-talk voice

🔲 Streaming multimodal responses
🔲 Persistent agent memory
🔲 Advanced SQL AST guardrails
🔲 Retrieval evaluation suite
🔲 Observability dashboard
🔲 Authentication / RBAC
🔲 Production deployment profile
```

---

# 👨‍💻 Developer Notes

The codebase intentionally keeps the main orchestration surface compact:

```text
API
 ↓
AIService
 ↓
Compiled LangGraph
 ↓
Planner / Tool Nodes
 ↓
Response + Validation
```

`AIService.chat()` invokes the compiled graph and returns the normalized `answer`, `sources`, and `confidence` fields expected by the API layer. citehttps://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG/blob/dbs/app/services/ai_service.py

---

# 📚 Useful Repository References

- [Agent Graph](./app/agent/graph.py)
- [Agent Nodes](./app/agent/nodes.py)
- [Agent State](./app/agent/state.py)
- [API Router](./app/api/router.py)
- [AI Service](./app/services/ai_service.py)
- [Image Handler](./app/multimodal/image_handler.py)
- [Audio Handler](./app/multimodal/audio_handler.py)
- [Video Handler](./app/multimodal/video_handler.py)
- [Voice WebSocket](./app/multimodal/voice_realtime.py)
- [Requirements](./requirements.txt)
- [Environment Template](./.env.example)

---

# 📄 License

This project is distributed under the license included in the repository.

See [LICENSE](./LICENSE) for the full license text.

---

<div align="center">

### ⭐ Build AI systems that can retrieve, reason, calculate, and understand more than text.

<br>

<a href="https://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG">
<img src="https://img.shields.io/badge/⭐%20Star%20Repository-181717?style=for-the-badge&logo=github&logoColor=white" alt="Star repository" />
</a>

<br><br>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=3200&pause=1200&center=true&vCenter=true&width=760&lines=Multimodal+AI;Hybrid+RAG;Agentic+Routing;Grounded+Responses" alt="Footer animation" />

<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4F46E5,50:7C3AED,100:06B6D4&height=130&section=footer&animation=fadeIn" width="100%" alt="Animated footer" />

</div>
