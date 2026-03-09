def _get(chunk, key, default=None):
    """
    Read `key` off a chunk regardless of whether it is a dict or an
    object with attributes. See app.response.citation for context.
    """

    if isinstance(chunk, dict):
        return chunk.get(key, default)

    return getattr(chunk, key, default)


class ConfidenceScorer:
    """
    Calculates a simple confidence score as the average rerank score
    of the retrieved chunks (falling back to a neutral default when a
    chunk has no rerank score, e.g. it only matched via BM25).
    """

    def calculate(
        self,
        retrieved_chunks,
    ) -> float:

        scores = [
            _get(chunk, "rerank_score", 0.8)
            for chunk in (retrieved_chunks or [])
        ]

        if not scores:
            return 0.0

        return round(
            sum(scores) / len(scores),
            2,
        )
