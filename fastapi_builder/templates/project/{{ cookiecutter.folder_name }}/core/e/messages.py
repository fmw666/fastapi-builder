from core.e.codes import ErrorCode


class ErrorMessage:
    _messages = {
        "en": {
            # 通用错误
            ErrorCode.INTERNAL_SERVER_ERROR: "Internal Server Error",
            ErrorCode.BAD_REQUEST: "Bad Request",
            ErrorCode.UNAUTHORIZED: "Unauthorized",
            ErrorCode.FORBIDDEN: "Forbidden",
            ErrorCode.NOT_FOUND: "Not Found",
            # 用户类 01
            ErrorCode.USER_ERROR: "User Error",
            ErrorCode.USER_EXIST: "User Exist",
            ErrorCode.USER_NOT_FOUND: "User Not Found",
            ErrorCode.USER_NAME_EXIST: "User Name Exist",
            ErrorCode.USER_PASSWORD_ERROR: "User Password Error",
            ErrorCode.USER_EMAIL_EXIST: "User Email Exist",
            ErrorCode.USER_SMS_CODE_ERROR: "User SMS Code Error",
            ErrorCode.USER_PHONE_INVALID: "User Phone Invalid",
            ErrorCode.USER_SMS_CODE_REQUEST_TOO_OFTEN: "User SMS Code Request Too Often",
            ErrorCode.USER_UNAUTHORIZED: "User Unauthorized",
            # ...
        },
        "zh": {
            # "NOT_FOUND": "未找到",
            # "UNAUTHORIZED": "未认证",
        },
    }

    @classmethod
    def get(cls, code: int, lang="en"):
        return cls._messages[lang].get(code, "Unknown error code.")
