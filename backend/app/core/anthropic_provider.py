"""
Anthropic LLM Provider

Wrapper for Claude models via Anthropic API.
"""

from typing import Optional
from anthropic import AsyncAnthropic
import structlog

from app.core.llm_providers import BaseLLMProvider

logger = structlog.get_logger()


class AnthropicLLMProvider(BaseLLMProvider):
    """
    Anthropic Claude provider.
    
    Benefits:
    - High quality outputs
    - Strong instruction following
    - 200K context window
    - Good at medical/formal content
    
    Trade-offs:
    - API costs (~$0.003/1K tokens)
    - Requires internet
    - Requires API key
    - Data leaves local environment
    """
    
    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.3,
        max_tokens: int = 1000,
        api_key: str = None
    ):
        super().__init__(model, temperature, max_tokens)
        
        if not api_key:
            raise ValueError("Anthropic API key is required")
        
        self.client = AsyncAnthropic(api_key=api_key)
        self.logger.info("anthropic_provider_initialized", model=model)
    
    async def agenerate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text using Claude API.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system context
            
        Returns:
            Generated text
        """
        try:
            messages = [{"role": "user", "content": prompt}]
            
            kwargs = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": messages
            }
            
            if system_prompt:
                kwargs["system"] = system_prompt
            
            response = await self.client.messages.create(**kwargs)
            
            generated_text = response.content[0].text
            
            self.logger.info(
                "anthropic_generation_success",
                prompt_length=len(prompt),
                response_length=len(generated_text),
                usage_tokens=response.usage.total_tokens
            )
            
            return generated_text
            
        except Exception as e:
            self.logger.error("anthropic_generation_failed", error=str(e))
            raise
    
    def get_provider_name(self) -> str:
        return "anthropic"
