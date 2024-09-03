from starlette.middleware.base import BaseHTTPMiddleware
from core.logger import app_logger as logger


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """自定义访问日志中间件，基于BaseHTTPMiddleware的中间件实例"""

    async def dispatch(self, request, call_next):
        """必须重载 dispatch 方法"""
        logger.info(
            f"{request.method} url:{request.url}\nheaders: {request.headers.get('user-agent')}"
            f"\nIP:{request.client.host}"
        )
        response = await call_next(request)
        return response
