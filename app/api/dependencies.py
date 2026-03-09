"""
Dependency-injection wiring for the enterprise agent.

Everything here is built once (via ``lru_cache``) and reused across
requests, since the embedding model, reranker, and DB engine are all
expensive to construct.

Imports of the heavy ML pieces (HuggingFace embeddings, the
cross-encoder reranker) are done *inside* the functions that need
them rather than at module level. That keeps `app.main` / the FastAPI
app importable -- and therefore `/health` and routing testable --
without requiring torch/transformers to be installed, and defers the
actual model download/load until the first real request needs it.
"""

from functools import lru_cache

from app.agent.graph import EnterpriseAgentGraph
from app.agent.nodes import AgentNodes
from app.core.config import get_settings
from app.llm.factory import LLMFactory
from app.multimodal.audio_handler import AudioHandler
from app.multimodal.image_handler import ImageHandler
from app.multimodal.video_handler import VideoHandler
from app.multimodal.voice_realtime import VoiceSession
from app.response.citation import CitationBuilder
from app.response.confidence import ConfidenceScorer
from app.response.context_builder import ContextBuilder
from app.response.generator import ResponseGenerator
from app.response.validator import ResponseValidator
from app.services.ai_service import AIService
from app.tools.calculator import CalculatorTool
from app.tools.knowledge import KnowledgeTool
from app.tools.sql import SQLTool


@lru_cache
def get_llm():
    settings = get_settings()

    return LLMFactory.create(
        provider=settings.llm_provider,
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )


@lru_cache
def get_embedding_service():
    from app.rag.indexing.embeddings import EmbeddingService

    settings = get_settings()

    return EmbeddingService(model_name=settings.embedding_model)


@lru_cache
def get_vector_store():
    from app.rag.indexing.vectorstore import QdrantVectorStore

    settings = get_settings()

    return QdrantVectorStore(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
    )


@lru_cache
def get_reranker():
    from app.rag.retrieval.reranker import Reranker

    settings = get_settings()

    return Reranker(model_name=settings.reranker_model)


@lru_cache
def get_bm25_retriever():
    from app.rag.retrieval.bm25 import BM25Retriever

    settings = get_settings()

    retriever = BM25Retriever()

    # If `scripts/index_documents.py` has been run, this populates the
    # keyword index from disk. Otherwise the retriever simply starts
    # empty and degrades gracefully (see BM25Retriever.search).
    retriever.load_from_file(settings.bm25_corpus_path)

    return retriever


@lru_cache
def get_retriever():
    from app.rag.retrieval.dense import DenseRetriever
    from app.rag.retrieval.hybrid import HybridRetriever
    from app.rag.retrieval.retriever import EnterpriseRetriever

    settings = get_settings()

    vector_store = get_vector_store()

    dense_retriever = DenseRetriever(
        client=vector_store.client,
        collection_name=settings.qdrant_collection,
    )

    return EnterpriseRetriever(
        embedding_service=get_embedding_service(),
        dense_retriever=dense_retriever,
        bm25_retriever=get_bm25_retriever(),
        hybrid_retriever=HybridRetriever(),
        reranker=get_reranker(),
    )


@lru_cache
def get_sql_engine():
    from sqlalchemy import create_engine

    settings = get_settings()

    return create_engine(settings.database_url)


@lru_cache
def get_agent_nodes() -> AgentNodes:
    settings = get_settings()
    llm = get_llm()

    knowledge_tool = KnowledgeTool(retriever=get_retriever())
    sql_tool = SQLTool(engine=get_sql_engine())
    calculator_tool = CalculatorTool()

    return AgentNodes(
        knowledge_tool=knowledge_tool,
        sql_tool=sql_tool,
        calculator_tool=calculator_tool,
        llm=llm,
        context_builder=ContextBuilder(),
        generator=ResponseGenerator(llm),
        citation_builder=CitationBuilder(),
        confidence_scorer=ConfidenceScorer(),
        validator=ResponseValidator(),
        sql_schema_description=settings.sql_schema_description,
    )


@lru_cache
def get_agent_graph():
    nodes = get_agent_nodes()

    return EnterpriseAgentGraph(nodes).build()


def get_ai_service() -> AIService:
    return AIService(get_agent_graph())


# -----------------------------
# Multimodal handlers
# -----------------------------


@lru_cache
def get_image_handler() -> ImageHandler:
    settings = get_settings()

    return ImageHandler(
        api_key=settings.openai_api_key,
        model=settings.vision_model,
    )


@lru_cache
def get_audio_handler() -> AudioHandler:
    settings = get_settings()

    return AudioHandler(
        api_key=settings.openai_api_key,
        stt_model=settings.stt_model,
        tts_model=settings.tts_model,
        tts_voice=settings.tts_voice,
    )


@lru_cache
def get_video_handler() -> VideoHandler:
    settings = get_settings()

    return VideoHandler(
        image_handler=get_image_handler(),
        audio_handler=get_audio_handler(),
        frame_interval_seconds=settings.video_frame_interval_seconds,
        max_frames=settings.video_max_frames,
        ffmpeg_path=settings.ffmpeg_path,
    )


def get_voice_session() -> VoiceSession:
    return VoiceSession(
        audio_handler=get_audio_handler(),
        ai_service=get_ai_service(),
    )
