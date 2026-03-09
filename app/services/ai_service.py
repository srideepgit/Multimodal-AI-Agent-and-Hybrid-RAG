from typing import Any


class AIService:
    """
    Thin façade over the compiled agent graph.

    ``graph`` is the object returned by
    ``EnterpriseAgentGraph.build()`` (a compiled LangGraph graph),
    not the ``EnterpriseAgentGraph`` wrapper itself.
    """

    def __init__(self, graph: Any):

        self.graph = graph

    def chat(
        self,
        question: str,
    ):

        state = {
            "question": question,
            "chat_history": [],
            "tool": "",
            "retrieved_chunks": [],
            "sql_query": "",
            "sql_result": [],
            "calculator_expression": "",
            "calculator_result": None,
            "context": "",
            "answer": "",
            "citations": [],
            "confidence": 0.0,
            "error": None,
        }

        result = self.graph.invoke(state)

        return {
            "answer": result["answer"],
            "sources": result["citations"],
            "confidence": result["confidence"],
        }
