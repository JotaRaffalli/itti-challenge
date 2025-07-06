"""FastAPI application for ITTI backend - Prompt Engineering Demo."""

import logging
import sys
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException

# Correct relative imports
from .models.fintech_models import (
    BotResponse,
    CustomerQuery,
    FullEvaluationReport,
)
from .services.comprehensive_evaluator import ComprehensiveEvaluator
from .services.prompt_service import PromptService

# Load environment variables from .env file
load_dotenv()

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
def get_prompt_service():
    """Provides a singleton instance of the PromptService."""
    return PromptService()


def get_evaluator():
    """Provides a singleton instance of the ComprehensiveEvaluator."""
    return ComprehensiveEvaluator()


# --- Type Hinting for Dependencies ---
PromptServiceDep = Annotated[PromptService, Depends(get_prompt_service)]
ComprehensiveEvaluatorDep = Annotated[ComprehensiveEvaluator, Depends(get_evaluator)]


# --- API Endpoints ---


@app.get("/", tags=["General"], summary="Root endpoint to check API status")
def read_root():
    """Returns a welcome message indicating the API is running."""
    return {
        "message": "ITTI Prompt Engineering Demo v2.0 - Running",
        "status": "healthy",
        "endpoints": {
            "chat": "/chat",
            "single_test": "/testing/run-single",
            "full_evaluation": "/evaluation/run-full-dataset",
        },
    }


@app.post(
    "/chat",
    tags=["Interaction"],
    response_model=BotResponse,
    summary="Invoke the chatbot with a single query",
)
async def chat_endpoint(query: CustomerQuery, prompt_service: PromptServiceDep):
    """Receives a customer query and returns the bot's response."""
    try:
        return prompt_service.generate_response(query)
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@app.post(
    "/testing/run-single",
    tags=["Testing & Evaluation"],
    response_model=FullEvaluationReport,
    summary="Run a single evaluation",
)
def run_single_evaluation(
    query: CustomerQuery,
    prompt_service: PromptServiceDep,
    evaluator: ComprehensiveEvaluatorDep,
):
    """Runs a comprehensive evaluation on a single query."""
    try:
        bot_response = prompt_service.generate_response(query)
        result = evaluator.evaluate_single_response(query, bot_response)
        report = evaluator.generate_report([result])
        return report
    except Exception as e:
        logging.error(f"Error during single evaluation: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@app.post(
    "/evaluation/run-full-dataset",
    tags=["Testing & Evaluation"],
    response_model=FullEvaluationReport,
    summary="Run full evaluation on the dataset",
)
async def run_full_evaluation(
    evaluator: ComprehensiveEvaluatorDep, prompt_service: PromptServiceDep
):
    """
    Triggers a full evaluation of the chatbot using the predefined dataset.
    This is a long-running process.
    """
    try:
        logging.info("Starting full dataset evaluation...")
        # Pass the prompt_service to the evaluator
        report = await evaluator.run_full_evaluation(prompt_service)
        logging.info("Full dataset evaluation completed.")
        return report
    except Exception as e:
        logging.error(f"Error during full evaluation: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


# To run the app locally: uvicorn itti_backend.main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
