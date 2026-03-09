from pydantic import BaseModel, Field, ValidationError


class ResponseSchema(BaseModel):
    answer: str
    sources: list = Field(default_factory=list)
    confidence: float


class ResponseValidator:

    def validate(
        self,
        response: dict,
    ) -> ResponseSchema:

        return ResponseSchema.model_validate(response)