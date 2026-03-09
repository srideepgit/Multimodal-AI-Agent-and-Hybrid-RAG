from unittest.mock import MagicMock

from app.tools.knowledge import KnowledgeTool


def test_knowledge_search():

    # Fake Retriever
    retriever = MagicMock()

    retriever.retrieve.return_value = [

        "Chunk 1",

        "Chunk 2",

        "Chunk 3",

    ]

    tool = KnowledgeTool(retriever)

    results = tool.search(
        "annual leave"
    )

    assert len(results) == 3

    assert results[0] == "Chunk 1"

    retriever.retrieve.assert_called_once()