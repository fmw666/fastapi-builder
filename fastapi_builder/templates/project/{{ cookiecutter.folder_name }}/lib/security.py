import bcrypt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from core.config import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.API_PREFIX + "/auth/token", auto_error=False
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_salt() -> str:
    """生成盐，用于对密码加密时安全"""
    return bcrypt.gensalt().decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证用户输入密码与加密过后的密码是否相等，使用 passlib 库完成

    Args:
        plain_password (str): 用户输入的明文密码
        hashed_password (str): 加密过后的密码

    Returns:
        bool: 验证结果
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    将用户输入的明文密码，使用 hash 算法加密,每次加密的算法都不一样

    Args:
        password (str): 用户输入的明文密码

    Returns:
        str: 加密过后的密码
    """
    return pwd_context.hash(password)


# Bearer eyJhbGc...
# Authorization
# http://127.0.0.1:8000/api/auth/login
