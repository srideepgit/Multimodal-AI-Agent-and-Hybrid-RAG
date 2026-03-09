from langchain_core.documents import Document

from app.rag.ingestion.splitter import DocumentSplitter


def test_split_document():

    splitter = DocumentSplitter(chunk_size=50, chunk_overlap=10)

    text = "A " * 1000

    chunks = splitter.split([Document(page_content=text, metadata={})])

    assert len(chunks) > 1


def test_small_document():

    splitter = DocumentSplitter()

    chunks = splitter.split(
        [Document(page_content="Enterprise AI", metadata={})]
    )

    assert len(chunks) == 1


def test_chunk_content():

    splitter = DocumentSplitter(chunk_size=50, chunk_overlap=10)

    text = "Hello World " * 300

    chunks = splitter.split([Document(page_content=text, metadata={})])

    assert "Hello" in chunks[0].text


def test_chunk_metadata_indexing():

    splitter = DocumentSplitter(chunk_size=50, chunk_overlap=10)

    text = "Hello World " * 300

    chunks = splitter.split([Document(page_content=text, metadata={})])

    assert chunks[0].metadata.chunk_index == 0
    assert chunks[0].metadata.total_chunks == len(chunks)
    assert chunks[-1].metadata.chunk_index == len(chunks) - 1
