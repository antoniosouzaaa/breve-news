import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    NOTIFICATION_EMAIL: str = os.getenv("NOTIFICATION_EMAIL", "antoniosouza1997@gmail.com")
    APP_BASE_URL: str = os.getenv("APP_BASE_URL", "http://localhost:8000")
    TIMEZONE: str = os.getenv("TIMEZONE", "America/Sao_Paulo")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./briefing.db")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
