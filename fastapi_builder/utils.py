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
from fastapi_builder.constants import Database


def check_env():
    """运行环境检查"""
    # 模块检查
    typer.secho("[module]", fg=typer.colors.MAGENTA, bold=True)
    if os.path.exists("./requirements.txt"):
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
    else:
         typer.secho("requirements.txt not found", fg=typer.colors.YELLOW)
    typer.echo()

    # 数据库检查
    typer.secho("[db]", fg=typer.colors.MAGENTA, bold=True)
    
    sys.path.append(os.path.join(".", "core"))
    try:
        config_module = __import__("config")
        db_url = config_module.DATABASE_URL
        # Try to infer database type from settings or config
        # Since config.py doesn't have the type directly, we might need to guess or look at fastap-builder.ini if available
        # But check_env is standalone?
        # Let's try to read fastapi-builder.ini to know the DB type
        conf = read_conf("fastapi-builder.ini")
        database_type = conf.get("config", "database", fallback=Database.MYSQL)

    except Exception:
        typer.secho("module databases not installed or config error", fg=typer.colors.RED)
        return

    if database_type == Database.MYSQL:
        _check_mysql(db_url)
    elif database_type == Database.POSTGRESQL:
        _check_postgres(db_url)
    elif database_type == Database.SQLITE:
        typer.echo("check sqlite      : ", nl=False)
        typer.secho("pass", fg=typer.colors.GREEN)
        # Check file existence?
        pass

def _check_mysql(db_url):
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
            charset='utf8mb4', # Default for check
        )
        typer.secho("pass", fg=typer.colors.GREEN)
    except Exception:
        typer.secho("failed", fg=typer.colors.RED)
    else:
        cursor = conn.cursor()
        dbname = db_url.database.lstrip('/')
        typer.echo("check database   ：", nl=False)
        if cursor.execute(f"show databases like '{dbname}';"):
            typer.secho("pass", fg=typer.colors.GREEN)
        else:
            typer.secho("not exist!", fg=typer.colors.RED)

