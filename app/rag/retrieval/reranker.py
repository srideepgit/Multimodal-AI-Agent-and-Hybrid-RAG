# Re-rank the merged (dense + BM25) results to find the best chunks.

from sentence_transformers import CrossEncoder


class Reranker:
    """
    Re-ranks retrieved chunks using a Cross Encoder model.

    Expects and returns the normalized dict shape used across the
    retrieval layer: {"id", "text", "metadata", "score", ...}.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        chunks: list,
        top_k: int = 5,
    ):

        if not chunks:
            return []

        pairs = [
            (query, chunk["text"])
            for chunk in chunks
        ]

        scores = self.model.predict(pairs)

        for chunk, score in zip(chunks, scores):
            chunk["rerank_score"] = float(score)

        chunks.sort(
            key=lambda item: item["rerank_score"],
            reverse=True,
        )

        return chunks[:top_k]
