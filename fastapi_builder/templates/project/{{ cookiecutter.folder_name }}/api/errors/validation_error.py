from typing import Union

from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from schemas.response import StandardResponse


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError, ValueError],
) -> JSONResponse:
    """
    Custom error handler for 422 status code
    :param _: Request
    :param exc: Union[RequestValidationError, ValidationError]
    :return: JSONResponse
    """
    if isinstance(exc, ValueError):
        errors = [
            {
                "type": "value_error",
                "loc": ["body"],
                "msg": str(exc),
                "input": None,
                "ctx": None,
            }
        ]
    else:
        errors = exc.errors()

    return StandardResponse(
        code=HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation error",
        data={"errors": errors},
    ).to_json(status_code=HTTP_422_UNPROCESSABLE_ENTITY)


# Add `errors` to the OpenAPI schema
validation_error_response_definition["properties"] = {
    "data": {
        "type": "object",
        "properties": {
            "errors": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "loc": {"type": "array", "items": {"type": "string"}},
                        "msg": {"type": "string"},
                        "input": {"type": "object"},
                        "ctx": {"type": "object"}
                    }
                }
            }
        }
    },
    "code": {"type": "integer", "example": 422},
    "message": {"type": "string"}
}
