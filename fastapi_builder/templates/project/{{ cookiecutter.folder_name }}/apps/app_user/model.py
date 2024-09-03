from sqlalchemy import Column, String

from lib.security import verify_password, get_password_hash, generate_salt

from models.base import Base
from models.mixins import DateTimeModelMixin, SoftDeleteModelMixin


DEFAULT_AVATAR_URL = "https://cdn.img.com/avatar.png"


class User(Base["User"], DateTimeModelMixin, SoftDeleteModelMixin):
    __tablename__ = "user"

    email = Column(String(32), unique=False, index=True)
    username = Column(String(32), unique=False, nullable=False)
    avatar_url = Column(
        String(256),
        nullable=True,
        default=DEFAULT_AVATAR_URL,
        server_default=DEFAULT_AVATAR_URL,
    )
    salt = Column(String(32))
    password = Column(String(600))

    def check_password(self, password: str) -> bool:
        """
        检查密码是否相等

        Args:
            password (str): 密码

        Returns:
            bool: 是否相等
        """
        return verify_password(self.salt + password, self.password)

    def change_password(self, password: str) -> None:
        """
        更改密码

        Args:
            password (str): 新密码
        """
        self.salt = generate_salt()
        self.password = get_password_hash(self.salt + password)
