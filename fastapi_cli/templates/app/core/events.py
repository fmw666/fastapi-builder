# events 事件中如果要使用 aiomysql + sqlalchemy：
# 1、定义模型需换成 aiomysql.sa.Table 来定义，无法再使用类定义
# 2、engine 使用 aiomysql.sa 中 create_engine，不再使用 sqlalchemy
# 3、执行查询操作需要在一个连接对象上，不再使用 session

from typing import Callable
from fastapi import FastAPI

from core.logger import logger
# from db.events import close_db_connection, connect_to_db


# fastapi 启动事件句柄
def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        logger.info("fastapi 项目启动.")
        # await connect_to_db(app)
    return start_app


# fastapi 结束事件句柄
def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        logger.info("fastapi 项目结束.")
        # await close_db_connection(app)
    return stop_app
