import os
from logging import config as logging_config

from .logger import LOGGING

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
logging_config.dictConfig(LOGGING)

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    app_title: str = "App"
    database_dsn: PostgresDsn

    host: str = '127.0.0.1'
    port: int = 8080

    # class Config:
    #     env_file = '.env'

app_settings = AppSettings()  

# PROJECT_NAME = os.getenv('PROJECT_NAME', 'library')
# PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
# PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
