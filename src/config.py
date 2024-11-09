from pathlib import Path
import secrets
from typing import List

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

file_path = Path(__file__).parent


class Settings(BaseSettings):
    BASE_DIR: Path = file_path

    # Application
    PROJECT_NAME: str = "Seconde mind"
    DEBUG: bool = True
    # Algorithm used to generate the JWT token
    JWT_ALGORITHM: str = "HS256"
    # CORS_ORIGINS is a JSON-formatted list of origins
    CORS_ORIGINS: List[str] = []
    USE_CORRELATION_ID: bool = True

    UVICORN_HOST: str
    UVICORN_PORT: int

    # MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "seconde_mind"

    # Superuser
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # Authentication
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # = 1 day
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # Config
    model_config = SettingsConfigDict(env_file=file_path.parent / '.env',
                                      env_prefix='SECONDE_MIND_',
                                      case_sensitive=True)


# Missing named arguments are filled with environment variables
settings = Settings()
