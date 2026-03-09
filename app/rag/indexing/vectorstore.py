# vector store -> Qdrant 

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)


class QdrantVectorStore:
    """
    Handles all Qdrant operations.
    """

    def __init__(
        self,
        url: str,
        collection_name: str,
    ):
        self.collection_name = collection_name

        self.client = QdrantClient(
            url=url,
        )

    def create_collection(
        self,
        vector_size: int,
    ):

        collections = self.client.get_collections()

        names = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name in names:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upload(
        self,
        ids: list[str],
        vectors: list[list[float]],
        payloads: list[dict],
    ):

        points = []

        for point_id, vector, payload in zip(
            ids,
            vectors,
            payloads,
        ):

            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )