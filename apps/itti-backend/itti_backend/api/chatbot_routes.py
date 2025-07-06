"""API routes for the VuelaConNosotros chatbot."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..services.chatbot_service import ChatbotService

# Create a router for the chatbot endpoints
router = APIRouter()


# Pydantic model for the chat request
class ChatRequest(BaseModel):
    """Request model for a chat message."""

    message: str
    session_id: str | None = None


# Dependency injection for the ChatbotService
def get_chatbot_service():
    """Provides a ChatbotService instance."""
    # This could be enhanced with a singleton pattern for production
    return ChatbotService()


@router.post("/chat", tags=["Chatbot"])
async def chat_with_bot(
    request: ChatRequest,
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
):
    """
    Handles a chat interaction with the VuelaConNosotros chatbot.

    Args:
        request: The chat request containing the user's message.
        chatbot_service: The injected ChatbotService instance.

    Returns:
        A JSON response with the chatbot's reply.
    """
    try:
        response = chatbot_service.process_message(
            user_message=request.message, session_id=request.session_id
        )
        return {"response": response}
    except Exception as e:
        # Log the exception properly in a real application
        print(f"Unhandled error in /chat endpoint: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e
