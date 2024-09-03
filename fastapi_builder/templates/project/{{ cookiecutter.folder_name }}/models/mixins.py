import datetime
from sqlalchemy import Column, DateTime, update
from sqlalchemy.ext.asyncio import AsyncSession


class DateTimeModelMixin(object):
    """创建默认时间"""

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class SoftDeleteModelMixin(object):
    """记录软删除"""

    deleted_at = Column(DateTime, nullable=True)

    async def remove(self, db: AsyncSession = None) -> "SoftDeleteModelMixin":
        """
        单个的实例删除

        Args:
            db (AsyncSession): db async session

        Returns:
            SoftDeleteModelMixin: self
        """
        self.deleted_at = datetime.datetime.now()
        db.add(self)
        return self

    @classmethod
    async def remove_by(cls, db: AsyncSession, **kw) -> None:
        """
        批量删除

        Args:
            db (AsyncSession): db async session
            **kw: 查询条件
        """
        stmt = update(cls).where(cls.deleted_at.is_(None)).filter_by(**kw).values(
            deleted_at=datetime.datetime.now()
        )
        await db.execute(stmt)
