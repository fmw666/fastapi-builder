from typing import Generic, List, Mapping, TypeVar
from pydantic import BaseModel

from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

T = TypeVar("T")


class StandardResponse(BaseModel):
    data: T | None = None
    code: int = 0
    message: str = ""

    def to_json(
        self,
        status_code: int = HTTP_200_OK,
        headers: Mapping[str, str] | None = None,
        **kwargs
    ):
        # Convert to JSON string using the custom encoder

        return JSONResponse(
            status_code=status_code,
            content=self.model_dump(mode="json"),
            headers=headers,
            **kwargs
        )


class PaginationResponse(BaseModel, Generic[T]):
    list: List[T]
    count: int
    total: int
    page: int = 1
    size: int | None = None
