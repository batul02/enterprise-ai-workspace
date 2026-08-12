from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=1000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class SearchResult(BaseModel):
    chunk_id: int
    content: str
    score: float
    document_id: int
    page_number: int | None = None
    filename: str


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]