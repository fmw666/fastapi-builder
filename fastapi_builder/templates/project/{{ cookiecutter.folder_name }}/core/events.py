# https://github.com/aio-libs-abandoned/aioredis-py/issues/1443
from redis import asyncio as aioredis
from typing import Callable, AsyncIterator
from fastapi import FastAPI

from core.config import settings
from core.logger import app_logger as logger


async def init_redis_pool(
    url: str, password: str | None = None, db: int = 0, port: int = 6379
) -> AsyncIterator[aioredis.Redis]:
    session = await aioredis.from_url(
        url=url,
        port=port,
        password=password,
        db=db,
        encoding="utf-8",
        decode_responses=True,
    )
    return session


def create_start_app_handler(app: FastAPI) -> Callable:
    """fastapi 启动事件句柄"""

    async def start_app() -> None:
        logger.info("fastapi 项目启动.")
        # 连接 redis
        app.state.redis = await init_redis_pool(settings.REDIS_URL, password=None)
        logger.info("redis 连接成功.")

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """fastapi 结束事件句柄"""

    @logger.catch
    async def stop_app() -> None:
        logger.info("fastapi 项目结束.")
        # 关闭 redis
        await app.state.redis.close()
        logger.info("redis 连接关闭成功.")

    return stop_app
