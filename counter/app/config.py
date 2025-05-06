from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
from typing import Tuple

from shared import helper


class Settings(BaseSettings):
    redis_url: str = None  # Redis server URL (redis://<host>:<port>)
    lower_hsv: Tuple[int, int, int] = (0, 0, 100)  # Lower HSV threshold
    upper_hsv: Tuple[int, int, int] = (180, 45, 255)  # Upper HSV threshold

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        alias_generator=helper.to_env_name,
        populate_by_name=True,
    )
