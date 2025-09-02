"""
Configuration module for the multimodal video transcriber.
Handles environment variables and API setup.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the transcriber."""
    
    # API Configuration
    GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False").lower() == "true"
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Configuration
    DEFAULT_MODEL = "gemini-2.0-flash"
    DEFAULT_TEMPERATURE = 0.0
    DEFAULT_TOP_P = 0.0
    DEFAULT_SEED = 42
    
    # Video Processing Configuration
    DEFAULT_FPS = 1.0
    MAX_FPS = 24.0
    MIN_FPS = 0.1
    
    # Timecode Configuration
    DEFAULT_TIMECODE_FORMAT = "MM:SS"
    EXTENDED_TIMECODE_FORMAT = "H:MM:SS"
    
    # Output Configuration
    NOT_FOUND_MARKER = "?"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate the configuration."""
        if cls.GOOGLE_GENAI_USE_VERTEXAI:
            # Vertex AI configuration
            if not cls.GOOGLE_CLOUD_PROJECT:
                print("❌ GOOGLE_CLOUD_PROJECT is required for Vertex AI")
                return False
        else:
            # Google AI Studio configuration
            if not cls.GOOGLE_API_KEY:
                print("❌ GOOGLE_API_KEY is required for Google AI Studio")
                return False
        
        return True
    
    @classmethod
    def setup_environment(cls) -> None:
        """Setup environment variables for the Google Gen AI SDK."""
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(cls.GOOGLE_GENAI_USE_VERTEXAI)
        os.environ["GOOGLE_CLOUD_PROJECT"] = cls.GOOGLE_CLOUD_PROJECT
        os.environ["GOOGLE_CLOUD_LOCATION"] = cls.GOOGLE_CLOUD_LOCATION
        os.environ["GOOGLE_API_KEY"] = cls.GOOGLE_API_KEY
    
    @classmethod
    def get_service_name(cls) -> str:
        """Get the service name being used."""
        # Check environment variables directly to handle UI configuration
        use_vertex_ai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False").lower() == "true"
        return "Vertex AI" if use_vertex_ai else "Google AI Studio"
