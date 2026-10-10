from pydantic import BaseModel, Field


class CompareRequest(BaseModel):
    query: str = Field(
        ...,
        description="User query to classify",
        min_length=1,
    )


class ClassificationResult(BaseModel):
    provider: str
    intent: str
    confidence: float
    latency_ms: float
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0


class CompareResponse(BaseModel):
    query: str
    jev: ClassificationResult
    gpt: ClassificationResult