# events 事件中如果要使用 aiomysql + sqlalchemy：
# 1、定义模型需换成 aiomysql.sa.Table 来定义，无法再使用类定义
# 2、engine 使用 aiomysql.sa 中 create_engine，不再使用 sqlalchemy
# 3、执行查询操作需要在一个连接对象上，不再使用 session

import aiomysql
from fastapi import FastAPI

from core.logger import logger
from core.config import MYSQL_DB_INFO_DICT


# 创建 mysql 连接池，并用 fastapi state 存储
async def connect_to_db(app: FastAPI) -> None:
    logger.info("===准备创建 mysql 数据库连接池===")

    app.state.pool = await aiomysql.create_pool(
        **MYSQL_DB_INFO_DICT,
        use_unicode=True,
    )

    logger.info("===创建 mysql 数据库连接池完成===")


# 关闭 mysql 连接池
async def close_db_connection(app: FastAPI) -> None:
    logger.info("===准备断开 mysql 数据库连接池===")

    await app.state.pool.close()

    logger.info("===断开 mysql 数据库连接池完成===")
