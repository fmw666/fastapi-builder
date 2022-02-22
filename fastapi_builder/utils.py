import os
import sys
import subprocess
import typer


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
    db_url = __import__("config").DATABASE_URL
    db_charset = __import__("config").DB_CHARSET

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
