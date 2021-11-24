from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from api.errors.http_error import http_error_handler
from api.errors.validation_error import http422_error_handler
from api.routes.api import router as api_router

from core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from core.events import create_start_app_handler, create_stop_app_handler

from utils.docs import get_custom_openapi

from middleware.logger import RequestLoggerMiddleware


def get_application() -> FastAPI:
    # 项目配置
    application = FastAPI(title=PROJECT_NAME, version=VERSION, debug=DEBUG)

    # 跨域中间件
    application.add_middleware(
        CORSMiddleware,
        # ALLOWED_HOSTS._items or ["*"]
        allow_origins=["http://127.0.0.1:8080", "http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 请求日志中间件
    application.add_middleware(RequestLoggerMiddleware)

    # 生成 OpenAPI 模式
    application.openapi = get_custom_openapi(application)

    # 事件处理句柄
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    # 异常处理句柄
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    # 路由导入
    application.include_router(api_router, prefix=API_PREFIX)

    return application


app = get_application()


if __name__ == "__main__":
    # 检查 mysql 相关内容
    import sys
    if "-c" in sys.argv:
        from utils.dbmanager import DBManager
        DBManager.check_and_autocreate()

    # 启动项目
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
