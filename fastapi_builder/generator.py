import os
import shutil
from typing import TypeVar

import typer
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from pydantic.main import BaseModel

from fastapi_builder.config import TEMPLATES_DIR
from fastapi_builder.context import AppContext, ProjectContext

ContextType = TypeVar("ContextType", bound=BaseModel)


# 清除 __pycache__ 文件夹
def del_all_pycache(filepath: str):
    for fname in os.listdir(filepath):
        cur_path = os.path.join(filepath, fname)
        if os.path.isdir(cur_path):
            if fname == "__pycache__":
                shutil.rmtree(cur_path)
            else:
                del_all_pycache(cur_path)


def fill_template(template_name: str, context: ContextType):
    try:
        cookiecutter(
            os.path.join(TEMPLATES_DIR, template_name),
            extra_context=context.dict(),
            no_input=True,
        )
    except OutputDirExistsException:
        typer.echo(f"\nFolder '{context.folder_name}' already exists. 😞")
    else:
        typer.echo(f"\nFastAPI {template_name} created successfully! 🎉")

        filepath = context.folder_name
        if template_name == "app":
            filepath = f"./app_{context.folder_name}"
        
        # 清除 __pycache__ 文件夹
        del_all_pycache(filepath)


def generate_app(context: AppContext):
    fill_template("app", context)


def generate_project(context: ProjectContext):
    fill_template("project", context)
