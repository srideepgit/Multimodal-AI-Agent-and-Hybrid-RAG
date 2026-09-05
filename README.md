<div align="center">

# 🤖 Multimodal AI Agent & Hybrid RAG

### GenAI • Agentic AI • Multimodal AI • Hybrid RAG • FastAPI

<br>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2600&pause=900&center=true&vCenter=true&width=900&lines=GenAI+%7C+LLMs+%7C+Agentic+AI;LangGraph+%2B+LangChain+%2B+FastAPI;Text+%7C+Image+%7C+Audio+%7C+Video+%7C+Voice;Hybrid+RAG+%2B+Qdrant+%2B+BM25;Cross-Encoder+Reranking+%2B+Grounded+Responses;SQL+%2B+APIs+%2B+Enterprise+AI+Workflows" alt="Typing animation" />

<br><br>

<img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/FastAPI-0F766E?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/LangGraph-Agentic%20AI-111827?style=for-the-badge" alt="LangGraph" />
<img src="https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge" alt="LangChain" />
<img src="https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" />
<img src="https://img.shields.io/badge/Qdrant-Vector%20Search-DC244C?style=for-the-badge" alt="Qdrant" />
<img src="https://img.shields.io/badge/BM25-Lexical%20Search-6B7280?style=for-the-badge" alt="BM25" />
<img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />

<br><br>

<a href="#-quick-start"><img src="https://img.shields.io/badge/🚀%20Quick%20Start-111827?style=for-the-badge" alt="Quick Start" /></a>
<a href="#-architecture"><img src="https://img.shields.io/badge/🏗️%20Architecture-1F2937?style=for-the-badge" alt="Architecture" /></a>
<a href="#-api"><img src="https://img.shields.io/badge/🔌%20API-4F46E5?style=for-the-badge" alt="API" /></a>
<a href="#-hybrid-rag"><img src="https://img.shields.io/badge/🔎%20Hybrid%20RAG-7C3AED?style=for-the-badge" alt="Hybrid RAG" /></a>

<br><br>

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&height=90&section=header&text=One%20Agent.%20Multiple%20Reasoning%20Paths.&fontSize=28&fontAlignY=55&animation=fadeIn" width="100%" alt="Animated project banner" />

</div>

---

## 👨‍💻 Developer Overview

**Srideep Sarkar** is a **GenAI Developer / Gen AI-ML Engineer** focused on building Python-based AI applications for enterprise workflows.

My work centers on **Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Prompt Engineering, Agentic AI, LangChain, LangGraph, FastAPI, REST APIs, and database-integrated AI systems**. I build modular backend services that connect language models with enterprise data, APIs, tools, and retrieval systems. fileciteturn49file0

### Professional focus

```text
                    GENAI / AI APPLICATIONS
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
       AGENTIC AI            RAG             MULTIMODAL AI
          │                   │                   │
     LangGraph           Qdrant / FAISS      Image / Audio
     LangChain           BM25 / pgvector     Video / Voice
     Tool Calling        Embeddings          OpenAI APIs
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
                     FASTAPI / REST APIs
                              │
                              ▼
                  SQL / PostgreSQL / MySQL
                              │
                              ▼
                  Enterprise AI Workflows
```

### Experience snapshot

| Area | Resume-backed experience |
|---|---|
| **GenAI / ML Engineering** | Python-based multi-agent AI applications using LangGraph, LangChain, FastAPI, and PostgreSQL |
| **LLM Integration** | Provider-agnostic gateway supporting 12+ LLM providers, including OpenAI, Claude, Gemini, AWS Bedrock, and Azure OpenAI |
| **Enterprise RAG** | RAG pipelines using FAISS and pgvector with configurable retrieval and reranking |
| **Backend Engineering** | REST APIs, backend services, AI workflow integration, enterprise tools and databases |
| **AI Quality** | Prompt refinement, workflow debugging, LLM output evaluation, retrieval tuning, and reliability improvements |
| **Agent Workflows** | LangGraph/LangChain orchestration and prompt-driven task execution |

These experience areas are reflected in the resume and align directly with the engineering patterns implemented in this project. fileciteturn49file0

---

## 🎯 Project Overview

