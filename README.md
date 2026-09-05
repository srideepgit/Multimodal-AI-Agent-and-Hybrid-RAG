<div align="center">

# 🤖 Multimodal AI Agent & Hybrid RAG

### Enterprise-Ready Multimodal AI • Agentic Routing • Hybrid Retrieval • Grounded Responses

<br>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2600&pause=900&center=true&vCenter=true&width=900&lines=Text+%7C+Image+%7C+Audio+%7C+Video+%7C+Voice;LangGraph+Agentic+Workflow;BM25+%2B+Dense+Vector+Search;Cross-Encoder+Reranking;SQL+%2B+Calculator+Tools;Citations+%2B+Confidence+%2B+Validation" alt="Typing animation" />

<br><br>

<img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/FastAPI-0F766E?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/LangGraph-Agentic%20Workflow-111827?style=for-the-badge" alt="LangGraph" />
<img src="https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" />
<img src="https://img.shields.io/badge/Qdrant-Vector%20Search-DC244C?style=for-the-badge" alt="Qdrant" />
<img src="https://img.shields.io/badge/BM25-Lexical%20Retrieval-6B7280?style=for-the-badge" alt="BM25" />
<img src="https://img.shields.io/badge/Cross--Encoder-Reranking-2563EB?style=for-the-badge" alt="Cross Encoder" />
<img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
<img src="https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic" />

<br><br>

<a href="#-quick-start"><img src="https://img.shields.io/badge/🚀%20Quick%20Start-111827?style=for-the-badge" alt="Quick Start" /></a>
<a href="#-architecture"><img src="https://img.shields.io/badge/🏗️%20Architecture-1F2937?style=for-the-badge" alt="Architecture" /></a>
<a href="#-api"><img src="https://img.shields.io/badge/🔌%20API-4F46E5?style=for-the-badge" alt="API" /></a>
<a href="#-hybrid-rag"><img src="https://img.shields.io/badge/🔎%20Hybrid%20RAG-7C3AED?style=for-the-badge" alt="Hybrid RAG" /></a>

<br><br>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&height=90&section=header&text=One%20Agent.%20Multiple%20Reasoning%20Paths.&fontSize=28&fontAlignY=55&animation=fadeIn" width="100%" alt="Animated project banner" />

</div>

---

## 📌 Overview

**Multimodal AI Agent & Hybrid RAG** is a modular AI backend built with **FastAPI, LangGraph, OpenAI, Qdrant, SQLAlchemy, and hybrid retrieval**.

The system accepts **text, images, audio, video, and push-to-talk voice**, then routes each request to the reasoning path that best fits the task:

```text
User Input
    │
    ▼
Multimodal Normalization
    │
    ▼
LangGraph Planner
    │
    ├──────────────► Knowledge → Hybrid RAG
    │
    ├──────────────► SQL       → Database Query
    │
    └──────────────► Math      → Calculator
                              │
                              ▼
                       Response Engine
                              │
                  ┌───────────┼───────────┐
                  ▼           ▼           ▼
              Citations   Confidence   Validation
                  │           │           │
                  └───────────┼───────────┘
                              ▼
                       Final Response
```

The architecture keeps multimodal preprocessing, planning, retrieval, database access, calculation, and response generation as separate modules so individual components can be replaced or extended without rewriting the entire application.

---

# ✨ Features

## 🌐 Multimodal Input

| Modality | Capability |
|---|---|
| 💬 **Text** | Natural-language questions and conversations |
| 🖼️ **Image** | Vision analysis and visible-text extraction |
| 🎙️ **Audio** | Speech-to-text and text-to-speech |
| 🎬 **Video** | Sampled-frame vision analysis + audio transcription |
| 🗣️ **Voice** | Push-to-talk WebSocket voice workflow |

Every non-text modality is normalized into textual context before entering the shared LangGraph pipeline. This keeps the core agent **modality-agnostic**.

## 🧠 Agentic AI

- LangGraph-based workflow orchestration
- Planner-driven routing
- Explicit execution nodes
- Shared state management
- Modular prompts and tools
- Separate reasoning paths for knowledge, SQL, and calculations

## 🔎 Hybrid RAG

- Dense vector retrieval
- BM25 lexical retrieval
- Hybrid candidate merging
- Cross-encoder reranking
- Metadata-aware retrieval
- Source-aware answers
- Confidence scoring

