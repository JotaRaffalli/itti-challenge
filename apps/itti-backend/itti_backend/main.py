"""FastAPI application for ITTI backend - Prompt Engineering Demo."""

import logging
import sys
from functools import lru_cache
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from langchain_core.language_models.chat_models import BaseChatModel

from .api import chatbot_routes

# Correct relative imports
from .models.fintech_models import (
    BotResponse,
    CustomerQuery,
    FullEvaluationReport,
)
from .services.comprehensive_evaluator import ComprehensiveEvaluator
from .services.llm_service import get_llm_client
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

# --- VuelaConNosotros Chatbot Router ---
app.include_router(chatbot_routes.router, prefix="/vuelaconnosotros")


# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,  # Direct logs to stdout
)


# --- Dependency Injection ---
@lru_cache
def get_llm() -> BaseChatModel:
    """Provides a cached singleton instance of the LLM client."""
    return get_llm_client()


def get_prompt_service(
    llm: Annotated[BaseChatModel, Depends(get_llm)],
) -> PromptService:
    """Provides an instance of the PromptService."""
    return PromptService(llm_client=llm)


def get_evaluator(
    llm: Annotated[BaseChatModel, Depends(get_llm)],
) -> ComprehensiveEvaluator:
    """Provides an instance of the ComprehensiveEvaluator."""
    return ComprehensiveEvaluator(llm_client=llm)


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
async def run_single_evaluation(
    query: CustomerQuery, evaluator: ComprehensiveEvaluatorDep
):
    """Runs a single evaluation and returns the report."""
    try:
        # This endpoint requires a prompt_service instance to generate the response
        # before evaluating it. We can get it from the dependency system.
        prompt_service = get_prompt_service(llm=evaluator.llm_client)
        bot_response = prompt_service.generate_response(query)
        evaluation_result = evaluator.evaluate_single_response(query, bot_response)
        return evaluator.generate_report([evaluation_result])
    except Exception as e:
        logging.error(f"Error in single evaluation endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@app.post(
    "/evaluation/run-full-dataset",
    tags=["Testing & Evaluation"],
    response_model=FullEvaluationReport,
    summary="Run full evaluation on the dataset",
)
async def run_full_evaluation_endpoint(
    evaluator: ComprehensiveEvaluatorDep, prompt_service: PromptServiceDep
):
    """Runs a full evaluation on the dataset and returns the report."""
    try:
        # Ensure both services use the same LLM instance
        report = await evaluator.run_full_evaluation(prompt_service=prompt_service)
        return report
    except Exception as e:
        logging.error(f"Error in full evaluation endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


# To run the app locally: uvicorn itti_backend.main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
