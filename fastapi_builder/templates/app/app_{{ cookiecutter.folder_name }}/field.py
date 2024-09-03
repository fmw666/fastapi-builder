import datetime
from dataclasses import dataclass

from pydantic import Field


@dataclass
class {{ cookiecutter.pascal_name }}Fields:
    id: int = Field(..., description="id", example=1)
    name: str = Field(..., min_length=1, max_length=255, description="名字", example="fmw666")
    created_at: datetime.datetime = Field(..., description="创建时间", example="2023-01-01 00:00:00")
    updated_at: datetime.datetime = Field(..., description="更新时间", example="2023-01-01 00:00:00")
