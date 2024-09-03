from datetime import timedelta, datetime
from fastapi import Depends, HTTPException

from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_401_UNAUTHORIZED

from apps.app_user.model import User

from core.config import settings
from core.e import ErrorCode, ErrorMessage
from db.database import get_async_db
from lib.security import oauth2_scheme


def create_access_token(subject: int, expires_delta: timedelta = None) -> str:
    """
    使用 python-jose 库生成用户 token

    Args:
        subject (int): 一般传递一个用户 id
        expires_delta (timedelta): token 有效时间

    Returns:
        str: 加密后的 token 字符串
    """
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=settings.SECRET_KEY._value,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


async def get_current_user(
    db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    获取当前登录用户

    Args:
        db (AsyncSession): 数据库连接
        token (str): 登录凭证

    Returns:
        User: 当前登录用户
    """
    try:
        payload = jwt.decode(
            token, key=settings.SECRET_KEY._value, algorithms=settings.JWT_ALGORITHM
        )
    except (ValidationError, AttributeError, JWTError):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=f"{ErrorCode.USER_UNAUTHORIZED}_{ErrorMessage.get(ErrorCode.USER_UNAUTHORIZED)}",
            # 根据 OAuth2 规范，认证失败需要在响应头中添加如下键值对
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload["sub"]
    async with db.begin():
        result = await db.execute(select(User).filter(User.id == user_id))
        db_user = result.scalars().first()

        if db_user is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=f"{ErrorCode.USER_NOT_FOUND}_{ErrorMessage.get(ErrorCode.USER_NOT_FOUND)}",
                # 根据 OAuth2 规范，认证失败需要在响应头中添加如下键值对
                headers={"WWW-Authenticate": "Bearer"},
            )
    return db_user
