from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv('.env', override=True)

class Settings(BaseSettings):
    DATABASE_URL : str
    API_VERSION : str
    JWT_SECRET : str
    JWT_ALGORITHM : str

    REDIS_URL : str

    class Config:
        env_file = ".env"  # Make sure it refers to your .env file
        extra = "ignore"  # Ignore any extra fields

config = Settings()

