"""
ClaimPilot™ Configuration Module

Manages all application settings using Pydantic Settings.
Environment variables are loaded from .env file.
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "ClaimPilot™"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 1500
    
    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL connection string")
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    
    # Security
    JWT_SECRET: str = Field(..., description="Secret key for JWT tokens")
    CORS_ORIGINS: str = "http://localhost:2400,http://localhost:3000"
    
    # AI/LLM
    # Default provider is 'local' (Ollama) - no API keys required
    # Options: 'local', 'anthropic', 'openai'
    LLM_PROVIDER: str = "local"
    
    # API keys (optional - only needed for non-local providers)
    ANTHROPIC_API_KEY: str = Field(default="", description="Anthropic API key for Claude (optional)")
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key for embeddings and GPT (optional)")
    
    # Ollama configuration (for local provider)
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    
    # Cloud LLM configuration (for anthropic/openai providers)
    LLM_MODEL: str = "claude-3-5-sonnet-20241022"  # Used when provider=anthropic
    EMBEDDING_MODEL: str = "text-embedding-3-small"  # OpenAI embeddings
    
    # LLM Temperature Settings
    CLASSIFIER_TEMPERATURE: float = 0.0
    DRAFTER_TEMPERATURE: float = 0.3
    GUARDRAIL_TEMPERATURE: float = 0.0
    
    # Token Limits
    MAX_TOKENS_CLASSIFIER: int = 100
    MAX_TOKENS_DRAFTER: int = 1500
    MAX_TOKENS_GUARDRAIL: int = 500
    
    # Performance
    RAG_TOP_K: int = 3
    MAX_LLM_RETRIES: int = 3
    LLM_RETRY_DELAY: int = 1
    MAX_COMPLIANCE_RETRIES: int = 2
    
    # Feature Flags
    ENABLE_AUDIT_LOGGING: bool = True
    ENABLE_PERFORMANCE_METRICS: bool = True
    ENABLE_RATE_LIMITING: bool = False
    
    def get_cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


# Global settings instance
settings = Settings()
