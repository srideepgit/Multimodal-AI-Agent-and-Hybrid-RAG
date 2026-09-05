<div align="center">

# 🤖 Multimodal AI Agent & Hybrid RAG

### Multimodal AI • LangGraph Agents • Hybrid Retrieval • Grounded Responses

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2600&pause=900&center=true&vCenter=true&width=900&lines=Text+%7C+Image+%7C+Audio+%7C+Video+%7C+Voice;LangGraph+Agentic+Workflow;BM25+%2B+Dense+Vector+Search;Cross-Encoder+Reranking;SQL+%2B+Calculator+Tools;Citations+%2B+Confidence+%2B+Validation" alt="Typing animation" />

<br><br>

<img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/FastAPI-0F766E?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/LangGraph-Agentic%20Workflow-111827?style=for-the-badge" alt="LangGraph" />
<img src="https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" />
<img src="https://img.shields.io/badge/Qdrant-Vector%20Search-DC244C?style=for-the-badge" alt="Qdrant" />
<img src="https://img.shields.io/badge/BM25-Lexical%20Retrieval-6B7280?style=for-the-badge" alt="BM25" />
<img src="https://img.shields.io/badge/Cross--Encoder-Reranking-2563EB?style=for-the-badge" alt="Cross Encoder" />

<br><br>

<a href="#-quick-start"><img src="https://img.shields.io/badge/🚀%20Quick%20Start-111827?style=for-the-badge" alt="Quick Start" /></a>
<a href="#-architecture"><img src="https://img.shields.io/badge/🏗️%20Architecture-1F2937?style=for-the-badge" alt="Architecture" /></a>
<a href="#-api"><img src="https://img.shields.io/badge/🔌%20API-4F46E5?style=for-the-badge" alt="API" /></a>
<a href="#-hybrid-rag"><img src="https://img.shields.io/badge/🔎%20Hybrid%20RAG-7C3AED?style=for-the-badge" alt="Hybrid RAG" /></a>

<br><br>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&height=90&section=header&text=One%20Agent.%20Multiple%20Reasoning%20Paths.&fontSize=28&fontAlignY=55&animation=fadeIn" width="100%" alt="Animated project banner" />

</div>

---

## ✨ Overview

**Multimodal AI Agent & Hybrid RAG** is a modular AI application that combines **agentic orchestration, multimodal understanding, hybrid retrieval, SQL reasoning, deterministic calculation, source-aware responses, confidence scoring, and response validation** behind a FastAPI service.

The core idea is:

> **Understand the input → choose the reasoning path → gather evidence → generate → validate.**

The project supports text, image, audio, video, and push-to-talk voice interactions while keeping the downstream agent workflow consistent.

---

## 🌟 What It Can Do

| Capability | Description |
|---|---|
| 💬 Text Chat | Natural-language interaction through the agent |
| 🖼️ Image | Vision analysis + visible text extraction |
| 🎙️ Audio | Speech-to-text + text-to-speech |
| 🎬 Video | Sampled-frame analysis + audio transcription |
| 🗣️ Voice | Push-to-talk WebSocket speech workflow |
| 🧠 Agentic Routing | Routes requests to the appropriate tool |
| 🔎 Hybrid RAG | BM25 + dense vector retrieval |
| 🎯 Reranking | Cross-encoder candidate reranking |
| 🗄️ SQL | Read-only database question answering |
| 🧮 Calculator | Controlled mathematical evaluation |
| 🔖 Citations | Source-aware knowledge responses |
| 📊 Confidence | Retrieval-based confidence signal |
| ✅ Validation | Final response validation |
| 🌐 Frontend | Browser-based chat interface |

---

# 🏗️ Architecture

```text
                              ┌──────────────────────┐
                              │        USER          │
                              │ Text / Image / Audio │
                              │ Video / Voice       │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │      FASTAPI API     │
                              │                      │
                              │ /chat                │
                              │ /chat/image          │
                              │ /chat/audio          │
                              │ /chat/video          │
                              │ /ws/voice            │
                              └──────────┬───────────┘
                                         │
                                         ▼
                         ┌──────────────────────────────┐
                         │    MULTIMODAL PROCESSING     │
                         │ Image → text                 │
                         │ Audio → transcript           │
                         │ Video → frames + transcript  │
                         │ Voice → transcript           │
                         └──────────────┬───────────────┘
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
                   ┌───────────────────┼───────────────────┐
                   ▼                   ▼                   ▼
             ┌────────────┐      ┌────────────┐      ┌────────────┐
             │ KNOWLEDGE  │      │    SQL     │      │ CALCULATOR │
             └─────┬──────┘      └─────┬──────┘      └─────┬──────┘
                   │                   │                   │
                   ▼                   ▼                   ▼
              Hybrid RAG        Read-only DB        Safe Evaluation
                   │                   │                   │
                   └───────────────────┼───────────────────┘
                                       ▼
                              ┌───────────────────┐
                              │  RESPONSE ENGINE  │
                              │ Context + LLM     │
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

# 🧠 Agentic Workflow

The LangGraph execution path is intentionally simple and explicit:

```text
START
  │
  ▼
