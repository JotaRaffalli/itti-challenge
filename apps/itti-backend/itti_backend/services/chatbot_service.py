"""High-level service for the VuelaConNosotros chatbot."""

import uuid

from ..orchestrator.chatbot_graph import create_chatbot_graph


class ChatbotService:
    """
    Provides a high-level interface to the chatbot.

    This class encapsulates the interaction with the LangGraph-based chatbot,
    adhering to the Single Responsibility Principle. It depends on the abstraction
    provided by the create_chatbot_graph factory function, following the
    Dependency Inversion Principle.
    """

    def __init__(self):
        """Initializes the ChatbotService."""
        self.chatbot_graph = create_chatbot_graph()

    def process_message(self, user_message: str, session_id: str | None = None) -> str:
        """
        Processes a user message and returns the chatbot's response.

        Args:
            user_message: The message from the user.
            session_id: An optional session ID to maintain conversation state.

        Returns:
            The final agent response from the chatbot graph.
        """
        if not session_id:
            session_id = str(uuid.uuid4())

        config = {"configurable": {"thread_id": session_id}}

        initial_state = {"current_message": user_message, "history": []}

        try:
            final_state = self.chatbot_graph.invoke(initial_state, config=config)
            return final_state.get("agent_response", "Lo siento, algo salió mal.")
        except Exception as e:
            print(f"Error processing message in ChatbotService: {e}")
            return "He encontrado un error inesperado. Por favor, intenta de nuevo más tarde."
