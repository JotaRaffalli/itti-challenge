"""Agent to handle flight status inquiries."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from ..core.config import settings
from .base_agent import BaseAgent
from .tools import get_flight_status


class FlightStatusAgent(BaseAgent):
    """
    Agent responsible for handling inquiries about flight status.

    This agent adheres to the Single Responsibility Principle by focusing
    solely on flight status-related tasks.
    """

    def __init__(self):
        """Initializes the FlightStatusAgent."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7,
        )

    def run(self, state: dict) -> dict:
        """
        Executes the flight status inquiry logic.

        Args:
            state: The current conversation state.

        Returns:
            The updated state with the agent's response.
        """
        print("--- Running Flight Status Agent ---")
        user_message = state.get("current_message", "")

        # Simple entity extraction (in a real scenario, use a proper NER model)
        flight_number = self._extract_flight_number(user_message)

        if not flight_number:
            response = "Por favor, indícame el número de vuelo que deseas consultar."
        else:
            try:
                tool_result = get_flight_status.invoke({"flight_number": flight_number})
                response = self._generate_response(tool_result)
            except Exception as e:
                print(f"Error calling get_flight_status tool: {e}")
                response = "Lo siento, tuve un problema al consultar el estado del vuelo. Por favor, intenta de nuevo."

        return {"agent_response": response}

    def _extract_flight_number(self, text: str) -> str | None:
        """Extracts a flight number from the text."""
        import re

        match = re.search(r"[A-Z]{2}\d{3,4}", text.upper())
        return match.group(0) if match else None

    def _generate_response(self, tool_result: dict) -> str:
        """Generates a user-friendly response based on the tool's output."""
        prompt = ChatPromptTemplate.from_template(
            """
            Eres un asistente de aerolínea amable y servicial.
            Tu tarea es informar al usuario sobre el estado de su vuelo de manera clara y concisa.

            Contexto de la herramienta:
            {context}

            Basado en el contexto, genera una respuesta amigable para el usuario.
            Si el vuelo está a tiempo, informa la hora de salida y llegada.
            Si el vuelo no fue encontrado, informa al usuario amablemente.
            """
        )
        chain = prompt | self.llm
        response = chain.invoke({"context": str(tool_result)})
        return response.content.strip()
