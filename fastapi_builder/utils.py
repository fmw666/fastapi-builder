import os
import sys
import subprocess
import configparser
import typer
import pymysql
import questionary

from configparser import ConfigParser


# 运行环境检查
def check_env():
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
        except:
            try:
                subprocess.check_call(["pip", "show", name], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                typer.secho("pass", fg=typer.colors.GREEN)
            except:
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
    except:
        typer.secho("module databases not installed", fg=typer.colors.RED)

    typer.echo("check mysql      : ", nl=False)
    try:
        subprocess.check_call(["mysql", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        typer.secho("pass", fg=typer.colors.GREEN)
    except:
        typer.secho("not exist!", fg=typer.colors.RED)
    
    typer.echo("check connection : ", nl=False)
    try:
        import pymysql
        conn = pymysql.connect(
            host=db_url.hostname,
            port=db_url.port,
            user=db_url.username,
            password=db_url.password,
            charset=db_charset
        )
        typer.secho("pass", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho("failed", fg=typer.colors.RED)
    else:
        cursor = conn.cursor()
        dbname = db_url.database
        typer.echo("check database   ：", nl=False)
        if cursor.execute(f"show databases like '{dbname}';"):
            typer.secho("pass", fg=typer.colors.GREEN)
        else:
            typer.secho("not exist!", fg=typer.colors.RED)


# 读取配置文件
def read_conf(file_name: str) -> ConfigParser:
    conf = configparser.ConfigParser()
    conf.read(file_name)
    return conf


# 修改配置文件内容
def set_config_file_content(file_path: str, key: str, new_value: str):
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


# 配置应用
def config_app(conf: ConfigParser):
    """
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
        subprocess.check_call(["mysql", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except:
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
                charset=db_charset
            )
            typer.secho("success", fg=typer.colors.GREEN)
            # 写入到配置文件中 core/.env alembic.ini
            sql_url = f"mysql+pymysql://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_url.database}?charset={db_charset}"
            set_config_file_content("alembic.ini", "sqlalchemy.url", sql_url)
            set_config_file_content(os.path.join(".", "core", ".env"), "DB_CONNECTION", sql_url)

            # 创建数据库
            cursor = conn.cursor()
            cursor.execute("create database if not exists %s default charset utf8mb4;" % db_url.database)
            break
        except Exception:
            typer.secho("fail", fg=typer.colors.RED)
            db_host = questionary.text("database host is:", default=db_host).ask()
            db_port = questionary.text("database port is:", default=str(db_port)).ask()
            db_port = int(db_port)
            db_user = questionary.text("database username is:", default=db_user).ask()
            db_pswd = questionary.text("database password is:", default=db_pswd).ask()

    # 5）创建数据库并运行迁移文件，创建相应的表
    os.system("alembic revision --autogenerate -m \"create migration\"")
    os.system("alembic upgrade head")


# 新 app 注入到 project
def new_app_inject_into_project(folder_name: str, pascal_name: str, snake_name: str):
    # 打开 api/routes/api.py 文件，创建路由
    api_file_path = os.path.join(".", "api", "routes", "api.py")
    with open(api_file_path, "r") as f:
        api_file_lines = f.readlines()

    # 找到最后一个 import，在其下一行导入 app
    last_import_line = 0
    for i in range(len(api_file_lines)-1, -1, -1):
        if api_file_lines[i].startswith("import"):
            last_import_line = i
            break
    
    api_file_lines.insert(last_import_line + 1, f"import app_{folder_name}.api\n")

    # 创建 router
    api_file_lines.append(f"router.include_router(app_{folder_name}.api.router, tags=[\"{pascal_name} 类\"], prefix=\"/{snake_name}s\")\n")

    # 将修改后的内容写回到 api.py 文件
    with open(api_file_path, "w") as f:
        f.writelines(api_file_lines)
    
    # 打开 db/base.py 导入 models
    db_file_path = os.path.join(".", "db", "base.py")
    with open(db_file_path, "a") as f:
        f.write(f"from app_{folder_name}.model import *\n")
