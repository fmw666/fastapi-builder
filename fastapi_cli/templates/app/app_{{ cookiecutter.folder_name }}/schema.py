import datetime
from typing import Optional

from schemas.base import BaseSchema


class {{ cookiecutter.pascal_name }}Base(BaseSchema):
    """{{ cookiecutter.snake_name }} 基础"""
    ...


class U{{ cookiecutter.pascal_name }}Create({{ cookiecutter.pascal_name }}Base):
    """{{ cookiecutter.snake_name }} 创建"""
    ...
    

class {{ cookiecutter.pascal_name }}Info({{ cookiecutter.pascal_name }}Base):
    """{{ cookiecutter.snake_name }} 信息"""
    id: int
    updated_at: Optional[datetime.datetime] = None
    class Config(object):
        orm_mode = True
