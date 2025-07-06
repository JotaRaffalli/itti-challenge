"""FastAPI application for ITTI backend - Prompt Engineering Demo."""

import logging
import sys
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from .models.fintech_models import BotResponse, CustomerQuery, FullEvaluationReport
from .services.evaluator import SemanticEvaluator, SimpleEvaluator
from .services.prompt_service import PromptService

# --- App Configuration ---
app = FastAPI(
    title="ITTI Prompt Engineering Demo",
    description=(
        "A sophisticated API for evaluating and interacting with a financial AI "
        "assistant. Demonstrates advanced prompt engineering, automated "
        "evaluation, and best practices."
    ),
    version="2.0.0",
)

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,  # Direct logs to stdout
)


# --- Dependency Injection ---
PromptServiceDep = Annotated[PromptService, Depends(PromptService)]
SimpleEvaluatorDep = Annotated[SimpleEvaluator, Depends(SimpleEvaluator)]
SemanticEvaluatorDep = Annotated[SemanticEvaluator, Depends(SemanticEvaluator)]


# --- API Endpoints ---


@app.get("/", tags=["General"])
async def root():
    """Root endpoint with service status and available endpoints."""
    return {
        "message": "ITTI Prompt Engineering Demo v2.0 - Running",
        "status": "healthy",
        "endpoints": {
            "chat": "/chat",
            "single_test": "/testing/run-single",
            "full_evaluation": "/evaluation/run-full-dataset",
        },
    }


@app.post("/chat", tags=["Interaction"], response_model=BotResponse)
async def chat_endpoint(query: CustomerQuery, prompt_service: PromptServiceDep):
    """Handles a single user interaction with the financial AI assistant."""
    try:
        return prompt_service.generate_response(query)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {e}"
        ) from e


@app.post("/testing/run-single", tags=["Testing & Evaluation"])
async def test_single_prompt(
    query: CustomerQuery,
    prompt_service: PromptServiceDep,
    evaluator: SimpleEvaluatorDep,
):
    """Tests a single query and provides a quick, heuristic evaluation."""
    try:
        response = prompt_service.generate_response(query)
        evaluation = evaluator.evaluate_response(query, response)
        return {"response": response, "evaluation": evaluation}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {e}"
        ) from e


@app.post(
    "/evaluation/run-full-dataset",
    tags=["Testing & Evaluation"],
    response_model=FullEvaluationReport,
    summary="Run full semantic evaluation on the dataset",
)
async def run_full_evaluation(
    prompt_service: PromptServiceDep, evaluator: SemanticEvaluatorDep
):
    """
    Processes the entire internal dataset, generates responses for each query,
    and returns a full semantic evaluation report.

    This endpoint is ideal for getting a comprehensive overview of the model's
    performance on a predefined set of test cases.
    """
    try:
        logging.info("Starting full dataset evaluation...")
        # 1. Get all queries from the evaluator's dataset
        dataset = evaluator.dataset
        queries = [CustomerQuery(message=q) for q in dataset["query"]]

        # 2. Generate responses for all queries
        generated_responses: list[BotResponse] = []
        for query in queries:
            response = prompt_service.generate_response(query)
            generated_responses.append(response)
        logging.info(f"Generated {len(generated_responses)} responses.")

        # 3. Evaluate the batch of responses
        evaluation_report = evaluator.evaluate_batch(generated_responses)
        logging.info("Batch evaluation complete.")

        return evaluation_report

    except FileNotFoundError as e:
        logging.error(f"Evaluation dataset not found: {e}", exc_info=True)
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        ) from e


# To run the app locally: uvicorn itti_backend.main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