## 🗄️ SQL Reasoning

- Natural-language-to-SQL workflow
- SQLAlchemy database integration
- Read-only database path
- Schema-aware prompting
- Query validation
- Structured database results

## 🧮 Calculator

- Dedicated mathematical execution path
- Deterministic calculation for supported expressions
- Separate from LLM response generation

## 🛡️ Response Quality

- Context construction
- Citation generation
- Retrieval-based confidence signal
- Final response validation
- Grounded-response prompting

---

# 🏗️ Architecture

```text
                                  ┌──────────────────────┐
                                  │        USER          │
                                  │ Text / Image / Audio │
                                  │ Video / Voice        │
                                  └──────────┬───────────┘
                                             │
                                             ▼
                              ┌───────────────────────────┐
                              │        FASTAPI API        │
                              │                           │
                              │ /chat                    │
                              │ /chat/image              │
                              │ /chat/audio              │
                              │ /chat/video              │
                              │ /ws/voice                │
                              └─────────────┬─────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │      MULTIMODAL PROCESSING       │
                         │                                  │
                         │ Image → vision + OCR             │
                         │ Audio → transcription            │
                         │ Video → frames + transcript      │
                         │ Voice → STT / agent / TTS        │
                         └────────────────┬─────────────────┘
                                          │
                                          ▼
                                ┌──────────────────┐
                                │    LANGGRAPH     │
                                │      AGENT       │
                                └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │     PLANNER      │
                                └────────┬─────────┘
                                         │
                  ┌──────────────────────┼──────────────────────┐
                  ▼                      ▼                      ▼
           ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
           │  KNOWLEDGE  │       │     SQL     │       │ CALCULATOR  │
           └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
                  │                     │                     │
                  ▼                     ▼                     ▼
             Hybrid RAG           Read-only DB        Controlled Math
                  │                     │                     │
                  └─────────────────────┼─────────────────────┘
                                        ▼
                              ┌───────────────────┐
                              │  RESPONSE ENGINE  │
                              │                   │
                              │ Context Builder   │
                              │ LLM Generation    │
                              │ Citations         │
                              │ Confidence        │
                              │ Validation        │
                              └─────────┬─────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ FINAL RESPONSE  │
                               └─────────────────┘
```

---

# 🔄 End-to-End Workflow

```text
Request
  │
  ▼
API Validation
  │
  ▼
Multimodal Preprocessing
  │
  ▼
Planner
  │
  ├───────────────┬────────────────┐
  ▼               ▼                ▼
Knowledge         SQL          Calculator
  │               │                │
  ▼               ▼                ▼
Hybrid RAG      SQLAlchemy      Calculation
  │               │                │
  └───────────────┴────────────────┘
                  │
                  ▼
             Response Node
                  │
                  ▼
             Validation
                  │
                  ▼
                JSON
```

---

# 🧠 LangGraph Workflow

The agent uses an explicit directed graph rather than placing all logic inside one large prompt.

```text
START
  │
  ▼
Planner
  │
  ├────────► Knowledge Node
  │               │
  │               ▼
  │          Hybrid Retrieval
  │
  ├────────► SQL Node
  │               │
  │               ▼
  │          Database Query
  │
  └────────► Calculator Node
                  │
                  ▼
             Math Result
                  │
                  └─────────────┐
                                ▼
                           Response Node
                                │
                                ▼
                         Validation Node
                                │
                                ▼
                               END
```

### Node responsibilities

| Node | Responsibility |
|---|---|
| **Planner** | Determines the appropriate execution path |
| **Knowledge** | Retrieves relevant enterprise context |
| **SQL** | Handles database-oriented questions |
| **Calculator** | Performs supported mathematical operations |
| **Response** | Builds context and generates the answer |
| **Validation** | Performs final response checks |

---

# 🔎 Hybrid RAG

The knowledge path combines lexical and semantic retrieval before reranking the candidate results.

```text
                     USER QUESTION
                           │
                           ▼
                   Query Embedding
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │ Dense Search │          │ BM25 Search  │
       │   Qdrant    │          │   Lexical    │
       └──────┬───────┘          └──────┬───────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                    Hybrid Retrieval
                           │
                           ▼
                  Candidate Documents
                           │
                           ▼
                 Cross-Encoder Reranker
                           │
                           ▼
                       Top-K Chunks
                           │
                           ▼
                    Context Builder
                           │
                           ▼
                     LLM Response
```

