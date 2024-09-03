import argparse
import sys
import os

import pymysql

from typing import Dict

from pymysql import Connection
from pymysql.cursors import Cursor

file_path = os.path.abspath(__file__)
proj_path = os.path.abspath(os.path.join(file_path, "..", ".."))
sys.path.insert(0, proj_path)

from core.config import settings  # noqa
from core.logger import app_logger as logger  # noqa


class DBManager(object):
    """
    提供系统 Mysql 服务：
    mysql 服务检查、数据库检查、迁移文件检查、表生成
    """

    _dbname = settings.DATABASE_URL.database
    _host = settings.DATABASE_URL.hostname
    _port = settings.DATABASE_URL.port
    _user = settings.DATABASE_URL.username
    _password = settings.DATABASE_URL.password

    @classmethod
    def get_conn(cls) -> Connection | None:
        # 连接 mysql 服务，并获取 connection
        logger.info(f'mysql 连接信息："{cls._dbname}"')
        try:
            conn: Connection = pymysql.connect(
                host=cls._host,
                port=cls._port,
                user=cls._user,
                password=cls._password,
                charset=settings.DB_CHARSET,
            )
            logger.info("数据库连接成功!")

        except Exception as e:
            # 打印错误信息
            error_reason: str = ""
            # (2003, "Can't connect to MySQL server on '127.0.0.1'
            # ([WinError 10061] 由于目标计算机积极拒绝，无法连接。)")
            if str(e).startswith("(2003"):
                error_reason = "mysql 无法连接，请检查 mysql 服务是否正常启动."
            # (1045, "Access denied for user 'root'@'localhost'
            # (using password: YES)")
            elif str(e).startswith("(1045"):
                error_reason = "mysql 拒绝访问，请检查参数是否有误."
            else:
                error_reason = "原因不详."
            logger.error(f"数据库连接失败! 原因：{error_reason}\n系统日志：{e}")
            conn = None

        return conn

    @classmethod
    def make_and_run_migrate(cls):
        # 执行迁移文件
        logger.info("执行迁移文件...")
        os.chdir(proj_path)
        os.system("alembic revision --autogenerate -m \"autocreate migration\"")
        os.system("alembic upgrade heads")
        logger.info("执行迁移文件完成.")

    @classmethod
    def run_migrate(cls):
        # 执行迁移文件
        logger.info("执行迁移文件...")
        os.chdir(proj_path)
        # os.system('alembic revision --autogenerate -m "autocreate migration"')
        os.system("alembic upgrade heads")
        logger.info("执行迁移文件完成.")

    @classmethod
    def check_and_autocreate(cls) -> Dict[str, str]:
        # 检查 mysql 服务、数据库及表是否存在
        logger.info("检查 mysql 服务、数据库及表.")

        # 建立游标
        conn = cls.get_conn()
        if not conn:
            return {"code": -1, "msg": "获取连接失败."}

        cursor: Cursor = conn.cursor()

        # 检查数据库是否存在
        if cursor.execute(f"show databases like '{cls._dbname}';"):
            logger.info(f"数据库：{cls._dbname} 已存在.")
        else:
            # 数据库不存在，创建数据库
            logger.info(f"数据库：{cls._dbname} 不存在. 正在自动创建...")
            cursor.execute(
                f"create database if not exists `{cls._dbname}` default charset utf8mb4;"
            )
            logger.info(f"数据库：{cls._dbname} 创建完成.")

        # 检查数据库表是否存在
        cls.run_migrate()

        logger.info("检查完成，已正确配置数据库及相关表!")

        return {"code": 0, "msg": "执行完成!"}

    @classmethod
    def reset_database(cls) -> Dict[str, str]:
        # 重置 mysql 数据库及数据库内所有表

        # 建立游标
        conn = cls.get_conn()
        if not conn:
            return {"code": -1, "msg": "获取连接失败."}

        cursor: Cursor = conn.cursor()

        # 检查数据库是否存在
        if cursor.execute(f"show databases like '{cls._dbname}';"):
            logger.info(f"数据库：{cls._dbname} 已存在. 正在自动删除...")
            cursor.execute(f"drop database if exists {cls._dbname};")
            logger.info(f"数据库：{cls._dbname} 删除完成. 正在重新创建...")
        else:
            # 数据库不存在，创建数据库
            logger.info(f"数据库：{cls._dbname} 不存在. 正在自动创建...")

        cursor.execute(
            f"create database if not exists {cls._dbname} " "default charset utf8mb4;"
        )
        logger.info(f"数据库：{cls._dbname} 创建完成.")

        # 检查数据库表是否存在
        cls.run_migrate()

        logger.info("重置完成，已正确配置数据库及相关表!")

        return {"code": 0, "msg": "执行完成!"}

    @classmethod
    def remove_database(cls) -> Dict[str, str]:
        # 删除数据库
        # 建立游标
        conn = cls.get_conn()
        if not conn:
            return {"code": -1, "msg": "获取连接失败."}

        cursor: Cursor = conn.cursor()

        if cursor.execute(f"show databases like '{cls._dbname}';"):
            logger.info(f"数据库：{cls._dbname} 已存在. 正在自动删除...")
            cursor.execute(f"drop database if exists `{cls._dbname}`;")
            logger.info(f"数据库：{cls._dbname} 删除完成.")
        else:
            # 数据库不存在，创建数据库
            logger.info(f"数据库：{cls._dbname} 不存在.")

        return {"code": 0, "msg": "执行完成!"}


__all__ = ["DBManager"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the database operations.")
    parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="Check and auto-create database if not exist",
    )
    parser.add_argument("-r", "--reset", action="store_true", help="Reset the database")
    parser.add_argument(
        "-d", "--delete", action="store_true", help="Delete the database"
    )
    parser.add_argument(
        "-m", "--migrate", action="store_true", help="Run alembic migration"
    )

    args = parser.parse_args()

    try:
        if args.create:
            ret = DBManager.check_and_autocreate()
        elif args.reset:
            ret = DBManager.reset_database()
        elif args.delete:
            ret = DBManager.remove_database()
        elif args.migrate:
            ret = DBManager.make_and_run_migrate()
        else:
            ret = "No command specified. Use -h for help."
    except Exception as e:
        ret = f"Error occurred: {str(e)}"

    print(ret)
