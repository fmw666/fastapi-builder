import re
import datetime

from pydantic import BaseModel, BaseConfig


# 转换日期格式. eg: 2021-11-04 14:17:10
def convert_datetime(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "").replace("T", " ")


# 转换命名格式. 驼峰命名：camel case  蛇形命名：snake case
def convert_field_to_snake_case(string: str) -> str:
    snake_case = re.sub(r"(?P<key>[A-Z])", r"_\g<key>", string)
    return snake_case.lower().strip("_")


class BaseSchema(BaseModel):
    """自定义基础 schema 类"""
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime}
        alias_generator = convert_field_to_snake_case

