from pydantic import BaseModel


class PlannerOutput(BaseModel):

    tool: str