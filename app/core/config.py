import os
import secrets
import typing
from typing import Any, Dict, List
from pathlib import Path
from databases import DatabaseURL

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret


class ConfigParser(Config):
    """重载 Config _read_file 方法，使其支持文件中文问题"""
    def _read_file(self, file_name: typing.Union[str, Path]) -> typing.Dict[str, str]:
        file_values: typing.Dict[str, str] = {}
        with open(file_name, encoding="utf-8") as input_file:
            for line in input_file.readlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    file_values[key] = value
        return file_values


config = ConfigParser(os.path.join(os.path.dirname(__file__), ".env"))

# databases
DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL, default="")
DB_CHARSET: str = config("CHARSET", cast=str, default="utf8")
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

MYSQL_DB_INFO_DICT: Dict[str, Any] = {
    "host": DATABASE_URL.hostname,
    "port": DATABASE_URL.port,
    "user": DATABASE_URL.username,
    "password": DATABASE_URL.password,
    "db": DATABASE_URL.database,
    "charset": DB_CHARSET,
    "maxsize": MAX_CONNECTIONS_COUNT,
    "minsize": MIN_CONNECTIONS_COUNT
}

# system
DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default=secrets.token_urlsafe(32))
ALLOWED_HOSTS: List[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=["*"])
API_PREFIX: str = config("API_PREFIX", cast=str, default="/api")

# application
PROJECT_NAME: str = config("PROJECT_NAME", cast=str, default="FastAPI example application")
VERSION: str = config("VERSION", cast=str, default="1.0.0")

# token
JWT_TOKEN_PREFIX: str = config("JWT_TOKEN_PREFIX", cast=str, default="Token")  # noqa: S105
JWT_ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # 三天，单位为分钟
