from app.prompts.planner import PLANNER_PROMPT

from app.planner.schema import PlannerOutput


class Planner:

    def __init__(self, llm):

        self.llm = llm

    def plan(
        self,
        question: str,
    ) -> PlannerOutput:

        prompt = PLANNER_PROMPT.format(

            question=question

        )

        response = self.llm.invoke(

            prompt
        )

        return PlannerOutput.model_validate_json(

            response
        )