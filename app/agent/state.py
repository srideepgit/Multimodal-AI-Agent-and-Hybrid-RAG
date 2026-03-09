from typing import Any

from typing_extensions import TypedDict


class AgentState(TypedDict):
    """
    Shared state across all LangGraph nodes.
    """

    # -------------------------
    # User Input
    # -------------------------

    question: str

    chat_history: list[dict[str, str]]

    # -------------------------
    # Planner
    # -------------------------

    tool: str

    # -------------------------
    # Knowledge Tool
    # -------------------------

    retrieved_chunks: list[Any]

    # -------------------------
    # SQL Tool
    # -------------------------

    sql_query: str

    sql_result: list[dict]

    # -------------------------
    # Calculator Tool
    # -------------------------

    calculator_expression: str

    calculator_result: float | None

    # -------------------------
    # Final Context
    # -------------------------

    context: str

    # -------------------------
    # LLM Output
    # -------------------------

    answer: str

    citations: list[dict]

    confidence: float

    # -------------------------
    # Errors
    # -------------------------

    error: str | None