"""LLM Service for creating and managing language model clients."""

import os

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

# Load environment variables from .env file for local development
load_dotenv()


def get_llm_client() -> BaseChatModel:
    """
    Initializes and returns the appropriate LLM client based on environment variables.

    Selects the provider based on the LLM_PROVIDER environment variable.
    Defaults to 'gemini' if not set.

    Supported providers:
    - 'gemini': Uses Google's Gemini Pro model. Requires GOOGLE_API_KEY.
    - 'openai': Uses OpenAI's GPT-4 model. Requires OPENAI_API_KEY.

    Raises:
        ValueError: If the provider is unsupported or the required API key is missing.

    Returns:
        An instance of a LangChain chat model
        (e.g., ChatGoogleGenerativeAI or ChatOpenAI).
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    print(f"Using LLM provider: {provider}")
    model_name = os.getenv(f"{provider.upper()}_MODEL")

    if provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        return ChatGoogleGenerativeAI(
            model=model_name or "gemini-2.0-flash",
            google_api_key=api_key,
        )

    elif provider == "openai":
        # Ensure the OpenAI API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        return ChatOpenAI(model=model_name or "gpt-4-turbo", api_key=SecretStr(api_key))

    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}. "
            f"Supported providers are 'gemini' and 'openai'."
        )