PLANNER
  │
  ├──────────────► KNOWLEDGE ──────► Hybrid RAG
  │
  ├──────────────► SQL ────────────► Database Tool
  │
  └──────────────► CALCULATOR ─────► Safe Evaluation
                                      │
                                      ▼
                                  RESPONSE
                                      │
                                      ▼
                                  VALIDATION
                                      │
                                      ▼
                                     END
```

### Routing

- Calculation-related requests → **Calculator**
- Database-oriented requests → **SQL**
- Other knowledge requests → **Knowledge / RAG**

The planner is separated from tool execution, making the workflow easier to extend with additional tools or routing strategies.

---

# 🔎 Hybrid RAG

The retrieval system combines lexical and semantic search before reranking the candidates.

```text
                 DOCUMENTS / KNOWLEDGE
                           │
                           ▼
                    ┌─────────────┐
                    │  INGESTION  │
                    │ Load/Clean  │
                    │ Metadata    │
                    │ Chunking    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  INDEXING   │
                    │ Embeddings  │
                    │ Vector Store│
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │ BM25 Search  │          │ Dense Search │
       │   Lexical    │          │   Semantic   │
       └──────┬───────┘          └──────┬───────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                    ┌─────────────┐
                    │    HYBRID   │
                    │   RETRIEVAL │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │ CROSS-ENCODER│
                    │   RERANKER  │
                    └──────┬──────┘
                           ▼
                       TOP RESULTS
                           │
                           ▼
                    RESPONSE ENGINE
```

### Retrieval components

| Component | Role |
|---|---|
| **BM25** | Exact keyword and lexical matching |
| **Dense Retrieval** | Semantic similarity using embeddings |
| **Hybrid Retrieval** | Combines lexical + semantic candidates |
| **Cross-Encoder** | Refines candidate relevance |
| **Qdrant** | Vector search / storage layer |

---

# 📚 Ingestion & Indexing

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

The separation between ingestion and indexing keeps document processing independent from the agent orchestration layer.

---

# 🖼️ Multimodal AI

## Image Understanding

```text
Image Upload
     │
     ▼
Vision Model
     │
     ├── Visual description
     └── Visible text
             │
             ▼
        Text Context
             │
             ▼
        Agent Workflow
```

The image handler produces grounded textual context so the rest of the agent does not need modality-specific reasoning logic.

## 🎙️ Audio

```text
Audio → Speech-to-Text → Agent → Answer → Text-to-Speech
```

The audio layer supports both transcription and speech synthesis through the configured OpenAI audio models.

## 🎬 Video

```text
                         VIDEO
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       Sample Frames               Extract Audio
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

Video processing requires **FFmpeg** and combines sampled visual frames with the extracted audio transcript.

## 🗣️ Voice

The voice interface uses a push-to-talk, turn-based WebSocket workflow:

```text
Audio Clip → Transcription → LangGraph → Answer → TTS → Audio Reply
```

---

# 🗄️ SQL Reasoning

```text
User Question
      │
      ▼
   Planner
      │
      ▼
     SQL
      │
      ▼
LLM SQL Generation
      │
      ▼
Safety Check
      │
      ▼
Read-Only Execution
      │
      ▼
 SQL Result
      │
      ▼
Response Engine
```

The SQL path is designed around read-only execution. Production deployments should additionally use least-privilege database credentials, strict query validation, timeouts, and appropriate database permissions.

---

# 🧮 Calculator

Mathematical requests are handled separately from language generation:

```text
Question → Planner → Calculator → Controlled Evaluation → Result
```

This provides a deterministic execution path for supported calculations.

---

# 🛡️ Response Quality Pipeline

