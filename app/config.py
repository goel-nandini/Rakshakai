"""
Configuration module for RakshakAI.
Loads environment variables and provides application settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class"""
    
    # API Security
    API_KEY = os.getenv("API_KEY", "")
    
    # Application Settings
    APP_NAME = "RakshakAI"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server Settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.API_KEY:
            raise ValueError("API_KEY must be set in environment variables")
        return True


# Create a global config instance
config = Config()
