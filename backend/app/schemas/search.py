from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request payload for document-grounded chat.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Question to answer using workspace documents.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of document chunks to retrieve.",
    )


class ChatSource(BaseModel):
    """
    Source document chunk used to generate an answer.
    """

    document_id: int
    chunk_id: int
    filename: str
    chunk_index: int
    score: float


class ChatResponse(BaseModel):
    """
    Grounded answer and supporting document sources.
    """

    answer: str
    sources: list[ChatSource]