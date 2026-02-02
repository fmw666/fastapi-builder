from __future__ import annotations

import configparser
import os
import re
import subprocess
import sys
from configparser import ConfigParser

import pymysql
import questionary
import typer


def check_env():
    """运行环境检查"""
    # 模块检查
    typer.secho("[module]", fg=typer.colors.MAGENTA, bold=True)
    fp = open("./requirements.txt")
    modules = {}
    max_length = 0
    for module in fp.readlines():
        module = module.strip()
        if "==" not in module:
            continue
        name, version = module.split("==")
        modules[name] = version
        max_length = len(name) if len(name) > max_length else max_length

    for name, version in modules.items():
        s_name = "*" + name + "*"
        typer.secho(f"check {s_name:{max_length + 2}} : ", nl=False)
        try:
            module_version = __import__(name).__version__
            if module_version == version:
                typer.secho("pass", fg=typer.colors.GREEN)
            elif module_version > version:
                typer.secho("higher version.", fg=typer.colors.YELLOW)
            else:
                typer.secho("lower version.", fg=typer.colors.YELLOW)
        except Exception:
            try:
                subprocess.check_call(
                    ["pip", "show", name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                )
                typer.secho("pass", fg=typer.colors.GREEN)
            except Exception:
                typer.secho("module not exist!", fg=typer.colors.RED)
    fp.close()
    typer.echo()

    # 数据库检查
    typer.secho("[db]", fg=typer.colors.MAGENTA, bold=True)
    """
    check mysql      : pass
    check connection : pass
    check database   : pass
    check tables     : pass
    """
    sys.path.append(os.path.join(".", "core"))
    try:
        db_url = __import__("config").DATABASE_URL
        db_charset = __import__("config").DB_CHARSET
    except Exception:
        typer.secho("module databases not installed", fg=typer.colors.RED)

    typer.echo("check mysql      : ", nl=False)
    try:
        subprocess.check_call(
            ["mysql", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        typer.secho("pass", fg=typer.colors.GREEN)
    except Exception:
        typer.secho("not exist!", fg=typer.colors.RED)

    typer.echo("check connection : ", nl=False)
    try:
        import pymysql

        conn = pymysql.connect(
            host=db_url.hostname,
            port=db_url.port,
            user=db_url.username,
            password=db_url.password,
            charset=db_charset,
        )
        typer.secho("pass", fg=typer.colors.GREEN)
    except Exception:
        typer.secho("failed", fg=typer.colors.RED)
    else:
        cursor = conn.cursor()
        dbname = db_url.database
        typer.echo("check database   ：", nl=False)
        if cursor.execute(f"show databases like '{dbname}';"):
            typer.secho("pass", fg=typer.colors.GREEN)
        else:
            typer.secho("not exist!", fg=typer.colors.RED)


def read_conf(file_name: str) -> ConfigParser:
    """读取配置文件"""
    conf = configparser.ConfigParser()
    conf.read(file_name)
    return conf


def set_config_file_content(file_path: str, key: str, new_value: str) -> None:
    """
    修改配置文件内容

    Args:
        file_path (str): 配置文件路径
        key (str): 配置项
        new_value (str): 新值
    """
    file_lines = []
    with open(file_path) as fp:
        for line in fp.readlines():
            line_lst = line.split("=")
            if line_lst[0] == key:
                line = f"{line_lst[0]}={new_value}\n"
            elif line_lst[0] == key + " ":
                line = f"{line_lst[0]}= {new_value}\n"
            file_lines.append(line)
    file_content = "".join(file_lines)
    with open(file_path, "w") as fp:
        fp.write(file_content)


def config_app(conf: ConfigParser) -> None:
    """
    配置应用

    0）读取 .fastapi-builder，获取虚拟环境、打包方式、数据库等信息
    1）检查是否在虚拟环境下，没有的话会检查是否存在虚拟环境，若不存在，询问用户是否创建
    2）进入虚拟环境
    3）安装 requirements.txt
    4）检查数据库连接，若失败，让用户填写数据库地址、用户名、端口。重复检查直到连接
    5）创建数据库并运行迁移文件，创建相应的表
    """
    # 3）安装 requirements.txt
    typer.echo("install required modules...")
    os.system("pip install -r requirements.txt")
    typer.echo("")

    # 4）检查数据库连接，若失败，让用户填写数据库地址、用户名、端口。重复检查直到连接
    # 若没安装 mysql/Postgres 直接退出
    try:
        subprocess.check_call(
            ["mysql", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
    except Exception:
        typer.secho("Please make sure you download mysql already!", fg=typer.colors.RED)
        return
    # 与数据库建立连接
    sys.path.append(os.path.join(".", "core"))
    db_url = __import__("config").DATABASE_URL
    db_charset = __import__("config").DB_CHARSET
    # 获取配置中数据库信息
    db_host: str = db_url.hostname
    db_port: int = db_url.port
    db_user: str = db_url.username
    db_pswd: str = db_url.password

    while True:
        typer.echo("check database connecting.....", nl=False)
        try:
            conn = pymysql.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_pswd,
                charset=db_charset,
            )
            typer.secho("success", fg=typer.colors.GREEN)
            # 写入到配置文件中 core/.env alembic.ini
            sql_url = f"mysql+pymysql://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_url.database}?charset={db_charset}"  # noqa
            set_config_file_content("alembic.ini", "sqlalchemy.url", sql_url)
            set_config_file_content(
                os.path.join(".", "core", ".env"), "DB_CONNECTION", sql_url
            )

            # 创建数据库
            cursor = conn.cursor()
            cursor.execute(
                f"create database if not exists {db_url.database} "
                "default charset utf8mb4;"
            )
            break
        except Exception:
            typer.secho("fail", fg=typer.colors.RED)
            db_host = questionary.text("database host is:", default=db_host).ask()
            db_port = questionary.text("database port is:", default=str(db_port)).ask()
            db_port = int(db_port)
            db_user = questionary.text("database username is:", default=db_user).ask()
            db_pswd = questionary.text("database password is:", default=db_pswd).ask()

    # 5）创建数据库并运行迁移文件，创建相应的表
    os.system('alembic revision --autogenerate -m "create migration"')
    os.system("alembic upgrade head")


def new_app_inject_into_project(
    folder_name: str, pascal_name: str, snake_name: str
) -> None:
    """
    新 app 注入到 project

    Args:
        folder_name (str): app 文件夹名. eg: computer-book
        pascal_name (str): app 驼峰命名. eg: ComputerBook
        snake_name (str): app 蛇形命名. eg: computer_book
    """

    # 1. 打开 api/routes/api.py 文件，创建路由
    import_line = (
        f"from apps.app_{folder_name}.api import router as {folder_name}_router"
    )
    include_router_line = f'router.include_router({folder_name}_router, tags=["{pascal_name} 类"], prefix="/{snake_name}s")'  # noqa

    def get_new_content(
        pattern: str | re.Pattern[str], content: str, new_line: str
    ) -> str:
        last_match = re.findall(pattern, content)
        if last_match:
            last_position = content.rfind(last_match[-1]) + len(last_match[-1])
        else:
            last_position = 0

        content = content[:last_position] + "\n" + new_line + content[last_position:]
        return content

    api_file_path = os.path.join(".", "api", "routes", "api.py")
    with open(api_file_path, "r+", encoding="utf8") as f:
        content = f.read()
        # 找到最后一个 from ... import ...
        content = get_new_content(r"from \S+ import \S+ as \S+", content, import_line)
        # 找到最后一个 router.include_router(...)
        content = get_new_content(
            r"router.include_router\([^)]*\)", content, include_router_line
        )

        f.seek(0)
        f.write(content)
        f.truncate()

    # 2. 打开 db/base.py 导入 models
    db_file_path = os.path.join(".", "db", "base.py")
    with open(db_file_path, "r+", encoding="utf8") as f:
        content = f.read()

        # 找到最后一个 from ... import ... 语句
        last_import_match = re.findall(r"from \S+ import \S+", content)
        if last_import_match:
            last_import_position = content.rfind(last_import_match[-1]) + len(
                last_import_match[-1]
            )
        else:
            last_import_position = 0

        # 构建新的内容，添加新的导入语句
        content = (
            content[:last_import_position]
            + "\n"
            + f"from apps.app_{snake_name}.model import {pascal_name}"
            + content[last_import_position:]
        )

        # 找到 __all__ 赋值语句
        all_match = re.search(r"__all__ = \[(.*?)\]", content)
        if all_match:
            all_entries = re.findall(r"\"(\w+)\"|\'(\w+)\'", all_match.group(1))
            all_entries = [
                entry[0] if entry[0] else entry[1] for entry in all_entries
            ]  # 处理元组结果
            all_entries.append(pascal_name)
            updated_all = ", ".join(f'"{entry}"' for entry in all_entries)
            content = (
                content[: all_match.start()]
                + f"__all__ = [{updated_all}]"
                + content[all_match.end() :]
            )

        f.seek(0)
        f.write(content)
        f.truncate()
