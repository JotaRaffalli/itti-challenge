"""Prompt engineering service using LangChain."""

import json
import logging
import re
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from ..models.fintech_models import BotResponse, CustomerQuery, ExtractedData

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptService:
    """Service for prompt engineering with real LLM integration."""

    def __init__(self, llm_client: BaseChatModel):
        """Initialize the prompt service with a LangChain LLM client."""
        try:
            self.llm_client = llm_client
            self.system_prompt = self._load_system_prompt()
            logger.info("PromptService initialized successfully.")
        except (ValueError, FileNotFoundError) as e:
            logger.error(f"Failed to initialize PromptService: {e}")
            raise

    def _load_system_prompt(self) -> str:
        """Loads the system prompt from the XML file."""
        try:
            prompt_path = Path(__file__).parent.parent / "prompts" / "system_prompt.xml"
            with open(prompt_path, encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"System prompt file not found at {prompt_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading system prompt: {e}")
            raise

    def _extract_json_from_response(self, text: str) -> Optional[dict]:
        """Extracts the first valid JSON block from the LLM's text response."""
        # Regex to find JSON block enclosed in ```json ... ```
        match = re.search(r"```json\s*({.*?})\s*```", text, re.DOTALL)
        if not match:
            logger.warning("No JSON block found in the response.")
            return None

        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(
                f"Error decoding JSON from response: {e}\nResponse text: {text}"
            )
            return None

    def _extract_reasoning(self, text: str) -> Optional[str]:
        """Extracts the reasoning section from the LLM's text response."""
        # Use regex to find the reasoning text before the json block
        match = re.search(
            r"\*\*RAZONAMIENTO:\*\*(.*?)(?=```json)",
            text,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            return match.group(1).strip()
        logger.warning("Reasoning section not found in the response.")
        return None

    def generate_response(self, query: CustomerQuery) -> BotResponse:
        """Generate a response to a customer query using the LLM."""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=query.text),
        ]

        try:
            logger.info(f"Sending query to LLM: {query.text}")
            response = self.llm_client.invoke(messages)
            content = response.content

            if not isinstance(content, str):
                err_msg = f"Expected string response from LLM, but got {type(content)}"
                raise TypeError(err_msg)

            logger.info(f"Received response from LLM: {content}")

            # Extract structured data and reasoning
            json_data = self._extract_json_from_response(content)
            reasoning = self._extract_reasoning(content)
            if not json_data:
                # Fallback if JSON extraction fails
                return BotResponse(
                    original_query=query.text,
                    response_text="No pude procesar la estructura de la respuesta.",
                    reasoning="Fallo en la extracción de JSON.",
                    detected_intent=None,
                    detected_product=None,
                    confidence=0.0,
                )

            # Use Pydantic to parse and validate the extracted data
            try:
                extracted_data = ExtractedData.parse_obj(json_data)
            except Exception as e:
                logger.error(f"Pydantic validation failed: {e}")
                return BotResponse(
                    original_query=query.text,
                    response_text=(
                        "La respuesta del modelo no tiene el formato esperado."
                    ),
                    reasoning=f"Error de validación de Pydantic: {e}",
                    detected_intent=None,
                    detected_product=None,
                    confidence=0.0,
                )

            # The user-facing response is now composed of the response and next steps
            final_response_text = (
                f"{extracted_data.response}\n\n"
                f"**Próximos Pasos:**\n{extracted_data.next_steps}"
            )

            return BotResponse(
                original_query=query.text,
                response_text=final_response_text,
                detected_intent=extracted_data.intent,
                detected_product=extracted_data.product,
                confidence=extracted_data.confidence,
                reasoning=reasoning or "No reasoning provided.",
            )

        except Exception as e:
            logger.error(f"Error generating response from LLM: {e}", exc_info=True)
            return BotResponse(
                original_query=query.text,
                response_text=(
                    "Lo siento, ocurrió un error inesperado al procesar tu solicitud."
                ),
                reasoning=f"Excepción: {e}",
                detected_intent=None,
                detected_product=None,
                confidence=0.0,
            )
