from app.prompts.response import RESPONSE_PROMPT


class ResponseGenerator:
    """
    Generates the final answer using the LLM.
    """

    def __init__(self, llm):
        self.llm = llm

    def generate(
        self,
        question: str,
        context: str,
        sql_result=None,
        calculator_result=None,
    ) -> str:

        prompt = RESPONSE_PROMPT.format(
            question=question,
            context=context,
            sql_result=sql_result,
            calculator_result=calculator_result,
        )

        response = self.llm.invoke(prompt)

        return response