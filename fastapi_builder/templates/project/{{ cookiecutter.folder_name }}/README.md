# 「 {{ cookiecutter.name }} 」

<div align="right">
    <a href="https://github.com/fmw666/fastapi-builder/">fastapi-builder 项目网址 ➡</a>
</div>

> 💡 **帮助您快速构建 fastapi 项目.**

+ ***[快速启用](#-快速启用)***

+ ***[项目结构](#-项目结构)***

+ ***[功能示例](#-功能示例)***

<div align="center">
    <img src="https://github.com/fmw666/my-image-file/blob/master/images/cute/small-cute-8.jpg" width=100>
</div>

<br>

## 🚀 快速启用

**0. 获取项目代码**

```sh
> git clone git@github.com:fmw666/fastapi-project-framework.git
> cd fastapi-project-framework
```

**1. 启用虚拟环境**

项目中使用虚拟环境是必要的，我们也强烈建议您通过虚拟环境来开发您的项目：

```sh
# cmd
app> pip install virtualenv   # 您的 python 版本需要 ≥ 3.7
app> virtualenv venv          # 创建虚拟环境
app> .\venv\Scripts\activate  # 启动虚拟环境

(venv) ...\app> pip install -r requirements.txt  # 安装必要模块
```

**2. 修改项目配置**

想要运行本项目，配置信息应该是您首先要关注的。

+ 在 [app/core/](#no-reply) 中创建 [.env](#no-reply) 文件来编写项目的配置信息：

    ```js
    app
    ├── core/
    │   ├── .env  # 这是您需要创建的文件. 注意，文件包含后缀，完整命名即为 .env
    ```

    正确创建完文件后，我们需要您写入至少如下内容：

    > 第一行为 **数据库连接信息**，第二行为 **密钥信息**（它们是以键值对形式存在，并且都为字符串类型，不需要引号）

    ```s
    DB_CONNECTION=mysql+pymysql://username:password@127.0.0.1:3306/dbname
    SECRET_KEY=OauIrgmfnwCdxMBWpzPF7vfNzga1JVoiJi0hqz3fzkY
    ```

    *（当您开始尝试阅读 [server/core/config.py](#no-reply) 文件后，您可以开始编写更多相关配置）*

+ [config.py](#no-reply) 文件已经基本满足项目所需的所有配置信息，但是对于迁移工具 [alembic](#no-reply) 我们还需要单独为其写入数据库配置信息：
    
    ```s
    # app/alembic.ini
    
    ...
    # 第 53 行，值同 .env 文件中 DB_CONNECTION
    sqlalchemy.url = mysql+pymysql://root:admin@localhost/dbname
    ```

**3. 启用数据库**

最后，您需要在环境中正确启动 mysql 服务，创建一个数据库，并执行迁移文件完成数据库中表的建立.<br>
幸运的是，这一点我们已经尽可能地为您考虑。您只需要正确启动 mysql 服务，并在 [app/utils/](#no-reply) 中执行：

```sh
app\utils> python dbmanager.py
```

**4. 运行项目**

```sh
app> python main.py
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