### Retrieval layers

| Layer | Purpose |
|---|---|
| **BM25** | Exact terms, keywords, identifiers and lexical matching |
| **Dense Retrieval** | Semantic similarity through embeddings |
| **Hybrid Retrieval** | Combines lexical and semantic candidates |
| **Cross-Encoder** | Re-ranks candidates based on query-document relevance |
| **Qdrant** | Vector storage and similarity search |

This architecture combines semantic search with exact keyword matching, making the retrieval layer more robust across different query styles.

---

# 📚 Ingestion & Indexing

```text
Documents
    │
    ▼
Document Loader
    │
    ▼
Text Cleaning
    │
    ▼
Metadata Extraction
    │
    ▼
Chunk Splitting
    │
    ▼
Embedding Generation
    │
    ▼
Qdrant Index
    │
    └──────────────► BM25 Corpus
```

The repository separates ingestion and indexing into dedicated modules, keeping document preparation independent from agent orchestration.

### Ingestion responsibilities

- Load documents
- Clean and normalize content
- Attach metadata
- Split content into retrieval chunks
- Prepare chunks for embedding

### Indexing responsibilities

- Generate embeddings
- Build vector representations
- Store vectors in Qdrant
- Maintain lexical-search data for BM25

---

# 🖼️ Multimodal Processing

## Image Understanding

```text
Image Upload
     │
     ▼
Vision Model
     │
     ├──── Visual Description
     └──── Visible Text
                │
                ▼
          Text Context
                │
                ▼
          LangGraph Agent
```

The image handler converts visual information into textual context so the downstream planner and tools can operate on a consistent representation.

## 🎙️ Audio

```text
Audio
  │
  ▼
Speech-to-Text
  │
  ▼
LangGraph Agent
  │
  ▼
Answer
  │
  ▼
Text-to-Speech
```

The audio layer supports transcription and speech synthesis through the configured OpenAI models.

## 🎬 Video

```text
                         VIDEO
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       Sample Video Frames       Extract Audio Track
              │                         │
              ▼                         ▼
       Vision Analysis           Speech-to-Text
              │                         │
              └────────────┬────────────┘
                           ▼
                  Combined Text Context
                           │
                           ▼
                     Agent Workflow
```

Video processing uses FFmpeg for frame/audio extraction and combines visual and spoken information before passing the context into the agent.

## 🗣️ Push-to-Talk Voice

```text
Recorded Utterance
       │
       ▼
     STT
       │
       ▼
   LangGraph
       │
       ▼
    Answer
       │
       ▼
     TTS
       │
       ▼
   Audio Reply
```

The current implementation is **turn-based push-to-talk**, rather than token-level continuous voice streaming.

---

# 🗄️ SQL Reasoning

Database questions are routed to a dedicated SQL execution path.

```text
Natural Language Question
          │
          ▼
       Planner
          │
          ▼
       SQL Node
          │
          ▼
Schema-aware SQL Generation
          │
          ▼
    Query Validation
          │
          ▼
 SQLAlchemy / Database
          │
          ▼
     Query Results
          │
          ▼
    Response Engine
```

The current configuration describes an `employees` table with fields including `id`, `name`, `department`, `salary`, and `hire_date`.

### Production controls

For production workloads, the SQL path should use:

- Least-privilege database credentials
- Read-only database permissions
- Query timeouts
- Result-size limits
- Strong SQL validation
- Query auditing/logging

---

# 🧮 Calculator

Mathematical requests use a dedicated execution path rather than relying entirely on language-model arithmetic.

```text
Question
   │
   ▼
Planner
   │
   ▼
Calculator
   │
   ▼
Controlled Evaluation
   │
   ▼
Numeric Result
   │
   ▼
Response
```

This separation makes numerical operations easier to reason about and test independently.

---

# 🛡️ Grounded Responses & Validation

The response layer separates evidence gathering, generation, citations, confidence, and validation.

```text
Retrieved / Tool Context
          │
          ▼
    Context Builder
          │
          ▼
    LLM Generation
          │
          ▼
   Citation Builder
          │
          ▼
 Confidence Scoring
          │
          ▼
 Response Validation
          │
          ▼
    Final Response
```

