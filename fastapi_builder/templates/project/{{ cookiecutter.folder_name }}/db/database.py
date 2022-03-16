from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import DATABASE_URL


# 依赖：greenlet
engine = create_engine(DATABASE_URL._url, encoding="utf8", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 自定义在了 models.base 下
# Base = declarative_base()

# Dependency
def get_db() -> Generator:
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

