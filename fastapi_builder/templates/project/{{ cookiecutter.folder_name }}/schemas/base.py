import re
import datetime

from enum import Enum

from fastapi import Query
from pydantic import BaseModel, ConfigDict


def convert_datetime(dt: datetime.datetime) -> str:
    """
    转换日期格式

    Args:
        dt (datetime.datetime): 日期时间对象

    Returns:
        str: 日期时间字符串. eg: 2021-11-04 14:17:10
    """
    return (
        dt.replace(tzinfo=datetime.timezone.utc)
        .isoformat()
        .replace("+00:00", "")
        .replace("T", " ")
    )


def convert_field_to_snake_case(string: str) -> str:
    """
    将驼峰命名转换为蛇形命名

    Args:
        string (str): 驼峰命名字符串

    Returns:
        str: 蛇形命名字符串. eg: camel_case
    """
    snake_case = re.sub(r"(?P<key>[A-Z])", r"_\g<key>", string)
    return snake_case.lower().strip("_")


class BaseSchema(BaseModel):
    """自定义基础 schema 类"""

    def model_dump_json(self, force_by_alias: bool = True, **kwargs):
        """重写 model_dump_json 方法, 默认不转换 alias"""
        if not force_by_alias:
            return super().model_dump_json(**kwargs)
        return super().model_dump_json(by_alias=True, **kwargs)

    class Config(ConfigDict):
        populate_by_name = True
        json_encoders = {datetime.datetime: convert_datetime}
        alias_generator = convert_field_to_snake_case


class OrderType(str, Enum):
    """排序方式"""

    ASC = "asc"
    DESC = "desc"


class QuerySchema(BaseModel):
    """自定义查询 schema 类"""

    page: int = Query(1, ge=1, example=1, description="页码. 如果不填则全查")
    size: int | None = Query(None, ge=1, description="每页数量. 如果不填则全查")
    order_by: str = Query("id", description="排序字段. eg: id updated_at")
    order_type: OrderType = Query(OrderType.ASC, description="排序方式. eg: desc asc")
    q: str | None = Query(None, description="模糊查询. eg: name=xxx")
