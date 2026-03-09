# Exact keyword search over the in-memory chunk corpus.

import json
from pathlib import Path

from rank_bm25 import BM25Okapi

from app.rag.ingestion.schemas import Chunk


class BM25Retriever:
    """
    Performs keyword-based retrieval using BM25.

    Returns the same normalized dict shape as DenseRetriever so both
    can be merged directly by HybridRetriever:

        {"id": ..., "text": ..., "metadata": {...}, "score": float}
    """

    def __init__(self):
        self.bm25 = None
        self.documents = []

    def build_index(self, chunks):
        """
        Build BM25 index from document chunks (a list of
        ``app.rag.ingestion.schemas.Chunk``).
        """

        self.documents = list(chunks)

        corpus = [
            chunk.text.split()
            for chunk in self.documents
        ]

        self.bm25 = BM25Okapi(corpus) if corpus else None

    def load_from_file(self, path: str | Path) -> int:
        """
        Rebuild the index from a JSON snapshot written by
        `scripts/index_documents.py` (a list of serialized
        `app.rag.ingestion.schemas.Chunk`).

        Returns the number of chunks loaded. If the file does not
        exist, the index is left empty and 0 is returned -- this lets
        callers use it directly in a startup hook without first
        checking for the file's existence.
        """

        snapshot_path = Path(path)

        if not snapshot_path.exists():
            return 0

        raw_chunks = json.loads(snapshot_path.read_text(encoding="utf-8"))

        chunks = [Chunk.model_validate(item) for item in raw_chunks]

        self.build_index(chunks)

        return len(chunks)

    def search(
        self,
        query: str,
        top_k: int = 10,
    ):

        if self.bm25 is None:
            # No corpus indexed yet -- degrade gracefully instead of
            # blowing up the whole retrieval pipeline.
            return []

        tokenized_query = query.split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda pair: pair[1],
            reverse=True,
        )

        results = []

        for chunk, score in ranked[:top_k]:
            results.append(
                {
                    "id": chunk.id,
                    "text": chunk.text,
                    "metadata": chunk.metadata.model_dump(),
                    "score": float(score),
                }
            )

        return results
