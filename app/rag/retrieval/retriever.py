# Retrieval Engine orchestrator
#
# NOTE: this module intentionally avoids importing the concrete
# EmbeddingService / Reranker classes at runtime. Those pull in heavy
# ML libraries (transformers, torch, sentence-transformers), and
# EnterpriseRetriever only ever calls a small duck-typed interface on
# its collaborators, so importing the concrete classes here would
# force every caller (including lightweight unit tests that pass in
# mocks) to have those heavy libraries installed just to import this
# file. Real type checking still works via TYPE_CHECKING.

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.rag.indexing.embeddings import EmbeddingService
    from app.rag.retrieval.bm25 import BM25Retriever
    from app.rag.retrieval.dense import DenseRetriever
    from app.rag.retrieval.hybrid import HybridRetriever
    from app.rag.retrieval.reranker import Reranker


class EnterpriseRetriever:
    """
    Orchestrates the full retrieval pipeline:

        embed query -> dense search -> bm25 search -> merge -> rerank
    """

    def __init__(
        self,
        embedding_service: "EmbeddingService",
        dense_retriever: "DenseRetriever",
        bm25_retriever: "BM25Retriever",
        hybrid_retriever: "HybridRetriever",
        reranker: "Reranker",
    ):

        self.embedding = embedding_service

        self.dense = dense_retriever

        self.bm25 = bm25_retriever

        self.hybrid = hybrid_retriever

        self.reranker = reranker

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        # Step 1
        query_vector = self.embedding.embed_text(query)

        # Step 2
        dense_results = self.dense.search(
            query_vector=query_vector,
            limit=20,
        )

        # Step 3
        bm25_results = self.bm25.search(
            query=query,
            top_k=20,
        )

        # Step 4
        hybrid_results = self.hybrid.merge(
            dense_results,
            bm25_results,
            top_k=20,
        )

        # Step 5
        final_results = self.reranker.rerank(
            query=query,
            chunks=hybrid_results,
            top_k=top_k,
        )

        return final_results
