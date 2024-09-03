from dataclasses import dataclass

from pydantic import EmailStr, Field


@dataclass
class UserFields:
    id: int = Field(..., description="用户ID", example=1)
    username: str = Field(..., min_length=6, max_length=12, description="用户名", example="fmw666")
    password: str = Field(..., min_length=6, max_length=12, description="密码", example="123456")
    email: EmailStr = Field(..., max_length=32, description="邮箱", example="fmw19990718@gmail.com")
    token: str = Field(..., description="token", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjU1MzIzOTMsInN1YiI6IjYifQ.MXJutcQ2e7HHUC0FVkeqRtHyn6fT1fclPugo-qpy8e4")  # noqa
