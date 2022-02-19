import os
import sys
import typer


# 运行环境检查
def check_env():
    # 模块检查
    typer.secho("[module]", bold=True)
    with open("./requirements.txt") as fp:
        for module in fp.readlines():
            module = module.strip()
            if "==" not in module:
                continue
            name, version = module.split("==")
            typer.secho(f"check *{name}* : ", fg=typer.colors.MAGENTA, nl=False)
            try:
                module_version = __import__(name).__version__
                if module_version == version:
                    typer.secho("pass", fg=typer.colors.GREEN)
                elif module_version > version:
                    typer.secho("higher version.", fg=typer.colors.YELLOW)
                else:
                    typer.secho("lower version.", fg=typer.colors.YELLOW)
            except:
                typer.secho("module not exist!", fg=typer.colors.RED)
    
    typer.echo("\n")

    # 数据库检查
    typer.secho("[db]", bold=True)
    """
    database *mysql* : pass
    dbconnection     : pass
    dbcreated        : pass
    table migrated   : pass
    """
    sys.path.append(os.path.join(".", "core"))
    db_url = __import__("config").DATABASE_URL

    if os.system("mysql --version") != 0:
        ...
    os.system("python ./utils/dbmanager.py --check")
