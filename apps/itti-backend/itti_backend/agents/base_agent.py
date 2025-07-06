"""Base agent definition for the VuelaConNosotros chatbot."""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the chatbot.

    This class defines the common interface that all agents must implement,
    ensuring compliance with the Liskov Substitution Principle (LSP) and
    Dependency Inversion Principle (DIP).
    """

    @abstractmethod
    def run(self, state: dict) -> dict:
        """
        Executes the agent's logic based on the current conversation state.

        Args:
            state: A dictionary representing the current state of the conversation.

        Returns:
            A dictionary containing the updated state after the agent's execution.
        """
        pass
