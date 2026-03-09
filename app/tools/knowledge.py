from app.rag.retrieval.retriever import EnterpriseRetriever


class KnowledgeTool:

    def __init__(
        self,
        retriever: EnterpriseRetriever,
    ):
        self.retriever = retriever

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):

        results = self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        return results