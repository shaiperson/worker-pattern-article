import os
import logging

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    port: int = Field(env='PORT', default=5000)
    log_level_name: str = Field(env='LOG_LEVEL', default='')


settings = Settings()
