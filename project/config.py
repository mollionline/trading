import os
import pathlib
from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl

"""Base Config Class for project"""


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    CONFIG_NAME: Literal["DEV", "PYTEST", "STG", "PRD"] = "DEV"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "0.0.0.0", "*"]
    PROJECT_NAME: str = "Trading API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Trading"
    WWW_DOMAIN = "/api/v1"


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
