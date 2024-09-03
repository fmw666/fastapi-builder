import os
import shutil
from typing import TypeVar

import typer
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from pydantic.main import BaseModel

from fastapi_builder.config import TEMPLATES_DIR
from fastapi_builder.context import AppContext, ProjectContext
from fastapi_builder.utils import new_app_inject_into_project

ContextType = TypeVar("ContextType", bound=BaseModel)


def del_all_pycache(filepath: str):
    """清除 __pycache__ 文件夹"""
    for fname in os.listdir(filepath):
        cur_path = os.path.join(filepath, fname)
        if os.path.isdir(cur_path):
            if fname == "__pycache__":
                shutil.rmtree(cur_path)
            else:
                del_all_pycache(cur_path)


def fill_template(template_name: str, context: ContextType, output_dir: str = "."):
    try:
        cookiecutter(
            os.path.join(TEMPLATES_DIR, template_name),
            extra_context=context.dict(),
            no_input=True,
            output_dir=output_dir,
        )
    except OutputDirExistsException:
        typer.echo(f"\nFolder '{context.folder_name}' already exists. 😞")
    else:
        typer.echo(f"\nFastAPI {template_name} created successfully! 🎉")

        filepath = context.folder_name
        if template_name == "app":
            filepath = os.path.join(output_dir, f"app_{context.folder_name}")

            # 尝试路由自动注入:
            # ps: 就算是 force 情况也会尝试自动注入
            # 1. 修改 db/base.py 导入 models
            # 2. 修改 api/routes/api.py 创建路由
            try:
                new_app_inject_into_project(
                    folder_name=context.folder_name,
                    pascal_name=context.pascal_name,
                    snake_name=context.snake_name,
                )
            except Exception:
                pass

        # 清除 __pycache__ 文件夹
        del_all_pycache(filepath)


def generate_app(context: AppContext, output_dir: str):
    fill_template("app", context, output_dir)


def generate_project(context: ProjectContext):
    fill_template("project", context)
