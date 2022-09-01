from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./db.sqlite3"

    class Config:
        env_file: str = ".env"


@cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for {settings.env_name}")
    return settings
