"""Configuration settings for the email agent project."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "1.0"))
    
    # Agent Configuration
    MAX_TURNS: int = int(os.getenv("MAX_TURNS", "10"))
    
    # Project Settings
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "email-agent")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Optional tracking
    WANDB_API_KEY: str = os.getenv("WANDB_API_KEY", "")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required settings."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
    
    @classmethod
    def print_config(cls) -> None:
        """Print current configuration."""
        print("=== Email Agent Configuration ===")
        print(f"Model: {cls.MODEL_NAME}")
        print(f"Temperature: {cls.TEMPERATURE}")
        print(f"Max Turns: {cls.MAX_TURNS}")
        print(f"Debug: {cls.DEBUG}")
        print(f"OpenAI API Key: {'Set' if cls.OPENAI_API_KEY else 'Not Set'}")
        print("================================")

# Creates an instance: Makes the settings available throughout the app, Global access: Other files can import and use these settings
settings = Settings()
settings.validate()