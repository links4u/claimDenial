"""
Local LLM Provider using Ollama

Provides access to locally-hosted LLMs via Ollama.
Default: Llama 3.1 (8B)

Requirements:
- Ollama installed and running (ollama.ai)
- Model pulled: ollama pull llama3.1:8b
"""

from typing import Optional
import httpx
import json
import structlog

from app.core.llm_providers import BaseLLMProvider

logger = structlog.get_logger()


class LocalLLMProvider(BaseLLMProvider):
    """
    Local LLM provider using Ollama.
    
    Benefits:
    - No API costs
    - Data privacy (no external calls)
    - No internet dependency
    - Faster for development
    
    Trade-offs:
    - Requires local GPU/CPU resources
    - Lower quality than Claude/GPT-4
    - Slower inference on CPU
    """
    
    def __init__(
        self, 
        model: str = "llama3.1:8b",
        temperature: float = 0.3,
        max_tokens: int = 1000,
        ollama_url: str = "http://localhost:11434"
    ):
        super().__init__(model, temperature, max_tokens)
        self.ollama_url = ollama_url
        self.logger.info("local_llm_initialized", model=model, url=ollama_url)
    
    async def agenerate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system context
            
        Returns:
            Generated text
            
        Raises:
            Exception: If Ollama is not running or model not found
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                generated_text = result.get("message", {}).get("content", "")
                
                self.logger.info(
                    "local_generation_success",
                    prompt_length=len(prompt),
                    response_length=len(generated_text)
                )
                
                return generated_text
                
        except httpx.ConnectError:
            error_msg = (
                f"Cannot connect to Ollama at {self.ollama_url}. "
                "Please ensure Ollama is running: 'ollama serve'"
            )
            self.logger.error("ollama_connection_failed", url=self.ollama_url)
            raise Exception(error_msg)
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                error_msg = (
                    f"Model '{self.model}' not found. "
                    f"Please pull it: 'ollama pull {self.model}'"
                )
            else:
                error_msg = f"Ollama API error: {e.response.text}"
            
            self.logger.error("ollama_api_error", status=e.response.status_code)
            raise Exception(error_msg)
        
        except Exception as e:
            self.logger.error("local_generation_failed", error=str(e))
            raise
    
    def get_provider_name(self) -> str:
        return "local"
