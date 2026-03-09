def _get(chunk, key, default=None):
    """
    Read `key` off a chunk regardless of whether it is a dict (the
    shape produced by the retrieval layer) or an object with
    attributes (the shape used by some unit tests / callers).
    """

    if isinstance(chunk, dict):
        return chunk.get(key, default)

    return getattr(chunk, key, default)


class CitationBuilder:
    """
    Builds citations from retrieved chunks.
    """

    def build(self, chunks):

        citations = []

        for chunk in chunks:

            metadata = _get(chunk, "metadata", {}) or {}

            document = _get(metadata, "document_name") or _get(
                metadata, "file_name"
            )
            page = _get(metadata, "page")
            section = _get(metadata, "section")

            citations.append(
                {
                    "document": document,
                    "page": page,
                    "section": section,
                }
            )

        return citations
