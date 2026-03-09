from langchain_core.documents import Document

from app.rag.ingestion.cleaner import DocumentCleaner


def _doc(text: str) -> Document:
    return Document(page_content=text, metadata={"source": "test.txt"})


def test_remove_extra_spaces():

    cleaner = DocumentCleaner()

    cleaned = cleaner.clean([_doc("Hello      World")])

    assert cleaned[0].page_content == "Hello World"


def test_remove_extra_newlines():

    cleaner = DocumentCleaner()

    cleaned = cleaner.clean([_doc("Hello\n\n\nWorld")])

    # 3+ newlines collapse to a single blank line (2 newlines), not 1,
    # so paragraph breaks are preserved.
    assert cleaned[0].page_content == "Hello\n\nWorld"


def test_strip_whitespace():

    cleaner = DocumentCleaner()

    cleaned = cleaner.clean([_doc("     Enterprise AI     ")])

    assert cleaned[0].page_content == "Enterprise AI"


def test_empty_string():

    cleaner = DocumentCleaner()

    cleaned = cleaner.clean([_doc("")])

    assert cleaned[0].page_content == ""


def test_preserves_metadata():

    cleaner = DocumentCleaner()

    cleaned = cleaner.clean([_doc("Hello   World")])

    assert cleaned[0].metadata["source"] == "test.txt"


def test_empty_list():

    cleaner = DocumentCleaner()

    assert cleaner.clean([]) == []
