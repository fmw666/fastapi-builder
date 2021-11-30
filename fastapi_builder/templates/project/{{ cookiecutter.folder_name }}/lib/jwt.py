from datetime import timedelta, datetime
from fastapi import Depends, HTTPException

from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app_user.model import User

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, JWT_ALGORITHM
from db.database import get_db
from lib.security import oauth2_scheme


# 生成token
def create_access_token(subject: int, expires_delta: timedelta = None) -> str:
    """
    使用 python-jose 库生成用户token
    :param subject: 一般传递一个用户 id
    :param expires_delta: 有效时间
    :return: 加密后的token字符串
    """
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY._value, algorithm=JWT_ALGORITHM)
    return encoded_jwt


# 获取当前用户. 登录依赖
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, key=SECRET_KEY._value, algorithms=JWT_ALGORITHM)
    except (jwt.JWTError, ValidationError, AttributeError):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="认证失败",
            # 根据 OAuth2 规范，认证失败需要在响应头中添加如下键值对
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload["sub"]
    user = User.get_by(db, id=user_id)
    if not user:
        raise HTTPException(status_code=403, detail="用户不存在")
    return {"id": user.id, "username": user.username}
