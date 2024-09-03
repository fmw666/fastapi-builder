import datetime
from typing import List, Literal

from fastapi import Query
from pydantic import Field, field_validator
from apps.app_{{ cookiecutter.snake_name }}.field import {{ cookiecutter.pascal_name }}Fields
from apps.app_{{ cookiecutter.snake_name }}.model import {{ cookiecutter.pascal_name }}
from models.base import get_model_fields_from_objects
from schemas.base import BaseSchema, QuerySchema
from schemas.response import PaginationResponse, StandardResponse


# ======================>>>>>>>>>>>>>>>>>>>>>> get_it_demos


class {{ cookiecutter.pascal_name }}ListQueryRequest(QuerySchema):
    """获取 {{ cookiecutter.snake_name }} 列表 查询 请求"""

    order_by: Literal["id", "created_at"] = Query(
        {{ cookiecutter.pascal_name }}.id.name, description="排序字段. eg: id created_at"
    )

    @field_validator("order_by")
    def validate_order_by(cls, v: str) -> str:
        order_fields = get_model_fields_from_objects({{ cookiecutter.pascal_name }}, [{{ cookiecutter.pascal_name }}.id, {{ cookiecutter.pascal_name }}.created_at])
        if v not in order_fields:
            raise ValueError(f"order_by: {v} not in {order_fields}")
        return v


class {{ cookiecutter.pascal_name }}ListResponse(BaseSchema):
    """获取 {{ cookiecutter.snake_name }} 列表 响应"""

    id: int = {{ cookiecutter.pascal_name }}Fields.id
    name: str = {{ cookiecutter.pascal_name }}Fields.name


class {{ cookiecutter.pascal_name }}ListResponseModel(StandardResponse):
    """获取 {{ cookiecutter.snake_name }} 列表 响应 Model"""

    data: PaginationResponse[{{ cookiecutter.pascal_name }}ListResponse]


# ======================>>>>>>>>>>>>>>>>>>>>>> create_{{ cookiecutter.snake_name }}


class {{ cookiecutter.pascal_name }}CreateRequest(BaseSchema):
    """创建 {{ cookiecutter.snake_name }} 请求"""

    name: str = {{ cookiecutter.pascal_name }}Fields.name


class {{ cookiecutter.pascal_name }}CreateResponse(BaseSchema):
    """创建 {{ cookiecutter.snake_name }} 响应"""

    id: int = {{ cookiecutter.pascal_name }}Fields.id
    name: str = {{ cookiecutter.pascal_name }}Fields.name


class {{ cookiecutter.pascal_name }}CreateResponseModel(StandardResponse):
    """创建 {{ cookiecutter.snake_name }} 响应 Model"""

    data: {{ cookiecutter.pascal_name }}CreateResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> patch_{{ cookiecutter.snake_name }}s


class {{ cookiecutter.pascal_name }}sPatchRequest(BaseSchema):
    """批量更新 {{ cookiecutter.snake_name }} 请求"""

    ids: List[int] = Field(..., description="{{ cookiecutter.snake_name }} id 列表")
    name: str = {{ cookiecutter.pascal_name }}Fields.name


class {{ cookiecutter.pascal_name }}sPatchResponse(BaseSchema):
    """批量更新 {{ cookiecutter.snake_name }} 响应"""

    ids: List[int] = Field(..., description="{{ cookiecutter.snake_name }} id 列表")
    name: str = {{ cookiecutter.pascal_name }}Fields.name


class {{ cookiecutter.pascal_name }}sPatchResponseModel(StandardResponse):
    """批量更新 {{ cookiecutter.snake_name }} 响应 Model"""

    data: {{ cookiecutter.pascal_name }}sPatchResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> delete_{{ cookiecutter.snake_name }}s


class {{ cookiecutter.pascal_name }}sDeleteResponse(BaseSchema):
    """批量删除 {{ cookiecutter.snake_name }} 响应"""

    ids: List[int] = Field(..., description="{{ cookiecutter.snake_name }} id 列表")


class {{ cookiecutter.pascal_name }}sDeleteResponseModel(StandardResponse):
    """批量删除 {{ cookiecutter.snake_name }} 响应 Model"""

    data: {{ cookiecutter.pascal_name }}sDeleteResponse


# ======================>>>>>>>>>>>>>>>>>>>>>> get_{{ cookiecutter.snake_name }}_by_id


class {{ cookiecutter.pascal_name }}InfoResponse(BaseSchema):
    """获取 {{ cookiecutter.snake_name }} by id 响应"""

    id: int = {{ cookiecutter.pascal_name }}Fields.id
    name: str = {{ cookiecutter.pascal_name }}Fields.name
    created_at: datetime.datetime = {{ cookiecutter.pascal_name }}Fields.created_at
    updated_at: datetime.datetime = {{ cookiecutter.pascal_name }}Fields.updated_at


class {{ cookiecutter.pascal_name }}InfoResponseModel(StandardResponse):
    """获取 {{ cookiecutter.snake_name }} by id 响应 Model"""

    data: {{ cookiecutter.pascal_name }}InfoResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> update_{{ cookiecutter.snake_name }}_by_id


class {{ cookiecutter.pascal_name }}UpdateRequest(BaseSchema):
    """更新 {{ cookiecutter.snake_name }} by id 请求"""

    name: str = {{ cookiecutter.pascal_name }}Fields.name


class {{ cookiecutter.pascal_name }}UpdateResponse(BaseSchema):
    """更新 {{ cookiecutter.snake_name }} by id 响应"""

    id: int = {{ cookiecutter.pascal_name }}Fields.id
    name: str = {{ cookiecutter.pascal_name }}Fields.name


class {{ cookiecutter.pascal_name }}UpdateResponseModel(StandardResponse):
    """更新 {{ cookiecutter.snake_name }} by id 响应 Model"""

    data: {{ cookiecutter.pascal_name }}UpdateResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> delete_{{ cookiecutter.snake_name }}_by_id


class {{ cookiecutter.pascal_name }}DeleteResponse(BaseSchema):
    """删除 {{ cookiecutter.snake_name }} by id 响应"""

    id: int = {{ cookiecutter.pascal_name }}Fields.id


class {{ cookiecutter.pascal_name }}DeleteResponseModel(StandardResponse):
    """删除 {{ cookiecutter.snake_name }} by id 响应 Model"""

    data: {{ cookiecutter.pascal_name }}DeleteResponse | None = None
