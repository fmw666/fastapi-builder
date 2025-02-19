from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from apps.app_user import doc, model, schema
from core.e import ErrorCode, ErrorMessage
from db.errors import EntityDoesNotExist
from db.database import get_async_db
from lib.jwt import create_access_token, get_current_user


router = APIRouter()


"""
接口：Authentication 用户认证

POST   /api/auth/login      ->  login    ->  用户登录
POST   /api/auth/register   ->  register ->  用户注册
GET    /api/auth/test       ->  test     ->  token 测试
POST   /api/auth/token      ->  token    ->  token 认证
"""


@router.post(
    "/login",
    name="用户登录",
    response_model=schema.UserLoginResponseModel,
    responses=doc.login_responses,
)
async def login(
    login_request: schema.UserLoginRequest = Body(..., openapi_examples=doc.login_request),
    db: AsyncSession = Depends(get_async_db),
):
    db_user: model.User | None = await model.User.get_by(db, username=login_request.username)
    if not db_user:
        return schema.UserLoginResponseModel(
            code=ErrorCode.USER_NOT_FOUND,
            message=ErrorMessage.get(ErrorCode.USER_NOT_FOUND),
        ).to_json(status_code=HTTP_404_NOT_FOUND)

    if not db_user.check_password(login_request.password):
        return schema.UserLoginResponseModel(
            code=ErrorCode.USER_PASSWORD_ERROR,
            message=ErrorMessage.get(ErrorCode.USER_PASSWORD_ERROR),
        ).to_json(HTTP_400_BAD_REQUEST)

    # 返回中必包含 "token_type": "bearer", "access_token": "xxxtokenxxx"
    return schema.UserLoginResponseModel(
        data=schema.UserLoginResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            token_type="bearer",
            access_token=create_access_token(db_user.id),
        )
    )


@router.post(
    "/register",
    name="用户注册",
    response_model=schema.UserRegisterResponseModel,
    responses=doc.register_responses,
)
async def register(
    user: schema.UserRegisterRequest = Body(..., openapi_examples=doc.register_request),
    db: AsyncSession = Depends(get_async_db),
):
    async with db.begin():
        db_user: model.User | None = await model.User.get_by(db, username=user.username)
        if db_user:
            return schema.UserRegisterResponseModel(
                code=ErrorCode.USER_NAME_EXIST,
                message=ErrorMessage.get(ErrorCode.USER_NAME_EXIST),
            ).to_json(status_code=HTTP_400_BAD_REQUEST)
        db_user: model.User | None = await model.User.get_by(db, email=user.email)
        if db_user:
            return schema.UserRegisterResponseModel(
                code=ErrorCode.USER_EMAIL_EXIST,
                message=ErrorMessage.get(ErrorCode.USER_EMAIL_EXIST),
            ).to_json(status_code=HTTP_400_BAD_REQUEST)

        db_user = await model.User.create(db, **user.model_dump())
        db_user.change_password(user.password)
        await db_user.save(db)
    return schema.UserRegisterResponseModel(
        data=schema.UserRegisterResponse.model_validate(db_user, from_attributes=True)
    )


"""以下接口只针对 Swagger UI 接口文档做测试，实际开发环境中不会存在"""


@router.get("/test", name="（仅用作 Swagger UI 调试）基于 token 身份认证测试")
async def test(current_user: model.User = Depends(get_current_user)):
    return current_user


@router.post("/token", name="（仅用作 Swagger UI 调试）文档身份认证接口")
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=f"{HTTP_400_BAD_REQUEST}_token error",
    )

    db_user: model.User | None = await model.User.get_by(db, username=form_data.username)
    if not db_user:
        raise wrong_login_error from EntityDoesNotExist

    if not db_user.check_password(form_data.password):
        raise wrong_login_error

    # 返回中必包含 "token_type": "bearer", "access_token": "xxxtokenxxx"
    return {
        "id": db_user.id,
        "name": db_user.username,
        "token_type": "bearer",
        "access_token": create_access_token(db_user.id),
    }
