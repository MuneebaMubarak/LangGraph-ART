"""LLM service for OpenAI interactions."""

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from typing import List, Optional
import openai
from config.settings import settings

class LLMService:
    """Service for managing LLM interactions."""
    
    def __init__(self):
        """Initialize the LLM service."""
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.chat_model = None
        self._initialize_chat_model()
    
    def _initialize_chat_model(self) -> None:
        """Initialize the LangChain chat model."""
        self.chat_model = ChatOpenAI(
            model_name=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY,
        )
    
    def get_chat_model(self, temperature: Optional[float] = None) -> ChatOpenAI:
        """Get a configured chat model."""
        if temperature is not None:
            return ChatOpenAI(
                model_name=settings.MODEL_NAME,
                temperature=temperature,
                openai_api_key=settings.OPENAI_API_KEY,
            )
        return self.chat_model
    
    async def complete_async(self, messages: List[dict], 
                           model: Optional[str] = None,
                           temperature: Optional[float] = None) -> str:
        """Get completion from OpenAI API."""
        response = await self.client.chat.completions.create(
            model=model or settings.MODEL_NAME,
            messages=messages,
            temperature=temperature or settings.TEMPERATURE,
        )
        return response.choices[0].message.content or ""
    
    def validate_connection(self) -> bool:
        """Validate OpenAI API connection."""
        try:
            # Simple test call
            self.chat_model.invoke([{"role": "user", "content": "Hello"}])
            return True
        except Exception as e:
            print(f"LLM connection failed: {e}")
            return False

# Global LLM service instance
llm_service = LLMService()