"""Agent to handle flight change requests."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from ..core.config import settings
from .base_agent import BaseAgent
from .tools import check_flight_availability, get_flight_details


class FlightChangeAgent(BaseAgent):
    """
    Agent for handling flight change requests.

    This agent manages the conversation flow to collect necessary details
    (flight number, passenger name, new destination/date) and uses tools to
    check for alternatives. It adheres to the Single Responsibility Principle.
    """

    def __init__(self):
        """Initializes the FlightChangeAgent."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7,
        )

    def run(self, state: dict) -> dict:
        """
        Executes the flight change logic, managing a simple conversational flow.

        Args:
            state: The current conversation state.

        Returns:
            The updated state with the agent's response.
        """
        print("--- Running Flight Change Agent ---")
        # Simplified state management within the agent for this PoC
        # In a real app, this might be a more robust state machine
        if not state.get("flight_number") or not state.get("passenger_name"):
            # Attempt to extract info first
            self._extract_initial_details(state)
            if not state.get("flight_number"):
                return {
                    "agent_response": "Por supuesto, para cambiar tu vuelo, primero necesito tu número de vuelo."
                }
            if not state.get("passenger_name"):
                return {
                    "agent_response": "Gracias. Ahora, por favor, dime el nombre completo del pasajero."
                }

        # Once we have flight and passenger, verify details
        if not state.get("flight_details_verified"):
            return self._verify_flight_details(state)

        # Now, ask for new flight preferences
        if (
            not state.get("new_origin")
            or not state.get("new_destination")
            or not state.get("new_date")
        ):
            # This part can be expanded with more sophisticated extraction
            return {
                "agent_response": "Perfecto. ¿A qué destino y en qué fecha te gustaría viajar? (ej. a Miami el 2025-09-20)"
            }

        # Check availability
        return self._check_new_flight_availability(state)

    def _extract_initial_details(self, state: dict):
        """Tries to extract flight number and name from the initial message."""
        import re

        message = state.get("current_message", "").upper()
        flight_match = re.search(r"[A-Z]{2}\d{3,4}", message)
        if flight_match:
            state["flight_number"] = flight_match.group(0)
        # This is a simplification; name extraction is complex.
        # We will rely on the user providing it in a separate step.

    def _verify_flight_details(self, state: dict) -> dict:
        """Uses the get_flight_details tool to verify the user's info."""
        try:
            details = get_flight_details.invoke(
                {
                    "flight_number": state["flight_number"],
                    "passenger_name": state["passenger_name"],
                }
            )
            if details.get("status") == "no_encontrado":
                return {
                    "agent_response": "No pude encontrar una reserva con esos datos. ¿Podrías verificar el número de vuelo y el nombre?"
                }

            state["flight_details_verified"] = True
            state["original_flight"] = details
            return {
                "agent_response": f"Encontré tu reserva, {details['passenger']}. Vuelo {details['flight_number']} de {details['origin']} a {details['destination']}. ¿A dónde y cuándo quieres cambiarlo?"
            }
        except Exception as e:
            print(f"Error calling get_flight_details tool: {e}")
            return {
                "agent_response": "Tuve un problema al verificar tu reserva. Inténtalo de nuevo, por favor."
            }

    def _check_new_flight_availability(self, state: dict) -> dict:
        """Uses the check_flight_availability tool and generates a final response."""
        try:
            availability = check_flight_availability.invoke(
                {
                    "origin": state["new_origin"],
                    "destination": state["new_destination"],
                    "date": state["new_date"],
                }
            )
            response = self._generate_final_response(availability)
            return {"agent_response": response}
        except Exception as e:
            print(f"Error calling check_flight_availability tool: {e}")
            return {
                "agent_response": "Lo siento, no pude verificar la disponibilidad de vuelos en este momento."
            }

    def _generate_final_response(self, availability: dict) -> str:
        """Generates a response based on flight availability."""
        prompt = ChatPromptTemplate.from_template(
            """
            Eres un asistente de aerolínea. Tu tarea es informar al usuario sobre la disponibilidad de vuelos para un cambio.

            Contexto de la herramienta:
            {context}

            Si hay vuelos, presenta las opciones de forma clara. Si no hay, informa amablemente.
            Recuerda que esto es una simulación, no confirmes ningún cambio ni hables de tarifas.
            """
        )
        chain = prompt | self.llm
        response = chain.invoke({"context": str(availability)})
        return response.content.strip()
