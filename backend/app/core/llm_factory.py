"""
LLM Provider Factory

Creates appropriate LLM provider based on configuration.
"""

from typing import Optional
import structlog

from app.core.llm_providers import BaseLLMProvider
from app.core.local_provider import LocalLLMProvider
from app.core.anthropic_provider import AnthropicLLMProvider
from app.core.openai_provider import OpenAILLMProvider
from app.core.config import settings

logger = structlog.get_logger()


class LLMFactory:
    """
    Factory for creating LLM providers.
    
    Centralizes provider selection logic and handles configuration.
    """
    
    @staticmethod
    def create_provider(
        provider_type: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> BaseLLMProvider:
        """
        Create an LLM provider based on configuration.
        
        Args:
            provider_type: Override provider (local/anthropic/openai)
            model: Override model name
            temperature: Override temperature
            max_tokens: Override max tokens
            
        Returns:
            Configured LLM provider instance
            
        Raises:
            ValueError: If provider type is unknown or configuration is invalid
        """
        provider_type = provider_type or settings.LLM_PROVIDER
        
        logger.info("creating_llm_provider", provider=provider_type)
        
        if provider_type == "local":
            return LocalLLMProvider(
                model=model or "llama3.1:8b",
                temperature=temperature or 0.3,
                max_tokens=max_tokens or 1000,
                ollama_url=getattr(settings, 'OLLAMA_URL', 'http://localhost:11434')
            )
        
        elif provider_type == "anthropic":
            api_key = getattr(settings, 'ANTHROPIC_API_KEY', None)
            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY is required when using 'anthropic' provider. "
                    "Either set the environment variable or use 'local' provider."
                )
            
            return AnthropicLLMProvider(
                model=model or settings.LLM_MODEL,
                temperature=temperature or 0.3,
                max_tokens=max_tokens or 1000,
                api_key=api_key
            )
        
        elif provider_type == "openai":
            api_key = getattr(settings, 'OPENAI_API_KEY', None)
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY is required when using 'openai' provider. "
                    "Either set the environment variable or use 'local' provider."
                )
            
            return OpenAILLMProvider(
                model=model or "gpt-4",
                temperature=temperature or 0.3,
                max_tokens=max_tokens or 1000,
                api_key=api_key
            )
        
        else:
            raise ValueError(
                f"Unknown LLM provider: {provider_type}. "
                f"Supported: local, anthropic, openai"
            )
    
    @staticmethod
    def get_classifier_llm() -> BaseLLMProvider:
        """Get LLM configured for classification (temperature=0.0)."""
        return LLMFactory.create_provider(
            temperature=settings.CLASSIFIER_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS_CLASSIFIER
        )
    
    @staticmethod
    def get_drafter_llm() -> BaseLLMProvider:
        """Get LLM configured for drafting (temperature=0.3)."""
        return LLMFactory.create_provider(
            temperature=settings.DRAFTER_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS_DRAFTER
        )
    
    @staticmethod
    def get_guardrail_llm() -> BaseLLMProvider:
        """Get LLM configured for compliance checks (temperature=0.0)."""
        return LLMFactory.create_provider(
            temperature=settings.GUARDRAIL_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS_GUARDRAIL
        )
