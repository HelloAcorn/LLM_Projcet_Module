from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Setting Configuration - API Keys 관리"""

    API_V1_STR: str = "/api"
    
    # LLM API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    class Config:
        case_sensitive = False
        env_file = Path(__file__).parent / ".api_key"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

settings = Settings()