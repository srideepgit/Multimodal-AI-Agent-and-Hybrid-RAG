from app.agent.state import AgentState
from app.prompts.sql import SQL_PROMPT
from app.tools.calculator import CalculatorTool
from app.tools.knowledge import KnowledgeTool
from app.tools.sql import SQLTool


class AgentNodes:
    """
    All LangGraph node implementations for the enterprise agent.

    The "response engine" collaborators (context_builder, generator,
    citation_builder, confidence_scorer, validator) are optional
    constructor arguments so this class stays easy to unit test: tests
    can build an ``AgentNodes`` with only the tool/llm dependencies and
    then attach mocks for the response engine pieces. In production,
    ``app.api.dependencies`` wires all of them up.
    """

    def __init__(
        self,
        knowledge_tool: KnowledgeTool,
        sql_tool: SQLTool,
        calculator_tool: CalculatorTool,
        llm,
        context_builder=None,
        generator=None,
        citation_builder=None,
        confidence_scorer=None,
        validator=None,
        sql_schema_description: str = "",
    ):
        self.knowledge_tool = knowledge_tool
        self.sql_tool = sql_tool
        self.calculator_tool = calculator_tool
        self.llm = llm

        self.context_builder = context_builder
        self.generator = generator
        self.citation_builder = citation_builder
        self.confidence_scorer = confidence_scorer
        self.validator = validator

        self.sql_schema_description = sql_schema_description

    # ------------------------
    # Planner Node
    # ------------------------

    def planner_node(
        self,
        state: AgentState,
    ):

        question = state["question"].lower()

        if any(
            word in question
            for word in [
                "calculate",
                "+",
                "-",
                "*",
                "/",
                "%",
            ]
        ):
            state["tool"] = "calculator"

        elif any(
            word in question
            for word in [
                "employee",
                "salary",
                "department",
                "count",
                "database",
            ]
        ):
            state["tool"] = "sql"

        else:
            state["tool"] = "knowledge"

        return state

    # ------------------------
    # Knowledge Node
    # ------------------------

    def knowledge_node(
        self,
        state: AgentState,
    ):

        chunks = self.knowledge_tool.search(
            query=state["question"],
            top_k=5,
        )

        state["retrieved_chunks"] = chunks

        return state

    # ------------------------
    # SQL Node
    # ------------------------

    def sql_node(
        self,
        state: AgentState,
    ):
        """
        Generate a read-only SQL query with the LLM (when available)
        and execute it. Falls back to a safe default query if no LLM
        is configured, or if the LLM output cannot be used safely.
        """

        sql = None

        if self.llm is not None:
            try:
                prompt = SQL_PROMPT.format(
                    schema=self.sql_schema_description,
                    question=state["question"],
                )

                generated = self.llm.invoke(prompt)

                sql = self._clean_sql(generated)
            except Exception:
                # Never let a flaky/mocked LLM response take down the
                # whole request -- fall back to the safe default below.
                sql = None

        if not sql or not isinstance(sql, str) or not sql.strip().lower().startswith("select"):
            sql = "SELECT * FROM employees LIMIT 5"

        state["sql_query"] = sql

        rows = self.sql_tool.execute(sql)

        state["sql_result"] = rows

        return state

    @staticmethod
    def _clean_sql(raw_sql: str) -> str:
        """
        Strip markdown code fences / stray whitespace from LLM SQL output.
        """

        if not raw_sql:
            return ""

        cleaned = raw_sql.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.split("\n", 1)[-1] if "\n" in cleaned else cleaned

        cleaned = cleaned.replace("```sql", "").replace("```", "")

        return cleaned.strip().rstrip(";")

    # ------------------------
    # Calculator Node
    # ------------------------

    def calculator_node(
        self,
        state: AgentState,
    ):

        result = self.calculator_tool.calculate(
            state["question"]
        )

        state["calculator_result"] = result

        return state

    # ------------------------
    # Response Node
    # ------------------------

    def response_node(
        self,
        state: AgentState,
    ):

        # Build context
        context = self.context_builder.build(state)

        state["context"] = context

        # Generate answer
        answer = self.generator.generate(
            question=state["question"],
            context=context,
            sql_result=state["sql_result"],
            calculator_result=state["calculator_result"],
        )

        # Build citations
        citations = self.citation_builder.build(
            state["retrieved_chunks"]
        )

        # Calculate confidence
        confidence = self.confidence_scorer.calculate(
            state["retrieved_chunks"]
        )

        # Validate final response
        validated_response = self.validator.validate(
            {
                "answer": answer,
                "sources": citations,
                "confidence": confidence,
            }
        )

        # Update state
        state["answer"] = validated_response.answer
        state["citations"] = validated_response.sources
        state["confidence"] = validated_response.confidence

        return state

    # ------------------------
    # Validation Node
    # ------------------------

    def validation_node(
        self,
        state: AgentState,
    ):

        if not state["answer"]:
            raise ValueError(
                "Empty answer generated."
            )

        return state