### Response goals

- Use available evidence
- Preserve source information
- Expose a confidence signal
- Validate the response structure
- Reduce unsupported answers in knowledge workflows

---

# ⚡ Performance & Engineering

The project separates expensive resources and shared services from request routing.

### Centralized configuration

Environment-driven settings are centralized in `app/core/config.py`, including:

- LLM provider and model
- Embedding and reranker models
- Qdrant connection
- Database connection
- Chunk size and overlap
- Retrieval top-k values
- Vision/STT/TTS models
- Video sampling limits
- Upload size limits

The settings accessor uses `lru_cache()` so configuration is parsed once per process.

### Dependency management

The API uses a dedicated dependency layer for service construction. This keeps route handlers focused on HTTP concerns and makes components easier to replace and test.

### Retrieval efficiency

The retrieval layer separates candidate retrieval from reranking, allowing the more expensive cross-encoder stage to process a smaller candidate pool rather than the entire corpus.

---

# 🔐 Security

The architecture includes several safety boundaries that should be retained and strengthened for production use.

### SQL

Use read-only credentials and validate generated queries before execution.

### Calculator

Keep calculation logic isolated from arbitrary Python execution. Never expose `eval()` or `exec()` to user-controlled input.

### File Uploads

The application has a configurable upload-size limit:

```env
MAX_UPLOAD_SIZE_MB=25
```

Video processing additionally requires FFmpeg.

### Secrets

Store API keys in environment variables or a proper secret manager.

> Never commit `.env` or real API keys to GitHub.

---

# 🔌 API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/chat` | Text chat |
| `POST` | `/chat/image` | Image understanding + question |
| `POST` | `/chat/audio` | Audio transcription + question |
| `POST` | `/chat/video` | Video frame + audio analysis |
| `WS` | `/ws/voice` | Push-to-talk voice |

## Text Chat

```http
POST /chat
Content-Type: application/json
```

```json
{
  "question": "What is the employee leave policy?"
}
```

### Response shape

```json
{
  "answer": "...",
  "sources": [],
  "confidence": 0.0
}
```

## Multimodal Uploads

The image, audio, and video endpoints accept multipart form data.

| Field | Required | Description |
|---|:---:|---|
| `file` | Yes | Image, audio, or video file |
| `question` | No | Optional question about the uploaded content |

Example:

```bash
curl -X POST "http://localhost:8000/chat/image" \
  -F "file=@invoice.png" \
  -F "question=What is the total amount?"
```

## Voice WebSocket

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/voice");
ws.binaryType = "arraybuffer";

ws.onmessage = (event) => {
  if (typeof event.data === "string") {
    console.log(JSON.parse(event.data));
  } else {
    // Handle synthesized audio bytes.
  }
};
```

The current voice implementation uses one complete recorded utterance per turn.

---

# ⚙️ Configuration

Create `.env` from `.env.example`.

```env
# LLM
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4o-mini

# Embeddings / Reranker
EMBEDDING_MODEL=BAAI/bge-m3
RERANKER_MODEL=BAAI/bge-reranker-base

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=enterprise_knowledge

# SQL
DATABASE_URL=sqlite:///./enterprise.db

# Ingestion
CHUNK_SIZE=500
CHUNK_OVERLAP=100

# Retrieval
RETRIEVAL_TOP_K=5
RETRIEVAL_CANDIDATE_K=20

# Multimodal
VISION_MODEL=gpt-4o-mini
STT_MODEL=whisper-1
TTS_MODEL=tts-1
TTS_VOICE=alloy
VIDEO_FRAME_INTERVAL_SECONDS=5
VIDEO_MAX_FRAMES=6
FFMPEG_PATH=ffmpeg
MAX_UPLOAD_SIZE_MB=25
```

---

# 🚀 Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG.git
cd Multimodal-AI-Agent-and-Hybrid-RAG
```

## 2. Create a virtual environment

### Windows

```powershell
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

## 4. Configure environment variables

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Add your real `OPENAI_API_KEY` and verify the database and Qdrant configuration.

## 5. Start Qdrant

Run Qdrant using your preferred local or hosted setup and make sure `QDRANT_URL` points to it.

## 6. Prepare the knowledge base

Run the repository's document indexing workflow to ingest the documents you want available to the knowledge path.

## 7. Run FastAPI

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# 📚 Document Indexing

A typical indexing lifecycle is:

```text
Documents
   ↓
