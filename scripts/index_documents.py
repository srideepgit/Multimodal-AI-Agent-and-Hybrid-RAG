"""
Offline document indexing CLI.

Usage:

    python scripts/index_documents.py /path/to/documents

Loads every supported file in the given directory, chunks it, embeds
the chunks, and upserts them into Qdrant. It also writes a JSON
snapshot of the chunks to `bm25_corpus.json` so the BM25 keyword index
can be rebuilt quickly at API startup without hitting Qdrant.

This intentionally lives outside `app/` since it's a one-off
operational tool, not part of the request-serving API.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import get_settings  # noqa: E402
from app.rag.indexing.embeddings import EmbeddingService  # noqa: E402
from app.rag.indexing.indexer import DocumentIndexer  # noqa: E402
from app.rag.indexing.vectorstore import QdrantVectorStore  # noqa: E402
from app.rag.ingestion.loader import DocumentLoader  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "documents_dir",
        type=Path,
        help="Directory containing documents to index (.pdf, .docx, .md, .txt, .csv, .html)",
    )
    parser.add_argument(
        "--bm25-out",
        type=Path,
        default=Path("bm25_corpus.json"),
        help="Where to write the BM25 corpus snapshot (default: ./bm25_corpus.json)",
    )
    args = parser.parse_args()

    settings = get_settings()

    embedding_service = EmbeddingService(model_name=settings.embedding_model)
    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
    )
    indexer = DocumentIndexer(
        vector_store=vector_store,
        embedding_service=embedding_service,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    loader = DocumentLoader()
    all_chunks = []

    file_paths = [
        path
        for path in sorted(args.documents_dir.iterdir())
        if path.is_file() and path.suffix.lower() in loader.SUPPORTED_EXTENSIONS
    ]

    if not file_paths:
        print(f"No supported files found in {args.documents_dir}")
        return

    for path in file_paths:
        print(f"Indexing {path} ...")
        chunk_count = indexer.index(str(path))
        print(f"  -> {chunk_count} chunks upserted to Qdrant")

        # Re-run the (cheap) load+clean+split steps to also collect
        # the chunks for the BM25 snapshot, so we don't have to fetch
        # everything back out of Qdrant.
        all_chunks.extend(indexer.pipeline.run(str(path)))

    args.bm25_out.write_text(
        json.dumps([chunk.model_dump(mode="json") for chunk in all_chunks], indent=2),
        encoding="utf-8",
    )

    print(
        f"\nDone. Indexed {len(file_paths)} file(s), "
        f"{len(all_chunks)} chunk(s) total."
    )
    print(f"BM25 corpus snapshot written to {args.bm25_out}")


if __name__ == "__main__":
    main()
