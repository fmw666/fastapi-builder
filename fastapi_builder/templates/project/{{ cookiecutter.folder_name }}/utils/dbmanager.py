import sys
import os
from typing import Any, Dict
file_path = os.path.abspath(__file__)
proj_path = os.path.abspath(os.path.join(file_path, "..", ".."))
sys.path.insert(0, proj_path)

import pymysql

from core.config import DATABASE_URL, DB_CHARSET
from core.logger import logger


class DBManager(object):
    """
    提供系统 Mysql 服务：
    mysql 服务检查、数据库检查、迁移文件检查、表生成
    """
    # 初始化数据
    _dbname = DATABASE_URL.database
    _host = DATABASE_URL.hostname
    _port = DATABASE_URL.port
    _user = DATABASE_URL.username
    _password = DATABASE_URL.password

    @classmethod
    def get_conn(cls) -> Any:
        # 连接 mysql 服务，并获取 connection
        logger.info("mysql 连接信息：\"%s\"" % DATABASE_URL)
        try:
            conn = pymysql.connect(
                host=cls._host,
                port=cls._port,
                user=cls._user,
                password=cls._password,
                charset=DB_CHARSET
            )
            logger.info("数据库连接成功!")

        except Exception as e:
            # 打印错误信息
            error_reason: str = ""
            # (2003, "Can't connect to MySQL server on '127.0.0.1' ([WinError 10061] 由于目标计算机积极拒绝，无法连接。)")
            if str(e).startswith("(2003"):
                error_reason = "mysql 无法连接，请检查 mysql 服务是否正常启动."
            # (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
            elif str(e).startswith("(1045"):
                error_reason = "mysql 拒绝访问，请检查参数是否有误."
            else:
                error_reason = "原因不详."
            logger.error("数据库连接失败! 原因：{error_reason}\n系统日志：{exc_msg}".format(error_reason=error_reason, exc_msg=e))
            conn = None

        return conn


    # 执行迁移文件
    @classmethod
    def run_migrate(cls):
        logger.info("执行迁移文件...")
        os.chdir(proj_path)
        os.system("alembic revision --autogenerate -m \"create migration\"")
        os.system("alembic upgrade head")
        logger.info("执行迁移文件完成.")


    # 检查 mysql 服务、数据库及表是否存在
    @classmethod
    def check_and_autocreate(cls) -> Dict[str, str]:
        logger.info("检查 mysql 服务、数据库及表.")

        # 建立游标
        conn = cls.get_conn()
        if not conn:
            return {"code": -1, "msg": "获取连接失败."}
        
        cursor = conn.cursor()

        # 检查数据库是否存在
        if cursor.execute("show databases like '%s';" % cls._dbname):
            logger.info("数据库：%s 已存在." % cls._dbname)
        else:
            # 数据库不存在，创建数据库
            logger.info("数据库：%s 不存在. 正在自动创建..." % cls._dbname)
            cursor.execute("create database if not exists %s default charset utf8mb4;" % cls._dbname)
            logger.info("数据库：%s 创建完成." % cls._dbname)

        # 检查数据库表是否存在
        cls.run_migrate()

        logger.info("检查完成，已正确配置数据库及相关表!")

        return {"code": 0, "msg": "执行完成!"}


    # 重置 mysql 数据库及数据库内所有表
    @classmethod
    def reset_database(cls) -> Dict[str, str]:
        # 建立游标
        conn = cls.get_conn()
        if not conn:
            return {"code": -1, "msg": "获取连接失败."}
        
        cursor = conn.cursor()

        # 检查数据库是否存在
        if cursor.execute("show databases like '%s';" % cls._dbname):
            logger.info("数据库：%s 已存在. 正在自动删除..." % cls._dbname)
            cursor.execute("drop database if exists %s;" % cls._dbname)
            logger.info("数据库：%s 删除完成. 正在重新创建..." % cls._dbname)
        else:
            # 数据库不存在，创建数据库
            logger.info("数据库：%s 不存在. 正在自动创建..." % cls._dbname)
        
        cursor.execute("create database if not exists %s default charset utf8mb4;" % cls._dbname)
        logger.info("数据库：%s 创建完成." % cls._dbname)

        # 检查数据库表是否存在
        cls.run_migrate()

        logger.info("重置完成，已正确配置数据库及相关表!")

        return {"code": 0, "msg": "执行完成!"}


    # 删除数据库
    @classmethod
    def remove_database(cls) -> Dict[str, str]:
        # 建立游标
        conn = cls.get_conn()
        if not conn:
            return {"code": -1, "msg": "获取连接失败."}

        cursor = conn.cursor()

        if cursor.execute("show databases like '%s';" % cls._dbname):
            logger.info("数据库：%s 已存在. 正在自动删除..." % cls._dbname)
            cursor.execute("drop database if exists %s;" % cls._dbname)
            logger.info("数据库：%s 删除完成." % cls._dbname)
        else:
            # 数据库不存在，创建数据库
            logger.info("数据库：%s 不存在." % cls._dbname)
        
        return {"code": 0, "msg": "执行完成!"}


__all__ = ["MysqlService"]

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "-c":
            ret = DBManager.check_and_autocreate()
        elif cmd == "-r":
            ret = DBManager.reset_database()
        elif cmd == "-d":
            ret = DBManager.remove_database()
        else:
            ret = "cmd error!"
    else:
        ret = DBManager.check_and_autocreate()
    print(ret)
