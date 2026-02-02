from enum import Enum, EnumMeta


class BaseMetadataEnum(EnumMeta):
    def __contains__(self, other):
        try:
            self(other)
        except ValueError:
            return False
        else:
            return True


class BaseEnum(str, Enum, metaclass=BaseMetadataEnum):
    """Base enum class."""


class Language(BaseEnum):
    CN = "cn"
    EN = "en"


class PackageManager(BaseEnum):
    PIP = "pip"
    POETRY = "poetry"


class PythonVersion(BaseEnum):
    THREE_DOT_EIGHT = "3.8"
    THREE_DOT_NINE = "3.9"
    THREE_DOT_TEN = "3.10"
    THREE_DOT_ELEVEN = "3.11"
    THREE_DOT_TWELVE = "3.12"


class License(BaseEnum):
    MIT = "MIT"
    BSD = "BSD"
    GNU = "GNU"
    APACHE = "Apache"


class Database(BaseEnum):
    POSTGRESQL = "PostgreSQL"
    MYSQL = "MySQL"
    SQLITE = "SQLite"


class DBCmd(BaseEnum):
    MAKEMIGRATIONS = "makemigrations"
    MIGRATE = "migrate"


class VenvCmd(BaseEnum):
    CREATE = "create"
    ON = "on"
    OFF = "off"
