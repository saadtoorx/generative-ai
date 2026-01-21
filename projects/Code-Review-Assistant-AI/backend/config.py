"""
Configuration settings for Code Review Assistant.
Uses Pydantic Settings to load from environment variables or .env file.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment."""
    
    # Ollama Configuration
    ollama_url: str = "http://localhost:11434/api/generate"
    model_name: str = "codellama"
    
    # Request Configuration
    request_timeout: int = 300
    
    # Backend Configuration
    backend_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
