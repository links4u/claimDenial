"""
LLM Provider Abstraction

Provides a unified interface for different LLM providers:
- Local (Ollama with Llama 3.1)
- Anthropic (Claude Sonnet)
- OpenAI (GPT-4)

This abstraction allows runtime switching between providers without
changing agent code, enabling cost optimization and local development.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import structlog

logger = structlog.get_logger()


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    All providers must implement:
    - generate(): Synchronous text generation
    - agenerate(): Async text generation
    - get_provider_name(): Identifier for logging
    """
    
    def __init__(self, model: str, temperature: float = 0.3, max_tokens: int = 1000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.logger = logger.bind(provider=self.get_provider_name())
    
    @abstractmethod
    async def agenerate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text asynchronously.
        
        Args:
            prompt: User prompt/question
            system_prompt: Optional system context
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider identifier (e.g., 'local', 'anthropic', 'openai')"""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Return model configuration for logging."""
        return {
            "provider": self.get_provider_name(),
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
