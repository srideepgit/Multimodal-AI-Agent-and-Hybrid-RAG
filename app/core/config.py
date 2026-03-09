"""
Centralized application configuration.

All environment-driven values live here so the rest of the codebase
never reads `os.environ` directly. This keeps configuration testable
and makes it obvious what the service depends on to run.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables / .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -------------------------
    # LLM
    # -------------------------
    llm_provider: str = "openai"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # -------------------------
    # Embeddings / Reranker
    # -------------------------
    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-base"

    # -------------------------
    # Vector Store (Qdrant)
    # -------------------------
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "enterprise_knowledge"

    # -------------------------
    # SQL Database
    # -------------------------
    database_url: str = "sqlite:///./enterprise.db"
    sql_schema_description: str = (
        "Table: employees(id INTEGER, name TEXT, department TEXT, "
        "salary REAL, hire_date TEXT)"
    )

    # -------------------------
    # Ingestion
    # -------------------------
    chunk_size: int = 500
    chunk_overlap: int = 100

    # -------------------------
    # Retrieval
    # -------------------------
    retrieval_top_k: int = 5
    retrieval_candidate_k: int = 20
    bm25_corpus_path: str = "bm25_corpus.json"

    # -------------------------
    # Multimodal
    # -------------------------
    vision_model: str = "gpt-4o-mini"
    stt_model: str = "whisper-1"
    tts_model: str = "tts-1"
    tts_voice: str = "alloy"
    video_frame_interval_seconds: int = 5
    video_max_frames: int = 6
    ffmpeg_path: str = "ffmpeg"
    max_upload_size_mb: int = 25


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings accessor so we only parse the environment once.
    """
    return Settings()
