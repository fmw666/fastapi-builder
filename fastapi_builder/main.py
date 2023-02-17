import os
import subprocess
import platform
from typing import Optional

import pkg_resources
import typer
from questionary.form import form

from fastapi_builder.constants import Database, Language, License, PackageManager, PythonVersion, DBCmd, VenvCmd
from fastapi_builder.context import AppContext, ProjectContext
from fastapi_builder.generator import generate_app, generate_project
from fastapi_builder.helpers import binary_question, question, text_question
from fastapi_builder.utils import check_env, read_conf, config_app, set_config_file_content


app = typer.Typer(
    add_completion=False,
    help="FastAPI-Builder make fastapi projects easy!",
    name="FastAPI-Builder",
)


@app.command(help="Create a FastAPI project.")
def startproject(
    name: str,
    interactive: bool = typer.Option(False, help="Run in interactive mode."),
    language: Optional[Language] = typer.Option("cn", case_sensitive=False),
    database: Optional[Database] = typer.Option("MySQL", case_sensitive=False),
    database_name: Optional[str] = typer.Option(None, "--dbname"),
    docker: bool = typer.Option(False),
    license_: Optional[License] = typer.Option(None, "--license", case_sensitive=False),
    packaging: PackageManager = typer.Option(PackageManager.PIP),
    pre_commit: bool = typer.Option(False, "--pre-commit"),
    python: PythonVersion = typer.Option(PythonVersion.THREE_DOT_EIG),
):
    if interactive:
        result = form(
            language=question(Language),
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
            language=language,
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
    if not (force or "fastapi-builder.ini" in os.listdir()):
        typer.echo(f"\nFastAPI app must be created under project root folder!")
        return
    
    # 尝试从配置文件读取 language 信息，使用 try 是因为 force 条件下，不一定存在配置信息
    try:
        conf = read_conf("fastapi-builder.ini")
        language = conf.get("fastapi_builder", "language") or "cn"
    except:
        language = "cn"

    context = AppContext(name=name, language=language)
    generate_app(context)


@app.command(help="Run a FastAPI application.")
def run(
    prod: bool = typer.Option(False),
    check: bool = typer.Option(False, help="Check required run environment."),
    config: bool = typer.Option(False, help="Configuring startup resources.")
):
    # 命令必须运行在 project 项目下
    if "fastapi-builder.ini" not in os.listdir():
        typer.echo(f"\nFastAPI app must run under project root folder!")
        return
    
    # 获取配置文件 conf
    conf = read_conf("fastapi-builder.ini")
    
    # 运行环境配置
    if config:
        config_app(conf)
        return
    
    # 运行环境检查
    if check:
        check_env()
        return

    # 如果是第一次启动项目，需要进行环境配置
    if conf.get("fastapi_builder", "first_launch") == "true":
        set_config_file_content("fastapi-builder.ini", "first_launch", "false")
        config_app(conf)
    
    args = []
    if not prod:
        args.append("--reload")
    app_file = os.getenv("FASTAPI_APP", "main")
    subprocess.call(["uvicorn", f"{app_file}:app", *args])


@app.command(help="Database migration manager.")
def db(
    cmd: DBCmd,
    migration_message: Optional[str] = typer.Option("create migration", "-m", help="migration message"),
):
    # 命令必须运行在 project 项目下
    if "fastapi-builder.ini" not in os.listdir():
        typer.echo(f"\n`fastapi db` command must run under project root folder!")
        return

    # 检查 alembic 是否安装
    try:
        subprocess.call(["alembic", "--version"])
    except:
        typer.echo(f"\nPlease install alembic correctly first!")
        return
    
    if cmd == DBCmd.MAKEMIGRATIONS:
        subprocess.call(["alembic", "revision", "--autogenerate", "-m", migration_message])
    elif cmd == DBCmd.MIGRATE:
        subprocess.call(["alembic", "upgrade", "head"])


@app.command(help="Virtual environment manager.")
def venv(
    cmd: VenvCmd,
    name: Optional[str] = typer.Option(None, "--name"),
):
    def _exec_venv_cmd(filename: str, activate: bool = True) -> bool:
        cmd = "activate" if activate else "deactivate"
        platform_cmd = {
            "Windows": f".\\{filename}\\Scripts\\{cmd}",
            "Linux": f"source ./{filename}/bin/{cmd}"
        }
        return os.system(platform_cmd[platform.system()]) == 0
    
    if cmd == VenvCmd.CREATE:
        name = name if name is not None else "venv"
        if name in os.listdir():
            typer.echo(f"\nVirtual environment {name} already exists.")
            return
        subprocess.call(["python", "-m", "venv", name])
        typer.echo(f"\nVirtual environment {name} created successfully!")
        return

    # cmd is ON or OFF
    for fname in os.listdir():
        if "env" not in fname:
            continue
        if _exec_venv_cmd(filename=fname, activate=cmd==VenvCmd.ON):
            typer.echo(f"\nVirtual environment {fname} {cmd} successfully!")
            return
    typer.echo(f"\nVirtual environment {cmd} failed!")


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
