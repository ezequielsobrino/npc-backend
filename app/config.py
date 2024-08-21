from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://tudominio.com", "null"]
    GROQ_API_KEY: str  # Ensure this is the only setting loaded from the environment
    GROQ_API_URL: str = "https://api.groq.com/v1/chat/completions"
    DEFAULT_LANGUAGE: str = "es"
    MAX_HISTORY_LENGTH: int = 100
    HISTORY_FORMAT: str = "simple"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()