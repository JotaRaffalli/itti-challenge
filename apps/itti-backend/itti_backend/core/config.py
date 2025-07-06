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
    """

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_PROJECT: str = "VuelaConNosotros-Demo"

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate settings to be used throughout the application
settings = Settings()

# Set environment variables for LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = str(settings.LANGCHAIN_TRACING_V2)
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
