from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)

from core.e import ErrorCode, ErrorMessage
from schemas.response import StandardResponse

# common

NOT_FOUND = {
    "description": "{{ cookiecutter.snake_name }} 不存在.",
    "model": StandardResponse,
    "content": {
        "application/json": {
            "example": {
                "code": ErrorCode.NOT_FOUND,
                "message": ErrorMessage.get(ErrorCode.NOT_FOUND),
            }
        }
    },
}

# ======================>>>>>>>>>>>>>>>>>>>>>> get_{{ cookiecutter.snake_name }}

get_{{ cookiecutter.snake_name }}s_responses = {
    HTTP_200_OK: {
        "description": "获取 {{ cookiecutter.snake_name }} 列表成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "list": [
                            {
                                "id": 1,
                                "name": "test1",
                            },
                            {
                                "id": 2,
                                "name": "test02",
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

# ======================>>>>>>>>>>>>>>>>>>>>>> create_{{ cookiecutter.snake_name }}

create_{{ cookiecutter.snake_name }}_request = {
    "创建 {{ cookiecutter.snake_name }}": {
        "description": "创建时需要输入 <u>**name**</u>.",
        "value": {
            "name": "new_name",
        }
    }
}

create_{{ cookiecutter.snake_name }}_responses = {
    HTTP_200_OK: {
        "description": "创建 {{ cookiecutter.snake_name }} 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "id": 1,
                        "name": "new_name",
                    },
                    "message": "",
                }
            }
        }
    }
}

# ======================>>>>>>>>>>>>>>>>>>>>>> patch_{{ cookiecutter.snake_name }}s

patch_{{ cookiecutter.snake_name }}s_responses = {
    HTTP_200_OK: {
        "description": "批量更新 {{ cookiecutter.snake_name }} 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "ids": [1, 2],
                        "name": "new_name",
                    },
                    "message": "",
                }
            }
        }
    }
}

patch_{{ cookiecutter.snake_name }}s_request = {
    "批量更新 {{ cookiecutter.snake_name }} name": {
        "description": "批量更新 {{ cookiecutter.snake_name }}，返回更新成功的 {{ cookiecutter.snake_name }} id 和更新条目",
        "value": {
            "ids": [1, 2, 3],
            "name": "new_name",
        },
    }
}

# ======================>>>>>>>>>>>>>>>>>>>>>> delete_{{ cookiecutter.snake_name }}s

delete_{{ cookiecutter.snake_name }}s_responses = {
    HTTP_200_OK: {
        "description": "批量删除 {{ cookiecutter.snake_name }} 成功",
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

delete_{{ cookiecutter.snake_name }}s_request = {
    "example": [1, 2, 3],
}

# ======================>>>>>>>>>>>>>>>>>>>>>> get_{{ cookiecutter.snake_name }}_by_id

get_{{ cookiecutter.snake_name }}_by_id_responses = {
    HTTP_200_OK: {
        "description": "获取 {{ cookiecutter.snake_name }} 信息成功.",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "message": "",
                    "data": {
                        "id": 1,
                        "name": "{{ cookiecutter.snake_name }}",
                        "created_at": "2023-07-03 08:03:03",
                        "updated_at": "2023-07-03 08:03:03",
                    },
                }
            }
        },
    },
    HTTP_404_NOT_FOUND: NOT_FOUND,
}

# ======================>>>>>>>>>>>>>>>>>>>>>> update_{{ cookiecutter.snake_name }}_by_id

update_{{ cookiecutter.snake_name }}_by_id_responses = {
    HTTP_200_OK: {
        "description": "更改 {{ cookiecutter.snake_name }} 成功",
        "content": {
            "application/json": {
                "example": {
                    "code": 0,
                    "data": {
                        "id": 1,
                        "name": "new_name",
                    },
                    "message": "",
                },
            },
        },
    },
    HTTP_404_NOT_FOUND: NOT_FOUND,
}

update_{{ cookiecutter.snake_name }}_by_id_request = {
    "更新 name": {
        "description": "设置 `name` 为新值.",
        "value": {
            "name": "new_name",
        },
    },
}

# ======================>>>>>>>>>>>>>>>>>>>>>> delete_{{ cookiecutter.snake_name }}_by_id

delete_{{ cookiecutter.snake_name }}_by_id_responses = {
    HTTP_200_OK: {
        "description": "注销 {{ cookiecutter.snake_name }} 成功",
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
    HTTP_404_NOT_FOUND: NOT_FOUND,
}
