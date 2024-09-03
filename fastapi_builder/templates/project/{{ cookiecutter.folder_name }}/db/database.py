from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings


# 同步数据库（依赖：greenlet）
engine = create_engine(settings.DATABASE_URL._url, echo=True, pool_size=10, max_overflow=20)

SessionLocal: Session = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)


# 异步数据库
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL._url,
    echo=True,
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 连接池溢出时最大创建的连接数
)

AsyncSessionLocal: AsyncSession = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# 自定义在了 models.base 下
# Base = declarative_base()


# Dependency
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    """
    async with AsyncSessionLocal() as session:
        yield session