Load
   ↓
Clean
   ↓
Metadata
   ↓
Chunk
   ↓
Embed
   ↓
Qdrant
   ↓
BM25 Snapshot
```

Before indexing a new corpus, verify the embedding model and vector-store configuration in `.env`.

---

# 🌐 Frontend

The project includes a lightweight browser interface under:

```text
frontend/
├── index.html
├── style.css
└── script.js
```

The UI supports:

- Text chat
- New conversations
- File attachments
- Image/audio/video input
- API configuration
- Suggested prompts
- Voice interaction

FastAPI serves the frontend when the frontend directory is available.

---

# 📁 Project Structure

```text
Multimodal-AI-Agent-and-Hybrid-RAG/
│
├── app/
│   ├── agent/
│   │   ├── graph.py              # LangGraph definition
│   │   ├── nodes.py              # Planner/tools/response nodes
│   │   └── state.py              # Shared graph state
│   │
│   ├── api/
│   │   ├── dependencies.py       # Dependency injection
│   │   ├── router.py             # REST + WebSocket routes
│   │   └── schemas.py            # API schemas
│   │
│   ├── core/
│   │   └── config.py             # Centralized configuration
│   │
│   ├── llm/
│   │   ├── base.py
│   │   ├── factory.py
│   │   └── openai_client.py
│   │
│   ├── multimodal/
│   │   ├── image_handler.py      # Vision + text extraction
│   │   ├── audio_handler.py      # STT + TTS
│   │   ├── video_handler.py      # FFmpeg + frame/audio processing
│   │   └── voice_realtime.py     # Push-to-talk WebSocket
│   │
│   ├── planner/
│   │   ├── planner.py
│   │   └── schema.py
│   │
│   ├── prompts/
│   │   ├── knowledge.py
│   │   ├── planner.py
│   │   ├── sql.py
│   │   └── ...
│   │
│   ├── rag/
│   │   ├── ingestion/
│   │   ├── indexing/
│   │   └── retrieval/
│   │
│   ├── response/
│   ├── services/
│   ├── tools/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── scripts/
├── tests/
├── .env.example
├── requirements.txt
├── LICENSE
└── README.md
```

---

# 🧪 Testing

Run the test suite with:

```bash
pytest
```

For a focused test module:

```bash
pytest tests/agent
```

For coverage:

```bash
pytest --cov=app
```

Recommended test areas include:

- Planner routing
- Retrieval behaviour
- SQL safety
- Calculator behaviour
- Multimodal handlers
- Response validation
- API contracts

---

# 🧩 Design Decisions

## LangGraph

Used for explicit workflow orchestration, state management, and conditional routing between reasoning paths.

## Hybrid Retrieval

Combines BM25 lexical matching with dense vector retrieval so the system can handle both exact terminology and semantic queries.

## Cross-Encoder Reranking

Reranking is performed after candidate retrieval, allowing a more expensive relevance model to focus on a smaller candidate set.

## Modular Multimodal Layer

Image, audio, video, and voice processing are isolated from the core agent so new modalities can be added without redesigning the LangGraph workflow.

## Centralized Configuration

Model, retrieval, database, Qdrant, and multimodal settings are centralized instead of being scattered across route handlers and services.

## Dedicated Response Layer

Context construction, generation, citations, confidence, and validation are kept separate so response quality can be improved independently.

---

# 📈 Engineering Strengths

```text
                 ┌─────────────────────────────┐
                 │     MODULAR ARCHITECTURE    │
                 └──────────────┬──────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
    Agentic Routing        Hybrid RAG           Multimodal
          │                     │                     │
          ▼                     ▼                     ▼
      LangGraph          BM25 + Dense       Image / Audio /
      State Graph         + Reranking       Video / Voice
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                ▼
                     Grounded Response Layer
                                │
                  ┌─────────────┼─────────────┐
                  ▼             ▼             ▼
              Citations    Confidence     Validation
