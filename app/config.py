from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
from shared import helper
from typing import Optional

import importlib
from dotenv import load_dotenv  # type: ignore

importlib.reload(helper)
load_dotenv(override=True)


class Settings(BaseSettings):
    pg_db: str = None
    pg_user: str = None
    pg_host: str = None
    pg_port: int = None
    pg_pass: Optional[str] = None
    redis_url: str = None
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        alias_generator=helper.to_env_name,
        populate_by_name=True,
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
