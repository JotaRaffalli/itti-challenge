"""Simple evaluation service for prompt responses."""

from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from ..models.fintech_models import (
    BotResponse,
    CustomerQuery,
    DetailedResult,
    EvaluationResult,
    FullEvaluationReport,
    SummaryMetrics,
)


class SemanticEvaluator:
    """Evaluator based on semantic similarity and a ground-truth dataset."""

    def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        """Initialize the evaluator with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        dataset_path = Path(__file__).parent.parent / "data" / "evaluation_dataset.csv"
        self.dataset = self._load_dataset(dataset_path)

    def _load_dataset(self, path: Path) -> pd.DataFrame:
        """Load the evaluation dataset from a CSV file."""
        if not path.exists():
            raise FileNotFoundError(f"Evaluation dataset not found at {path}")
        return pd.read_csv(path)

    def evaluate_batch(
        self, generated_responses: list[BotResponse]
    ) -> FullEvaluationReport:
        """
        Evaluate a batch of generated responses against the ground-truth dataset.
        """
        if not generated_responses:
            # Return a valid empty report
            return FullEvaluationReport(
                summary_metrics=SummaryMetrics(total_evaluated=0),
                detailed_results=[],
            )

        response_map = {resp.original_query: resp for resp in generated_responses}
        queries_to_eval = [resp.original_query for resp in generated_responses]
        eval_df = self.dataset[self.dataset["query"].isin(queries_to_eval)].copy()

        if eval_df.empty:
            return FullEvaluationReport(
                summary_metrics=SummaryMetrics(total_evaluated=0),
                detailed_results=[],
            )

        generated_texts = [response_map[q].response_text for q in eval_df["query"]]
        ideal_texts = eval_df["ideal_response"].tolist()
        eval_df["generated_response"] = generated_texts

        generated_embeddings = self.model.encode(generated_texts)
        ideal_embeddings = self.model.encode(ideal_texts)
        similarities = cosine_similarity(generated_embeddings, ideal_embeddings)

        eval_df["semantic_similarity"] = pd.Series(
            np.diag(similarities), index=eval_df.index
        ).replace([np.inf, -np.inf], np.nan)

        eval_df["detected_intent"] = [
            resp.detected_intent.value if resp.detected_intent else None
            for resp in (response_map[q] for q in eval_df["query"])
        ]
        eval_df["detected_product"] = [
            resp.detected_product.value if resp.detected_product else None
            for resp in (response_map[q] for q in eval_df["query"])
        ]

        eval_df["intent_correct"] = (
            eval_df["detected_intent"].str.lower()
            == eval_df["expected_intent"].str.lower()
        )
        eval_df["product_correct"] = (
            eval_df["detected_product"].str.lower()
            == eval_df["expected_product"].str.lower()
        )

        # Calculate metrics, handling potential NaNs from empty series
        intent_accuracy = eval_df["intent_correct"].mean()
        product_accuracy = eval_df["product_correct"].mean()
        avg_similarity = eval_df["semantic_similarity"].mean()

        summary = SummaryMetrics(
            total_evaluated=len(eval_df),
            intent_accuracy=intent_accuracy if pd.notna(intent_accuracy) else None,
            product_accuracy=product_accuracy if pd.notna(product_accuracy) else None,
            average_semantic_similarity=(
                avg_similarity if pd.notna(avg_similarity) else None
            ),
        )

        # Replace all remaining NaNs in the DataFrame with None for Pydantic
        eval_df.replace({np.nan: None}, inplace=True)
        detailed_results_data = eval_df[
            [
                "query",
                "generated_response",
                "ideal_response",
                "semantic_similarity",
                "detected_intent",
                "expected_intent",
                "intent_correct",
                "detected_product",
                "expected_product",
                "product_correct",
            ]
        ].to_dict(orient="records")

        detailed_results = [
            DetailedResult(**{str(k): v for k, v in record.items()})
            for record in detailed_results_data
        ]

        return FullEvaluationReport(
            summary_metrics=summary, detailed_results=detailed_results
        )


class SimpleEvaluator:
    """Simple evaluator for bot responses."""

    def evaluate_response(
        self, query: CustomerQuery, response: BotResponse
    ) -> EvaluationResult:
        """Evaluate a single response and provide actionable feedback."""
        score = 0.0
        strengths = []
        improvements = []

        # Check if response has proper structure
        if "**RAZONAMIENTO:**" in response.response_text:
            score += 0.25
            strengths.append("Incluye razonamiento explicado")
        else:
            improvements.append(
                "No se encontró la sección '**RAZONAMIENTO:**'. "
                "El modelo debe explicar sus conclusiones."
            )

        # Check if JSON block is present
        if "```json" in response.response_text:
            score += 0.25
            strengths.append("Incluye bloque de código JSON con datos estructurados")
        else:
            improvements.append(
                "No se encontró un bloque de código JSON. "
                "El modelo debe devolver la intención y el producto en formato JSON."
            )

        # Check if intent and product were detected
        if response.detected_intent:
            score += 0.25
            strengths.append(
                f"Intención detectada correctamente: {response.detected_intent.value}"
            )
        else:
            improvements.append(
                "No se pudo extraer la intención del bloque JSON o el bloque no existe."
            )

        if response.detected_product:
            score += 0.25
            strengths.append(
                f"Producto detectado correctamente: {response.detected_product.value}"
            )
        else:
            improvements.append(
                "No se pudo extraer el producto del bloque JSON o el bloque no existe."
            )

        # Final evaluation
        if not improvements:
            feedback = (
                "¡Excelente respuesta! El modelo sigue todas las "
                "instrucciones del prompt."
            )
        else:
            feedback = (
                "La respuesta es parcialmente correcta, pero necesita mejoras. "
                "Consulta las siguientes recomendaciones."
            )

        return EvaluationResult(
            query=query.message,
            response=response.response_text,
            score=score,
            feedback=feedback,
            strengths=strengths,
            improvements=improvements,
        )
