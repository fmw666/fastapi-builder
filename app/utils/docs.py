from typing import Any, Dict
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


# 生成 OpenAPI 模式
def get_custom_openapi(app: FastAPI, **kw) -> Dict[str, Any]:

    def custom_openapi() -> Dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=kw.get("title", "OpenAPI schema Docs"),
            version=kw.get("version", "1.0.1"),
            description=kw.get("description", "nice to meet you."),
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return custom_openapi
