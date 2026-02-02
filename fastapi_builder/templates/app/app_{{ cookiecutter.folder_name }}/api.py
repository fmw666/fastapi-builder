from typing import List

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from apps.app_{{ cookiecutter.folder_name }} import doc
from apps.app_{{ cookiecutter.folder_name }}.schema import (
    {{ cookiecutter.pascal_name }}CreateRequest,
    {{ cookiecutter.pascal_name }}CreateResponse,
    {{ cookiecutter.pascal_name }}CreateResponseModel,
    {{ cookiecutter.pascal_name }}DeleteResponse,
    {{ cookiecutter.pascal_name }}DeleteResponseModel,
    {{ cookiecutter.pascal_name }}InfoResponse,
    {{ cookiecutter.pascal_name }}InfoResponseModel,
    {{ cookiecutter.pascal_name }}ListQueryRequest,
    {{ cookiecutter.pascal_name }}ListResponse,
    {{ cookiecutter.pascal_name }}ListResponseModel,
    {{ cookiecutter.pascal_name }}UpdateRequest,
    {{ cookiecutter.pascal_name }}UpdateResponse,
    {{ cookiecutter.pascal_name }}UpdateResponseModel,
    {{ cookiecutter.pascal_name }}sDeleteResponse,
    {{ cookiecutter.pascal_name }}sDeleteResponseModel,
    {{ cookiecutter.pascal_name }}sPatchRequest,
    {{ cookiecutter.pascal_name }}sPatchResponse,
    {{ cookiecutter.pascal_name }}sPatchResponseModel,
)
from apps.app_{{ cookiecutter.folder_name }}.service import {{ cookiecutter.pascal_name }}Service
from core.e import ErrorCode, ErrorMessage
from db.database import get_async_db
from schemas.response import PaginationResponse


router = APIRouter()


"""
接口：{{ cookiecutter.pascal_name }} 表增删改查

GET    /api/{{ cookiecutter.snake_name }}s      {% for i in range(cookiecutter.snake_name|length - 1) %} {% endfor %}   ->  get_{{ cookiecutter.snake_name }}s    ->  获取所有 {{ cookiecutter.snake_name }}
POST   /api/{{ cookiecutter.snake_name }}s      {% for i in range(cookiecutter.snake_name|length - 1) %} {% endfor %}   ->  add_{{ cookiecutter.snake_name }}     ->  创建单个 {{ cookiecutter.snake_name }}
PATCH  /api/{{ cookiecutter.snake_name }}s      {% for i in range(cookiecutter.snake_name|length - 1) %} {% endfor %}   ->  patch_{{ cookiecutter.snake_name }}s  ->  批量更新 {{ cookiecutter.snake_name }}
DELETE /api/{{ cookiecutter.snake_name }}s      {% for i in range(cookiecutter.snake_name|length - 1) %} {% endfor %}   ->  delete_{{ cookiecutter.snake_name }}s ->  批量注销 {{ cookiecutter.snake_name }}
GET    /api/{{ cookiecutter.snake_name }}s/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}  ->  get_{{ cookiecutter.snake_name }}     ->  获取单个 {{ cookiecutter.snake_name }}
PUT    /api/{{ cookiecutter.snake_name }}s/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}  ->  update_{{ cookiecutter.snake_name }}  ->  更新单个 {{ cookiecutter.snake_name }}
DELETE /api/{{ cookiecutter.snake_name }}s/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}  ->  delete_{{ cookiecutter.snake_name }}  ->  注销单个 {{ cookiecutter.snake_name }}
"""


