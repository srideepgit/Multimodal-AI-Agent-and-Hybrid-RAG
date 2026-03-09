from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
    )


class Source(BaseModel):

    document: str

    page: int | None = None

    section: str | None = None


class ChatResponse(BaseModel):

    answer: str

    sources: list[Source]

    confidence: float


class MultimodalChatResponse(ChatResponse):
    """
    Same shape as ChatResponse, plus a record of what was extracted
    from the non-text input so callers can see what the model
    actually "saw"/"heard" before it answered.
    """

    modality: str

    extracted_text: str