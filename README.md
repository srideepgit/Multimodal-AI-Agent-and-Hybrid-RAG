# 🤖 Multimodal AI Agent & Hybrid RAG

<div align="center">

### Enterprise-Grade Multimodal AI • Agentic Workflows • Hybrid Retrieval

<br>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=19&duration=2800&pause=900&center=true&vCenter=true&width=850&lines=Text+%7C+Image+%7C+Audio+%7C+Video+%7C+Realtime+Voice;LangGraph+Agentic+Workflow;Hybrid+RAG+%2B+BM25+%2B+Vector+Search;Cross-Encoder+Reranking;Safe+SQL+%2B+Confidence+Scoring" alt="Typing animation">

<br><br>

<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white">
<img src="https://img.shields.io/badge/LangGraph-Agentic%20Workflow-1C3C3C?style=for-the-badge">
<img src="https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white">

<br>

<img src="https://img.shields.io/badge/Qdrant-Vector%20DB-DC244C?style=for-the-badge">
<img src="https://img.shields.io/badge/BM25-Hybrid%20Search-6B7280?style=for-the-badge">
<img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white">
<img src="https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white">

<br><br>

<a href="#-quick-start">
<img src="https://img.shields.io/badge/🚀%20Quick%20Start-0078D4?style=for-the-badge">
</a>
<a href="#-architecture">
<img src="https://img.shields.io/badge/🏗️%20Architecture-24292F?style=for-the-badge">
</a>
<a href="#-api">
<img src="https://img.shields.io/badge/🔌%20API-6B4FBB?style=for-the-badge">
</a>

</div>

---

## 🌟 Overview

**Multimodal AI Agent & Hybrid RAG** is an enterprise-oriented AI backend designed to answer questions across multiple input modalities while intelligently selecting the right execution path.

The system accepts:

- 💬 Text
- 🖼️ Images
- 🎵 Audio
- 🎬 Video
- 🎙️ Realtime voice

A multimodal preprocessing layer converts non-text inputs into a normalized textual representation before passing the request into the shared agent workflow.

The LangGraph-based agent then routes the request to the appropriate execution engine:

```text
                    User Request
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Knowledge         SQL        Calculator
          │              │              │
          ▼              ▼              ▼
      Hybrid RAG      Read-Only      Safe AST
                      Database       Evaluation
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                 Response Engine
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Citations   Confidence  Validation
                         │
                         ▼
                    Final Answer
