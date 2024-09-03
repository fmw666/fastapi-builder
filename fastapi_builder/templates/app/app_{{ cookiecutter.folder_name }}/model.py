from sqlalchemy import Column, String

from models.base import Base
from models.mixins import DateTimeModelMixin, SoftDeleteModelMixin


class {{ cookiecutter.pascal_name }}(Base["{{ cookiecutter.pascal_name }}"], DateTimeModelMixin, SoftDeleteModelMixin):
    __tablename__ = "{{ cookiecutter.snake_name }}"

    name = Column(String(255))
