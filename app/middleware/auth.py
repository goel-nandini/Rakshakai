"""
Authentication middleware for API key validation.
Validates the x-api-key header on protected endpoints.
"""

from fastapi import Header, HTTPException, status
from app.config import config


async def verify_api_key(x_api_key: str = Header(..., description="API key for authentication")):
    """
    Dependency function to verify API key from request header.
    
    Args:
        x_api_key: The API key from the x-api-key header
        
    Returns:
        The API key if valid
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required"
        )
    
    if x_api_key != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return x_api_key
