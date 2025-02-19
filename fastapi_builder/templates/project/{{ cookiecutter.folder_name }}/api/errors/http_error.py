from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from schemas.response import StandardResponse


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """
    fastapi http 异常处理句柄. 包含返回内容、状态码、响应头

    Args:
        _ (Request): starlette.requests.Request
        exc (HTTPException): 响应异常

    Returns:
        JSONResponse: 返回内容、状态码、响应头

    Raises:
        ValueError: 消息处理失败，抛出 ValueError 异常
    """
    try:
        code, message = exc.detail.split("_", 1)
        code = int(code)
    except ValueError:
        code, message = exc.status_code, "Unknown error"

    return StandardResponse(
        code=code,
        message=message,
        data=None,
    ).to_json(status_code=exc.status_code, headers=getattr(exc, "headers"))
