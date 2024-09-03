# 导入 declarative，方便 alembic 直接从这个文件导入数据
from models.base import Base

# 导入 models
from apps.app_user.model import User


__all__ = ["Base", "User"]
