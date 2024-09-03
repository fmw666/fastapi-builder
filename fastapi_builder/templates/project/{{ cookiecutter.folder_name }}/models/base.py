from typing import Generic, List, Type, TypeVar, Union

from sqlalchemy import Column, Integer, Select, delete, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import ColumnProperty


T = TypeVar("T", bound="Base")


@as_declarative()
class Base(Generic[T]):

    # 默认表名
    @declared_attr
    def __tablename__(cls) -> str:
        # 转换成小写
        return cls.__name__.lower()

    # 默认字段
    id = Column(Integer, primary_key=True, index=True)

    # 打印实例返回值
    def __repr__(self) -> str:
        values = ", ".join(
            f"{n}={repr(getattr(self, n))}" for n in self.__table__.c.keys()
        )
        return f"{self.__class__.__name__}({values})"

    # 自定义方法
    @classmethod
    async def query(cls) -> Select[T]:
        return (
            select(cls).where(cls.deleted_at.is_(None))
            if hasattr(cls, "deleted_at")
            else select(cls)
        )

    @classmethod
    async def create(cls, db: AsyncSession, **kw) -> T:
        obj = cls(**kw)
        db.add(obj)
        return obj

    async def save(self, db: AsyncSession) -> None:
        db.add(self)

    @classmethod
    async def get_by(cls, db: AsyncSession, **kw) -> T | None:
        stmt = await cls.query()
        result = await db.execute(stmt.filter_by(**kw))
        return result.scalars().first()

    @classmethod
    async def get_or_create(cls, db: AsyncSession, **kw) -> T:
        obj = await cls.get_by(db, **kw)
        if not obj:
            obj = await cls.create(db, **kw)
        return obj

    @classmethod
    async def all(cls, db: AsyncSession, /) -> List[T]:
        stmt = await cls.query()
        return (await db.execute(stmt)).scalars().all()

    @classmethod
    async def delete_by(cls, db: AsyncSession, /, **kw) -> None:
        stmt = delete(cls).filter_by(**kw)
        await db.execute(stmt)

    async def delete(self, db: AsyncSession, /) -> None:
        await db.delete(self)
        await db.commit()


def get_model_fields_from_objects(
    model: Type, fields: List[Union[ColumnProperty]] | None = None
) -> List[str]:
    """从 SQLAlchemy 模型字段对象中提取字段名"""
    mapper = inspect(model)
    if fields is None:
        field_names = [column.name for column in mapper.columns]
    else:
        field_names = [column.name for column in mapper.columns if column in fields]
    return field_names
