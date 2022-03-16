import os
import subprocess
import platform
from typing import Optional

import pkg_resources
import typer
from questionary.form import form

from fastapi_builder.constants import Database, License, PackageManager, PythonVersion, VenvCmd
from fastapi_builder.context import AppContext, ProjectContext
from fastapi_builder.generator import generate_app, generate_project
from fastapi_builder.helpers import binary_question, question, text_question
from fastapi_builder.utils import check_env


app = typer.Typer(
    add_completion=False,
    help="FastAPI-Builder make fastapi projects easy!",
    name="FastAPI-Builder",
)


@app.command(help="Create a FastAPI project.")
def startproject(
    name: str,
    interactive: bool = typer.Option(False, help="Run in interactive mode."),
    database: Optional[Database] = typer.Option(None, case_sensitive=False),
    database_name: Optional[str] = typer.Option(None, "--dbname"),
    docker: bool = typer.Option(False),
    license_: Optional[License] = typer.Option(None, "--license", case_sensitive=False),
    packaging: PackageManager = typer.Option(PackageManager.PIP),
    pre_commit: bool = typer.Option(False, "--pre-commit"),
    python: PythonVersion = typer.Option(PythonVersion.THREE_DOT_EIG),
):
    if interactive:
        result = form(
            packaging=question(PackageManager),
            python=question(PythonVersion),
            license=question(License),
            pre_commit=binary_question("pre commit"),
            docker=binary_question("docker"),
            database=question(Database),
            database_name=text_question(name),
        ).ask()
        context = ProjectContext(name=name, **result)
    else:
        database_name = database_name if database_name else name
        context = ProjectContext(
            name=name,
            packaging=packaging,
            python=python,
            license=license_,
            pre_commit=pre_commit,
            docker=docker,
            database=database,
            database_name=database_name
        )
    generate_project(context)


@app.command(help="Create a FastAPI app.")
def startapp(
    name: str,
    force: bool = typer.Option(False, help="Create a FastAPI app by force.")
):
    # force=False 时，app 必须生成在 project 项目下
    if not (force or ".fastapi-builder" in os.listdir()):
        typer.echo(f"\nFastAPI app must be created under project folder!")
        return
    
    context = AppContext(name=name)
    generate_app(context)


@app.command(help="Run a FastAPI application.")
def run(
    prod: bool = typer.Option(False),
    check: bool = typer.Option(False, help="Check required run environment.")
):
    # 命令必须运行在 project 项目下
    if ".fastapi-builder" not in os.listdir():
        typer.echo(f"\nFastAPI app must run under project folder!")
        return

    if check:
        return check_env()
    
    args = []
    if not prod:
        args.append("--reload")
    app_file = os.getenv("FASTAPI_APP", "main")
    subprocess.call(["uvicorn", f"{app_file}:app", *args])


@app.command(help="Virtual environment manager.")
def venv(
    cmd: VenvCmd,
    name: Optional[str] = typer.Option(None, "--name"),
):
    if cmd == VenvCmd.CREATE:
        name = name if name else "venv"
        if name in os.listdir():
            typer.echo(f"\nVirtual environment {name} already exists.")
            return
        subprocess.call(["python", "-m", "venv", name])
        typer.echo(f"\nVirtual environment {name} created successfully!")
        return

    # ON or OFF    
    if name:
        if _exec_venv_cmd(filename=name, activate=cmd):
            typer.echo(f"\nVirtual environment {name} {cmd} successfully!")
        else:
            typer.echo(f"\nVirtual environment {name} {cmd} failed!")
        return
    
    for fname in os.listdir():
        if "env" not in fname:
            continue
        if _exec_venv_cmd(filename=fname, activate=cmd):
            break

    def _exec_venv_cmd(filename: str, activate: bool = True) -> bool:
        cmd = "activate" if activate else "deactivate"
        platform_cmd = {
            "Windows": f".\\{filename}\\Scripts\\{cmd}",
            "Linux": f"source ./{filename}/bin/{cmd}"
        }
        return os.system(platform_cmd[platform.system()]) == 0


def version_callback(value: bool):
    if value:
        version = pkg_resources.get_distribution("fastapi-builder").version
        typer.echo(f"fastapi-builder, version {version}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the FastAPI-Builder version information.",
    )
):
    ...
