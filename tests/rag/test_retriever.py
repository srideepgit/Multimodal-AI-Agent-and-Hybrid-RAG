from unittest.mock import MagicMock

from app.rag.retrieval.retriever import EnterpriseRetriever


def test_retrieve():

    # -------------------------
    # Embedding Model
    # -------------------------

    embedding = MagicMock()

    embedding.embed_text.return_value = [0.1, 0.2, 0.3]

    # -------------------------
    # Dense Search
    # -------------------------

    dense = MagicMock()

    dense.search.return_value = [
        {
            "id": "1",
            "text": "Dense Chunk",
            "metadata": {},
            "score": 0.5,
        }
    ]

    # -------------------------
    # BM25
    # -------------------------

    bm25 = MagicMock()

    bm25.search.return_value = [
        {
            "id": "2",
            "text": "BM25 Chunk",
            "metadata": {},
            "score": 0.4,
        }
    ]

    # -------------------------
    # Hybrid
    # -------------------------

    hybrid = MagicMock()

    hybrid.merge.return_value = [
        {
            "id": "3",
            "text": "Merged Chunk",
            "metadata": {},
            "score": 0.9,
        }
    ]

    # -------------------------
    # Reranker
    # -------------------------

    reranker = MagicMock()

    reranker.rerank.return_value = [
        {
            "id": "3",
            "text": "Final Chunk",
            "metadata": {},
            "score": 0.9,
            "rerank_score": 0.95,
        }
    ]

    # -------------------------
    # Retriever
    # -------------------------

    retriever = EnterpriseRetriever(
        embedding_service=embedding,
        dense_retriever=dense,
        bm25_retriever=bm25,
        hybrid_retriever=hybrid,
        reranker=reranker,
    )

    result = retriever.retrieve(
        "leave policy"
    )

    # -------------------------
    # Assertions
    # -------------------------

    assert len(result) == 1

    assert result[0]["text"] == "Final Chunk"

    embedding.embed_text.assert_called_once()

    dense.search.assert_called_once()

    bm25.search.assert_called_once()

    hybrid.merge.assert_called_once()

    reranker.rerank.assert_called_once()
