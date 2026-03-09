import json

import pytest

from app.rag.ingestion.schemas import Chunk, ChunkMetadata
from app.rag.retrieval.bm25 import BM25Retriever
from app.rag.retrieval.hybrid import HybridRetriever


def _chunk(chunk_id, text):
    return Chunk(
        id=chunk_id,
        text=text,
        metadata=ChunkMetadata(
            source="doc.txt",
            file_name="doc.txt",
            file_type="txt",
            chunk_index=0,
            total_chunks=1,
        ),
    )


def test_bm25_search_before_index_returns_empty():

    retriever = BM25Retriever()

    assert retriever.search("leave policy") == []


def test_bm25_load_from_missing_file_returns_zero():

    retriever = BM25Retriever()

    loaded = retriever.load_from_file("/tmp/does-not-exist-bm25.json")

    assert loaded == 0
    assert retriever.search("anything") == []


def test_bm25_load_from_file_roundtrip(tmp_path):

    chunk = _chunk("1", "Annual leave policy for employees")

    snapshot = tmp_path / "corpus.json"
    snapshot.write_text(
        json.dumps([chunk.model_dump(mode="json")]),
        encoding="utf-8",
    )

    retriever = BM25Retriever()
    loaded = retriever.load_from_file(snapshot)

    assert loaded == 1

    results = retriever.search("leave policy")

    assert results[0]["id"] == "1"


def test_bm25_search_ranks_matching_chunk_first():

    retriever = BM25Retriever()

    chunks = [
        _chunk("1", "Annual leave policy for employees"),
        _chunk("2", "Company holiday calendar for the year"),
    ]

    retriever.build_index(chunks)

    results = retriever.search("leave policy", top_k=2)

    assert results[0]["id"] == "1"
    assert results[0]["text"] == "Annual leave policy for employees"


def test_hybrid_merge_sums_scores_for_shared_ids():

    hybrid = HybridRetriever()

    dense_results = [
        {"id": "1", "text": "Chunk A", "metadata": {}, "score": 0.6},
    ]

    bm25_results = [
        {"id": "1", "text": "Chunk A", "metadata": {}, "score": 0.3},
        {"id": "2", "text": "Chunk B", "metadata": {}, "score": 0.9},
    ]

    merged = hybrid.merge(dense_results, bm25_results, top_k=2)

    assert merged[0]["id"] == "2"
    assert merged[1]["id"] == "1"
    assert merged[1]["score"] == pytest.approx(0.9)
