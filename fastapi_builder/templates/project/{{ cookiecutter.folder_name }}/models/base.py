from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer

from db.database import SessionLocal

@as_declarative()
class Base(object):

    # 默认表名
    @declared_attr
    def __tablename__(cls) -> str:
        # 转换成小写
        return cls.__name__.lower()

    # 默认字段
    id = Column(Integer, primary_key=True, index=True)

    # 打印实例返回值
    def __repr__(self) -> str:
        values = ", ".join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys())
        return "%s(%s)" % (self.__class__.__name__, values)

    # 自定义方法
    @classmethod
    def query(cls, db: Session = SessionLocal()):
        return db.query(cls).filter_by(deleted=False) if hasattr(cls, "deleted") else db.query(cls)

    @classmethod
    def create(cls, db: Session = SessionLocal(), **kw):
        obj = cls(**kw)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def save(self, db: Session = SessionLocal()):
        db.add(self)
        db.commit()
        db.refresh(self)

    @classmethod
    def get_by(cls, db: Session = SessionLocal(), **kw):
        return cls.query(db).filter_by(**kw).first()

    @classmethod
    def get_or_create(cls, db: Session = SessionLocal(), **kw):
        obj = cls.get_by(db, **kw)
        if not obj:
            obj = cls.create(db, **kw)
        return obj

    @classmethod
    def get_or_404(cls, db: Session = SessionLocal(), **kw):
        obj = cls.get_by(db, **kw)
        if not obj:
            return 404
        return obj

    @classmethod
    def filter_by(cls, db: Session = SessionLocal(), **kw):
        return cls.query(db).filter_by(**kw).all()

    @classmethod
    def all(cls, db: Session = SessionLocal(), /):
        return cls.query(db).all()

    @classmethod
    def update_by(cls, db: Session = SessionLocal(), /, *, user_id: int, update_fields: dict):
        cls.query(db).filter_by(id=user_id).update(update_fields)
        db.commit()

    @classmethod
    def delete_by(cls, db: Session = SessionLocal(), /, *, user_id: int):
        cls.query(db).filter_by(id=user_id).delete(synchronize_session=False)
        db.commit()

    def delete(self, db: Session = SessionLocal(), /):
        db.delete(self)
        db.commit()
