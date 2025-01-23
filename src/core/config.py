"""Settings."""

from datetime import date, timedelta

from pydantic import ConfigDict, PastDate
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

    CI_INFRASTRUCTURE_PRICING_RATE: int = 0.14  # the machine pricing rate in $/min

    DEVELOPER_HOURLY_RATE: int = 0.6 * 60  # salary in $/60 min

    RECENCY_REFERENCE_DATE: PastDate = date.today() - timedelta(milliseconds=1)

    RECENCY_N_LAST: int = 3


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
