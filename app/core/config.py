# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    DATABASE_URL: str = "postgresql://localhost:1234@db:5432/tech-debt_gamify"

    class Config:
        case_sensitive = True

settings = Settings()