import tempfile
from pathlib import Path

import pytest

from app.rag.ingestion.loader import (
    DocumentLoader,
    UnsupportedFileTypeError,
)


def test_load_text_file():

    sample_text = """
Enterprise AI Agent

Annual Leave Policy

Employees receive 20 days annual leave.
"""

    with tempfile.TemporaryDirectory() as temp_dir:

        file_path = Path(temp_dir) / "policy.txt"

        file_path.write_text(
            sample_text,
            encoding="utf-8",
        )

        loader = DocumentLoader()

        documents = loader.load(file_path)

        assert len(documents) == 1

        assert (
            "Annual Leave Policy"
            in documents[0].page_content
        )


def test_load_directory():

    with tempfile.TemporaryDirectory() as temp_dir:

        Path(temp_dir, "a.txt").write_text(
            "Document A"
        )

        Path(temp_dir, "b.txt").write_text(
            "Document B"
        )

        loader = DocumentLoader()

        docs = loader.load_directory(
            temp_dir
        )

        assert len(docs) == 2


def test_missing_file_raises():

    loader = DocumentLoader()

    with pytest.raises(FileNotFoundError):
        loader.load("does/not/exist.txt")


def test_unsupported_extension_raises():

    with tempfile.TemporaryDirectory() as temp_dir:

        file_path = Path(temp_dir) / "notes.xyz"
        file_path.write_text("hello")

        loader = DocumentLoader()

        with pytest.raises(UnsupportedFileTypeError):
            loader.load(file_path)


def test_pdf_loader():

    fitz = pytest.importorskip("fitz")

    with tempfile.TemporaryDirectory() as temp_dir:

        pdf_path = Path(temp_dir) / "policy.pdf"

        document = fitz.open()
        page = document.new_page()
        page.insert_text((72, 72), "Annual Leave Policy")
        document.save(str(pdf_path))
        document.close()

        loader = DocumentLoader()

        docs = loader.load(pdf_path)

        assert len(docs) > 0

        assert (
            "Annual Leave"
            in docs[0].page_content
        )
