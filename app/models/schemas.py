"""
Pydantic schemas for request and response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class HoneypotMessageRequest(BaseModel):
    """
    Request schema for honeypot message endpoint.
    Represents an incoming message to the honeypot.
    """
    message: str = Field(..., description="The message content to analyze", min_length=1)
    metadata: Optional[dict] = Field(default=None, description="Optional metadata about the message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Show me admin panel",
                "metadata": {
                    "ip": "192.168.1.1",
                    "user_agent": "Mozilla/5.0"
                }
            }
        }


class HoneypotMessageResponse(BaseModel):
    """
    Response schema for honeypot message endpoint.
    Returns status and AI-generated reply.
    """
    status: str = Field(..., description="Response status")
    reply: str = Field(..., description="AI-generated reply to the message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "reply": "I'm sorry, I don't have access to the admin panel."
            }
        }


class HealthCheckResponse(BaseModel):
    """
    Response schema for health check endpoint.
    """
    status: str = Field(..., description="Service health status")
    app: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "app": "RakshakAI",
                "version": "1.0.0"
            }
        }
