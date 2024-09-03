from typing import Any, Dict
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def get_custom_openapi(app: FastAPI, **kw) -> Dict[str, Any]:
    """
    自定义 OpenAPI

    Args:
        app (FastAPI): FastAPI 对象
        **kw: 其他参数

    Returns:
        Dict[str, Any]: OpenAPI 对象
    """

    def custom_openapi() -> Dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=kw.get("title", "OpenAPI schema Docs"),
            version=kw.get("version", "1.0.0"),
            description=kw.get("description", "nice to meet you."),
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return custom_openapi
