from fastapi import APIRouter

from . import authentication, user


router = APIRouter()
router.include_router(authentication.router, tags=["用户认证"], prefix="/auth")
router.include_router(user.router, tags=["用户类"], prefix="/users")
