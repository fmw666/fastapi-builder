import datetime
from typing import Optional

from pydantic import EmailStr

from schemas.base import BaseSchema

class UserBase(BaseSchema):
    """用户基础"""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """用户创建"""
    password: str

class UserInfo(UserBase):
    """用户信息"""
    id: int
    updated_at: Optional[datetime.datetime] = None
    class Config(object):
        orm_mode = True