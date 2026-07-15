from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from dronzer.domain.constants import Environment


class Settings(BaseSettings):
    """
    Core Configuration Settings.
    These are the lowest level environment variables required to boot the app.
    All dynamic routing/tenant config comes from the DB later.
    """
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False

    # Application Info
    APP_NAME: str = "Dronzer AI Gateway"
    APP_VERSION: str = "0.1.0"

    # HTTP Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://dronzer:password@localhost:5432/dronzer_dev"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security (Valid Fernet Key Default for Dev)
    SECRET_KEY: str = "kR8r_7qHj8tZ1z2wO3c4V5b6N7m8M9l0K1j2H3g4F5E="

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FORMAT: Literal["JSON", "CONSOLE"] = "CONSOLE"

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if self.ENVIRONMENT == Environment.PRODUCTION:
            if self.SECRET_KEY == "kR8r_7qHj8tZ1z2wO3c4V5b6N7m8M9l0K1j2H3g4F5E=":
                raise ValueError("CRITICAL: SECRET_KEY must be changed in production! Do not use the default key.")
        return self


# Global settings singleton for initial boot
settings = Settings()
