"""Simple models for ITTI backend application."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator


class ProductType(str, Enum):
    """Types of financial products."""

    DEBIT_CARD = "DEBIT_CARD"
    CREDIT_CARD = "CREDIT_CARD"
    LOAN = "LOAN"
    UNKNOWN = "UNKNOWN"


class QueryIntent(str, Enum):
    """Intent classification for customer queries."""

    BENEFITS = "BENEFITS"
    REQUIREMENTS = "REQUIREMENTS"
    FEES_RATES = "FEES_RATES"
    APPLICATION_PROCESS = "APPLICATION_PROCESS"
    GENERAL = "GENERAL"
    OTHER = "OTHER"


class ExtractedData(BaseModel):
    """Structured data extracted from the LLM response."""

    intent: QueryIntent = Field(
        ..., description="The classified intent of the user's query."
    )
    product: ProductType = Field(
        ..., description="The specific product the user is asking about."
    )
    confidence: float = Field(
        ...,
        description="The confidence score (0.0 to 1.0) of the classification.",
        ge=0.0,
        le=1.0,
    )
    response: str = Field(
        ...,
        description=(
            "The user-facing response, written in a helpful and empathetic tone."
        ),
    )
    next_steps: str = Field(
        ..., description="A clear and concise call to action for the user."
    )

    @validator("intent", pre=True, allow_reuse=True)
    def map_intent(cls, v):
        """Map raw string from LLM to QueryIntent enum."""
        if isinstance(v, str):
            v = v.upper().strip()  # Convert to uppercase to match enum values
        return (
            QueryIntent(v) if v in QueryIntent._value2member_map_ else QueryIntent.OTHER
        )

    @validator("product", pre=True, allow_reuse=True)
    def map_product(cls, v):
        """Map raw string from LLM to ProductType enum."""
        if isinstance(v, str):
            v = v.upper().strip()  # Convert to uppercase to match enum values
        return (
            ProductType(v)
            if v in ProductType._value2member_map_
            else ProductType.UNKNOWN
        )


class CustomerQuery(BaseModel):
    """Customer query model."""

    message: str = Field(..., min_length=1, max_length=2000)
    user_id: str = Field(default="anonymous")


class BotResponse(BaseModel):
    """Bot response model."""

    original_query: str
    response_text: str
    detected_intent: Optional[QueryIntent] = None
    detected_product: Optional[ProductType] = Field(
        None, description="The detected product of the query."
    )
    reasoning: Optional[str] = Field(
        None, description="The reasoning behind the bot's response."
    )
    confidence: Optional[float] = Field(
        None, description="The confidence score of the intent detection."
    )


class EvaluationResult(BaseModel):
    """Simple evaluation result."""

    query: str
    response: str
    score: float
    feedback: str
    strengths: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)


class SummaryMetrics(BaseModel):
    """Metrics for the full evaluation report."""

    total_evaluated: int
    intent_accuracy: Optional[float] = None
    product_accuracy: Optional[float] = None
    average_semantic_similarity: Optional[float] = None


class DetailedResult(BaseModel):
    """Detailed result for a single query in the evaluation report."""

    query: str
    generated_response: str
    ideal_response: str
    semantic_similarity: Optional[float] = None
    detected_intent: Optional[str] = None
    expected_intent: Optional[str] = None
    intent_correct: bool
    detected_product: Optional[str] = None
    expected_product: Optional[str] = None
    product_correct: bool


class FullEvaluationReport(BaseModel):
    """Full evaluation report model."""

    summary_metrics: SummaryMetrics
    detailed_results: list[DetailedResult]