def _check_postgres(db_url):
    typer.echo("check psql       : ", nl=False)
    try:
        subprocess.check_call(
            ["psql", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        typer.secho("pass", fg=typer.colors.GREEN)
    except Exception:
        typer.secho("not exist!", fg=typer.colors.YELLOW) # psql CLI optional

    typer.echo("check connection : ", nl=False)
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=db_url.hostname,
            port=db_url.port,
            user=db_url.username,
            password=db_url.password,
            dbname='postgres' # Connect to default db to check existence
        )
        typer.secho("pass", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"failed: {e}", fg=typer.colors.RED)
        return
    
    # Check if target database exists
    dbname = db_url.database.lstrip('/')
    typer.echo(f"check database {dbname} : ", nl=False)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
    exists = cur.fetchone()
    if exists:
         typer.secho("pass", fg=typer.colors.GREEN)
    else:
         typer.secho("not exist!", fg=typer.colors.RED)
    cur.close()
    conn.close()


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
    """
    # 3）安装 requirements.txt
    typer.echo("install required modules...")
    os.system("pip install -r requirements.txt")
    typer.echo("")

    sys.path.append(os.path.join(".", "core"))
    
    # Try import config, might fail if .env not set up, but we need structure
    # Actually we get params from config object usually or interactive
    
    database = conf.get("config", "database", fallback=Database.MYSQL)
    
    if database == Database.MYSQL:
        _config_mysql(conf)
    elif database == Database.POSTGRESQL:
        _config_postgres(conf)
    elif database == Database.SQLITE:
        _config_sqlite(conf)
    
    # 5）创建数据库并运行迁移文件，创建相应的表
    typer.echo("Running migrations...")
    os.system('alembic revision --autogenerate -m "create migration"')
    os.system("alembic upgrade head")

def _config_mysql(conf):
    try:
        subprocess.check_call(
            ["mysql", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
    except Exception:
        typer.secho("Please make sure you download mysql already!", fg=typer.colors.RED)
        return
    
    db_url = __import__("config").DATABASE_URL
    db_charset = __import__("config").DB_CHARSET
    
    db_host: str = db_url.hostname or "localhost"
    db_port: int = db_url.port or 3306
    db_user: str = db_url.username or "root"
    db_pswd: str = db_url.password or ""
    dbname = db_url.database
    
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
            
            # Sync URL
            sql_url = f"mysql+pymysql://{db_user}:{db_pswd}@{db_host}:{db_port}/{dbname}?charset={db_charset}"
            # Async URL
            async_sql_url = f"mysql+aiomysql://{db_user}:{db_pswd}@{db_host}:{db_port}/{dbname}?charset={db_charset}"
            
            set_config_file_content("alembic.ini", "sqlalchemy.url", sql_url)
            set_config_file_content(os.path.join(".", "core", ".env"), "DB_CONNECTION", sql_url)
            set_config_file_content(os.path.join(".", "core", ".env"), "ASYNC_DB_CONNECTION", async_sql_url)

            # 创建数据库
            cursor = conn.cursor()
            cursor.execute(
                f"create database if not exists {dbname} "
                "default charset utf8mb4;"
            )
            break
        except Exception as e:
            typer.secho(f"fail: {e}", fg=typer.colors.RED)
            db_host = questionary.text("database host is:", default=db_host).ask()
            db_port = questionary.text("database port is:", default=str(db_port)).ask()
            db_port = int(db_port)
            db_user = questionary.text("database username is:", default=db_user).ask()
            db_pswd = questionary.text("database password is:", default=db_pswd).ask()

def _config_postgres(conf):
    # Try check psql but don't force return
    try:
        subprocess.check_call(
            ["psql", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
    except Exception:
        pass # Optional
        
    db_url = __import__("config").DATABASE_URL
    
    db_host: str = db_url.hostname or "localhost"
    db_port: int = db_url.port or 5432
    db_user: str = db_url.username or "postgres"
    db_pswd: str = db_url.password or ""
    dbname = db_url.database.lstrip('/')

    import psycopg2
    
    while True:
        typer.echo("check database connecting.....", nl=False)
        try:
            # Connect to default 'postgres' db to check creds and create DB
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_pswd,
                dbname='postgres'
            )
            conn.autocommit = True
            typer.secho("success", fg=typer.colors.GREEN)
            
            # Sync URL
            sql_url = f"postgresql+psycopg2://{db_user}:{db_pswd}@{db_host}:{db_port}/{dbname}"
            # Async URL
            async_sql_url = f"postgresql+asyncpg://{db_user}:{db_pswd}@{db_host}:{db_port}/{dbname}"
            
            set_config_file_content("alembic.ini", "sqlalchemy.url", sql_url)
            set_config_file_content(os.path.join(".", "core", ".env"), "DB_CONNECTION", sql_url)
            set_config_file_content(os.path.join(".", "core", ".env"), "ASYNC_DB_CONNECTION", async_sql_url)

            # 创建数据库
            cur = conn.cursor()
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
            if not cur.fetchone():
                typer.echo(f"Creating database {dbname}...")
                cur.execute(f"CREATE DATABASE {dbname}")
            
            cur.close()
            conn.close()
            break
        except Exception as e:
            typer.secho(f"fail: {e}", fg=typer.colors.RED)
            db_host = questionary.text("database host is:", default=db_host).ask()
            db_port = questionary.text("database port is:", default=str(db_port)).ask()
            db_port = int(db_port)
            db_user = questionary.text("database username is:", default=db_user).ask()
            db_pswd = questionary.text("database password is:", default=db_pswd).ask()

def _config_sqlite(conf):
    db_url = __import__("config").DATABASE_URL
    # For sqlite, we usually just use the path.
    # If using absolute path or relative
    # Default URL might be sqlite:///./test.db
    
    # We really just need to ensure the connection string is set correctly for async
    
    # If the default in config.py is sqlite:///./db.sqlite3
    # We want async to be sqlite+aiosqlite:///./db.sqlite3
    
    # Let's extract the path from existing URL or just ask?
    # Usually for sqlite we don't ask user for host/port.
    
    dbname = db_url.database
    if not dbname:
         dbname = "db.sqlite3"
         
    # Handle relative paths properly
    # If it is sqlite:///./db.sqlite3, database is "db.sqlite3" (if parsed correctly by DatabaseURL)
    # Actually DatabaseURL parsing for sqlite is tricky.
    
    # Let's just use what's there or default
    
    # Sync URL
    sql_url = f"sqlite:///./{dbname}"
    # Async URL
    async_sql_url = f"sqlite+aiosqlite:///./{dbname}"
    
    set_config_file_content("alembic.ini", "sqlalchemy.url", sql_url)
    set_config_file_content(os.path.join(".", "core", ".env"), "DB_CONNECTION", sql_url)
    set_config_file_content(os.path.join(".", "core", ".env"), "ASYNC_DB_CONNECTION", async_sql_url)
    
    typer.echo(f"Configured SQLite: {dbname}")


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
