from app.response.citation import CitationBuilder


def test_citation_from_dict_chunks():

    builder = CitationBuilder()

    chunks = [
        {
            "text": "Chunk A",
            "metadata": {
                "document_name": "policy.pdf",
                "page": 2,
                "section": "Leave",
            },
        }
    ]

    citations = builder.build(chunks)

    assert citations == [
        {"document": "policy.pdf", "page": 2, "section": "Leave"}
    ]


def test_citation_falls_back_to_file_name():

    builder = CitationBuilder()

    chunks = [
        {
            "text": "Chunk A",
            "metadata": {
                "file_name": "policy.pdf",
                "page": None,
                "section": None,
            },
        }
    ]

    citations = builder.build(chunks)

    assert citations[0]["document"] == "policy.pdf"


def test_citation_empty_chunks():

    builder = CitationBuilder()

    assert builder.build([]) == []
