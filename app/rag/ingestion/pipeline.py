# Pipeline [ Running strategy ]

from pathlib import Path

from .cleaner import DocumentCleaner
from .loader import DocumentLoader
from .metadata import MetadataBuilder
from .splitter import DocumentSplitter


class IngestionPipeline:
    """
    End-to-end document ingestion pipeline:

        Load -> Clean -> Enrich metadata -> Split into chunks
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):

        self.loader = DocumentLoader()
        self.cleaner = DocumentCleaner()
        self.metadata_builder = MetadataBuilder()
        self.splitter = DocumentSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def run(self, file_path: str | Path):
        """
        Execute ingestion pipeline for a single file and return the
        list of ``app.rag.ingestion.schemas.Chunk`` produced from it.
        """

        # Step 1: load
        documents = self.loader.load(file_path)

        # Step 2: clean
        documents = self.cleaner.clean(documents)

        # Step 3: enrich metadata (document_name, file_type, ...)
        documents = self.metadata_builder.build(documents)

        # Step 4: split into chunks
        chunks = self.splitter.split(documents)

        return chunks
