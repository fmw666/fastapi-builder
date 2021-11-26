from starlette.middleware.base import BaseHTTPMiddleware
from core.logger import logger


# 自定义访问日志中间件，基于BaseHTTPMiddleware的中间件实例
class RequestLoggerMiddleware(BaseHTTPMiddleware):

    # dispatch 必须实现
    async def dispatch(self, request, call_next):
        logger.info(f"{request.method} url:{request.url}\nheaders: {request.headers.get('user-agent')}"
                f"\nIP:{request.client.host}")
        response = await call_next(request)
        return response
