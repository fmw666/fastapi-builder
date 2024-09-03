from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from core.e import ErrorCode, ErrorMessage
from schemas.response import StandardResponse

# ======================>>>>>>>>>>>>>>>>>>>>>> login

login_responses = {
    HTTP_200_OK: {
        "description": "登录成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "message": "",
                    "data": {
                        "id": 1,
                        "username": "fmw666",
                        "email": "fmw19990718@gmail.com",
                        "token_type": "bearer",
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjU1MzIzOTMsInN1YiI6IjYifQ.MXJutcQ2e7HHUC0FVkeqRtHyn6fT1fclPugo-qpy8e4",  # noqa
                    },
                }
            }
        },
    },
    HTTP_400_BAD_REQUEST: {
        "description": "密码错误",
        "model": StandardResponse,
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.USER_PASSWORD_ERROR,
                    "message": ErrorMessage.get(ErrorCode.USER_PASSWORD_ERROR),
                    "data": None,
                }
            }
        },
    },
    HTTP_404_NOT_FOUND: {
        "description": "用户不存在",
        "model": StandardResponse,
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.USER_NOT_FOUND,
                    "message": ErrorMessage.get(ErrorCode.USER_NOT_FOUND),
                    "data": None,
                }
            }
        },
    },
}

login_request = {
    "普通用户登录": {
        "description": "使用 <u>**自己的用户名**</u> 和 <u>**密码**</u> 进行登录.",
        "value": {
            "username": "fmw666",
            "password": "123456",
        },
    },
    "内置管理员登录": {
        "description": "使用 <u>**内置管理员**</u> 的账号 `root01` 和密码 `123456` 进行登录.",
        "value": {
            "username": "root01",
            "password": "123456",
        },
    },
}

# ======================>>>>>>>>>>>>>>>>>>>>>> register

register_responses = {
    HTTP_200_OK: {
        "description": "用户注册成功.",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "message": "",
                    "data": {
                        "id": 1,
                        "username": "fmw666",
                        "email": "fmw19990718@gmail.com",
                    },
                }
            }
        },
    },
    HTTP_400_BAD_REQUEST: {
        "description": "用户注册失败（用户名已存在/邮箱已存在）.",
        "model": StandardResponse,
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.USER_NAME_EXIST,
                    "message": ErrorMessage.get(ErrorCode.USER_NAME_EXIST),
                }
            }
        },
    },
}

register_request = {
    "普通用户注册": {
        "description": (
            "注册时需要使用 <u>**邮箱**</u>、<u>**用户名**</u> 和 <u>**密码**</u>.\n"
            "* 账号和密码长度为 6~12\n* 邮箱不超过 32 位"
        ),
        "value": {
            "email": "fmw19990718@gmail.com",
            "username": "fmw666",
            "password": "123456",
        },
    },
    "内置用户注册": {
        "description": "注册 <u>**内置管理员**</u> 的账号使用 `root01` 和密码 `123456`.",
        "value": {
            "email": "root01@example.com",
            "username": "root01",
            "password": "123456",
        },
    },
}

# ======================>>>>>>>>>>>>>>>>>>>>>> get_user_info

get_user_info_response = {
    HTTP_200_OK: {
        "description": "获取用户信息成功.",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "message": "",
                    "data": {
                        "id": 1,
                        "username": "admin",
                        "phone": "18066666666",
                        "avator_url": "",
                        "portfolio_name": "work",
                        "created_at": "2023-07-03 08:03:03",
                        "updated_at": "2023-07-03 08:03:03",
                    },
                }
            }
        },
    },
    HTTP_401_UNAUTHORIZED: {
        "description": "用户未登录.",
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.UNAUTHORIZED,
                    "message": ErrorMessage.get(ErrorCode.UNAUTHORIZED),
                }
            }
        },
    },
    HTTP_404_NOT_FOUND: {
        "description": "用户不存在.",
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.USER_NOT_FOUND,
                    "message": ErrorMessage.get(ErrorCode.USER_NOT_FOUND),
                }
            }
        },
    },
}

# ======================>>>>>>>>>>>>>>>>>>>>>> get_users

get_users_responses = {
    HTTP_200_OK: {
        "description": "获取 User 列表成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "list": [
                            {
                                "id": 1,
                                "email": "user01",
                                "username": "user01@example.com",
                            },
                            {
                                "id": 2,
                                "email": "user02",
                                "username": "user02@example.com",
                            }
                        ],
                        "count": 2,
                        "total": 5,
                        "page": 1,
                        "size": 2
                    },
                    "message": "",
                }
            }
        },
    }
}

