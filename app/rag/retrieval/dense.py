# Qdrant Vector Semantic search

from qdrant_client import QdrantClient


class DenseRetriever:
    """
    Performs dense vector search using Qdrant.

    Returns a normalized list of dicts so downstream components
    (HybridRetriever, Reranker) never need to know they came from
    Qdrant specifically:

        {"id": ..., "text": ..., "metadata": {...}, "score": float}
    """

    def __init__(
        self,
        client: QdrantClient,
        collection_name: str,
    ):
        self.client = client
        self.collection_name = collection_name

    def search(
        self,
        query_vector: list[float],
        limit: int = 10,
    ):

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )

        results = []

        for point in response.points:
            payload = dict(point.payload or {})
            text = payload.pop("text", "")

            results.append(
                {
                    "id": point.id,
                    "text": text,
                    "metadata": payload,
                    "score": point.score,
                }
            )

        return results
