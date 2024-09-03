import os
import time

from loguru import logger


LOG_APP = "app"
LOG_CELERY = "celery"

basedir = os.path.dirname(os.path.abspath(__file__))

# 定位到 log 日志文件
log_path = os.path.join(basedir, "../logs")

os.makedirs(log_path, exist_ok=True)
os.makedirs(os.path.join(log_path, LOG_APP), exist_ok=True)
os.makedirs(os.path.join(log_path, LOG_CELERY), exist_ok=True)

app_log_path_file = os.path.join(log_path, LOG_APP, f"{time.strftime('%Y-%m-%d')}.log")
celery_log_path_file = os.path.join(log_path, LOG_CELERY, f"{time.strftime('%Y-%m-%d')}.log")


# 日志简单配置
logger.add(
    app_log_path_file,
    rotation="00:00",
    retention="5 days",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["extra"]["name"] == LOG_APP,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
    "{name}:{function}:{line} | {thread.name} | {message}",
)
logger.add(
    celery_log_path_file,
    rotation="00:00",
    retention="5 days",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["extra"]["name"] == LOG_CELERY,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
    "{name}:{function}:{line} | {thread.name} | {message}",
)

app_logger = logger.bind(name=LOG_APP)
celery_logger = logger.bind(name=LOG_CELERY)


__all__ = ["app_logger", "celery_logger"]