# ======================>>>>>>>>>>>>>>>>>>>>>> create_user

create_user_request = {
    "创建用户": {
        "description": (
            "创建时需要使用 <u>**邮箱**</u>、<u>**用户名**</u> 和 <u>**密码**</u>.\n"
            "* 账号和密码长度为 6~12\n* 邮箱不超过 32 位"
        ),
        "value": {
            "email": "fmw19990718@gmail.com",
            "username": "fmw666",
            "password": "123456",
        }
    }
}

create_user_responses = {
    HTTP_200_OK: {
        "description": "创建用户成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "id": 1,
                        "username": "fmw666",
                        "email": "fmw19990718@gmail.com",
                    },
                    "message": "",
                }
            }
        }
    },
    HTTP_400_BAD_REQUEST: {
        "description": "创建用户失败（用户名已存在/邮箱已存在）",
        "model": StandardResponse,
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.USER_EXIST,
                    "message": ErrorMessage.get(ErrorCode.USER_EXIST),
                }
            }
        },
    }
}

# ======================>>>>>>>>>>>>>>>>>>>>>> patch_users

patch_users_responses = {
    HTTP_200_OK: {
        "description": "批量更新用户成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "ids": [1, 2],
                        "avatar_url": "https://example.com/avatar.png",
                    },
                    "message": "",
                }
            }
        }
    }
}

patch_users_request = {
    "批量更新用户头像": {
        "description": "批量更新用户，返回更新成功的用户 id 和更新条目",
        "value": {
            "ids": [1, 2, 3],
            "avatar_url": "https://example.com/avatar.png",
        },
    }
}

# ======================>>>>>>>>>>>>>>>>>>>>>> delete_users

delete_users_responses = {
    HTTP_200_OK: {
        "description": "批量删除用户成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "ids": [1, 2],
                    },
                    "message": "",
                }
            }
        }
    }
}

delete_users_request = {
    "example": [1, 2, 3],
}

# ======================>>>>>>>>>>>>>>>>>>>>>> get_user_by_id

get_user_by_id_responses = {
    HTTP_200_OK: {
        "description": "获取用户信息成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "id": 1,
                        "username": "fmw666",
                        "email": "fmw19990718@gmail.com",
                    },
                    "message": ""
                }
            }
        }
    },
    HTTP_404_NOT_FOUND: {
        "description": "用户不存在",
        "model": StandardResponse,
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.USER_NOT_FOUND,
                    "message": ErrorMessage.get(ErrorCode.USER_NOT_FOUND),
                }
            }
        }
    }
}

# ======================>>>>>>>>>>>>>>>>>>>>>> update_user_by_id

update_user_by_id_responses = {
    HTTP_200_OK: {
        "description": "更改 user 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "id": 1,
                        "username": "fmw666",
                        "email": "fmw19990718@gmail.com",
                    },
                    "message": "",
                },
            },
        },
    },
    HTTP_400_BAD_REQUEST: {
        "description": "更改 user 失败（用户名已存在/邮箱已存在）",
        "model": StandardResponse,
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.USER_EXIST,
                    "message": ErrorMessage.get(ErrorCode.USER_EXIST),
                }
            }
        },
    },
    HTTP_404_NOT_FOUND: {
        "description": "用户不存在",
        "model": StandardResponse,
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.USER_NOT_FOUND,
                    "message": ErrorMessage.get(ErrorCode.USER_NOT_FOUND),
                }
            }
        }
    },
}

update_user_by_id_request = {
    "仅更新 username 的情况": {
        "description": "只设置 `username`，其余的字段设置为 None，或者不要.",
        "value": {
            "username": "new username",
        },
    },
    "仅更新 email 的情况": {
        "description": "只设置 `email`，其余的字段设置为 None，或者不要.",
        "value": {
            "email": "new_email@example.com",
        },
    },
    "同时更新 username 和 email 的情况": {
        "description": "同时设置 `username` 和 `email`，其余的字段设置为 None，或者不要.",
        "value": {
            "username": "new username",
            "email": "new_email@example.com",
        },
    },
}

# ======================>>>>>>>>>>>>>>>>>>>>>> delete_user_by_id

delete_user_by_id_responses = {
    HTTP_200_OK: {
        "description": "注销 user 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "id": 1,
                    },
                    "message": ""
                },
            },
        },
    },
    HTTP_404_NOT_FOUND: {
        "description": "user 不存在",
        "model": StandardResponse,
        "content": {
            "application/json": {
                "example": {
                    "code": ErrorCode.USER_NOT_FOUND,
                    "message": ErrorMessage.get(ErrorCode.USER_NOT_FOUND),
                },
            },
        },
    },
}
