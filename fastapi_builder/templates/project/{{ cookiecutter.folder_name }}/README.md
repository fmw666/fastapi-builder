# 「 {{ cookiecutter.name }} 」

<div align="right">
    <a href="https://github.com/fmw666/fastapi-builder/">fastapi-builder 项目网址 ➡</a>
</div>

<br>

> 💡 **帮助您快速构建 fastapi 项目.**

+ ***[快速启用](#-快速启用)***

+ ***[项目结构](#-项目结构)***

+ ***[功能示例](#-功能示例)***

<div align="center">
    <img src="https://github.com/fmw666/my-image-file/blob/master/images/cute/small-cute-8.jpg" width=100>
</div>

<br>

## 🚀 快速启用

**1. 修改项目配置**

> 想要运行本项目，配置信息应该是您首先要关注的。

```js
project
├── core/
│   ├── .env     // 项目整体配置
├── alembic.ini  // 数据迁移配置
```

```s
# core/.env
DB_CONNECTION=mysql+pymysql://username:password@127.0.0.1:3306/dbname
SECRET_KEY=OauIrgmfnwCdxMBWpzPF7vfNzga1JVoiJi0hqz3fzkY


# alembic.ini
...
# 第 53 行，值同 .env 文件中 DB_CONNECTION
sqlalchemy.url = mysql+pymysql://root:admin@localhost/dbname
```
    
*（当您开始尝试阅读 [server/core/config.py](#no-reply) 文件后，您可以开始编写更多相关配置）*

**2. 启用数据库**

最后，您需要在环境中正确启动 mysql 服务，创建一个数据库，并执行迁移文件完成数据库中表的建立.<br>
幸运的是，这一点我们已经尽可能地为您考虑。您只需要正确启动 mysql 服务，并在 [app/utils/](#no-reply) 中执行：

```sh
project\utils> python dbmanager.py
```

**3. 运行项目**

```sh
project> python main.py
```

<br>

## 📌 项目结构

```js
app
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── api/               - web related stuff.
│   └── errors/        - definition of error handlers.
│   │   ├── http_error.py
│   │   └── validation_error.py
│   └── routes/        - web routes.
│       ├── api.py
│       ├── authentication.py
│       └── user.py
├── core/              - application configuration, startup events, logging.
│   ├── .env    - manually written alembic migrations.
│   ├── config.py    - manually written alembic migrations.
│   ├── events.py    - manually written alembic migrations.
│   ├── logger.py    - manually written alembic migrations.
├── db/                - db related stuff.
│   ├── base.py    - manually written alembic migrations.
│   └── database.py  - all crud stuff.
│   ├── errors.py    - manually written alembic migrations.
│   ├── events.py    - manually written alembic migrations.
├── lib/               - db related stuff.
│   ├── jwt.py    - manually written alembic migrations.
│   ├── security.py    - manually written alembic migrations.
├── logs/               - db related stuff.
├── middleware/            - pydantic models for this application.
│   ├── logger.py    - manually written alembic migrations.
├── models/            - pydantic models for this application.
│   ├── base.py        - main models that are used almost everywhere.
│   └── mixins.py       - schemas for using in web routes.
│   ├── user.py        - main models that are used almost everywhere.
├── schemas/            - pydantic models for this application.
│   ├── auth.py        - main models that are used almost everywhere.
│   └── base.py       - schemas for using in web routes.
│   ├── jwt.py        - main models that are used almost everywhere.
│   ├── user.py        - main models that are used almost everywhere.
├── utils/             - strings that are used in web responses.
├── ├── consts.py      - logic that is not just crud related.
├── ├── dbmanager.py      - logic that is not just crud related.
├── ├── docs.py      - logic that is not just crud related.
└── main.py            - FastAPI application creation and configuration.
```

<br>

## 💬 功能示例

swigger docs

<br>

## License

This project is licensed under the terms of the {{ cookiecutter.license }} license.
