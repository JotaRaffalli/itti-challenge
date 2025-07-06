"""Orchestrator for the VuelaConNosotros chatbot using LangGraph."""

from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from ..agents.flight_change_agent import FlightChangeAgent
from ..agents.flight_status_agent import FlightStatusAgent
from ..nlu.intent_classifier import IntentClassifier


# 1. Define the state of the graph
class ChatbotState(TypedDict):
    """Represents the state of the chatbot conversation."""

    current_message: str
    intent: str
    agent_response: str
    history: list


# 2. Define the nodes of the graph
def classify_node(state: ChatbotState) -> ChatbotState:
    """Classifies the user's intent."""
    print("--- Node: Classifying Intent ---")
    classifier = IntentClassifier()
    intent = classifier.classify(state["current_message"])
    return {
        "current_message": state["current_message"],
        "intent": intent,
        "agent_response": state.get("agent_response", ""),
        "history": state.get("history", []),
    }


def flight_status_node(state: ChatbotState) -> ChatbotState:
    """Handles flight status inquiries."""
    print("--- Node: Handling Flight Status ---")
    agent = FlightStatusAgent()
    response = agent.run(dict(state))
    return {
        "current_message": state["current_message"],
        "intent": state["intent"],
        "agent_response": response["agent_response"],
        "history": state.get("history", []),
    }


def flight_change_node(state: ChatbotState) -> ChatbotState:
    """Handles flight change requests."""
    print("--- Node: Handling Flight Change ---")
    # This is a simplified implementation for the PoC.
    # A real-world scenario would require more sophisticated state management.
    agent = FlightChangeAgent()
    response = agent.run(dict(state))
    return {
        "current_message": state["current_message"],
        "intent": state["intent"],
        "agent_response": response["agent_response"],
        "history": state.get("history", []),
    }


def default_response_node(state: ChatbotState) -> ChatbotState:
    """Provides a default response for unhandled intents."""
    print("--- Node: Handling Default Response ---")
    intent = state.get("intent", "desconocida")
    responses = {
        "saludo": (
            "¡Hola! Soy el asistente de VuelaConNosotros. ¿En qué puedo ayudarte?"
        ),
        "despedida": "¡Adiós! Gracias por contactarnos.",
        "agradecimiento": "¡De nada! Ha sido un placer ayudarte.",
        "desconocida": (
            "Lo siento, no he entendido tu solicitud. "
            "Puedo ayudarte a consultar el estado de un vuelo "
            "o a cambiar una reserva."
        ),
    }
    return {
        "current_message": state["current_message"],
        "intent": state["intent"],
        "agent_response": responses.get(intent, responses["desconocida"]),
        "history": state.get("history", []),
    }


# 3. Define the conditional edges
def route_by_intent(state: ChatbotState) -> str:
    """Routes the conversation to the appropriate agent based on intent."""
    print(f"--- Routing by Intent: {state['intent']} ---")
    intent = state["intent"]
    if intent == "consultar_estado_vuelo":
        return "flight_status_agent"
    if intent == "cambiar_vuelo":
        return "flight_change_agent"
    return "default_responder"


# 4. Create the graph
def create_chatbot_graph():
    """
    Builds and compiles the LangGraph StateGraph for the chatbot.

    This function encapsulates the graph creation logic, adhering to the
    Single Responsibility Principle.

    Returns:
        A compiled LangGraph runnable.
    """
    workflow = StateGraph(ChatbotState)

    # Add nodes
    workflow.add_node("classifier", classify_node)
    workflow.add_node("flight_status_agent", flight_status_node)
    workflow.add_node("flight_change_agent", flight_change_node)
    workflow.add_node("default_responder", default_response_node)

    # Define entry and conditional routing
    workflow.set_entry_point("classifier")
    workflow.add_conditional_edges(
        "classifier",
        route_by_intent,
        {
            "flight_status_agent": "flight_status_agent",
            "flight_change_agent": "flight_change_agent",
            "default_responder": "default_responder",
        },
    )

    # Connect agent nodes to the end
    workflow.add_edge("flight_status_agent", END)
    workflow.add_edge("flight_change_agent", END)
    workflow.add_edge("default_responder", END)

    # Compile the graph with memory
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
