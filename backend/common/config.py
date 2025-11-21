from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Oil Drilling Dashboard API"
    debug: bool = False
    version: str = "1.0.0"

    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
