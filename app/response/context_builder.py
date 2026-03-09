from app.agent.state import AgentState


class ContextBuilder:

    def build(
        self,
        state: AgentState,
    ) -> str:

        context = []

        # -------------------------
        # Knowledge
        # -------------------------

        if state["retrieved_chunks"]:

            context.append("Knowledge Context:\n")

            for chunk in state["retrieved_chunks"]:

                if hasattr(chunk, "text"):
                    context.append(chunk.text)

                elif isinstance(chunk, dict):
                    context.append(
                        chunk.get("text", "")
                    )

        # -------------------------
        # SQL
        # -------------------------

        if state["sql_result"]:

            context.append("\nSQL Result:\n")

            context.append(
                str(state["sql_result"])
            )

        # -------------------------
        # Calculator
        # -------------------------

        if state["calculator_result"] is not None:

            context.append(
                "\nCalculator Result:\n"
            )

            context.append(
                str(state["calculator_result"])
            )

        return "\n".join(context)