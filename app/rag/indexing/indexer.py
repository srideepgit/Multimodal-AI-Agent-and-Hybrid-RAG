# Knowledge Engine final orchestration layer 

from app.rag.ingestion.pipeline import IngestionPipeline
from app.rag.indexing.embeddings import EmbeddingService
from app.rag.indexing.vectorstore import QdrantVectorStore


class DocumentIndexer:
    """
    Complete document indexing pipeline.

    File
      ↓
    Chunks
      ↓
    Embeddings
      ↓
    Qdrant
    """

    def __init__(
        self,
        vector_store: QdrantVectorStore,
        embedding_service: EmbeddingService,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        self.pipeline = IngestionPipeline(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index(self, file_path: str):

        # Step 1
        chunks = self.pipeline.run(file_path)

        # Step 2
        texts = [chunk.text for chunk in chunks]

        vectors = self.embedding_service.embed_documents(texts)

        # Step 3
        ids = []
        payloads = []

        for chunk in chunks:

            ids.append(chunk.id)

            payloads.append(
                {
                    "text": chunk.text,
                    **chunk.metadata.model_dump(),
                }
            )

        # Step 4
        vector_size = len(vectors[0])

        self.vector_store.create_collection(
            vector_size=vector_size,
        )

        # Step 5
        self.vector_store.upload(
            ids=ids,
            vectors=vectors,
            payloads=payloads,
        )

        return len(chunks)