"""Configuration management for API keys and endpoints."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load local .env if present
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


class Config:
    """Central configuration class."""
    
    # TMDB Settings
    TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
    TMDB_BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/original"
    
    # AI Brain Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
    
    # Application Defaults
    DEFAULT_NUM_RECOMMENDATIONS = 5
    DEFAULT_REGION = "US"
    
    @classmethod
    def get_gemini_key(cls, override_key: str = "") -> str:
        return override_key.strip() or cls.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")

    @classmethod
    def get_tmdb_key(cls, override_key: str = "") -> str:
        return override_key.strip() or cls.TMDB_API_KEY or os.getenv("TMDB_API_KEY", "")

    @classmethod
    def get_openai_key(cls, override_key: str = "") -> str:
        return override_key.strip() or cls.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
