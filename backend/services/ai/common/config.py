from pydantic_settings import BaseSettings
from typing import Optional, Literal
from common.config import settings as global_settings


class AISettings(BaseSettings):
    model_provider: Literal["openai", "ollama"] = "ollama"

    # OpenAI settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.1
    openai_max_tokens: int = 1000

    # Ollama settings
    ollama_model: str = "deepseek-v3.1:671b-cloud"  # Chat model
    ollama_embedding_model: str = "nomic-embed-text"  # Embedding model
    ollama_temperature: float = 0.1
    ollama_max_tokens: int = 1000
    ollama_api_key: Optional[str] = None
    ollama_base_url: Optional[str] = None

    # RAG settings
    rag_max_chunks: int = 5
    rag_chunk_overlap: int = 50

    # Agent settings
    agent_max_iterations: int = 10
    agent_verbose: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "AI_"
        extra = "ignore"


ai_settings = AISettings()
