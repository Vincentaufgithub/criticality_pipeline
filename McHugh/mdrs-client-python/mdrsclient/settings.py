import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mdrs_client_config_dirname: str = "~/.mdrs-client"
    mdrs_client_concurrent: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

CONCURRENT = settings.mdrs_client_concurrent
CONFIG_DIRNAME = os.path.realpath(os.path.expanduser(settings.mdrs_client_config_dirname))
