from fastapi import APIRouter

from api.routes.authentication import router as authentication_router
from apps.app_user.api import router as user_router


router = APIRouter()
router.include_router(authentication_router, tags=["用户认证"], prefix="/auth")
router.include_router(user_router, tags=["用户类"], prefix="/users")
