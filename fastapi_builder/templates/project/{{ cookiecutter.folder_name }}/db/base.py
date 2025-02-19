"""自动从 apps 目录下导入所有应用的 models"""
import importlib
import pkgutil

from typing import List

from models.base import Base


# 指定模型所在的包路径
models_package = "apps"


def import_models(package_name: str) -> List[Base]:
    # 导入包
    package = importlib.import_module(package_name)
    # 遍历包中的所有模块
    discovered_models = []
    for _, name, is_pkg in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        # 只考虑模块，不考虑子包
        if not is_pkg and name.endswith((".model", ".models")):
            module = importlib.import_module(name)
            # 尝试从每个模块中导入 Model 类
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if (
                    isinstance(attribute, type)
                    and issubclass(attribute, Base)
                    and attribute.__module__ == module.__name__
                ):
                    discovered_models.append(attribute)
    return discovered_models


all_models = import_models(models_package)

# 动态创建 __all__ 并设置全局变量
__all__ = [cls.__name__ for cls in all_models] + ["Base"]
globals().update({cls.__name__: cls for cls in all_models})
