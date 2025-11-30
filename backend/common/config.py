from pydantic_settings import BaseSettings
from typing import Optional, Literal


class Settings(BaseSettings):
    app_name: str = "Oil Drilling Dashboard API"
    debug: bool = False
    version: str = "1.0.0"

    database_url: str = "sqlite:///./test.db"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = "your_secure_password_here"
    redis_decode_responses: bool = True
    redis_socket_timeout: int = 5
    redis_mode: Literal["local", "cloud"] = "local"
    upstash_redis_url: Optional[str] = None
    upstash_redis_token: Optional[str] = None

    chroma_mode: Literal["local", "cloud"] = "local"
    chroma_cloud_tenant: Optional[str] = None
    chroma_cloud_database: Optional[str] = None
    chroma_api_token: Optional[str] = None
    chroma_host: str = "localhost"
    chroma_port: int = 8000

    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    ollama_embedding_model: str = "nomic-embed-text"
    ollama_base_url: Optional[str] = "http://localhost:11434"
    openai_embedding_model: str = "text-embedding-3-large"
    model_provider: Literal["openai", "ollama", "anthropic"] = "ollama"

    embedding_provider: Literal["voyage", "ollama"] = "voyage"
    voyage_embedding_model: str = "voyage-3-large"

    class Config:
        case_sensitive = False
        env_file = ".env"
        extra = "ignore"


settings = Settings()
