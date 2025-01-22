"""Settings."""

from typing import Optional
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application Settings from .env file.

    Args:
        BaseSettings (pydantic.BaseSettings): Base settings to override

    Raises
        ValueError: if something is wrong with .env file
    """

    model_config = ConfigDict(extra="allow")

    PROJECT_NAME: str

    CI_INFRA_PRICING_RATE: int = 0.14  # the machine pricing rate in $/min


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
