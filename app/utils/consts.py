# API messages. 定义为常量类型
from typing import Any

class _const(object):

    # 定义异常类型
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass
    
    def __setattr__(self, name: str, value: Any) -> None:
        # 不允许修改常量
        if name in self.__dict__:
            raise self.ConstError("Const '%s' has been existing." % name)
        # 不允许包含小写
        if not name.isupper():
            raise self.ConstCaseError("Const name '%s' is not all uppercase." % name)
        # 添加到常量中
        self.__dict__[name] = value

    def __init__(self) -> None:
        # 常量定义位置
        self.USER_DOES_NOT_EXIST_ERROR = "user does not exist"
        self.ARTICLE_DOES_NOT_EXIST_ERROR = "article does not exist"
        self.ARTICLE_ALREADY_EXISTS = "article already exists"
        self.USER_IS_NOT_AUTHOR_OF_ARTICLE = "you are not an author of this article"

        self.INCORRECT_LOGIN_INPUT = "incorrect email or password"
        self.USERNAME_TAKEN = "user with this username already exists"
        self.EMAIL_TAKEN = "user with this email already exists"

        self.UNABLE_TO_FOLLOW_YOURSELF = "user can not follow him self"
        self.UNABLE_TO_UNSUBSCRIBE_FROM_YOURSELF = "user can not unsubscribe from him self"
        self.USER_IS_NOT_FOLLOWED = "you don't follow this user"
        self.USER_IS_ALREADY_FOLLOWED = "you follow this user already"

        self.WRONG_TOKEN_PREFIX = "unsupported authorization type"  # noqa: S105
        self.MALFORMED_PAYLOAD = "could not validate credentials"

        self.ARTICLE_IS_ALREADY_FAVORITED = "you are already marked this articles as favorite"
        self.ARTICLE_IS_NOT_FAVORITED = "article is not favorited"

        self.COMMENT_DOES_NOT_EXIST = "comment does not exist"

        self.AUTHENTICATION_REQUIRED = "authentication required"


# 只能导出 const 对象属性
__all__ = []

for k, v in _const().__dict__.items():
    globals()[k] = v
    __all__.append(k)
