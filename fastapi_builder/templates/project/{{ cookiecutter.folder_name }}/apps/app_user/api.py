from datetime import datetime
from typing import List

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from apps.app_user import doc, model, schema
from core.e import ErrorCode, ErrorMessage
from db.database import get_async_db
from lib.jwt import get_current_user
from schemas.base import OrderType
from schemas.response import PaginationResponse


router = APIRouter()


"""
接口：User 用户表增删改查

GET    /api/users            ->  get_users    ->  获取所有用户
POST   /api/users            ->  add_user     ->  创建单个用户
PATCH  /api/users            ->  patch_users  ->  批量更新用户
DELETE /api/users            ->  delete_users ->  批量注销用户
GET    /api/users/{user_id}  ->  get_user     ->  获取单个用户
PUT    /api/users/{user_id}  ->  update_user  ->  更新单个用户
DELETE /api/users/{user_id}  ->  delete_user  ->  注销单个用户
"""


@router.get(
    "",
    name="获取用户列表",
    response_model=schema.UserListResponseModel,
    responses=doc.get_users_responses,
    dependencies=[Depends(get_current_user)],
)
async def get_users(
    query_params: schema.UserListQueryRequest = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    # 获取总数
    total_count = (await db.execute(select(func.count()).select_from(model.User))).scalar()

    # 查询
    stmt = await model.User.query()
    if query_params.size is not None:
        offset = (query_params.page - 1) * query_params.size
        stmt = stmt.offset(offset).limit(query_params.size)
    if query_params.order_type:
        stmt = stmt.order_by(
            getattr(model.User, query_params.order_by).desc()
            if query_params.order_type == OrderType.DESC
            else getattr(model.User, query_params.order_by).asc()
        )

    db_users: List[model.User] = (await db.execute(stmt)).scalars().all()

    return schema.UserListResponseModel(
        data=PaginationResponse(
            list=[
                schema.UserListResponse.model_validate(
                    db_user, from_attributes=True
                ).model_dump()
                for db_user in db_users
            ],
            count=len(db_users),
            page=query_params.page,
            size=query_params.size,
            total=total_count,
        ).model_dump()
    )


@router.post(
    "",
    name="创建单个用户",
    response_model=schema.UserCreateResponseModel,
    responses=doc.create_user_responses,
    dependencies=[Depends(get_current_user)],
)
async def create_user(
    user: schema.UserCreateRequest = Body(..., openapi_examples=doc.create_user_request),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        # 参数检查
        stmt = (await model.User.query()).filter(
            model.User.email == user.email or model.User.username == user.username
        )
        db_users: List[model.User] = (await db.execute(stmt)).scalars().all()
        if len(db_users) > 0:
            return schema.UserCreateResponseModel(
                code=ErrorCode.USER_EXIST,
                message=ErrorMessage.get(ErrorCode.USER_EXIST),
            ).to_json(status_code=HTTP_400_BAD_REQUEST)

        db_user: model.User = await model.User.create(db, **user.model_dump())
    return schema.UserCreateResponseModel(
        data=schema.UserCreateResponse.model_validate(db_user, from_attributes=True)
    )


@router.patch(
    "",
    name="批量更新用户",
    response_model=schema.UsersPatchResponseModel,
    responses=doc.patch_users_responses,
    dependencies=[Depends(get_current_user)],
)
async def patch_users(
    users_patch_request: schema.UsersPatchRequest = Body(
        ..., openapi_examples=doc.patch_users_request
    ),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        stmt = (await model.User.query()).filter(model.User.id.in_(users_patch_request.ids))
        db_users: List[model.User] = (await db.execute(stmt)).scalars().all()
        for db_user in db_users:
            db_user.avatar_url = users_patch_request.avatar_url
        db.flush()
    return schema.UsersPatchResponseModel(
        data=schema.UsersPatchResponse(
            ids=[db_user.id for db_user in db_users],
            avatar_url=users_patch_request.avatar_url,
        )
    )


@router.delete(
    "",
    name="批量注销用户",
    response_model=schema.UsersDeleteResponseModel,
    responses=doc.delete_users_responses,
    dependencies=[Depends(get_current_user)],
)
async def delete_users(
    ids: List[int] = Body(
        ...,
        description="用户 id 列表",
        embed=True,
        json_schema_extra=doc.delete_users_request,
    ),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        stmt_select = (await model.User.query()).filter(model.User.id.in_(ids))
        db_users: List[model.User] = (await db.execute(stmt_select)).scalars().all()

        stmt_update = update(model.User).where(model.User.deleted_at.is_(None)).filter(
            model.User.id.in_(ids)
        ).values(deleted_at=datetime.now())
        await db.execute(stmt_update)
    return schema.UsersDeleteResponseModel(
        data=schema.UsersDeleteResponse(ids=[db_user.id for db_user in db_users])
    )


@router.get(
    "/{user_id}",
    name="查询用户 by user_id",
    response_model=schema.UserInfoResponseModel,
    responses=doc.get_user_by_id_responses,
    dependencies=[Depends(get_current_user)],
)
async def get_user_by_id(
    user_id: int = Path(..., description="用户 id", ge=1, example=1),
    db: AsyncSession = Depends(get_async_db),
):
    db_user: model.User | None = await model.User.get_by(db, id=user_id)
    if db_user is None:
        return schema.UserInfoResponseModel(
            code=ErrorCode.USER_NOT_FOUND,
            message=ErrorMessage.get(ErrorCode.USER_NOT_FOUND),
        ).to_json(status_code=HTTP_404_NOT_FOUND)

    return schema.UserInfoResponseModel(
        data=schema.UserInfoResponse.model_validate(db_user, from_attributes=True)
    )


@router.put(
    "/{user_id}",
    name="更改用户 by user_id",
    response_model=schema.UserUpdateResponseModel,
    responses=doc.update_user_by_id_responses,
    dependencies=[Depends(get_current_user)],
)
async def update_user_by_id(
    user_id: int = Path(..., ge=1),
    user_update_request: schema.UserUpdateRequest = Body(
        ..., openapi_examples=doc.update_user_by_id_request
    ),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        db_user: model.User | None = await model.User.get_by(db, id=user_id)
        if db_user is None:
            return schema.UserUpdateResponseModel(
                code=ErrorCode.USER_NOT_FOUND,
                message=ErrorMessage.get(ErrorCode.USER_NOT_FOUND),
            )

        # 更新 username
        if user_update_request.username is not None:
            if await model.User.get_by(db, username=user_update_request.username):
                return schema.UserUpdateResponseModel(
                    code=ErrorCode.USER_EXIST,
                    message=ErrorMessage.get(ErrorCode.USER_EXIST),
                )
            db_user.username = user_update_request.username
        # 更新 email
        if user_update_request.email is not None:
            if await model.User.get_by(db, email=user_update_request.email):
                return schema.UserUpdateResponseModel(
                    code=ErrorCode.USER_EXIST,
                    message=ErrorMessage.get(ErrorCode.USER_EXIST),
                )
            db_user.email = user_update_request.email

        await db_user.save(db)

    return schema.UserUpdateResponseModel(
        data=schema.UserUpdateResponse.model_validate(
            db_user, from_attributes=True
        ).model_dump(),
    )


@router.delete(
    "/{user_id}",
    name="注销用户 by user_id",
    response_model=schema.UserDeleteResponseModel,
    responses=doc.delete_user_by_id_responses,
    dependencies=[Depends(get_current_user)],
)
async def delete_user_by_id(
    user_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        db_user: model.User | None = await model.User.get_by(db, id=user_id)
        if db_user is None:
            return schema.UserDeleteResponseModel(
                code=ErrorCode.USER_NOT_FOUND,
                message=ErrorMessage.get(ErrorCode.USER_NOT_FOUND),
            ).to_json(status_code=HTTP_404_NOT_FOUND)
        await db_user.remove(db)
    return schema.UserDeleteResponseModel(
        data=schema.UserDeleteResponse(id=db_user.id)
    )