```

### Core principles

- **Separation of concerns** — each subsystem has a focused responsibility.
- **Replaceability** — LLM, embedding, reranker, vector store, and database layers are configuration-driven.
- **Evidence-first answering** — knowledge requests use retrieval before response generation.
- **Explicit routing** — the planner determines the execution path.
- **Validation** — responses pass through a dedicated validation stage.
- **Operational boundaries** — multimodal uploads, SQL execution, and external model calls have separate control points.

---

# 📊 Capability Matrix

| Capability | Status |
|---|:---:|
| FastAPI backend | ✅ |
| LangGraph workflow | ✅ |
| Planner-based routing | ✅ |
| Hybrid RAG | ✅ |
| BM25 retrieval | ✅ |
| Dense vector retrieval | ✅ |
| Cross-encoder reranking | ✅ |
| Qdrant integration | ✅ |
| SQL reasoning | ✅ |
| Calculator path | ✅ |
| Image processing | ✅ |
| Audio processing | ✅ |
| Video processing | ✅ |
| Push-to-talk voice | ✅ |
| Citations | ✅ |
| Confidence scoring | ✅ |
| Response validation | ✅ |
| Browser frontend | ✅ |
| Continuous realtime voice | 🔜 |
| Advanced multi-agent orchestration | 🔜 |

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.12+ |
| **API** | FastAPI |
| **Agent Orchestration** | LangGraph |
| **LLM** | OpenAI API |
| **Embeddings** | BAAI/bge-m3 |
| **Vector Database** | Qdrant |
| **Lexical Retrieval** | BM25 |
| **Reranking** | BAAI/bge-reranker-base |
| **Database / ORM** | SQLAlchemy |
| **Validation / Settings** | Pydantic / Pydantic Settings |
| **Speech-to-Text** | Whisper |
| **Text-to-Speech** | OpenAI TTS |
| **Video Processing** | FFmpeg |
| **Testing** | Pytest |
| **Frontend** | HTML / CSS / JavaScript |

---

# 📌 Example Use Cases

### 🏢 Enterprise Knowledge Assistant

Ask questions over indexed internal documentation and business knowledge.

### 📄 Document & Image Analysis

Upload an image and ask questions about visible information.

### 🎙️ Voice Assistant

Use push-to-talk voice input and receive synthesized responses.

### 🗄️ Business Data Assistant

Ask natural-language questions over structured SQL data.

### 📊 Analytical Assistant

Combine retrieved business context with deterministic calculations.

---

# 🔮 Roadmap

Planned extensions include:

- True token-level realtime voice streaming
- Interruptible voice conversations
- Multimodal document ingestion
- Image/diagram-aware RAG
- Multi-turn conversation memory
- Streaming agent responses
- Authentication and authorization
- Role-based document access
- More advanced planner routing
- Async retrieval pipelines
- Redis caching
- OpenTelemetry tracing
- Prometheus/Grafana monitoring
- Multi-LLM provider support
- Automated RAG evaluation
- Continuous document indexing
- Agent analytics dashboard

These are roadmap items rather than claims about the current implementation.

---

# ⚠️ Production Considerations

Before exposing the system to sensitive production workloads, consider adding:

- Authentication and authorization
- Role-based document access
- Secret management
- Rate limiting
- Structured logging
- Request tracing
- Retrieval and answer evaluation
- Prompt-injection defenses
- File-type validation and malware scanning
- Resource and concurrency limits
- Persistent conversation storage
- Stronger SQL controls

---

# 🤝 Contributing

Contributions and improvements are welcome.

```text
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Run the test suite
6. Open a Pull Request
```

Please keep new components modular and update the documentation when introducing new agent nodes, tools, retrieval strategies, or API endpoints.

---

# 📄 License

This project is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

# ⭐ Support the Project

If you find the project useful, consider giving the repository a ⭐ **Star** and sharing it with others working on GenAI, RAG, LangGraph, and multimodal AI systems.

<div align="center">

<br>

<a href="https://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG">
<img src="https://img.shields.io/badge/⭐%20Star%20Repository-181717?style=for-the-badge&logo=github&logoColor=white" alt="Star Repository" />
</a>

<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0078D4,50:7C3AED,100:14B8A6&height=150&section=footer&text=Multimodal%20AI%20%2B%20Hybrid%20RAG&fontSize=25&fontColor=ffffff&animation=fadeIn" width="100%" alt="Animated footer" />

</div>
