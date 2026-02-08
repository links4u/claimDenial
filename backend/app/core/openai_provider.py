"""
OpenAI LLM Provider

Wrapper for GPT models via OpenAI API.
"""

from typing import Optional
from openai import AsyncOpenAI
import structlog

from app.core.llm_providers import BaseLLMProvider

logger = structlog.get_logger()


class OpenAILLMProvider(BaseLLMProvider):
    """
    OpenAI GPT provider.
    
    Benefits:
    - Widely documented
    - Good general performance
    - Fast inference
    - Strong coding/technical tasks
    
    Trade-offs:
    - API costs (~$0.002/1K tokens for GPT-4)
    - Requires internet
    - Requires API key
    - Less specialized for medical content than Claude
    """
    
    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.3,
        max_tokens: int = 1000,
        api_key: str = None
    ):
        super().__init__(model, temperature, max_tokens)
        
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.logger.info("openai_provider_initialized", model=model)
    
    async def agenerate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system context
            
        Returns:
            Generated text
        """
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            generated_text = response.choices[0].message.content
            
            self.logger.info(
                "openai_generation_success",
                prompt_length=len(prompt),
                response_length=len(generated_text),
                usage_tokens=response.usage.total_tokens
            )
            
            return generated_text
            
        except Exception as e:
            self.logger.error("openai_generation_failed", error=str(e))
            raise
    
    def get_provider_name(self) -> str:
        return "openai"
