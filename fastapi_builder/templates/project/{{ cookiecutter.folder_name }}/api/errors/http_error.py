from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from schemas.response import StandardResponse


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """
    http 异常处理句柄. 包含返回内容、状态码、响应头
    :param _: 请求对象
    :param exc: 异常对象
    :return: JSONResponse
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
