from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class ChunkMetadata(BaseModel):
    """Metadata attached to every chunk."""

    model_config = ConfigDict(extra="allow")

    source: str
    file_name: str
    file_type: str

    page: int | None = None
    section: str | None = None
    department: str | None = None
    version: str | None = None

    chunk_index: int
    total_chunks: int

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Chunk(BaseModel):
    """Single chunk ready for embedding."""

    id: str
    text: str
    metadata: ChunkMetadata


class IngestionResult(BaseModel):
    """Output of the ingestion pipeline."""

    document_name: str
    total_chunks: int
    chunks: list[Chunk]
