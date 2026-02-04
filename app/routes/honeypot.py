"""
Honeypot routes - Endpoints for handling honeypot messages.
This is where the AI agent will analyze and respond to incoming messages.
"""

from fastapi import APIRouter, Depends
from app.models.schemas import HoneypotMessageRequest, HoneypotMessageResponse
from app.middleware.auth import verify_api_key

# Create router for honeypot endpoints
router = APIRouter(
    prefix="/honeypot",
    tags=["honeypot"],
    dependencies=[Depends(verify_api_key)]  # All routes in this router require API key
)


@router.post("/message", response_model=HoneypotMessageResponse)
async def process_message(request: HoneypotMessageRequest):
    """
    Process an incoming message to the honeypot.
    
    This endpoint receives messages from potential attackers and generates
    AI-powered responses to engage and analyze their behavior.
    
    Args:
        request: The honeypot message request containing the message and optional metadata
        
    Returns:
        A response with status and AI-generated reply
        
    Note:
        In production, this would call your AI agent/LLM to generate context-aware responses.
        For now, it returns a placeholder response.
    """
    
    # TODO: Integrate with your AI agent/LLM here
    # Example: reply = await ai_agent.generate_response(request.message, request.metadata)
    
    # Placeholder response for hackathon
    reply = f"Received your message: '{request.message}'. How can I help you further?"
    
    return HoneypotMessageResponse(
        status="success",
        reply=reply
    )
