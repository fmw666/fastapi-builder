from typing import List, Literal
from fastapi import Query
from pydantic import EmailStr, Field, field_validator

from apps.app_user.field import UserFields
from apps.app_user.model import User
from models.base import get_model_fields_from_objects
from schemas.base import BaseSchema, QuerySchema
from schemas.response import PaginationResponse, StandardResponse


# ======================>>>>>>>>>>>>>>>>>>>>>> user_register


class UserRegisterRequest(BaseSchema):
    """用户注册 请求"""

    email: EmailStr = UserFields.email
    username: str = UserFields.username
    password: str = UserFields.password


class UserRegisterResponse(BaseSchema):
    """用户注册 响应"""

    id: int = UserFields.id
    username: str = UserFields.username
    email: EmailStr = UserFields.email


class UserRegisterResponseModel(StandardResponse):
    """用户注册 响应 Model"""

    data: UserRegisterResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> user_login


class UserLoginRequest(BaseSchema):
    """登录 User 请求"""

    username: str = Field(..., min_length=6, max_length=12, description="用户名")
    password: str = Field(..., min_length=6, max_length=12, description="密码")


class UserLoginResponse(BaseSchema):
    """登录 User 响应"""

    id: int = UserFields.id
    username: str = UserFields.username
    email: EmailStr = UserFields.email
    token_type: str = Field("bearer", description="token 类型")
    access_token: str = UserFields.token


class UserLoginResponseModel(StandardResponse):
    """登录 User 响应 Model"""

    data: UserLoginResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> get_user_list


class UserListQueryRequest(QuerySchema):
    """获取用户列表 查询 请求"""

    order_by: Literal["id", "created_at"] = Query(
        User.id.name, description="排序字段. eg: id created_at"
    )

    @field_validator("order_by")
    def validate_order_by(cls, v: str) -> str:
        order_fields = get_model_fields_from_objects(User, [User.id, User.created_at])
        if v not in order_fields:
            raise ValueError(f"order_by must be one of {order_fields}")
        return v


class UserListResponse(BaseSchema):
    """获取用户列表 响应"""

    id: int = UserFields.id
    username: str = UserFields.username
    email: EmailStr = UserFields.email


class UserListResponseModel(StandardResponse):
    """获取用户列表 响应 Model"""

    data: PaginationResponse[UserListResponse]


# ======================>>>>>>>>>>>>>>>>>>>>>> create_user


class UserCreateRequest(BaseSchema):
    """用户创建 请求"""

    email: EmailStr = UserFields.email
    username: str = UserFields.username
    password: str = UserFields.password


class UserCreateResponse(BaseSchema):
    """用户创建 响应"""

    id: int = UserFields.id
    email: EmailStr = UserFields.email
    username: str = UserFields.username


class UserCreateResponseModel(StandardResponse):
    """用户创建 响应 Model"""

    data: UserCreateResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> patch_users


class UsersPatchRequest(BaseSchema):
    """更新用户信息 请求"""

    ids: List[int] = Field(..., description="用户 id 列表")
    avatar_url: str = Field(..., description="头像地址")


class UsersPatchResponse(BaseSchema):
    """更新用户信息 响应"""

    ids: List[int] = Field(..., description="用户 id 列表")
    avatar_url: str = Field(..., description="头像地址")


class UsersPatchResponseModel(StandardResponse):
    """更新用户信息 响应 Model"""

    data: UsersPatchResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> delete_users


class UsersDeleteResponse(BaseSchema):
    """删除用户信息 响应"""

    ids: List[int] = Field(..., description="用户 id 列表")


class UsersDeleteResponseModel(StandardResponse):
    """删除用户信息 响应 Model"""

    data: UsersDeleteResponse


# ======================>>>>>>>>>>>>>>>>>>>>>> get_user_by_id


class UserInfoResponse(BaseSchema):
    """获取用户信息 响应"""

    id: int = UserFields.id
    username: str = UserFields.username
    email: EmailStr = UserFields.email


class UserInfoResponseModel(StandardResponse):
    """获取用户信息 响应 Model"""

    data: UserInfoResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> update_user_by_id


class UserUpdateRequest(BaseSchema):
    """更新用户信息 请求"""

    username: str | None = Field(None, min_length=6, max_length=12, description="用户名")
    email: EmailStr | None = Field(None, max_length=32, description="邮箱")


class UserUpdateResponse(BaseSchema):
    """更新用户信息 响应"""

    id: int = UserFields.id
    username: str = UserFields.username
    email: EmailStr = UserFields.email


class UserUpdateResponseModel(StandardResponse):
    """更新用户信息 响应 Model"""

    data: UserUpdateResponse | None = None


# ======================>>>>>>>>>>>>>>>>>>>>>> delete_user_by_id


class UserDeleteResponse(BaseSchema):
    """删除用户信息 响应"""

    id: int = UserFields.id


class UserDeleteResponseModel(StandardResponse):
    """删除用户信息 响应 Model"""

    data: UserDeleteResponse | None = None
