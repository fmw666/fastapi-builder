import os
import secrets

from typing import Dict, List, Union

from pathlib import Path
from databases import DatabaseURL

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret


class CommaSeparatedStrings(CommaSeparatedStrings):

    def __eq__(self, value: object) -> bool:
        """重载 eq 方法，基于 _items 作比较"""
        return self._items == value


class ConfigParser(Config):
    """重载 Config _read_file 方法，使其支持文件中文问题"""

    def _read_file(
        self, file_name: Union[str, Path], encoding: str = "utf-8"
    ) -> Dict[str, str]:
        file_values: Dict[str, str] = {}
        with open(file_name, encoding=encoding) as input_file:
            for line in input_file.readlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    file_values[key] = value
        return file_values


class Settings(object):
    """Application settings."""

    # Initialize the ConfigParser
    config = ConfigParser(os.path.join(os.path.dirname(__file__), ".env"))

    # databases
    REDIS_URL: str = config("REDIS_URL", cast=str, default="")
    DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL, default="")
    ASYNC_DATABASE_URL: DatabaseURL = config("ASYNC_DB_CONNECTION", cast=DatabaseURL, default="")
    DB_CHARSET: str = config("CHARSET", cast=str, default="utf8")

    # system
    DEBUG: bool = config("DEBUG", cast=bool, default=False)
    SECRET_KEY: Secret = config(
        "SECRET_KEY", cast=Secret, default=secrets.token_urlsafe(32)
    )
    API_PREFIX: str = config("API_PREFIX", cast=str, default="/api")

    # application
    PROJECT_NAME: str = config(
        "PROJECT_NAME", cast=str, default="FastAPI example application"
    )
    VERSION: str = config("VERSION", cast=str, default="1.0.0")

    # authentication
    USER_BLACKLIST: List[str] = config("USER_BLACKLIST", cast=CommaSeparatedStrings, default=[])

    # token
    JWT_TOKEN_PREFIX: str = config(
        "JWT_TOKEN_PREFIX", cast=str, default="Token"
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # 三天，单位为分钟


settings = Settings()
