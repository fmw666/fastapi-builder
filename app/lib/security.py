import bcrypt
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.config import API_PREFIX


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=API_PREFIX + "/auth/token", auto_error=False)

class OAuth2Form(OAuth2PasswordRequestForm):
    """将登录使用的表单中部分字段隐藏, 使用该模型将无法使用swagger登录"""
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 生成盐，用于对密码加密时安全
def generate_salt() -> str:
    return bcrypt.gensalt().decode()

# 检查密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证用户输入密码与加密过后的密码是否相等，使用passlib库完成
    :param plain_password: 用户输入的明文密码
    :param hashed_password: hash加密过后的密码
    :return: 是否相等
    """
    return pwd_context.verify(plain_password, hashed_password)

# 得到加密后的密码
def get_password_hash(password: str) -> str:
    """
    将用户输入的明文密码，使用hash算法加密,每次加密的算法都不一样
    :param password: 明文密码
    :return: 加密过后的密码
    """
    return pwd_context.hash(password)


# Bearer eyJhbGc...
# Authorization
# http://127.0.0.1:8000/api/auth/login