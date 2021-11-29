from fastapi import APIRouter

from . import authentication
import app_user.api


router = APIRouter()
router.include_router(authentication.router, tags=["用户认证"], prefix="/auth")
router.include_router(app_user.api.router, tags=["用户类"], prefix="/users")
