from fastapi import APIRouter

router = APIRouter()


# 路由配置列表
routes_config = [
    {"module": "api.routes.authentication", "tag": "用户认证", "prefix": "/auth"},
    {"module": "apps.app_user.api", "tag": "用户类", "prefix": "/users"},
]

# 通过循环动态注册路由
for route in routes_config:
    module_path = route["module"]
    api_router = __import__(f"{module_path}", fromlist=["api"]).router
    router.include_router(api_router, tags=[route["tag"]], prefix=route["prefix"])