@router.get(
    "",
    name="获取所有 {{ cookiecutter.snake_name }}",
    response_model={{ cookiecutter.pascal_name }}ListResponseModel,
    responses=doc.get_{{ cookiecutter.snake_name }}s_responses,
)
async def get_{{ cookiecutter.snake_name }}s(
    query_params: {{ cookiecutter.pascal_name }}ListQueryRequest = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    service = {{ cookiecutter.pascal_name }}Service(db)
    data, total_count = await service.get_list(query_params)

    return {{ cookiecutter.pascal_name }}ListResponseModel(
        data=PaginationResponse(
            list=[
                {{ cookiecutter.pascal_name }}ListResponse.model_validate(
                    item, from_attributes=True
                ).model_dump()
                for item in data
            ],
            count=len(data),
            page=query_params.page,
            size=query_params.size,
            total=total_count,
        ).model_dump()
    )


@router.post(
    "",
    name="创建单个 {{ cookiecutter.snake_name }}",
    response_model={{ cookiecutter.pascal_name }}CreateResponseModel,
    responses=doc.create_{{ cookiecutter.snake_name }}_responses,
)
async def create_{{ cookiecutter.snake_name }}(
    {{ cookiecutter.snake_name }}: {{ cookiecutter.pascal_name }}CreateRequest = Body(
        ..., openapi_examples=doc.create_{{ cookiecutter.snake_name }}_request
    ),
    db: AsyncSession = Depends(get_async_db),
):
    service = {{ cookiecutter.pascal_name }}Service(db)
    db_{{ cookiecutter.snake_name }} = await service.create({{ cookiecutter.snake_name }})
    return {{ cookiecutter.pascal_name }}CreateResponseModel(
        data={{ cookiecutter.pascal_name }}CreateResponse.model_validate(db_{{ cookiecutter.snake_name }}, from_attributes=True)
    )


@router.patch(
    "",
    name="批量更新 {{ cookiecutter.snake_name }}",
    response_model={{ cookiecutter.pascal_name }}sPatchResponseModel,
    responses=doc.patch_{{ cookiecutter.snake_name }}s_responses,
)
async def patch_{{ cookiecutter.snake_name }}s(
    {{ cookiecutter.snake_name }}s_patch_request: {{ cookiecutter.pascal_name }}sPatchRequest = Body(
        ..., openapi_examples=doc.patch_{{ cookiecutter.snake_name }}s_request
    ),
    db: AsyncSession = Depends(get_async_db),
):
    service = {{ cookiecutter.pascal_name }}Service(db)
    db_{{ cookiecutter.snake_name }}s = await service.patch_batch({{ cookiecutter.snake_name }}s_patch_request)
    return {{ cookiecutter.pascal_name }}sPatchResponseModel(
        data={{ cookiecutter.pascal_name }}sPatchResponse(
            ids=[item.id for item in db_{{ cookiecutter.snake_name }}s],
            name={{ cookiecutter.snake_name }}s_patch_request.name,
        )
    )


@router.delete(
    "",
    name="批量注销 {{ cookiecutter.snake_name }}",
    response_model={{ cookiecutter.pascal_name }}sDeleteResponseModel,
    responses=doc.delete_{{ cookiecutter.snake_name }}s_responses,
)
async def delete_{{ cookiecutter.snake_name }}s(
    ids: List[int] = Body(
        ...,
        description="{{ cookiecutter.snake_name }} id 列表",
        embed=True,
        json_schema_extra=doc.delete_{{ cookiecutter.snake_name }}s_request,
    ),
    db: AsyncSession = Depends(get_async_db),
):
    service = {{ cookiecutter.pascal_name }}Service(db)
    db_{{ cookiecutter.snake_name }}s = await service.delete_batch(ids)
    return {{ cookiecutter.pascal_name }}sDeleteResponseModel(
        data={{ cookiecutter.pascal_name }}sDeleteResponse(
            ids=[item.id for item in db_{{ cookiecutter.snake_name }}s]
        )
    )


@router.get(
    "/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}",
    name="获取单个 {{ cookiecutter.snake_name }} by id",
    response_model={{ cookiecutter.pascal_name }}InfoResponseModel,
    responses=doc.get_{{ cookiecutter.snake_name }}_by_id_responses,
)
async def get_{{ cookiecutter.snake_name }}_by_id(
    {{ cookiecutter.snake_name }}_id: int = Path(..., description="{{ cookiecutter.snake_name }} id", ge=1, example=1),
    db: AsyncSession = Depends(get_async_db),
):
    service = {{ cookiecutter.pascal_name }}Service(db)
    db_{{ cookiecutter.snake_name }} = await service.get_by_id({{ cookiecutter.snake_name }}_id)
    if db_{{ cookiecutter.snake_name }} is None:
        return {{ cookiecutter.pascal_name }}InfoResponseModel(
            code=ErrorCode.NOT_FOUND,
            message=ErrorMessage.get(ErrorCode.NOT_FOUND),
        ).to_json(status_code=HTTP_404_NOT_FOUND)

    return {{ cookiecutter.pascal_name }}InfoResponseModel(
        data={{ cookiecutter.pascal_name }}InfoResponse.model_validate(db_{{ cookiecutter.snake_name }}, from_attributes=True)
    )


@router.put(
    "/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}",
    name="更新单个 {{ cookiecutter.snake_name }} by id",
    response_model={{ cookiecutter.pascal_name }}UpdateResponseModel,
    responses=doc.update_{{ cookiecutter.snake_name }}_by_id_responses,
)
async def update_{{ cookiecutter.snake_name }}_by_id(
    {{ cookiecutter.snake_name }}_id: int = Path(..., description="{{ cookiecutter.snake_name }} id", ge=1),
    {{ cookiecutter.snake_name }}_update_request: {{ cookiecutter.pascal_name }}UpdateRequest = Body(
        ..., openapi_examples=doc.update_{{ cookiecutter.snake_name }}_by_id_request
    ),
    db: AsyncSession = Depends(get_async_db),
):
    service = {{ cookiecutter.pascal_name }}Service(db)
    db_{{ cookiecutter.snake_name }} = await service.update_by_id({{ cookiecutter.snake_name }}_id, {{ cookiecutter.snake_name }}_update_request)
    
    if db_{{ cookiecutter.snake_name }} is None:
        return {{ cookiecutter.pascal_name }}UpdateResponseModel(
            code=ErrorCode.NOT_FOUND,
            message=ErrorMessage.get(ErrorCode.NOT_FOUND),
        )

    return {{ cookiecutter.pascal_name }}UpdateResponseModel(
        data={{ cookiecutter.pascal_name }}UpdateResponse.model_validate(
            db_{{ cookiecutter.snake_name }}, from_attributes=True
        ).model_dump(),
    )


@router.delete(
    "/{{'{'}}{{ cookiecutter.snake_name }}_id{{'}'}}",
    name="注销单个 {{ cookiecutter.snake_name }} by id",
    response_model={{ cookiecutter.pascal_name }}DeleteResponseModel,
    responses=doc.delete_{{ cookiecutter.snake_name }}_by_id_responses,
)
async def delete_{{ cookiecutter.snake_name }}_by_id(
    {{ cookiecutter.snake_name }}_id: int = Path(..., description="{{ cookiecutter.snake_name }} id", ge=1),
    db: AsyncSession = Depends(get_async_db),
):
    service = {{ cookiecutter.pascal_name }}Service(db)
    db_{{ cookiecutter.snake_name }} = await service.delete_by_id({{ cookiecutter.snake_name }}_id)
    if db_{{ cookiecutter.snake_name }} is None:
        return {{ cookiecutter.pascal_name }}DeleteResponseModel(
            code=ErrorCode.NOT_FOUND,
            message=ErrorMessage.get(ErrorCode.NOT_FOUND),
        ).to_json(status_code=HTTP_404_NOT_FOUND)

    return {{ cookiecutter.pascal_name }}DeleteResponseModel(data={{ cookiecutter.pascal_name }}DeleteResponse(id=db_{{ cookiecutter.snake_name }}.id))
