"""
Comprehensive Evaluator for the Fintech Chatbot.

This module unifies semantic, intent, and advanced quality metrics into a
single, robust evaluation system.
"""

import logging
import os
from typing import Optional

import pandas as pd
from sentence_transformers import SentenceTransformer, util
from textstat import flesch_reading_ease

from ..models.fintech_models import (
    BotResponse,
    CustomerQuery,
    EvaluationResult,
    FullEvaluationReport,
    Intent,
    Product,
    SummaryMetrics,
)
from ..services.prompt_service import PromptService

# --- Configuration ---
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG
logger = logging.getLogger(__name__)

# --- Constants ---
SIMILARITY_THRESHOLD = 0.7
CONFIDENCE_THRESHOLD = 0.8
DATASET_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "evaluation_dataset.csv"
)


class ComprehensiveEvaluator:
    """
    A unified evaluator that combines semantic, intent, and advanced quality metrics.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the ComprehensiveEvaluator.

        Args:
            model_name (str): The name of the sentence-transformer model to use.
        """
        try:
            self.model = SentenceTransformer(model_name)
            self.dataset = self._load_dataset()
            logger.info(
                f"SentenceTransformer model '{model_name}' loaded successfully."
            )
            logger.info(f"Evaluation dataset loaded with {len(self.dataset)} records.")
        except Exception as e:
            logger.error(f"Failed to initialize ComprehensiveEvaluator: {e}")
            raise

    def _load_dataset(self) -> pd.DataFrame:
        """Loads the evaluation dataset from the specified path."""
        try:
            df = pd.read_csv(DATASET_PATH)
            # Replace pandas' NaN with None for Pydantic compatibility
            return df.where(pd.notnull(df), None)
        except FileNotFoundError:
            logger.error(f"Evaluation dataset not found at {DATASET_PATH}")
            raise
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise

    def _calculate_semantic_similarity(
        self, generated_text: str, ideal_text: Optional[str]
    ) -> float:
        """Calculates semantic similarity between two texts."""
        if not ideal_text:
            return 0.0
        try:
            embedding1 = self.model.encode(generated_text, convert_to_tensor=True)
            embedding2 = self.model.encode(ideal_text, convert_to_tensor=True)
            cosine_scores = util.cos_sim(embedding1, embedding2)
            return cosine_scores.item()
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {e}")
            return 0.0

    def _calculate_empathy_score(self, text: str) -> float:
        """Calculates a nuanced empathy score."""
        score = 0.0
        if any(p in text.lower() for p in ["entiendo tu", "comprendo tu", "lamento"]):
            score += 0.5
        if any(p in text.lower() for p in ["me alegra", "qué bueno", "claro que sí"]):
            score += 0.25
        if "¡hola!" in text.lower():
            score += 0.25
        return min(1.0, score)

    def _calculate_clarity_score(self, text: str) -> float:
        """Calculates a more granular clarity score."""
        word_count = len(text.split())
        if 15 <= word_count <= 40:
            return 1.0
        if 10 <= word_count < 15 or 40 < word_count <= 50:
            return 0.75
        return 0.5

    def _calculate_actionability_score(self, text: str) -> float:
        """Calculates actionability based on clear next steps."""
        if "**próximos pasos:**" in text.lower():
            return 1.0
        if any(p in text.lower() for p in ["puedes", "te gustaría", "anímate a"]):
            return 0.5
        return 0.0

    def _calculate_professional_tone_score(self, text: str) -> float:
        """Calculates professional tone, penalizing hedging."""
        score = 1.0
        if any(p in text.lower() for p in ["creo que", "parece que", "podría ser"]):
            score -= 0.25
        if any(p in text.lower() for p in ["chao", "parce", "pues..."]):
            score -= 0.5
        return max(0.0, score)

    def _calculate_readability_score(self, text: str) -> float:
        """Calculates readability using Flesch Reading Ease score."""
        try:
            score = flesch_reading_ease(text)
            return max(0, min(1, score / 100.0))
        except Exception:
            return 0.0

    def _evaluate_confidence_alignment(
        self, response: BotResponse, query: CustomerQuery
    ) -> float:
        """Evaluates if the bot's confidence aligns with its performance."""
        if query.expected_intent is None or query.expected_product is None:
            return 0.0
        is_correct = (
            response.detected_intent == query.expected_intent
            and response.detected_product == query.expected_product
        )
        confidence = response.confidence
        if is_correct and confidence >= CONFIDENCE_THRESHOLD:
            return 1.0
        if not is_correct and confidence < CONFIDENCE_THRESHOLD:
            return 1.0
        return 0.0

    def evaluate_single_response(
        self, query: CustomerQuery, response: BotResponse
    ) -> EvaluationResult:
        """
        Performs a comprehensive evaluation of a single bot response.
        """
        similarity = self._calculate_semantic_similarity(
            response.response_text, query.ideal_response
        )

        # --- Calculate all metrics individually for clarity ---
        empathy_score = self._calculate_empathy_score(response.response_text)
        clarity_score = self._calculate_clarity_score(response.response_text)
        actionability_score = self._calculate_actionability_score(
            response.response_text
        )
        professional_tone_score = self._calculate_professional_tone_score(
            response.response_text
        )
        readability_score = self._calculate_readability_score(response.response_text)
        confidence_alignment = self._evaluate_confidence_alignment(response, query)

        # --- Debug Logging ---
        logger.info(f"--- Scores for Query: '{query.text[:40]}...' ---")
        logger.info(
            f"  - Empathy: {empathy_score:.2f}, Clarity: {clarity_score:.2f}, "
            f"Actionability: {actionability_score:.2f}"
        )
        logger.info(
            f"  - Professionalism: {professional_tone_score:.2f}, "
            f"Readability: {readability_score:.2f}"
        )
        logger.info(
            f"  - Confidence: {response.confidence:.2f}, "
            f"Alignment: {confidence_alignment:.2f}"
        )
        logger.info("-" * 30)

        result = EvaluationResult(
            query=query.text,
            generated_response=response.response_text,
            ideal_response=query.ideal_response or "",
            detected_intent=response.detected_intent or Intent.OTHER,
            expected_intent=query.expected_intent or Intent.OTHER,
            intent_correct=(response.detected_intent == query.expected_intent),
            detected_product=response.detected_product or Product.UNKNOWN,
            expected_product=query.expected_product or Product.UNKNOWN,
            product_correct=(response.detected_product == query.expected_product),
            semantic_similarity=similarity,
            is_semantically_similar=(similarity >= SIMILARITY_THRESHOLD),
            confidence=response.confidence,
            confidence_alignment=confidence_alignment,
            empathy=empathy_score,
            clarity=clarity_score,
            actionability=actionability_score,
            professional_tone=professional_tone_score,
            readability=readability_score,
        )
        return result

    def generate_report(self, results: list[EvaluationResult]) -> FullEvaluationReport:
        """
        Generates a summary report from a list of evaluation results.
        """
        total = len(results)
        if total == 0:
            return FullEvaluationReport(
                summary_metrics={},  # type: ignore
                detailed_results=[],
                logs=["No results to report."],
            )

        intent_accuracy = sum(r.intent_correct for r in results) / total
        product_accuracy = sum(r.product_correct for r in results) / total
        avg_semantic_similarity = sum(r.semantic_similarity for r in results) / total
        avg_confidence = sum(r.confidence for r in results) / total
        avg_confidence_alignment = sum(r.confidence_alignment for r in results) / total

        # Calculate averages for all quality metrics
        quality_keys = [
            "empathy",
            "clarity",
            "actionability",
            "professional_tone",
            "readability",
        ]
        avg_quality_scores = {
            f"average_{key}": sum(getattr(r, key, 0.0) for r in results) / total
            for key in quality_keys
        }

        summary_metrics = {
            "total_evaluated": total,
            "intent_accuracy": intent_accuracy,
            "product_accuracy": product_accuracy,
            "average_semantic_similarity": avg_semantic_similarity,
            "average_confidence": avg_confidence,
            "average_confidence_alignment": avg_confidence_alignment,
            **avg_quality_scores,
        }

        summary_metrics_model = SummaryMetrics(**summary_metrics)

        return FullEvaluationReport(
            summary_metrics=summary_metrics_model,
            detailed_results=results,
            logs=[f"Report generated for {total} items."],
        )

    async def run_full_evaluation(
        self, prompt_service: PromptService
    ) -> FullEvaluationReport:
        """
        Runs a full evaluation on the dataset.
        """
        logger.info("Generating responses for the full evaluation dataset...")

        # Clean up column names before creating CustomerQuery objects
        self.dataset.columns = self.dataset.columns.str.strip()

        # Map the CSV columns to the CustomerQuery model fields
        queries = []
        for row in self.dataset.to_dict(orient="records"):
            query = CustomerQuery(
                text=row["query"],  # Map 'query' column to 'text' field
                expected_intent=(
                    Intent(row["expected_intent"])
                    if row.get("expected_intent")
                    else None
                ),
                expected_product=(
                    Product(row["expected_product"])
                    if row.get("expected_product")
                    else None
                ),
                ideal_response=row.get("ideal_response"),
            )
            queries.append(query)

        bot_responses = [prompt_service.generate_response(q) for q in queries]

        logger.info("Evaluating responses...")
        evaluation_results = [
            self.evaluate_single_response(query, response)
            for query, response in zip(queries, bot_responses)
        ]

        logger.info("Generating final report...")
        return self.generate_report(evaluation_results)
