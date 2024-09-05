import os
from logging import config as logging_config

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
        )

    app_title: str = "App"
    database_dsn: PostgresDsn

    host: str = '127.0.0.1'
    port: int = 8080


app_settings = AppSettings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
