# Chunks Text -> Vector

from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    """
    Generates embeddings for text.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
    ):
        self.model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            },
        )

    def embed_text(self, text: str) -> list[float]:
        """
        Generate embedding for one text.
        """
        return self.model.embed_query(text)

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        return self.model.embed_documents(texts)