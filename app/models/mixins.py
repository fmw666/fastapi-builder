import datetime
from sqlalchemy import Column, Boolean, DateTime
from sqlalchemy.orm.session import Session


class DateTimeModelMixin(object):
    """创建默认时间"""
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())


class SoftDeleteModelMixin(object):
    """记录软删除"""
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    # 单个的实例删除
    def remove(self, db: Session = None):
        self.deleted = True
        self.deleted_at = datetime.datetime.now()
        if db:
            db.commit()
            return self

    # 批量删除
    @classmethod
    def remove_by(cls, db: Session, **kw):
        objs = db.query(cls).filter_by(**kw).all()
        for obj in objs:
            obj.remove(db)

