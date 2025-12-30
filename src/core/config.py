import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Keys as defined in 01_CORE_SPEC_en.md
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    VECTOR_STORE_PATH: Optional[str] = None
    
    # Internal Configuration (System defaults)
    COST_LOG_PATH: str = "logs/cost.jsonl"
    API_REQUEST_LOG_PATH: str = "logs/api_requests.jsonl"
    PROMPT_TEMPLATE_DIR: str = "src/prompts/templates"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