**Multimodal AI Agent & Hybrid RAG** is a practical GenAI backend that brings together the areas I work with most: **agentic orchestration, RAG, multimodal processing, API development, database integration, and LLM-powered response generation**.

The system accepts **text, image, audio, video, and push-to-talk voice** inputs. It normalizes non-text inputs and routes requests through a LangGraph workflow to one of three execution paths:

```text
User Input
    │
    ▼
Multimodal Processing
    │
    ▼
LangGraph Planner
    │
    ├──────────────► Knowledge → Hybrid RAG
    │
    ├──────────────► SQL       → Database Reasoning
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

The project demonstrates how an LLM application can be structured as a collection of replaceable services instead of a single monolithic prompt.

---

# 🧩 Why This Project Reflects My GenAI Profile

The architecture maps closely to the capabilities highlighted in my GenAI resume:

### 🧠 LLM & Generative AI

The application uses OpenAI-powered services for language generation, vision, speech transcription, and text-to-speech.

### 🔗 Agentic AI

LangGraph provides explicit stateful routing between planner, knowledge, SQL, calculator, response, and validation nodes.

### 🔎 RAG Engineering

The knowledge path combines **dense retrieval, BM25 lexical search, hybrid retrieval, embeddings, and cross-encoder reranking**.

### ⚙️ Python Backend Engineering

FastAPI exposes the AI system through REST and WebSocket interfaces, while the application is divided into modular services, tools, and configuration layers.

### 🗄️ Database-Integrated AI

The SQL path connects natural-language questions with database operations through SQLAlchemy and a schema-aware workflow.

### 🛡️ AI Reliability

The response pipeline includes citations, confidence scoring, and response validation rather than returning raw model output directly.

---

# 🌟 Core Capabilities

| Capability | Implementation |
|---|---|
| 💬 Text AI | LangGraph + OpenAI |
| 🖼️ Image AI | Vision analysis + visible text extraction |
| 🎙️ Audio AI | Speech-to-text + text-to-speech |
| 🎬 Video AI | Sampled-frame analysis + audio transcription |
| 🗣️ Voice AI | Push-to-talk WebSocket workflow |
| 🤖 Agentic AI | LangGraph planner + execution nodes |
| 📚 RAG | Dense + BM25 + hybrid retrieval |
| 🎯 Reranking | Cross-encoder reranking |
| 🗄️ SQL AI | Natural-language database reasoning |
| 🧮 Calculation | Dedicated calculator execution |
| 🔖 Grounding | Citations + retrieval context |
| 📊 Confidence | Retrieval-based confidence signal |
| ✅ Validation | Final response validation |
| 🔌 APIs | FastAPI REST + WebSocket |

---

# 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Language** | Python |
| **GenAI / LLM** | OpenAI APIs, LLM workflows |
| **Agent Frameworks** | LangGraph, LangChain |
| **Backend** | FastAPI, AsyncIO, REST APIs, Pydantic |
| **RAG** | Embeddings, BM25, Semantic Search, Hybrid Retrieval |
| **Vector Search** | Qdrant, FAISS, pgvector |
| **Reranking** | Cross-Encoder |
| **Databases** | SQL, PostgreSQL, MySQL, SQLAlchemy |
| **Multimodal** | Vision, Speech-to-Text, Text-to-Speech, FFmpeg |
| **Cloud / DevOps** | AWS, Azure, Docker, CI/CD |
| **Development** | Git, GitHub, API Testing, Debugging, Model Evaluation |

These categories are aligned with the technical skills listed in the GenAI resume. fileciteturn49file0

---

# 📈 Engineering Highlights

### Modular architecture

Each major subsystem is isolated so that components such as the LLM client, retriever, reranker, SQL engine, or multimodal handler can be modified independently.

### Explicit agent workflow

The execution graph makes routing behavior visible and testable instead of hiding business logic inside an oversized prompt.

### Grounded generation

Knowledge responses are built around retrieved context, followed by citation construction, confidence scoring, and validation.

### Multimodal normalization

Image, audio, and video are converted into textual context before entering the shared agent graph, keeping downstream reasoning consistent.

### API-first design

The application can be consumed through REST endpoints while voice interaction uses a dedicated WebSocket channel.

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
├── scripts/
├── tests/
├── .env.example
├── requirements.txt
├── LICENSE
└── README.md
```

---

