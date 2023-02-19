import subprocess
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, root_validator

from fastapi_builder.config import FASTAPI_VERSION
from fastapi_builder.constants import Database, Language, License, PackageManager, PythonVersion


class AppContext(BaseModel):
    name: str
    folder_name: str
    snake_name: str
    camel_name: str
    pascal_name: str
    language: Optional[Language]

    @root_validator(pre=True)
    def validate_app(cls, values: dict):
        # values["folder_name"] = values["name"].lower().replace(" ", "-").strip()
        # values["snake_name"] = values["folder_name"].replace("-", "_")
        # values["camel_name"] = snake_to_camel(values["snake_name"])
        # values["pascal_name"] = camel_to_pascal(values["camel_name"])
        return values
    
    class Config:
        use_enum_values = True


class ProjectContext(BaseModel):
    name: str
    folder_name: str

    language: Optional[Language]
    packaging: PackageManager

    username: Optional[str] = None
    email: Optional[EmailStr] = None

    python: PythonVersion
    fastapi: str = FASTAPI_VERSION

    license: Optional[License]
    year: int

    pre_commit: bool
    docker: bool

    database: Optional[Database]
    database_name: Optional[str]

    @root_validator(pre=True)
    def validate_project(cls, values: dict):
        try:
            values["username"] = subprocess.check_output(
                ["git", "config", "--get", "user.name"]
            )
            values["email"] = subprocess.check_output(
                ["git", "config", "--get", "user.email"]
            )
        except subprocess.CalledProcessError:
            ...
        values["folder_name"] = values["name"].lower().replace(" ", "-").strip()
        values["year"] = datetime.today().year
        return values

    class Config:
        use_enum_values = True