```text
Tool / Retrieval Context
          │
          ▼
    Context Builder
          │
          ▼
      Generation
          │
          ▼
      Citations
          │
          ▼
 Confidence Scoring
          │
          ▼
      Validation
          │
          ▼
   Final Response
```

The response layer separates evidence gathering, generation, citation construction, confidence calculation, and final validation.

---

# 🔌 API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/chat` | Text chat |
| `POST` | `/chat/image` | Image + question |
| `POST` | `/chat/audio` | Audio + question |
| `POST` | `/chat/video` | Video + question |
| `WS` | `/ws/voice` | Push-to-talk voice |

### Example

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"What can you help me with?"}'
```

Example response shape:

```json
{
  "answer": "...",
  "sources": [],
  "confidence": 0.0
}
```

---

# 🚀 Quick Start

## 1. Clone

```bash
git clone https://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG.git
cd Multimodal-AI-Agent-and-Hybrid-RAG
```

## 2. Create environment

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

## 4. Configure `.env`

Copy the example file:

```bash
cp .env.example .env
```

On PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure your API, model, database, vector-store, retrieval, and upload settings.

> ⚠️ Never commit API keys or secrets to GitHub.

## 5. Install FFmpeg

Verify:

```bash
ffmpeg -version
```

## 6. Run

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

---

# 🌐 Frontend

The repository includes a lightweight browser UI with:

- Chat history
- New chat
- File attachments
- Image/audio/video uploads
- API base URL configuration
- Suggested prompts
- Voice interaction support

```text
frontend/
├── index.html
├── style.css
└── script.js
```

FastAPI serves the frontend from `frontend/` when the directory is available.

---

# 📁 Project Structure

```text
Multimodal-AI-Agent-and-Hybrid-RAG/
│
├── app/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── state.py
│   │
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── router.py
│   │   └── schemas.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── llm/
│   │   ├── base.py
│   │   ├── factory.py
│   │   └── openai_client.py
│   │
│   ├── multimodal/
│   │   ├── image_handler.py
│   │   ├── audio_handler.py
│   │   ├── video_handler.py
│   │   └── voice_realtime.py
│   │
│   ├── planner/
│   ├── prompts/
│   ├── rag/
│   ├── services/
│   └── main.py
│
├── frontend/
├── .env.example
├── LICENSE
├── README.md
└── requirements.txt
```

---

# 🧰 Technology Stack

| Layer | Technologies |
|---|---|
| Language | Python 3.12+ |
| API | FastAPI, Uvicorn |
| Agent | LangGraph, LangChain |
| LLM | OpenAI API |
| Vector Search | Qdrant |
| Lexical Search | BM25 |
| Reranking | Cross-Encoder |
| Database | SQLAlchemy + configured relational DB |
| Validation | Pydantic |
| Document Processing | PyMuPDF, pypdf, python-docx, Unstructured |
| Video | FFmpeg |
| Frontend | HTML, CSS, JavaScript |

---

# 🔐 Security & Production Notes

Before production deployment, consider:

- Restrict CORS origins instead of allowing `*`
- Use least-privilege database credentials
- Enforce strict SQL validation and allowlists
- Add authentication and authorization
- Add request rate limiting
- Validate MIME types and file contents
- Scan uploaded files
- Add model/tool timeouts
- Add structured logging and tracing
- Store secrets in a dedicated secret manager
- Add retrieval and answer-quality evaluation

---

# 🗺️ Roadmap

- [ ] Continuous realtime audio streaming
- [ ] Advanced intent classification
- [ ] Persistent conversation memory
- [ ] Authentication and RBAC
- [ ] Background document ingestion
- [ ] Retrieval evaluation benchmarks
- [ ] Observability and tracing
- [ ] Containerized deployment
- [ ] Production database hardening
- [ ] CI/CD automation

---

# 🤝 Contributing

```bash
git checkout -b feature/your-feature
git add .
git commit -m "feat: describe your change"
git push origin feature/your-feature
```

Open a pull request with a clear description of the change and testing performed.

---

# 📄 License

See [`LICENSE`](LICENSE) for license information.

---

<div align="center">

### Built with Python • LangGraph • FastAPI • OpenAI • Hybrid RAG

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&duration=3000&pause=1000&center=true&vCenter=true&width=700&lines=Multimodal+AI;Agentic+Reasoning;Hybrid+Retrieval;Grounded+Responses" alt="Footer animation" />

<br><br>

⭐ **If you find this project useful, consider giving it a star.**

</div>