# 🔐 Configuration

The project centralizes environment-driven configuration through `app/core/config.py`.

Important settings include:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

EMBEDDING_MODEL=BAAI/bge-m3
RERANKER_MODEL=BAAI/bge-reranker-base

QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=enterprise_knowledge

DATABASE_URL=sqlite:///./enterprise.db

CHUNK_SIZE=500
CHUNK_OVERLAP=100

RETRIEVAL_TOP_K=5
RETRIEVAL_CANDIDATE_K=20

VISION_MODEL=gpt-4o-mini
STT_MODEL=whisper-1
TTS_MODEL=tts-1
TTS_VOICE=alloy

VIDEO_FRAME_INTERVAL_SECONDS=5
VIDEO_MAX_FRAMES=6
MAX_UPLOAD_SIZE_MB=25
```

Never commit real API keys to source control.

---

# 🚀 Quick Start

```bash
git clone https://github.com/srideepgit/Multimodal-AI-Agent-and-Hybrid-RAG.git
cd Multimodal-AI-Agent-and-Hybrid-RAG
```

Create an environment:

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

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Then start the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

For video support, make sure `ffmpeg` is installed and available on `PATH`.

---

# 🔌 API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/chat` | Text question |
| `POST` | `/chat/image` | Image analysis + question |
| `POST` | `/chat/audio` | Audio transcription + question |
| `POST` | `/chat/video` | Video frames + audio analysis |
| `WS` | `/ws/voice` | Push-to-talk voice interaction |

### Example request

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question":"What can this agent help me with?"}'
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

# 🧪 Testing

Run the test suite with:

```bash
pytest
```

Run a specific test module:

```bash
pytest tests/tools/test_calculator.py
```

Run coverage:

```bash
pytest --cov=app
```

---

# 🛡️ Reliability & Security

The project separates AI generation from validation and tool execution.

### SQL

Use read-only database credentials, strict query validation, query timeouts, and least-privilege database permissions in production.

### Calculator

Keep mathematical evaluation isolated from arbitrary code execution.

### Multimodal uploads

The current configuration includes upload-size limits and explicit FFmpeg dependency handling for video processing.

### Response quality

The response layer supports citations, confidence scoring, and final validation before returning the answer.

---

# 🔮 Roadmap

- Token-level / continuous realtime voice streaming
- Multimodal document ingestion and retrieval
- Multi-turn conversation memory
- Streaming agent responses
- Authentication and authorization
- Role-based document access
- Multi-agent workflows
- Async retrieval improvements
- Redis caching
- Kubernetes deployment
- Prometheus / Grafana monitoring
- OpenTelemetry tracing
- Multi-provider evaluation framework
- Continuous document ingestion and indexing

---

# 📌 Resume Alignment

This project directly demonstrates the GenAI engineering areas highlighted in my resume:

```text
Python
  ↓
LLMs / Generative AI
  ↓
LangChain / LangGraph
  ↓
Agentic Workflows
  ↓
RAG / Embeddings / Semantic Search
  ↓
Qdrant / FAISS / pgvector
  ↓
FastAPI / REST APIs / Pydantic
  ↓
SQL / PostgreSQL / Database Integration
  ↓
Multimodal AI
  ↓
Enterprise AI Applications
```

The broader professional profile also includes experience with multi-agent applications, provider-agnostic LLM integrations, enterprise RAG, backend APIs, prompt engineering, and AI workflow evaluation. fileciteturn49file0

---

# 👤 About Me

**Srideep Sarkar**

GenAI Developer / Gen AI-ML Engineer

Bengaluru, India

🔗 [GitHub](https://github.com/srideepgit)  
🔗 [LinkedIn](https://www.linkedin.com/)  

I build **LLM-powered, agentic, RAG, and multimodal applications** using Python and modern AI engineering frameworks, with a focus on enterprise APIs, retrieval systems, databases, and reliable AI workflows.

---

<div align="center">

### ⭐ Build intelligent systems. Ground them in data. Make them reliable.

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4F46E5,50:06B6D4,100:7C3AED&height=150&section=footer&text=GenAI%20%7C%20RAG%20%7C%20Agentic%20AI&fontSize=24&fontColor=ffffff&animation=fadeIn" width="100%" alt="Animated footer" />

</div>
