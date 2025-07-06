"""Pydantic models for the ITTI Fintech Chatbot API."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Product(str, Enum):
    """Types of financial products."""

    DEBIT_CARD = "DEBIT_CARD"
    CREDIT_CARD = "CREDIT_CARD"
    LOAN = "LOAN"
    UNKNOWN = "UNKNOWN"


class Intent(str, Enum):
    """Intent classification for customer queries."""

    BENEFITS = "BENEFITS"
    REQUIREMENTS = "REQUIREMENTS"
    FEES_RATES = "FEES_RATES"
    APPLICATION_PROCESS = "APPLICATION_PROCESS"
    GENERAL = "GENERAL"
    OTHER = "OTHER"


class CustomerQuery(BaseModel):
    """Model for a customer's query, including ground truth for evaluation."""

    customer_id: str = Field(default="anonymous", description="Unique ID for the user.")
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's query text.",
    )
    expected_intent: Optional[Intent] = Field(
        None, description="The ground truth intent for evaluation."
    )
    expected_product: Optional[Product] = Field(
        None, description="The ground truth product for evaluation."
    )
    ideal_response: Optional[str] = Field(
        None, description="The ideal response for semantic comparison."
    )


class BotResponse(BaseModel):
    """Bot response model, containing the generated text and extracted data."""

    original_query: str
    response_text: str
    detected_intent: Optional[Intent]
    detected_product: Optional[Product]
    confidence: float
    reasoning: Optional[str] = None


class ExtractedData(BaseModel):
    """Model for structured data extracted from LLM responses."""

    intent: Intent
    product: Product
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence score between 0 and 1"
    )
    response: str = Field(description="The main response text")
    next_steps: str = Field(description="Suggested next steps for the customer")


class EvaluationResult(BaseModel):
    """Comprehensive evaluation result for a single interaction."""

    # Core Details
    query: str
    generated_response: str
    ideal_response: str

    # Intent & Product Accuracy
    detected_intent: Intent
    expected_intent: Intent
    intent_correct: bool
    detected_product: Product
    expected_product: Product
    product_correct: bool

    # Semantic & Confidence Metrics
    semantic_similarity: float
    is_semantically_similar: bool
    confidence: float = 0.0
    confidence_alignment: float = 0.0

    # Advanced Quality Metrics (Likert-style)
    empathy: float = 0.0
    clarity: float = 0.0
    actionability: float = 0.0
    professional_tone: float = 0.0
    readability: float = 0.0


class SummaryMetrics(BaseModel):
    total_evaluated: int
    intent_accuracy: float
    product_accuracy: float
    average_semantic_similarity: float
    average_confidence: float = 0.0
    average_confidence_alignment: float = 0.0
    average_empathy: float = 0.0
    average_clarity: float = 0.0
    average_actionability: float = 0.0
    average_professional_tone: float = 0.0
    average_readability: float = 0.0


class FullEvaluationReport(BaseModel):
    """The full report containing summary metrics and detailed results."""

    summary_metrics: SummaryMetrics
    detailed_results: list[EvaluationResult]
    logs: list[str] = []
