from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

ENVIRONMENT: Literal[
    "development",
    "staging",
    "production"
] = "development"

class Settings(BaseSettings):
    APP_NAME: str = "AI Receptionist API"
    APP_VERSION: str = "1.0.0"
    
    DATABASE_URL: str
    OPENAI_API_KEY: str = ""
    RETELL_API_KEY: str = ""
    
    ENVIRONMENT: str = "development"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()  #type: ignore