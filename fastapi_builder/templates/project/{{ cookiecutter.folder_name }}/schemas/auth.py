from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from app_user.model import User
from schemas.base import Schema


class UserInLogin(Schema):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class UserWithToken(User):
    token: str


class UserInResponse(Schema):
    user: UserWithToken
