"""Core configuration for the VuelaConNosotros chatbot."""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Manages application settings and environment variables using Pydantic.

    Attributes:
        GEMINI_API_KEY (str): API key for Google Gemini.
        LANGCHAIN_API_KEY (str): API key for LangSmith.
        LANGCHAIN_TRACING_V2 (bool): Enables LangSmith tracing.
        LANGCHAIN_PROJECT (str): The project name for LangSmith tracing.
        LLM_PROVIDER (str): The LLM provider to use.
        LANGSMITH_TRACING (bool): Enables LangSmith tracing (alternative).
        LANGSMITH_ENDPOINT (str): LangSmith API endpoint.
    """

    # --- LLM Provider Settings ---
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # --- Model Configuration ---
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.1))

    # --- LangSmith Tracing (optional) ---
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_PROJECT: str = "VuelaConNosotros-Demo"
    LANGSMITH_TRACING: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    LANGSMITH_ENDPOINT: str = os.getenv(
        "LANGSMITH_ENDPOINT", "https://api.smith.langchain.com"
    )

    class Config:
        """Pydantic configuration."""

        extra = "ignore"  # Ignore extra fields from .env
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate settings to be used throughout the application
settings = Settings()

# Set environment variables for LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = str(settings.LANGCHAIN_TRACING_V2)
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
os.environ["LANGSMITH_TRACING"] = str(settings.LANGSMITH_TRACING)
os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
