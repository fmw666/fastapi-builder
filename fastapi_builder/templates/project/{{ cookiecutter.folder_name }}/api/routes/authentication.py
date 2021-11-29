from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_400_BAD_REQUEST

from db.errors import EntityDoesNotExist
from db.database import get_db
from app_user.schema import UserCreate
from app_user.model import User

from utils import consts
from lib.jwt import create_access_token, get_current_user
from lib.security import OAuth2Form


router = APIRouter()


"""
接口：Authentication 用户认证

POST   /api/auth/login      ->  login    ->  用户登录
POST   /api/auth/register   ->  register ->  用户注册
GET    /api/auth/test       ->  test     ->  token 测试
"""

# 用户登录
@router.post("/login", name="用户登录")
async def login(form_data: OAuth2Form = Depends(), db: Session = Depends(get_db)):
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=consts.INCORRECT_LOGIN_INPUT,
    )

    user = User.get_by(db, username=form_data.username)
    if not user:
        raise wrong_login_error from EntityDoesNotExist

    if not user.check_password(form_data.password):
        raise wrong_login_error
    
    # 返回中必包含 "token_type": "bearer", "access_token": "xxxtokenxxx"
    return {"id": user.id, "name": user.username, "token_type": "bearer", "access_token": create_access_token(user.id)}


# 用户注册
@router.post("/register", name="用户注册")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # 判断数据库是否存在
    if User.get_by(db, username=user.username):
        raise HTTPException(
            status_code=404,
            detail="用户已存在"
        )

    db_user = User(**user.dict())
    db_user.change_password(user.password)
    db_user.save(db)
    return db_user


"""以下接口只针对 Swagger UI 接口文档做测试，实际开发环境中不会存在"""

# 测试 token 的接口
@router.get("/test", name="基于 token 身份认证测试")
async def test(current_user: User = Depends(get_current_user)):
    return current_user


# docs 身份认证表单接口（仅做测试）
@router.post("/token", name="文档身份认证接口")
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 使用 OAuth2PasswordRequestForm 才能正常登录
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=consts.INCORRECT_LOGIN_INPUT,
    )

    user = User.get_by(db, username=form_data.username)
    if not user:
        raise wrong_login_error from EntityDoesNotExist

    if not user.check_password(form_data.password):
        raise wrong_login_error
    
    # 返回中必包含 "token_type": "bearer", "access_token": "xxxtokenxxx"
    return {"id": user.id, "name": user.username, "token_type": "bearer", "access_token": create_access_token(user.id)}
